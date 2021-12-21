use std::io::BufRead;
use std::fmt;

#[derive(Clone)]
enum Number {
    Regular(usize),
    Pair((Box<Number>, Box<Number>))
}

impl fmt::Display for Number {
    // This trait requires `fmt` with this exact signature.
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Number::Regular(i) => {
                write!(f, "{}", i)
            },
            Number::Pair((left, right)) => {
                write!(f, "[{},{}]", *left, *right)
            }
        }
    }
}

impl fmt::Debug for Number {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self)
    }
}

fn parse(chars: &mut impl Iterator<Item = char>) -> Number {
    let c = chars.next().unwrap();
    match c {
        '[' => {
            let left = parse(chars);
            let comma = chars.next().unwrap();
            assert_eq!(comma, ',');
            let right = parse(chars);
            let close_bracket = chars.next().unwrap();
            assert_eq!(close_bracket, ']');
            return Number::Pair((Box::new(left), Box::new(right)));
        },
        _ => { return Number::Regular(c.to_digit(10).unwrap() as usize)},
    }
}

pub fn part1() {
    let mut numbers = Vec::new();
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        let mut chars = line.chars();
        numbers.push(parse(&mut chars));
    }
    let sum = numbers.into_iter().reduce(|n1, n2| reduce(add(n1, n2))).unwrap();
    println!("{}", magnitude(sum));
}

pub fn part2() {
    let mut numbers = Vec::new();
    for maybe_line in std::io::stdin().lock().lines() {
        let line = maybe_line.unwrap();
        let mut chars = line.chars();
        numbers.push(parse(&mut chars));
    }
    let mut max_magnitude = 0;
    for i in 0..numbers.len() {
        for j in 0..numbers.len() {
            if i == j {
                continue
            }
            max_magnitude = max_magnitude.max(magnitude(reduce(add(numbers[i].clone(), numbers[j].clone()))));
        }
    }
    println!("{}", max_magnitude);
}

fn magnitude(n: Number) -> usize {
    match n {
        Number::Pair((left, right)) => 3 * magnitude(*left) + 2 * magnitude(*right),
        Number::Regular(i) => i,
    }
}

fn reduce(mut n: Number) -> Number {
    // Explode
    {
        let mut regulars = get_regulars(&mut n, 0);
        // Explode if there's a pair of regulars
        // deeper than 4 levels of nesting.
        for i in 0..regulars.len() {
            if let Some((left_value, right_value)) = {
                match &regulars[i].0 {
                    Number::Pair((left, right)) if regulars[i].1 == 4 => Some((value(&*left), value(&*right))),
                    _ => None
                }
            }{
                if i > 0 {
                    modify(&mut regulars[i-1].0, left_value, true);
                }
                if i < regulars.len() - 1 {
                    modify(&mut regulars[i+1].0, right_value, false);
                }
                *regulars[i].0 = Number::Regular(0);
                return reduce(n);
            }
        }
    }
    // Split
    {
        let mut regulars = get_regulars(&mut n, 0);
        for i in 0..regulars.len() {
            let changed = split(&mut regulars[i].0);
            if changed {
                return reduce(n);
            }
        }
    }
    return n
}

fn modify(n: &mut Number, i: usize, right_most: bool) {
    match n {
        Number::Pair((left, right)) => {
            if right_most {
                modify(&mut *right, i, right_most)
            } else {
                modify(&mut *left, i, right_most)
            }
        }
        Number::Regular(j) => {
            *n = Number::Regular(*j + i);
        },
    }
}

fn value(n: &Number) -> usize {
    match n {
        Number::Pair(_) => panic!("Cannot get value of pair"),
        Number::Regular(i) => *i,
    }
}

/// Return a vector of regular pairs encoded as (&number, depth) tuples
fn get_regulars(n: &mut Number, depth: usize) -> Vec<(&mut Number, usize)>{
    let mut regulars = Vec::new();
    match n {
        Number::Pair((left, right)) if matches!(**left, Number::Regular(_)) && matches!(**right, Number::Regular(_))=> {
            regulars.push((n, depth));
        }
        Number::Pair((left, right)) => {
                regulars.extend(get_regulars(&mut *left, depth + 1));
                regulars.extend(get_regulars(&mut *right, depth + 1));
            }
        Number::Regular(_) => {
            regulars.push((n, depth));
        }
    }
    regulars
}

fn add(n1: Number, n2: Number) -> Number {
    Number::Pair((Box::new(n1), Box::new(n2)))
}

fn split(n: &mut Number) -> bool {
    match n {
        Number::Regular(i) if *i >= 10 => {
            let k = *i;
            *n = Number::Pair((
                Box::new(Number::Regular((k - (k % 2)) / 2)),
                Box::new(Number::Regular((k + (k % 2)) / 2)),
            ));
            true
        },
        Number::Pair((left, right)) => {
            let changed = split(left);
            if changed {
                true
            } else {
                let changed = split(right);
                if changed {
                    true
                } else {
                    false
                }
            }
        }
        _ => false,
    }
}
