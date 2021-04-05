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
    Mul(Vec<Expr>),
    Add(Vec<Expr>),
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
        let mut simplified = self.clone();
        loop {
            if let Some(e) = simplified.apply_add_identity() { simplified = e; }
            else if let Some(e) = simplified.apply_multiply_by_zero() { simplified = e; }
            else if let Some(e) = simplified.apply_mul_constants() { simplified = e; }
            else if let Some(e) = simplified.apply_add_constants() { simplified = e; }
            else if let Some(e) = simplified.apply_mul_identity() { simplified = e; }
            else if let Some(e) = simplified.apply_sort_children() { simplified = e; }
            else if let Some(e) = simplified.apply_undo_nested_add() { simplified = e; }
            else if let Some(e) = simplified.apply_undo_nested_mul() { simplified = e; }
            else if let Some(e) = simplified.apply_distribute() { simplified = e; }
            else {
                let nested_simplified = match &simplified {
                    Expr::Add(es) => Expr::Add(es.iter().map(|e| e.simplify()).collect()),
                    Expr::Mul(es) => Expr::Mul(es.iter().map(|e| e.simplify()).collect()),
                    _ => {
                        if simplified != *self {
                            println!("Simplified {} to {}", self, simplified);
                        }
                        return simplified;
                    }
                };
                if nested_simplified == simplified {
                    return simplified;
                }
                simplified = nested_simplified;
            }
        }
    }

    pub fn apply_distribute(&self) -> Option<Expr> {
        // Addition expressions float to the end, so we only have to look at the last element of a
        // Mul.
        match self {
            Expr::Mul(es) => {
                if es.len() == 1 { return None; }
                match es.last().unwrap() {
                    Expr::Add(sub_es) => {
                        let mut terms = Vec::new();
                        for e in sub_es {
                            let mut factors = es.clone();
                            let last_index = factors.len() - 1;
                            factors[last_index] = e.clone();
                            terms.push(Expr::Mul(factors));
                        }
                        Some(Expr::Add(terms))
                    },
                    _ => None
                }
            },
            _ => None
        }
    }

    pub fn apply_undo_nested_add(&self) -> Option<Expr> {
        match self {
            Expr::Add(es) => {
                let mut simplified = Vec::new();
                for e in es {
                    match e.clone() {
                        Expr::Add(mut sub_es) => simplified.append(&mut sub_es),
                        other => simplified.push(other)
                    }
                }
                return if simplified.len() != es.len() {
                    Some(Expr::Add(simplified))
                } else { None }
            },
            _ => return None
        }
    }

    pub fn apply_undo_nested_mul(&self) -> Option<Expr> {
        match self {
            Expr::Mul(es) => {
                let mut simplified = Vec::new();
                for e in es {
                    match e.clone() {
                        Expr::Mul(mut sub_es) => simplified.append(&mut sub_es),
                        other => simplified.push(other)
                    }
                }
                return if simplified.len() != es.len() {
                    Some(Expr::Mul(simplified))
                } else { None }
            },
            _ => return None
        }
    }

    pub fn apply_sort_children(&self) -> Option<Expr> {
        match self {
            Expr::Mul(es) => {
                let mut sorted = es.clone();
                sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
                if &sorted != es {
                    return Some(Expr::Mul(sorted));
                } else {
                    return None;
                }
            },
            Expr::Add(es) => {
                let mut sorted = es.clone();
                sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
                if &sorted != es {
                    return Some(Expr::Add(sorted));
                } else {
                    return None;
                }
            },
            _ => return None,
        }
    }

    pub fn apply_multiply_by_zero(&self) -> Option<Expr> {
        match self {
            Expr::Mul(es) => {
                if es.iter().any(|e| e == &Expr::Constant(0.)) {
                    return Some(Expr::Constant(0.));
                }
            },
            _ => ()
        }

        return None;
    }

    pub fn apply_mul_constants(&self) -> Option<Expr> {
        match self {
            Expr::Mul(es) => {
                let mut simplified = Vec::new();
                let mut scale = 1.;
                for e in es {
                    match e {
                        Expr::Constant(k) => scale *= k,
                        _ => simplified.push(e.clone()),
                    }
                }
                if scale != 1. {
                    simplified.push(Expr::Constant(scale));
                }
                if simplified.len() != es.len() {
                    Some(Expr::Mul(simplified))
                } else {
                    None
                }
            },
            _ => None
        }
    }

    pub fn apply_add_constants(&self) -> Option<Expr> {
        match self {
            Expr::Add(es) => {
                let mut simplified = Vec::new();
                let mut scale = 0.;
                for e in es {
                    match e {
                        Expr::Constant(k) => scale += k,
                        _ => simplified.push(e.clone()),
                    }
                }
                if scale != 0. {
                    simplified.push(Expr::Constant(scale));
                }
                if simplified.len() != es.len() {
                    Some(Expr::Add(simplified))
                } else {
                    None
                }
            },
            _ => None
        }
    }

    pub fn apply_add_identity(&self) -> Option<Expr> {
        match self {
            Expr::Add(es) => {
                let filtered: Vec<Expr> = es.iter().cloned().filter(|e| e != &Expr::Constant(0.)).collect();
                if filtered.len() != es.len() {
                    Some(Expr::Add(filtered))
                }
                else {
                    return None;
                }
            },
            _ => None
        }
    }

    pub fn apply_mul_identity(&self) -> Option<Expr> {
        match self {
            Expr::Mul(es) => {
                let filtered: Vec<Expr> = es.iter().cloned().filter(|e| e != &Expr::Constant(1.)).collect();
                if filtered.len() != es.len() {
                    Some(Expr::Mul(filtered))
                }
                else {
                    return None;
                }
            },
            _ => None
        }
    }

    pub fn descale(&self) -> (f32, Expr) {
        match self {
            Expr::Mul(es) => {
                let mut factors = Vec::new();
                let mut scale = 1.;
                for sub_e in es {
                    match sub_e {
                        Expr::Constant(k) => scale *= k,
                        other => factors.push(other.clone()),
                    }
                }
                (scale, Expr::Mul(factors))
            },
            Expr::Constant(k) => (*k, Expr::Constant(1.)),
            other => (1., other.clone())
        }
}
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
                Rule::digit | Rule::q | Rule::dots | Rule::expr => unreachable!("Trying to parse sub-expression out of context")
            }
        }
        return Ok(parse_value(pair));
    }
}

