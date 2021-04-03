use std::ops;

#[derive(Clone, PartialEq, PartialOrd)]
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

    pub fn unwrap_mul(self) -> Vec<Expr> {
        match self {
            Expr::Mul(es) => es,
            _ => panic!("Tried to unwrap_mul on non-Mul expression")
        }
    }

}

pub fn simplify_add(es: &Vec<Expr>) -> Expr {
    let mut simplified = es.iter()
        .filter(|&e| e != &Expr::Constant(0.))
        .map(|e| e.simplify())
        .collect::<Vec<Expr>>();
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
        Expr::Mul(vec![self.clone(), rhs])
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
