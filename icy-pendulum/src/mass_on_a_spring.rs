use super::expr::Expr;
use super::lagrangian::Lagrangian;

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
