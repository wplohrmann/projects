use std::str::FromStr;
use std::io::BufRead;
use std::io;

#[derive(Debug, Clone)]
struct Command {
    digits: [u32; 12],
}

#[derive(Debug)]
struct ParseErr;

impl FromStr for Command {
    type Err = ParseErr;
    fn from_str(line: &str) -> Result<Self, Self::Err> {
        let mut digits = [0; 12];
        let mut chars = line.chars();
        for i in 0..12 {
            let digit = chars.next().unwrap();
            if digit == '1' {
                digits[i] += 1;
            }
        }
        Ok(Command{digits})
    }
}

pub fn part1() {
    let stdin = io::stdin();
    let mut final_state = [0; 12];
    let mut count = 0;
    stdin.lock().lines().map(|x| {
        match x {
            Ok(line) => Command::from_str(&line).unwrap(),
            Err(_) => panic!("Unable to read from stdin")
        }
    }).for_each(|command| {
        count += 1;
        for (i, digit) in command.digits.into_iter().enumerate() {
            final_state[i] += digit;
        }
    });
    let threshold = count / 2;
    let mut most_digits = 0;
    let mut least_digits = 0;
    for i in 0..12 {
        most_digits *= 2;
        least_digits *= 2;
        if final_state[i] > threshold {
            most_digits += 1;
        } else {
            least_digits += 1;
        }
    }
    let answer = most_digits * least_digits;

    println!("{}", answer)
}