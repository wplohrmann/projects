use std::io::BufRead;
use std::collections::BinaryHeap;

pub fn part1() {
    let mut risks = Vec::new();
    let mut width = 1;
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        width = line.len();
        risks.extend(line.chars().map(|c| c.to_digit(10).unwrap()));
    }
    let height = risks.len() / width;
    let mut distances = vec![u32::MAX; width * height];
    distances[0] = 0;
    let mut heap = BinaryHeap::new();
    heap.push((-(distances[0] as isize), 0));
    while let Some((distance, i)) = heap.pop() {
        let distance = (-distance) as u32;
        if i == (width * height - 1) {
            println!("{}", distance);
            return;
        }
        if distance > distances[i] { continue; }
        for k in neighbours(i, width, height) {
            let new_distance = distance + risks[k];

            if new_distance < distances[k] {
                heap.push((-(new_distance as isize), k));
                distances[k] = new_distance;
            }
        }
    }
}

fn neighbours(start: usize, width: usize, height: usize) -> impl Iterator<Item=usize> {
    let x = start % width;
    let y = (start - x) / width;
    let mut coords = Vec::new();
    if x > 0 {
        coords.push(y * width + x - 1);
    }
    if x < width -1 {
        coords.push(y * width + x + 1);
    }
    if y > 0 {
        coords.push((y - 1) * width + x);
    }
    if y < height - 1 {
        coords.push((y + 1) * width + x);
    }
    coords.into_iter()
}

pub fn part2() {
    const N: u32 = 5;
    let mut risks = Vec::new();
    let mut width = 1;
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        width = line.len();
        for i in 0..N {
            risks.extend(line.chars().map(|c| (c.to_digit(10).unwrap() - 1 + i) % 9 + 1));
        }
    }
    let mut big_risks = Vec::new();
    width = width * (N as usize);
    for i in 0..N { // Copy the board 5 times
        big_risks.extend(risks.iter().map(|n| (n - 1 + i) % 9 + 1))
    }
    risks = big_risks;
    let height = risks.len() / width;
    let mut distances = vec![u32::MAX; width * height];
    distances[0] = 0;
    let mut heap = BinaryHeap::new();
    heap.push((-(distances[0] as isize), 0));
    while let Some((distance, i)) = heap.pop() {
        let distance = (-distance) as u32;
        if i == (width * height - 1) {
            println!("{}", distance);
            return;
        }
        if distance > distances[i] { continue; }
        for k in neighbours(i, width, height) {
            let new_distance = distance + risks[k];

            if new_distance < distances[k] {
                heap.push((-(new_distance as isize), k));
                distances[k] = new_distance;
            }
        }
    }
}

fn print(board: &Vec<u32>, height: usize, width: usize) {
    for i in 0..height {
        for j in 0..width {
            print!("{} ", board[i * width + j]);
        }
        println!();
    }
    println!();
}