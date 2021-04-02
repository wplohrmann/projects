mod dynamic;
mod pendulum;

use iced::{
    canvas::{self, Cache, Canvas, Cursor, Geometry, LineCap, Path, Stroke},
    executor, time, Application, Clipboard, Color, Command, Container, Element, Length, Point,
    Rectangle, Settings, Subscription, Vector,
};

use dynamic::Dynamic;
use pendulum::Pendulum;

pub fn main() -> iced::Result {
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

impl Application for App<Pendulum> {
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
        time::every(std::time::Duration::from_millis(20)).map(|_| Message::Tick(20e-3))
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

impl canvas::Program<Message> for App<Pendulum> {
    fn draw(&self, bounds: Rectangle, _cursor: Cursor) -> Vec<Geometry> {
        let background = self.canvas.draw(bounds.size(), |frame| {
            let background = Path::rectangle(Point { x: 0., y: 0. }, frame.size());
            frame.fill(&background, Color::new(0., 1., 0., 0.5));

            self.system.draw(frame);
        });

        // let drawn_system = self.system.draw(bounds, &self.canvas);

        vec![background]
    }
}
