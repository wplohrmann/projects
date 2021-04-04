use pest::Parser;
use pest::error::Error;
use pest::iterators::Pair;

use std::ops;

#[derive(Parser)]
#[grammar = "algebra.pest"]
struct AlgebraParser;

#[derive(Clone, PartialEq, PartialOrd, Debug)]
pub enum Expr {
    Constant(f32), // Constant value
    Coord(usize, usize), // An indexed coordinate, time-differentiated n times
    Add(Vec<Expr>),
    Mul(Vec<Expr>),
    // Sin(Box<Expr>), // sin (trig)
    // Cos(Box<Expr>), // cos (trig)
}

pub trait Lagrangian {
    fn lagrangian(&self) -> Expr;
}

impl Expr {
    pub fn dot(&self) -> Expr {
        match self {
            Expr::Coord(i, n) => Expr::Coord(*i, n+1),
            Expr::Add(es) => Expr::Add(es.iter().map(|e| e.dot()).collect()),
            Expr::Mul(es) => {
                let mut result = Expr::Constant(0.);
                for i in 0..es.len() {
                    let mut product = Expr::Constant(1.);
                    for (j, e) in es.iter().enumerate() {
                        if i == j {
                            product = product * e.dot();
                        } else {
                            product = product * e.clone();
                        }
                    }
                    result = result + product;
                }
                result
            },
            Expr::Constant(_) => Expr::Constant(0.),
        }
    }

    pub fn simplify(&self) -> Expr {
        let mut last = self.clone();
        loop {
            let simplified = match self {
                Expr::Add(es) => simplify_add(es),
                Expr::Mul(es) => simplify_mul(es),
                _ => self.clone(),
            };
            if simplified == last {
                println!("Simplified {} to {}", self, simplified);
                return simplified;
            }
            last = simplified;
        }
    }
}

pub fn simplify_add(es: &Vec<Expr>) -> Expr {
    let mut simplified = es.iter()
        .filter(|&e| e != &Expr::Constant(0.))
        .map(|e| e.simplify())
        .collect::<Vec<Expr>>();

    if simplified.len() == 1 { return simplified[0].clone(); }
    simplified.sort_by(|a, b| a.partial_cmp(b).unwrap());

    Expr::Add(simplified)
}

pub fn simplify_mul(es: &Vec<Expr>) -> Expr {

    let mut simplified = Vec::new();
    for e in es {
        match e {
            zero if *zero == Expr::Constant(0.) => return Expr::Constant(0.), // 0 * anything is 0
            one if *one == Expr::Constant(1.) => (), // 0 * anything is 0
            Expr::Mul(sub_es) => { // Flatten nested multiplication
                let simplified_sub_es = simplify_mul(sub_es);
                match simplified_sub_es {
                    Expr::Mul(mut x) => simplified.append(&mut x),
                    _ => return Expr::Constant(0.),
                }
            }
            e => simplified.push(e.simplify()) // anything else is pushed onto the stack of factors
        };
    }

    if simplified.len() == 1 { return simplified[0].clone(); }
    simplified.sort_by(|a, b| a.partial_cmp(b).unwrap());
    Expr::Mul(simplified)
}

impl std::fmt::Display for Expr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Expr::Coord(i, n) => write!(f, "q_{}{}", i, ".".repeat(*n)),
            Expr::Add(es) => write!(f, "({})", es.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(" + ")),
            Expr::Mul(es) => write!(f, "({})", es.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(" * ")),
            Expr::Constant(k) => write!(f, "{}", k)
        }
    }
}

impl ops::Mul<Expr> for f32 {
    type Output = Expr;

    fn mul(self, rhs: Expr) -> Self::Output {
        Expr::Mul(vec![Expr::Constant(self), rhs])
    }
}

impl ops::Mul<Expr> for &f32 {
    type Output = Expr;

    fn mul(self, rhs: Expr) -> Self::Output {
        Expr::Mul(vec![Expr::Constant(*self), rhs])
    }
}

impl ops::Add<Expr> for Expr {
    type Output = Expr;

    fn add(self, rhs: Expr) -> Self::Output {
        match self {
            Expr::Add(es) => { 
                let mut cloned = es.clone();
                cloned.push(rhs);
                Expr::Add(cloned)
            },
            e => Expr::Add(vec![e, rhs])
        }
    }
}

impl ops::Mul<Expr> for Expr {
    type Output = Expr;

    fn mul(self, rhs: Expr) -> Self::Output {
        match self {
            Expr::Mul(es) => { 
                let mut cloned = es.clone();
                cloned.push(rhs);
                Expr::Mul(cloned)
            },
            e => Expr::Mul(vec![e, rhs])
        }
    }
}

