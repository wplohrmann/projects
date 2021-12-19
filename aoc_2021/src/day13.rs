use std::io::BufRead;
use std::collections::HashSet;

pub fn part1() {
    let mut dots = HashSet::new(); // Indexed by x
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    for maybe_line in &mut lines {
        let line = maybe_line.unwrap();
        if line == "" {
            break
        }
        let mut split = line.split(",").map(|s| s.parse::<u32>().unwrap());
        let x = split.next().unwrap();
        let y = split.next().unwrap();
        dots.insert((x, y));
    }
    let mut commands = Vec::new();
    for maybe_line in &mut lines {
        let line = maybe_line.unwrap();
        let mut command = line.split(" ").last().unwrap().split("=");
        match command.next() {
            Some("y") => {
                let coord = command.next().unwrap().parse::<u32>().unwrap();
                commands.push((0, coord));
            }
            Some("x") => {
                let coord = command.next().unwrap().parse::<u32>().unwrap();
                commands.push((coord, 0));
            }
            Some(_) | None => {
                panic!("Oh no")
            }
        }
    }
    for (fold_x, fold_y) in commands.into_iter() {
        if fold_x > 0 {
            let (folded, kept): (Vec<(u32, u32)>, Vec<(u32, u32)>) = dots.drain().partition(|(x, _)| x > &fold_x);
            dots.extend(kept.iter());
            dots.extend(folded.iter().map(|(x, y)| (fold_x - (x - fold_x), *y)));
        } else { // fold_y > 0
            let (folded, kept): (Vec<(u32, u32)>, Vec<(u32, u32)>) = dots.drain().partition(|(_, y)| y > &fold_y);
            dots.extend(kept.iter());
            dots.extend(folded.iter().map(|(x, y)| (*x, fold_y - (y - fold_y))));
        }
    }
    for (x, y) in dots.iter() {
        println!("{},{}", x, y);
    }
}