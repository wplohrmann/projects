use iced::button;

pub struct Counter {
    // The counter value
    pub value: i32,

    // The local state of the two buttons
    increment_button: button::State,
    decrement_button: button::State,
}
