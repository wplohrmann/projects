use std::collections::{HashMap, HashSet};
use std::io::BufRead;

pub fn part1() {
    let stdin = std::io::stdin();
    let mut count = 0;
    for s in stdin.lock().lines() {
        let line = s.unwrap();
        let mut words = line.split_whitespace();
        let _combinations: Vec<_> = words.by_ref().take(10).collect();
        let output: Vec<_> = words.skip(1).collect();
        assert_eq!(output.len(), 4);
        output.into_iter().for_each(|x| {
            match x.len() {
                2 | 3 | 4 | 7 => {count += 1; }
                _ => {}
            }
        })
    }
    println!("{}", count);
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut wires: HashSet<usize> = HashSet::new();
    for i in 0..7 {
        wires.insert(i);
    }
    let mut digits: HashMap<usize, HashSet<usize>> = HashMap::new();
    digits.insert(0, HashSet::from([0, 1, 2, 4, 5, 6]));
    digits.insert(1, HashSet::from([2, 5]));
    digits.insert(2, HashSet::from([0, 2, 3, 4, 6]));
    digits.insert(3, HashSet::from([0, 2, 3, 5, 7]));
    digits.insert(4, HashSet::from([1, 2, 3, 5]));
    digits.insert(5, HashSet::from([0, 1, 3, 5, 7]));
    digits.insert(6, HashSet::from([0, 1, 3, 4, 5, 6]));
    digits.insert(7, HashSet::from([0, 2, 6]));
    digits.insert(8, HashSet::from([0, 1, 2, 3, 4, 5, 6]));
    digits.insert(9, HashSet::from([0, 1, 2, 3, 5, 6]));
    
    for s in stdin.lock().lines() {
        let line = s.unwrap();
        let mut words = line.split_whitespace().map(|word| word.chars().map(|c| match c {
            'a' => 0,
            'b' => 1,
            'c' => 2,
            'd' => 3,
            'e' => 4,
            'f' => 5,
            'g' => 6,
            'h' => 7,
            '|' => 8, // Ignored anyway
            _ => panic!("{}", c),
        }).collect::<HashSet<usize>>());
        let combinations: Vec<_> = words.by_ref().take(10).collect();
        let output: Vec<_> = words.skip(1).collect();
        assert_eq!(output.len(), 4);

        // possibilities map each character to the set of possible wires
        let mut possibilities: HashMap<usize, HashSet<usize>> = HashMap::new();
        for i in 0..7 {
            possibilities.insert(i,  wires.clone());
        }
        for combination in combinations {

        }
    }
    // println!("{}", count);
}