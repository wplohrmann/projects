use std::io::BufRead;
use std::collections::{HashMap};

pub fn part1() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let line = lines.next().unwrap().unwrap();
    let mut pairs: HashMap<(char, char), usize> = HashMap::new();
    let mut elements: HashMap<char, usize> = HashMap::new();
    let mut last_char = None;
    for c in line.chars() {
        match last_char {
            None => {},
            Some(last_c) => {
                *pairs.entry((last_c, c)).or_insert(0) += 1;
            }
        }
        last_char = Some(c);
        *elements.entry(c).or_insert(0) += 1;
    }

    lines.next(); // Skip blank line
    let mut rules: HashMap<(char, char), char> = HashMap::new();
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        let mut split = line.split(" -> ");
        let lhs: Vec<_> = split.next().unwrap().chars().collect();
        let rhs = split.next().unwrap().chars().last().unwrap();
        rules.insert((lhs[0], lhs[1]), rhs);
    }
    for _ in 0..10 {
        let mut new_pairs = HashMap::new();
        for ((c1, c2), count) in pairs.drain() {
            if let Some(insert_c) = rules.get(&(c1, c2)) {
                *elements.entry(*insert_c).or_insert(0) += count;
                // Insert new pairs
                *new_pairs.entry((c1, *insert_c)).or_insert(0) += count;
                *new_pairs.entry((*insert_c, c2)).or_insert(0) += count;
                // Remove old pairs
            }
        }
        pairs = new_pairs;
    }
    println!("{}", elements.values().max().unwrap() - elements.values().min().unwrap());
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let line = lines.next().unwrap().unwrap();
    let mut pairs: HashMap<(char, char), usize> = HashMap::new();
    let mut elements: HashMap<char, usize> = HashMap::new();
    let mut last_char = None;
    for c in line.chars() {
        match last_char {
            None => {},
            Some(last_c) => {
                *pairs.entry((last_c, c)).or_insert(0) += 1;
            }
        }
        last_char = Some(c);
        *elements.entry(c).or_insert(0) += 1;
    }

    lines.next(); // Skip blank line
    let mut rules: HashMap<(char, char), char> = HashMap::new();
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        let mut split = line.split(" -> ");
        let lhs: Vec<_> = split.next().unwrap().chars().collect();
        let rhs = split.next().unwrap().chars().last().unwrap();
        rules.insert((lhs[0], lhs[1]), rhs);
    }
    for _ in 0..40 {
        let mut new_pairs = HashMap::new();
        for ((c1, c2), count) in pairs.drain() {
            if let Some(insert_c) = rules.get(&(c1, c2)) {
                *elements.entry(*insert_c).or_insert(0) += count;
                // Insert new pairs
                *new_pairs.entry((c1, *insert_c)).or_insert(0) += count;
                *new_pairs.entry((*insert_c, c2)).or_insert(0) += count;
                // Remove old pairs
            }
        }
        pairs = new_pairs;
    }
    println!("{}", elements.values().max().unwrap() - elements.values().min().unwrap());
}