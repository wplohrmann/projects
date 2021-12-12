use std::io::BufRead;

pub fn part1() {
    let mut crabs: Vec<_> = std::io::stdin().lock().lines().next().unwrap().unwrap()
        .split(",")
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    crabs.sort();
    let position = crabs[crabs.len() / 2];

    let answer: isize = crabs.iter().map(|x| (*x as isize-position as isize).abs()).sum();
    println!("{}", answer);
}

fn score(x: usize, y: usize) -> usize {
    let n = if x > y {x-y} else {y-x};
    if n == 0 { return 0 }
    if n == 1 { return 1 }
    (n + 1) * n / 2
}

pub fn part2() {
    let crabs: Vec<_> = std::io::stdin().lock().lines().next().unwrap().unwrap()
        .split(",")
        .map(|s| s.parse::<usize>().unwrap())
        .collect();

    let mut best_score = 1000000000000000;
    let crab_max = *crabs.iter().max().unwrap();
    let crab_min = *crabs.iter().min().unwrap();
    for position in crab_min..crab_max {
        let one_score: usize = crabs.iter().map(|x| score(*x, position)).sum();
        best_score = best_score.min(one_score);
    }
    println!("{}", best_score);
}