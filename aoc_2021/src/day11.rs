use std::collections::HashSet;
use std::io::BufRead;

pub fn part1() {
    let stdin = std::io::stdin();
    let mut map = Vec::new();
    let mut width = 0;
    for s in stdin.lock().lines() {
        let line = s.unwrap();
        width = line.len();
        map.extend(line.chars().map(|c| c.to_digit(10).unwrap()));
    }
    let height = map.len() / width;
    let mut count = 0;
    for _ in 0..100 {
        let mut flashes = HashSet::new();
        let mut maybe_flashes = Vec::new();
        for i in 0..height {
            for j in 0..width {
                let index = i * width + j;
                map[index] += 1;
                if map[index] > 9 {
                    flashes.insert((i, j));
                    for (k, l) in neighbours(i, j, width, height) {
                        let index = k * width + l;
                        map[index] += 1;
                        maybe_flashes.push((k, l));
                    }
                }

            }
        }
        while let Some((i, j)) = maybe_flashes.pop() {
            let index = i * width + j;
            if !flashes.contains(&(i, j)) && map[index] > 9 {
                flashes.insert((i, j));
                for (k, l) in neighbours(i, j, width, height) {
                    let index = k * width + l;
                    map[index] += 1;
                    maybe_flashes.push((k, l));
                }
            }
        }
        for (i, j) in flashes.iter() {
            let index = i * width + j;
            count += 1;
            map[index] = 0;
        }
    }
    println!("{}", count);
}

fn neighbours(i: usize, j: usize, width: usize, height: usize) -> impl Iterator<Item=(usize, usize)> {
    let mut coords = Vec::new();
    for di in [-1, 0, 1] {
        for dj in [-1, 0, 1] {
            let k;
            if di < 0 {
                if i == 0 {
                    continue
                } else {
                    k = i - 1;
                }
            } else if di == 0 {
                k = i;
            } else {
                if i == height - 1 {
                    continue
                } else {
                    k = i + 1;
                }
            }
            let l;
            if dj < 0 {
                if j == 0 {
                    continue
                } else {
                    l = j - 1;
                }
            } else if dj == 0 {
                l = j;
            } else {
                if j == width - 1 {
                    continue
                } else {
                    l = j + 1;
                }
            }
            coords.push((k, l));

        }
    }
    coords.into_iter()
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut map = Vec::new();
    let mut width = 0;
    for s in stdin.lock().lines() {
        let line = s.unwrap();
        width = line.len();
        map.extend(line.chars().map(|c| c.to_digit(10).unwrap()));
    }
    let height = map.len() / width;
    for n in 0.. {
        let mut flashes = HashSet::new();
        let mut maybe_flashes = Vec::new();
        for i in 0..height {
            for j in 0..width {
                let index = i * width + j;
                map[index] += 1;
                if map[index] > 9 {
                    flashes.insert((i, j));
                    for (k, l) in neighbours(i, j, width, height) {
                        let index = k * width + l;
                        map[index] += 1;
                        maybe_flashes.push((k, l));
                    }
                }
            }
        }
        while let Some((i, j)) = maybe_flashes.pop() {
            let index = i * width + j;
            if !flashes.contains(&(i, j)) && map[index] > 9 {
                flashes.insert((i, j));
                for (k, l) in neighbours(i, j, width, height) {
                    let index = k * width + l;
                    map[index] += 1;
                    maybe_flashes.push((k, l));
                }
            }
        }
        for (i, j) in flashes.iter() {
            let index = i * width + j;
            map[index] = 0;
        }
        if flashes.len() == width * height {
            println!("{}", n + 1);
            return;
        }
    }
}
