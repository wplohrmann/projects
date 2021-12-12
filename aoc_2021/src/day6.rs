use std::io::BufRead;

pub fn part1() {
    const n: usize = 9;
    let mut fish: [usize; n] = [0; n];
    std::io::stdin().lock().lines().next().unwrap().unwrap()
        .split(",")
        .for_each(|s| {
            fish[s.parse::<usize>().unwrap()] += 1;
        });
    let mut zero_pointer = 0;
    for _ in 0..256 {
        let zeros = fish[zero_pointer];
        fish[zero_pointer] = 0;
        fish[(zero_pointer + 9) % n] += zeros; // New fish
        fish[(zero_pointer + 7) % n] += zeros; // Old fish
        zero_pointer = (zero_pointer + 1) % n;
    }
    let answer: usize = fish.iter().sum();
    println!("{}", answer);
}