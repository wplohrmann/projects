use std::collections::HashSet;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::io::BufRead;

const START: u32 = 0;
const END: u32 = 1000;

pub fn part1() {
    let mut edges = HashMap::new();
    let mut sizes = HashMap::new();
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        let split: Vec<_> = line.split("-").collect();
        let start_upper = split[0].chars().all(char::is_uppercase);
        let end_upper = split[1].chars().all(char::is_uppercase);
        let start_index = str_to_int(split[0]) + if start_upper {1000} else {0};
        let end_index = str_to_int(split[1]) + if end_upper {1000} else {0};
        sizes.insert(start_index, start_upper);
        sizes.insert(end_index, end_upper);
        edges.entry(start_index).or_insert(Vec::new()).push(end_index);
        edges.entry(end_index).or_insert(Vec::new()).push(start_index);
    }
    let mut paths: VecDeque<(u32, HashSet<u32>)> = VecDeque::from([(START, HashSet::from([START]))]);
    let mut count = 0;
    while let Some((leaf, visited)) = paths.pop_front() {
        if leaf == END {
            count += 1;
        } else {
            for next in &edges[&leaf] {
                if !visited.contains(&next) {
                    let mut new_visited = visited.clone();
                    if !sizes[&next] { // Small cave
                        new_visited.insert(*next);
                    }
                    paths.push_back((*next, new_visited));
                }
            }
        }
    }
    println!("{}", count);

}

fn str_to_int(s: &str) -> u32 {
    match s.len() {
        5 => START, // start
        3 => END, // end
        2 => {
            let chars: Vec<_> = s.chars().collect();
            chars[0].to_digit(36).unwrap() * 36 + chars[1].to_digit(36).unwrap()
        }
        1 => {
            let chars: Vec<_> = s.chars().collect();
            chars[0].to_digit(36).unwrap()
        }
        _ => panic!("string of length {} encountered", s.len())
    }

}

pub fn part2() {
    let mut edges = HashMap::new();
    let mut sizes = HashMap::new();
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        let split: Vec<_> = line.split("-").collect();
        let start_upper = split[0].chars().all(char::is_uppercase);
        let end_upper = split[1].chars().all(char::is_uppercase);
        let start_index = str_to_int(split[0]) + if start_upper {1000} else {0};
        let end_index = str_to_int(split[1]) + if end_upper {1000} else {0};
        sizes.insert(start_index, start_upper);
        sizes.insert(end_index, end_upper);
        edges.entry(start_index).or_insert(Vec::new()).push(end_index);
        edges.entry(end_index).or_insert(Vec::new()).push(start_index);
    }
    let mut paths: VecDeque<(u32, HashMap<u32, usize>, bool)> = VecDeque::from([(START, HashMap::new(), false)]);
    let mut count = 0;
    while let Some((leaf, visited, twice)) = paths.pop_front() {
        if leaf == END {
            count += 1;
        } else {
            for next in &edges[&leaf] {
                let mut new_visited = visited.clone();
                if *next == START {
                    continue
                }
                if !sizes[&next] { // Small cave
                    let entry = new_visited.entry(*next).or_insert(0);
                    if *entry == 0 || (!twice && *entry == 1) {
                        debug_assert!(*entry <= 1);
                        if *entry == 1 { // Already visited once - `twice` must be false
                            *entry += 1;
                            paths.push_back((*next, new_visited, true));
                        } else { // First time
                            *entry += 1;
                            paths.push_back((*next, new_visited, twice));
                        }
                    }
                } else {
                    paths.push_back((*next, new_visited, twice));
                }
            }
        }
    }
    println!("{}", count);

}