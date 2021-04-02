use iced::widget::canvas::Frame;

pub trait Drawable {
    fn draw(&self, frame: &mut Frame);
}
