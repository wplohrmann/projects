use std::collections::HashMap;
use std::io::BufRead;

fn parse_player(line: String) -> usize {
    let number = line.split_whitespace().last().unwrap();
    number.parse::<usize>().unwrap()
}

pub fn part1() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let mut p1 = parse_player(lines.next().unwrap().unwrap());
    let mut p2 = parse_player(lines.next().unwrap().unwrap());
    let mut p1_score = 0;
    let mut p2_score = 0;
    let mut next = 1;
    loop {
        p1 = (p1 + next * 3 + 3 - 1) % 10 + 1;
        next += 3;
        p1_score += p1;
        if p1_score >= 1000 {
            println!("{}", p2_score * (next-1));
            return
        }
        p2 = (p2 + next * 3 + 3 - 1) % 10 + 1;
        next += 3;
        p2_score += p2;
        if p2_score >= 1000 {
            println!("{}", p1_score * (next-1));
            return
        }
    }
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let p1 = parse_player(lines.next().unwrap().unwrap());
    let p2 = parse_player(lines.next().unwrap().unwrap());
    let possible_throws = {
        let mut outcomes: HashMap<usize, usize> = HashMap::new();
        for t1 in [1, 2, 3] {
            for t2 in [1, 2, 3] {
                for t3 in [1, 2, 3] {
                    *outcomes.entry(t1+t2+t3).or_insert(0) += 1;
                }
            }
        }
        outcomes
    };
    // Mapping from (p1_pos, p1_score, p2_pos, p2_score) to number
    // of universes in which that outcome occurs
    let mut outcomes: HashMap<(usize, usize, usize, usize), usize> = HashMap::from([
        ((p1, 0, p2, 0), 1),
    ]);
    let mut p1_wins = 0;
    let mut p2_wins = 0;
    loop {
        let mut new_outcomes = HashMap::new();
        for ((p1_pos, p1_score, p2_pos, p2_score), num_outcomes) in outcomes.drain() {
            for (total, total_frequency) in &possible_throws {
                let new_p1_pos = (p1_pos + total -1) % 10 + 1;
                let new_p1_score = p1_score + new_p1_pos;
                if new_p1_score >= 21 {
                    p1_wins += num_outcomes * total_frequency;
                } else {
                    *new_outcomes.entry((new_p1_pos, new_p1_score, p2_pos, p2_score)).or_insert(0) += num_outcomes * total_frequency;
                }
            }
        }
        outcomes = new_outcomes;
        let mut new_outcomes = HashMap::new();
        for ((p1_pos, p1_score, p2_pos, p2_score), num_outcomes) in outcomes.drain() {
            for (total, total_frequency) in &possible_throws {
                let new_p2_pos = (p2_pos + total -1) % 10 + 1;
                let new_p2_score = p2_score + new_p2_pos;
                if new_p2_score >= 21 {
                    p2_wins += num_outcomes * total_frequency;
                } else {
                    *new_outcomes.entry((p1_pos, p1_score, new_p2_pos, new_p2_score)).or_insert(0) += num_outcomes * total_frequency;
                }
            }
        }
        outcomes = new_outcomes;
        if outcomes.len() == 0 {
            break
        }
    }
    println!("{}", p1_wins.max(p2_wins));
}