#[cfg(test)]
mod tests {
    use super::Expr;

    #[test]
    fn parse_coord() {
        assert_eq!("q_0".parse::<Expr>().unwrap(), Expr::Coord(0, 0));
        assert_eq!("q_1.".parse::<Expr>().unwrap(), Expr::Coord(1, 1));
        assert_eq!("q_2..".parse::<Expr>().unwrap(), Expr::Coord(2, 2));
    }

    #[test]
    fn parse_float() {
        assert_eq!("0.1".parse::<Expr>().unwrap(), Expr::Constant(0.1));
        assert_eq!("5".parse::<Expr>().unwrap(), Expr::Constant(5.));
        assert_eq!("1.1".parse::<Expr>().unwrap(), Expr::Constant(1.1));
    }

    #[test]
    fn parse_add() {
        assert_eq!("(2 + 1)".parse::<Expr>().unwrap(), Expr::Add(vec![Expr::Constant(2.), Expr::Constant(1.)]));
        assert_eq!("(2 + 1 + 1)".parse::<Expr>().unwrap(), Expr::Add(vec![Expr::Constant(2.), Expr::Constant(1.), Expr::Constant(1.)]));
    }

    #[test]
    fn parse_mul() {
        assert_eq!("(2 * 1)".parse::<Expr>().unwrap(), Expr::Mul(vec![Expr::Constant(2.), Expr::Constant(1.)]));
        assert_eq!("(2 * 1 * 1)".parse::<Expr>().unwrap(), Expr::Mul(vec![Expr::Constant(2.), Expr::Constant(1.), Expr::Constant(1.)]));
    }

    #[test]
    fn parse_nested() {
        assert_eq!("((1 * 0.5) * q_0..)".parse::<Expr>().unwrap(), (Expr::Constant(1.) * Expr::Constant(0.5)) * Expr::Coord(0, 2));
    }

    fn descales_to(e1: &str, descaled: (f32, &str)) {
        let e1_parsed = e1.parse::<Expr>().unwrap();
        let e1_descaled = e1_parsed.descale();
        assert_eq!((e1_descaled.0, e1_descaled.1.to_string().as_str()), descaled);
    }

    #[test]
    fn descale_constant() {
        descales_to("5.", (5., "1"));
    }

    #[test]
    fn descale_mul() {
        descales_to("(5. * 2. * q_0 * q_5.)", (10., "(q_0 * q_5.)"));
    }

    #[test]
    fn descale_add() {
        descales_to("(5. + 2. + q_0 + q_5.)", (1., "(5 + 2 + q_0 + q_5.)"));
    }



    fn simplifies_to(e1: &str, e2: &str) {
        let e1_parsed = e1.parse::<Expr>().unwrap();
        assert_eq!(e1_parsed.simplify().to_string(), e2);
    }

    // simplify_mul
    #[test]
    fn simplify_mul_reduces_to_zero() {
        simplifies_to("(1 * 0 * (q_0. * q_0.))", "0");
    }

    #[test]
    fn simplify_mul_one_disappears() {
        simplifies_to("(1 * 0.5 * q_0.. * q_0.)", "(0.5 * q_0. * q_0..)");
    }

    #[test]
    fn simplify_mul_scales_combine() {
        simplifies_to("(-1 * ((q_0 * q_0. * 6)))", "(-6 * q_0 * q_0.)");
    }

    // simplify_add
    #[test]
    fn simplify_add_scales_combine() {
        simplifies_to("(-1 + ((q_0 + q_0. + 6)))", "(5 + q_0 + q_0.)");
    }

    #[test]
    fn simplify_add_nested() {
        simplifies_to("(q_1.... + ((q_0 + q_0. + 6)))", "(6 + q_0 + q_0. + q_1....)");
    }

    #[test]
    fn simplify_add_zero_disappears() {
        simplifies_to("(0 + 0.5 + q_0.. + q_0.)", "(0.5 + q_0. + q_0..)");
    }


    //simplify
    #[test]
    fn simplify_nested() {
        simplifies_to("(0 + (-1 * (0 + (3 * q_0 * q_0.) + (3 * q_0 * q_0.))))", "(-6 * q_0 * q_0.))");
    }
}
