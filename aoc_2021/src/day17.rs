use std::collections::HashSet;
use std::io::BufRead;
use std::ops::{Range, RangeBounds};
use regex::Regex;
use itertools::Itertools;

pub fn part1() {
    let line = std::io::stdin().lock().lines().next().unwrap().unwrap();
    let re = Regex::new(r"-?\d+").unwrap();
    let mut numbers = re.captures_iter(&line).map(|cap| cap.get(0).unwrap().as_str().parse::<isize>().unwrap());

    let target_x: (_, _) = numbers.next_tuple().unwrap();
    let target_y: (_, _) = numbers.next_tuple().unwrap();
    let mut top_ys = Vec::new();
    for y_velocity in 0..100 {
        let top_y = get_max(y_velocity);
        if top_y < target_y.0 {
            continue // We did not even reach the bottom of the target - increase speed!
        }
        let maybe_y_range  = get_range_steps(top_y - target_y.1, top_y - target_y.0, 0, 1);
        let y_range;
        match maybe_y_range {
            Some(range) => {
                if range.is_empty() {
                    continue // We've passed the range in one step - we're going too fast
                }
                y_range = range;
            },
            None => {unreachable!()}
        }
        for x_velocity in 0..100 {
            let maybe_x_range  = get_range_steps(target_x.0, target_x.1, x_velocity, -1);
            match maybe_x_range {
                Some(range) => {
                    if range.is_empty() {
                        continue
                    }
                    if overlap(&y_range, &range) {
                        top_ys.push(top_y);
                    }
                },
                None => {
                    continue
                }
            }
        }
    }
    println!("{}", top_ys.iter().max().unwrap());
}

pub fn part2() {
    let line = std::io::stdin().lock().lines().next().unwrap().unwrap();
    let re = Regex::new(r"-?\d+").unwrap();
    let mut numbers = re.captures_iter(&line).map(|cap| cap.get(0).unwrap().as_str().parse::<isize>().unwrap());

    let target_x: (_, _) = numbers.next_tuple().unwrap();
    let target_y: (_, _) = numbers.next_tuple().unwrap();
    let mut velocity_pairs = HashSet::new();
    for y_velocity in -50..100 {
        let top_y = get_max(y_velocity);
        if top_y < target_y.0 {
            continue // We did not even reach the bottom of the target - increase speed!
        }
        let maybe_y_range  = get_range_steps(top_y - target_y.1, top_y - target_y.0, 0, 1);
        let y_range;
        match maybe_y_range {
            Some(range) => {
                if range.is_empty() {
                    continue // We've passed the range in one step - we're going too fast
                }
                y_range = range;
            },
            None => {unreachable!()}
        }
        for x_velocity in -50..100 {
            let maybe_x_range  = get_range_steps(target_x.0, target_x.1, x_velocity, -1);
            match maybe_x_range {
                Some(range) => {
                    if range.is_empty() {
                        continue
                    }
                    if overlap(&y_range, &range) {
                        velocity_pairs.insert((x_velocity, y_velocity));
                    }
                },
                None => {
                    continue
                }
            }
        }
    }
    dbg!(&velocity_pairs);
    println!("{}", velocity_pairs.len());
}

/// Returns true if two ranges have overlapping items
fn overlap(range1: &Range<usize>, range2: &Range<usize>) -> bool {
    range1.contains(&range2.start) ||
    range1.contains(&(range2.end-1)) ||
    range2.contains(&range1.start) ||
    range2.contains(&(range1.end-1))
}

/// Range of steps in which distance travelled >= min_distance but <= max_distance
/// Returns an empty range (0..0) if it never exceeds min_distance
fn get_range_steps(min_distance: isize, max_distance: isize, initial_velocity: isize, acceleration: isize) -> Option<Range<usize>> {
    // initial_velocity * num_steps + acceleration * (num_steps + 1) * num_steps / 2 >= distance
    //  TODO: Calculate directly by solving the quadratic
    let mut velocity = initial_velocity;
    let mut distance_so_far = 0;
    let mut lower = None;
    for step in 0.. {
        distance_so_far += velocity;
        if lower.is_none() && distance_so_far >= min_distance {
            lower = Some(step);
        }
        if distance_so_far > max_distance {
            return Some(lower.unwrap()..step);
        }
        velocity += acceleration;
        if velocity <= 0 && acceleration < 0 {
            return match lower {
                Some(min_step) => Some(min_step..usize::MAX),
                None => None,
            }
        }
    }
    unreachable!();
}

fn get_max(velocity: isize) -> isize {
    // y_velocity + (y_velocity - 1) + ... + 1
    if velocity < 0 { 0 } else { velocity * (velocity + 1) / 2 }
}