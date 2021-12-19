use std::io::BufRead;

pub fn part1() {
    for line in std::io::stdin().lock().lines() {
        println!("{}", line.unwrap());
    }
}