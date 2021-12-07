use std::io::BufRead;
use std::io;

pub fn part1() {
    let stdin = io::stdin();
    let answer: u32 = stdin.lock().lines().map(|x| {
        match x {
            Ok(line) => line.parse::<u32>().unwrap(),
            Err(_) => panic!("Unable to read from stdin")
        }
    }).fold((0, 0), |acc, new| {
        if new > acc.1 {(acc.0 + 1, new)} else {(acc.0, new)}
    }).0 - 1;
    println!("{}", answer)
}

pub fn part2() {
    let stdin = io::stdin();
    let running_average = stdin.lock().lines().map(|x| {
        match x {
            Ok(line) => line.parse::<u32>().unwrap(),
            Err(_) => panic!("Unable to read from stdin")
        }
    }).scan((0, 0, 0), |state, new| {
        *state = (state.1, state.2, new);
        Some(*state)
    }).map(|x| x.0+x.1+x.2).skip(2);
    let answer = running_average.fold((0, 0), |acc, new| {
        if new > acc.1 {(acc.0 + 1, new)} else {(acc.0, new)}
    }).0 - 1;
    println!("{}", answer)
}