impl ops::Sub<Expr> for Expr {
    type Output = Expr;

    fn sub(self, rhs: Expr) -> Self::Output {
        (-1. * self) + rhs
    }
}

pub struct MassOnASpring {
    pub x: f32,
    pub omega_sq: f32, // k/m
    pub v: f32
}

impl Lagrangian for MassOnASpring {
    fn lagrangian(&self) -> Expr {
        // KE = 0.5 * m v^2
        // PE = 0.5 * k * x^2
        // L = KE - PE
        let ke = 0.5 * Expr::Coord(0, 1) * Expr::Coord(0, 1);
        let pe = 0.5 * self.omega_sq * Expr::Coord(0, 0) * Expr::Coord(0, 0);
        pe - ke
    }
}

impl std::str::FromStr for Expr {
    type Err = Error<Rule>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let pair = AlgebraParser::parse(Rule::expr, s)?.next().unwrap();
        fn parse_value(pair: Pair<Rule>) -> Expr {
            match pair.as_rule() {
                Rule::float => Expr::Constant(pair.as_str().parse().unwrap()),
                Rule::coord => {
                    let mut inner_pairs = pair.into_inner();
                    inner_pairs.next(); // Consume q
                    let index = inner_pairs.next().unwrap().as_str().parse().unwrap();
                    let n_dots = inner_pairs.next().unwrap().as_str().len();
                    Expr::Coord(index, n_dots)
                },
                Rule::sum => {
                    pair.into_inner()
                        .map(|p| parse_value(p))
                        .reduce(|a, b| a+b)
                        .unwrap()
                },
                Rule::mul => {
                    pair.into_inner()
                        .map(|p| parse_value(p))
                        .reduce(|a, b| a*b)
                        .unwrap()
                },
                Rule::digit => todo!("digit"),
                Rule::q => todo!("q"),
                Rule::dots => todo!("dots"),
                Rule::expr => todo!("expr"),
            }
        }
        return Ok(parse_value(pair));
    }
}

#[cfg(test)]
mod tests {
    use super::Expr;
    #[test]
    fn coord() {
        assert_eq!("q_0".parse::<Expr>().unwrap(), Expr::Coord(0, 0));
        assert_eq!("q_1.".parse::<Expr>().unwrap(), Expr::Coord(1, 1));
        assert_eq!("q_2..".parse::<Expr>().unwrap(), Expr::Coord(2, 2));
    }

    #[test]
    fn float() {
        assert_eq!("0.1".parse::<Expr>().unwrap(), Expr::Constant(0.1));
        assert_eq!("5".parse::<Expr>().unwrap(), Expr::Constant(5.));
        assert_eq!("1.1".parse::<Expr>().unwrap(), Expr::Constant(1.1));
    }

    #[test]
    fn add() {
        assert_eq!("(2 + 1)".parse::<Expr>().unwrap(), Expr::Add(vec![Expr::Constant(2.), Expr::Constant(1.)]));
        assert_eq!("(2 + 1 + 1)".parse::<Expr>().unwrap(), Expr::Add(vec![Expr::Constant(2.), Expr::Constant(1.), Expr::Constant(1.)]));
    }

    #[test]
    fn mul() {
        assert_eq!("(2 * 1)".parse::<Expr>().unwrap(), Expr::Mul(vec![Expr::Constant(2.), Expr::Constant(1.)]));
        assert_eq!("(2 * 1 * 1)".parse::<Expr>().unwrap(), Expr::Mul(vec![Expr::Constant(2.), Expr::Constant(1.), Expr::Constant(1.)]));
    }

    #[test]
    fn nested() {
        assert_eq!("((1 * 0.5) * q_0..)".parse::<Expr>().unwrap(), (Expr::Constant(1.) * Expr::Constant(0.5)) * Expr::Coord(0, 2));
    }

    #[test]
    fn simplify() {
        assert_eq!("(1 * 0.5 * q_0.. * q_0.)".parse::<Expr>().unwrap().simplify(), "(0.5 * q_0. * q_0..)".parse().unwrap());
        assert_eq!("(1 * 0 * (q_0. * q_0.))".parse::<Expr>().unwrap().simplify(), "0".parse().unwrap());
        assert_eq!("(0 + (-1 * (0 + (3 * q_0 * q_0.) + (3 * q_0 * q_0.))))".parse::<Expr>().unwrap().simplify(), "(-1 * ((3 * q_0 * q_0.) + (3 * q_0 * q_0.)))".parse().unwrap());
    }
}
