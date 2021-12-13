use std::collections::BTreeMap;
use std::collections::HashMap;
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
    let mut num_lows = 0;
    for i in 0..height {
        for j in 0..width {
            let value = map[i * width + j];
            if j < width - 1 && map[i * width + j + 1] <= value {
                continue
            }
            if j > 0 && map[i * width + j-1] <= value {
                continue
            }
            if i < height-1 && map[(i+1) * width + j] <= value {
                continue
            }
            if i > 0 && map[(i - 1) * width + j] <= value {
                continue
            }

            // None of neighbours are lower than value
            num_lows += 1 + value;

        }
    }
    // dbg!(map);
    println!("{}", num_lows);
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut map= Vec::new();
    let mut width = 0;
    for s in stdin.lock().lines() {
        let line = s.unwrap();
        width = line.len();
        map.extend(line.chars().map(|c| c.to_digit(10).unwrap() as usize));
    }
    let height = map.len() / width;
    let mut directions = BTreeMap::new();
    let mut basins = vec![0; width * height];
    let mut max_label = 0;
    for i in 0..height {
        for j in 0..width {
            let value = map[i * width + j];
            if value == 9 {
                continue
            }
            let mut lowest = true;
            if j < width - 1 && map[i * width + j + 1] < value {
                directions.insert((i, j), (i, j+1));
                lowest = false;
            }
            if j > 0 && map[i * width + j-1] <= value {
                directions.insert((i, j), (i, j-1));
                lowest = false;
            }
            if i < height-1 && map[(i+1) * width + j] < value {
                directions.insert((i, j), (i+1, j));
                lowest = false;
            }
            if i > 0 && map[(i - 1) * width + j] < value {
                directions.insert((i, j), (i-1, j));
                lowest = false;
            }

            if lowest {
                max_label += 1;
                basins[i * width + j] = max_label;
            }
        }
    }
    let mut done = false;
    while !done {
        done = true;
        for (key, value) in directions.iter() {
            if basins[value.0 * width + value.1] != 0 {
                basins[key.0 * width + key.1] = basins[value.0 * width + value.1];
            } else {
                done = false;
            }
        }
    }
    let mut sizes = vec![0; max_label];
    basins.iter().for_each(|x| {
        if x != &0 {
            sizes[x-1] += 1;
        }
    });
    sizes.sort();
    let answer = sizes.into_iter().rev().take(3).reduce(|a, b| a*b).unwrap();
    println!("{}", answer);
}
