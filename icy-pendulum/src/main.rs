extern crate pest;
#[macro_use]
extern crate pest_derive;

mod drawable;
mod dynamic;
mod pendulum;
mod lagrangian;

use iced::{
    canvas::{self, Cache, Canvas, Cursor, Geometry, LineCap, Path, Stroke},
    executor, time, Application, Clipboard, Color, Command, Container, Element, Length, Point,
    Rectangle, Settings, Subscription, Vector,
};

use drawable::Drawable;
use dynamic::Dynamic;
use pendulum::Pendulum;
use lagrangian::{MassOnASpring, Lagrangian, Expr};

pub fn main() -> iced::Result {
    // let mass_on_a_spring = MassOnASpring{x: 5., v: 5., omega_sq: 6.};
    // println!("{}", mass_on_a_spring.lagrangian().dot().simplify());
    let e = Expr::Constant(0.) + (Expr::Constant(0.5) + Expr::Coord(0, 2));
    println!("{}", e.simplify());
    if true {
        panic!("ohno");
    }
    App::<Pendulum>::run(Settings {
        antialiasing: true,
        ..Settings::default()
    })
}

struct App<T: dynamic::Dynamic + Default> {
    system: T,
    canvas: Cache,
}

#[derive(Debug, Clone, Copy)]
enum Message {
    Tick(f32),
}

impl<T: Dynamic + Default + Drawable> Application for App<T> {
    type Executor = executor::Default;
    type Message = Message;
    type Flags = ();

    fn new(_flags: ()) -> (Self, Command<Message>) {
        (
            App {
                system: Default::default(),
                canvas: Default::default(),
            },
            Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("App - Iced")
    }

    fn update(&mut self, message: Message, _clipboard: &mut Clipboard) -> Command<Message> {
        match message {
            Message::Tick(dt) => {
                self.system.step(dt);
                self.canvas.clear();
            }
        }

        Command::none()
    }

    fn subscription(&self) -> Subscription<Message> {
        time::every(std::time::Duration::from_millis(5)).map(|_| Message::Tick(5e-3))
    }

    fn view(&mut self) -> Element<Message> {
        let canvas = Canvas::new(self)
            .width(Length::Units(400))
            .height(Length::Units(400));

        Container::new(canvas)
            .width(Length::Fill)
            .height(Length::Fill)
            .padding(20)
            .center_x()
            .center_y()
            .into()
    }
}

impl<T: Drawable + Dynamic + Default> canvas::Program<Message> for App<T> {
    fn draw(&self, bounds: Rectangle, _cursor: Cursor) -> Vec<Geometry> {
        let background = self.canvas.draw(bounds.size(), |frame| {
            let background = Path::rectangle(Point { x: 0., y: 0. }, frame.size());
            frame.fill(&background, Color::new(0., 1., 0., 1.));

            Drawable::draw(&self.system, frame);
        });

        // let drawn_system = self.system.draw(bounds, &self.canvas);

        vec![background]
    }
}
