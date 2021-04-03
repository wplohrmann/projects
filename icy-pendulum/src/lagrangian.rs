use std::ops;

#[derive(Clone, PartialEq, PartialOrd)]
pub enum Expr {
    Constant(f32), // Constant value
    Coord(usize, usize), // An indexed coordinate, time-differentiated n times
    Add(Vec<Expr>),
    Mul(Box<Expr>, Box<Expr>), // Binary multiplication
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
            Expr::Mul(e1, e2) => e1.dot() * (**e2).clone() + (**e1).clone() * e2.dot(),
            Expr::Constant(_) => Expr::Constant(0.),
        }
    }

    pub fn simplify(&self) -> Expr {
        let mut last = self.clone();
        loop {
            let simplified = match self {
                Expr::Add(es) => simplify_add(es),
                Expr::Mul(e1, e2) => simplify_mul(e1, e2),
                _ => self.clone(),
            };
            if simplified == last {
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
    simplified.sort_by(|a, b| a.partial_cmp(b).unwrap());

    Expr::Add(simplified)
}

pub fn simplify_mul(e1: &Expr, e2: &Expr) -> Expr {
    if e1 == &Expr::Constant(0.) {
        return Expr::Constant(0.);
    } else if e2 == &Expr::Constant(0.) {
        return Expr::Constant(0.);
    }

    let e1_simplified = e1.simplify();
    let e2_simplified = e2.simplify();

    if e1_simplified <= e2_simplified {
        return e1_simplified * e2_simplified;
    } else {
        return e2_simplified * e1_simplified;
    }
}

impl std::fmt::Display for Expr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Expr::Coord(i, n) => write!(f, "q_{}{}", i, ".".repeat(*n)),
            Expr::Add(es) => write!(f, "({})", es.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(" + ")),
            Expr::Mul(e1, e2) => write!(f, "{} * {}", e1, e2),
            Expr::Constant(k) => write!(f, "{}", k)
        }
    }
}

impl ops::Mul<Expr> for f32 {
    type Output = Expr;

    fn mul(self, rhs: Expr) -> Self::Output {
        Expr::Mul(Box::new(rhs), Box::new(Expr::Constant(self)))
    }
}

impl ops::Mul<Expr> for &f32 {
    type Output = Expr;

    fn mul(self, rhs: Expr) -> Self::Output {
        Expr::Mul(Box::new(rhs), Box::new(Expr::Constant(*self)))
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
        Expr::Mul(Box::new(self.clone()), Box::new(rhs))
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
