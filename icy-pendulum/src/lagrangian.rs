use super::expr::Expr;

pub trait Lagrangian {
    fn lagrangian(&self) -> Expr;
}

