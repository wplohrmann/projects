use super::expr::Expr;

pub struct Equation {
    lhs: Expr,
    rhs: Expr
}

impl Equation {
    pub fn new(lhs: &Expr, rhs: &Expr) -> Self {
        Equation{lhs: lhs.clone(), rhs: rhs.clone()}
    }

    pub fn simplify(&mut self) {
        self.rhs = self.rhs.simplify();
        self.lhs = self.lhs.simplify();
    }

    pub fn solve_for(&mut self, variable: &Expr) -> Option<Expr> {
        println!("{} == {}", self.lhs, self.rhs);
        let mut equation = Equation::new(&(self.lhs.clone() - self.rhs.clone()), &Expr::Constant(0.));
        loop {
            equation.simplify();
            println!("{} == {}", equation.lhs, equation.rhs);
            match equation.lhs.clone() {
                Expr::Add(es) => {
                    for e in es {
                        if !e.contains(variable) {
                            equation -= e;
                        }
                    }
                },
                Expr::Mul(_es) => {
                    todo!()
                },
                e if e == *variable => return Some(equation.rhs),
                _ => return None
            }
        }
    }
}

impl std::ops::SubAssign<Expr> for Equation {
    fn sub_assign(&mut self, rhs: Expr) {
        self.rhs = self.rhs.clone() - rhs.clone();
        self.lhs = self.lhs.clone() - rhs.clone();
    }
}

impl std::ops::AddAssign<f32> for Equation {
    fn add_assign(&mut self, rhs: f32) {
        self.rhs = self.rhs.clone() + Expr::Constant(rhs);
        self.lhs = self.lhs.clone() + Expr::Constant(rhs);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_to_equation() {
        let lhs = "(q_0 + -5)".parse::<Expr>().unwrap();
        let rhs = Expr::Constant(5.);
        let mut equation = Equation::new(&lhs, &rhs);
        equation += 5.;
        equation.simplify();
        assert_eq!(equation.lhs, Expr::Coord(0, 0));
        assert_eq!(equation.rhs, Expr::Constant(10.));
    }

    #[test]
    fn solve_for() {
        let lhs = "(q_0 + -5)".parse::<Expr>().unwrap();
        let rhs = Expr::Constant(5.);
        let mut equation = Equation::new(&lhs, &rhs);
        assert_eq!(equation.solve_for(&Expr::Coord(0, 0)).unwrap(), Expr::Constant(10.));
    }
}

