use std::str::FromStr;
use std::io::BufRead;
use std::io;
use std::collections::HashSet;

pub fn part1() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let numbers: Vec<_> = lines.next().unwrap().unwrap().split(",").map(|s| s.parse::<i32>().unwrap()).collect();
    lines.next(); // Skip empty line
    let mut boards: Vec<[i32; 25]> = Vec::new();
    let mut board = [0; 25];
    let mut offset = 0;
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        if line == "" {
            offset = 0;
            boards.push(board.clone());
            continue
        }

        for (i, number) in line.split_whitespace().enumerate() {
            board[i + offset] = number.parse::<i32>().unwrap();
        }
        offset += 5;
    }
    boards.push(board.clone());
    let mut marks: Vec<[bool; 25]> = vec![[false; 25]; boards.len()];
    for number in numbers {
        for j in 0..boards.len() {
            for i in 0..25 {
                if boards[j][i] == number {
                    marks[j][i] = true;
                }
            }
        }
        'board: for j in 0..boards.len() {
            let mut possible_rows: HashSet<usize> = (0..5).collect();
            let mut possible_cols: HashSet<usize> = (0..5).collect();
            for row in 0..5 {
                for col in 0..5 {
                    if !marks[j][row * 5 + col] {
                        possible_rows.remove(&row);
                        possible_cols.remove(&col);
                    }
                    if possible_rows.len() + possible_cols.len() == 0 {
                        continue 'board; // Ran out of options
                    }
                }
            }
            if possible_rows.len() + possible_cols.len() > 0 {
                let mut score = 0;
                for i in 0..25 {
                    if !marks[j][i] {
                        score += boards[j][i];
                    }
                }
                score *= number;
                println!("{}", score);
                return


            }
        }
    }

}

pub fn part2() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let numbers: Vec<_> = lines.next().unwrap().unwrap().split(",").map(|s| s.parse::<i32>().unwrap()).collect();
    lines.next(); // Skip empty line
    let mut boards: Vec<[i32; 25]> = Vec::new();
    let mut board = [0; 25];
    let mut offset = 0;
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        if line == "" {
            offset = 0;
            boards.push(board.clone());
            continue
        }

        for (i, number) in line.split_whitespace().enumerate() {
            board[i + offset] = number.parse::<i32>().unwrap();
        }
        offset += 5;
    }
    boards.push(board.clone());
    let mut marks: Vec<[bool; 25]> = vec![[false; 25]; boards.len()];
    let mut boards_won = HashSet::new();
    for number in numbers {
        for j in 0..boards.len() {
            for i in 0..25 {
                if boards[j][i] == number {
                    marks[j][i] = true;
                }
            }
        }
        'board: for j in 0..boards.len() {
            let mut possible_rows: HashSet<usize> = (0..5).collect();
            let mut possible_cols: HashSet<usize> = (0..5).collect();
            for row in 0..5 {
                for col in 0..5 {
                    if !marks[j][row * 5 + col] {
                        possible_rows.remove(&row);
                        possible_cols.remove(&col);
                    }
                    if possible_rows.len() + possible_cols.len() == 0 {
                        continue 'board; // Ran out of options
                    }
                }
            }
            if possible_rows.len() + possible_cols.len() > 0 {
                if !boards_won.contains(&j) {
                    boards_won.insert(j);
                }
                if boards_won.len() == boards.len() {
                    let mut score = 0;
                    for i in 0..25 {
                        if !marks[j][i] {
                            score += boards[j][i];
                        }
                    }
                    score *= number;
                    println!("{}", score);
                    return
                }
            }
        }
    }

}