use std::str::FromStr;
use std::io::BufRead;
use std::io;

#[derive(Debug, Clone)]
struct Line {
    x1: usize,
    y1: usize,
    x2: usize,
    y2: usize,
    cur_x: usize,
    cur_y: usize,
    done: bool,
}

impl Line {
    pub fn new(x1: usize, y1: usize, x2: usize, y2: usize) -> Self {
        return Line{x1, y1, x2, y2, cur_x: x1, cur_y: y1, done: false}
    }
}

impl Iterator for Line {
    type Item = (usize, usize);
    fn next(&mut self) -> Option<Self::Item> {
        if self.done { return None }
        if self.cur_x == self.x2 && self.cur_y == self.y2 {
            self.done = true;
        }
        let cur_x  = self.cur_x;
        let cur_y = self.cur_y;
        if cur_x != self.x2 {
            if self.x2 > self.x1 {
                self.cur_x += 1;
            } else {
                self.cur_x -= 1;
            }
        }
        if cur_y != self.y2 {
            if self.y2 > self.y1 {
                self.cur_y += 1;
            } else {
                self.cur_y -= 1;
            }
        }
        return Some((cur_x, cur_y))
    }
}

pub fn part1() {
    let stdin = io::stdin();
    let mut lines = Vec::new();
    let mut max_coord = 0;
    for s in stdin.lock().lines() {
        let coords: Vec<usize> = s.unwrap()
            .split(" -> ")
            .flat_map(|x| x.split(","))
            .map(|x| x.parse::<usize>().unwrap())
            .collect();
        max_coord = max_coord.max(*coords.iter().max().unwrap()) + 1;
        lines.push(Line::new(coords[0], coords[1], coords[2], coords[3]));
    }
    let mut board = vec![0; max_coord*max_coord];
    for line in lines {
        if line.x1 != line.x2 && line.y1 != line.y2 {
            continue
        }
        for (x, y) in line {
            board[x + y * max_coord] += 1;
        }
    }
    let answer = board.into_iter().filter(|x| x > &1).count();
    println!("{}", answer);
}


pub fn part2() {
    let stdin = io::stdin();
    let mut lines = Vec::new();
    let mut max_coord = 0;
    for s in stdin.lock().lines() {
        let coords: Vec<usize> = s.unwrap()
            .split(" -> ")
            .flat_map(|x| x.split(","))
            .map(|x| x.parse::<usize>().unwrap())
            .collect();
        max_coord = max_coord.max(*coords.iter().max().unwrap()) + 1;
        lines.push(Line::new(coords[0], coords[1], coords[2], coords[3]));
    }
    let mut board = vec![0; max_coord*max_coord];
    for line in lines {
        for (x, y) in line {
            board[x + y * max_coord] += 1;
        }
    }
    let answer = board.into_iter().filter(|x| x > &1).count();
    println!("{}", answer);
}