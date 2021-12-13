use std::collections::HashMap;
use std::io::BufRead;

pub fn part1() {
    let pairs = HashMap::from([
        ('(', ')'),
        ('[', ']'),
        ('{', '}'),
        ('<', '>'),

    ]);
    let points = HashMap::from([
        (')', 3),
        (']', 57),
        ('}', 1197),
        ('>', 25137),

    ]);
    let mut score = 0;
    for s in std::io::stdin().lock().lines() {
        let line = s.unwrap();
        let mut stack = Vec::new();
        line.chars().for_each(|c| {
            if stack.len() == 0 {
                stack.push(c);
            } else if pairs.contains_key(&c) {
                stack.push(c);
            } else { // c is a closing bracket - must match
                if c != pairs[&stack.pop().unwrap()] {
                    score += points[&c];
                }
            }
        })
    }
    println!("{}", score);
}

pub fn part2() {
    let pairs = HashMap::from([
        ('(', ')'),
        ('[', ']'),
        ('{', '}'),
        ('<', '>'),

    ]);
    let points = HashMap::from([
        ('(', 1),
        ('[', 2),
        ('{', 3),
        ('<', 4),

    ]);
    let mut scores: Vec<u128> = Vec::new();
    for s in std::io::stdin().lock().lines() {
        let mut score = 0;
        let line = s.unwrap();
        let mut stack = Vec::new();
        let mut corrupt = false;
        line.chars().for_each(|c| {
            if stack.len() == 0 {
                stack.push(c);
            } else if pairs.contains_key(&c) {
                stack.push(c);
            } else { // c is a closing bracket - must match
                if c != pairs[&stack.pop().unwrap()] {
                    corrupt = true;
                    return
                }
            }
        });
        if corrupt {
            continue
        }
        while let Some(c) = stack.pop() {
            score = score * 5 + points[&c];
        }
        scores.push(score);
    }
    println!("{}", quick_median(&scores));
}

fn quick_median(v: &Vec<u128>) -> u128 {
    quick_select(v, v.len() / 2)
}

fn quick_select(v: &Vec<u128>, k: usize) -> u128 {
    if v.len() == 1 {
        assert_eq!(k, 0);
        return v[0];
    }
    let pivot = v[v.len() / 2];
    let (greaters, lessers): (Vec<u128>, Vec<u128>) = v.iter().partition(|x| x > &&pivot);
    if lessers.len() > k {
        return quick_select(&lessers, k)
    } else {
        return quick_select(&greaters, k - lessers.len())
    }

}