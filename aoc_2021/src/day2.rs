use std::str::FromStr;
use std::io::BufRead;
use std::io;

#[derive(Debug)]
struct State {
    x: i32,
    y: i32
}

impl State {
    pub fn new() -> Self {
        State{x: 0, y: 0}
    }
}

#[derive(Debug)]
struct ParseErr;

impl FromStr for State {
    type Err = ParseErr;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let split: Vec<_> = s.split(" ").collect();
        let distance = split[1].parse::<i32>().unwrap();
        match split[0] {
            "forward" => Ok(Self{x: distance, y: 0}),
            "down" => Ok(Self{x: 0, y: distance}),
            "up" => Ok(Self{x: 0, y: -distance}),
            _ => Err(ParseErr)
        }
    }
}


pub fn part1() {
    let stdin = io::stdin();
    let final_state: State = stdin.lock().lines().map(|x| {
        match x {
            Ok(line) => State::from_str(&line).unwrap(),
            Err(_) => panic!("Unable to read from stdin")
        }
    }).fold(State::new(), |acc, new| {
        State{x: acc.x + new.x, y: acc.y + new.y}
    });
    let answer = final_state.x * final_state.y;
    println!("{}", answer)
}

pub fn part2() {
    let stdin = io::stdin();
    let final_state: State = stdin.lock().lines().map(|x| {
        match x {
            Ok(line) => State::from_str(&line).unwrap(),
            Err(_) => panic!("Unable to read from stdin")
        }
    }).fold(State::new(), |acc, new| {
        State{x: acc.x + new.x, y: acc.y + new.y}
    });
    let answer = final_state.x * final_state.y;
    println!("{}", answer)
}