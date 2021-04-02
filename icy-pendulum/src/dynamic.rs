#[derive(Clone)]
pub enum Expr {
    Coord(usize), // An indexed coordinate
    CoordDot(usize), // Derivative of an indexed coordinate
    CoordDotDot(usize), // Derivative of an indexed coordinate
    Add(Box<Expr>, Box<Expr>), // Binary addition
    Mul(Box<Expr>, Box<Expr>), // Binary multiplication
    Scaled(Box<Expr>, f32), // Scalar multiplication
    // Sin(Box<Expr>), // sin (trig)
    // Cos(Box<Expr>), // cos (trig)
}
pub trait Dynamic {
    fn step(&mut self, dt: f32);

    fn lagrangian(&self) -> Expr {
        Expr::Coord(5)
    }
}

impl Expr {
    fn dot(&self) -> Expr {
        match self {
            Expr::Coord(i) => Expr::CoordDot(*i),
            Expr::CoordDot(i) => Expr::CoordDotDot(*i),
            Expr::CoordDotDot(_i) => todo!(), // Need to handle this error properly but should not be possible from simple lagrangian system
            Expr::Add(e1, e2) => Expr::Add(Box::new(e1.dot()), Box::new(e2.dot())),
            Expr::Mul(e1, e2) => Expr::Add(Box::new(Expr::Mul(Box::new(e1.dot()), (*e2).clone())), Box::new(Expr::Mul(Box::new(e2.dot()), (*e1).clone()))),
            Expr::Scaled(e, scale) => Expr::Scaled(Box::new(e.dot()), *scale),
        }
    }
}
