use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use itertools::Itertools;
use std::io::BufRead;

fn parse_scanner(mut lines: impl Iterator<Item=Result<String, std::io::Error>>) -> Option<Vec<(isize, isize, isize)>> {
    let maybe_line = lines.next(); // Skip header but check if it's there before continuing
    match maybe_line {
        Some(_) => Some(lines.take_while(|maybe_line| match maybe_line {
                       Ok(line) => line != "",
                       Err(_) => false,
                   }).map(|line| line.unwrap().split(",").map(|s| {
                       s.parse::<isize>().unwrap()
                   }).next_tuple().unwrap()).collect()),
        None => None
    }
}

fn permutations() -> impl Iterator<Item=(isize, usize, usize, usize)> {
    vec![
        (1, 0, 1, 2), (1, 2, 0, 1), (1, 1, 2, 0),
        (-1, 1, 0, 2), (-1, 0, 2, 1), (-1, 2, 1, 0)].into_iter()
}

pub fn part1() {
    let orientations = {
        let mut orientations = Vec::new();
        for (parity, x_axis, y_axis, z_axis) in permutations() {
            for x_sign in [-1, 1] {
                for y_sign in [-1, 1] {
                    // z_sign is whatever it needs to be to form a right-handed coordinate system
                    let z_sign = x_sign * y_sign * parity;
                    debug_assert_ne!(x_axis, y_axis);
                    debug_assert_ne!(x_axis, z_axis);
                    debug_assert_ne!(y_axis, z_axis);
                    let mut orientation = [[0; 3]; 3];
                    orientation[0][x_axis] = x_sign;
                    orientation[1][y_axis] = y_sign;
                    orientation[2][z_axis] = z_sign;
                    orientations.push(orientation);
                }
            }
        }
        assert_eq!(orientations.len(), 24);
        orientations
    };
    let mut scanners = VecDeque::new();
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    while let Some(new_beacons) = parse_scanner(&mut lines) {
        scanners.push_back(new_beacons);
    }
    // Everything relative to scanner 0
    // Push into beacons
    let mut aligned_scanners = Vec::new();
    aligned_scanners.push(scanners.pop_front().unwrap());
    while let Some(new_beacons) = scanners.pop_front() {
        let mut found_match = false;
        for current_beacons in &aligned_scanners {
            match overlap(current_beacons, &new_beacons, &orientations)  {
                Some((aligned_beacons, _)) => {
                    aligned_scanners.push(aligned_beacons);
                    found_match = true;
                    break
                },
                None => {}
            }
        }
        if !found_match {
            scanners.push_back(new_beacons);
        }
    }
    let all_beacons: HashSet<_> = aligned_scanners.into_iter().flatten().collect();
    println!("{}", all_beacons.len());
}

pub fn part2() {
    let orientations = {
        let mut orientations = Vec::new();
        for (parity, x_axis, y_axis, z_axis) in permutations() {
            for x_sign in [-1, 1] {
                for y_sign in [-1, 1] {
                    // z_sign is whatever it needs to be to form a right-handed coordinate system
                    let z_sign = x_sign * y_sign * parity;
                    debug_assert_ne!(x_axis, y_axis);
                    debug_assert_ne!(x_axis, z_axis);
                    debug_assert_ne!(y_axis, z_axis);
                    let mut orientation = [[0; 3]; 3];
                    orientation[0][x_axis] = x_sign;
                    orientation[1][y_axis] = y_sign;
                    orientation[2][z_axis] = z_sign;
                    orientations.push(orientation);
                }
            }
        }
        assert_eq!(orientations.len(), 24);
        orientations
    };
    let mut scanners = VecDeque::new();
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    while let Some(new_beacons) = parse_scanner(&mut lines) {
        scanners.push_back(new_beacons);
    }
    // Everything relative to scanner 0
    // Push into beacons
    let mut aligned_scanners = Vec::new();
    aligned_scanners.push(scanners.pop_front().unwrap());
    let mut diffs = Vec::new();
    while let Some(new_beacons) = scanners.pop_front() {
        let mut found_match = false;
        for current_beacons in &aligned_scanners {
            match overlap(current_beacons, &new_beacons, &orientations)  {
                Some((aligned_beacons, diff)) => {
                    aligned_scanners.push(aligned_beacons);
                    diffs.push(diff);
                    found_match = true;
                    break
                },
                None => {}
            }
        }
        if !found_match {
            scanners.push_back(new_beacons);
        }
    }
    let all_beacons: HashSet<_> = aligned_scanners.into_iter().flatten().collect();
    // Calculate 
    let mut max_distance = 0;
    for b1 in &diffs {
        for b2 in &diffs {
            max_distance = max_distance.max((b1.0-b2.0).abs() +(b1.1 - b2.1).abs() + (b1.2 - b2.2).abs());
        }
    }
    println!("{}", max_distance);
}


fn overlap(aligned: &Vec<(isize, isize, isize)>, other: &Vec<(isize, isize, isize)>, orientations: &Vec<[[isize; 3]; 3]>) -> Option<(Vec<(isize, isize, isize)>, (isize, isize, isize))> {
    for orientation in orientations {
        let maybe_aligned = align(other, orientation);
        let mut diffs = HashMap::new();
        for p1 in aligned {
            for p2 in &maybe_aligned {
                let diff = (p1.0 - p2.0, p1.1 - p2.1, p1.2 - p2.2);
                let entry = diffs.entry(diff).or_insert(0);
                *entry += 1;
                if *entry >= 12 {
                    return Some((maybe_aligned.iter().map(|(x, y, z)| (x+diff.0, y+diff.1, z+diff.2)).collect(), diff));
                }
            }
        }
    }
    None
}

fn align(coords: &Vec<(isize, isize, isize)>, orientation: &[[isize; 3]; 3]) -> Vec<(isize, isize, isize)> {
    coords.iter().map(|(x, y, z)| (
        (x * orientation[0][0] + y * orientation[0][1] + z * orientation[0][2]),
        (x * orientation[1][0] + y * orientation[1][1] + z * orientation[1][2]),
        (x * orientation[2][0] + y * orientation[2][1] + z * orientation[2][2]),
    )).collect()
}