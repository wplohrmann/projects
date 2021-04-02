use iced::{
    canvas::{self, Cache, Canvas, Cursor, Geometry, LineCap, Path, Stroke},
    Color, Command, Container, Point, Rectangle, Settings, Subscription, Vector,
};

use iced::widget::canvas::Frame;

use super::dynamic::Dynamic;

pub struct Pendulum {
    theta: f32,
    dtheta_dt: f32, // angular velocity in units of tick
    omega_sq: f32,
}

impl Default for Pendulum {
    fn default() -> Self {
        // Hanging to the right at 45 degrees with a period of 1 second
        Self {
            theta: std::f32::consts::PI / 4.,
            dtheta_dt: 0.,
            omega_sq: (2. * std::f32::consts::PI).powi(2),
        }
    }
}

impl Dynamic for Pendulum {
    fn step(&mut self, dt: f32) {
        // ODE: theta.. = - omega^2 * theta
        self.theta += self.dtheta_dt * dt;
        self.dtheta_dt += -self.omega_sq * self.theta * dt;
    }
}

impl Pendulum {
    pub fn draw(&self, frame: &mut Frame) {
        let center = frame.center();
        frame.translate(Vector::new(center.x, center.y));

        let length = frame.width().min(frame.height()) / 2.0;
        let line = Path::line(
            Point::ORIGIN,
            Point::new(length * self.theta.sin(), -length * self.theta.cos()),
        );

        let thin_stroke = Stroke {
            width: length / 100.0,
            color: Color::new(1., 0., 0., 1.),
            line_cap: LineCap::Round,
            ..Stroke::default()
        };

        frame.stroke(&line, thin_stroke);
    }
}
