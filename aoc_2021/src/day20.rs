use std::collections::HashMap;
use std::collections::HashSet;
use std::io::BufRead;

fn parse_binary(line: String) -> Vec<bool> {
    line.chars().map(|c| match c {
        '#' => true,
        '.' => false,
        _ => panic!("Invalid character '{}'", c)
    }).collect()

}

pub fn part1() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let code = parse_binary(lines.next().unwrap().unwrap());
    lines.next();
    let mut grid: HashMap<(isize, isize), bool> = HashMap::new();
    let mut min_row = isize::MAX;
    let mut max_row = isize::MIN;
    let mut min_col = isize::MAX;
    let mut max_col = isize::MIN;
    for (i, maybe_line) in lines.enumerate() {
        let row = parse_binary(maybe_line.unwrap());
        for (j, is) in row.iter().enumerate() {
            if *is {
                min_row = min_row.min((i-5) as isize);
                max_row = max_row.max((i+5) as isize);
                min_col = min_col.min((j-5) as isize);
                max_col = max_col.max((j+5) as isize);
                grid.insert((i as isize, j as isize), true);
            }
        }
    }
    assert_ne!(code[0], code[code.len()-1]);
    let mut default = false;
    for _ in 0..2 {
        grid = enhance(&grid, &code, &mut min_row, &mut max_row, &mut min_col, &mut max_col, default);
        if code[0] {
            default = !default;
        }
    }
    println!("{}", grid.iter().filter(|(_, v)| **v).count());
}

pub fn part2() {
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let code = parse_binary(lines.next().unwrap().unwrap());
    lines.next();
    let mut grid: HashMap<(isize, isize), bool> = HashMap::new();
    let mut min_row = isize::MAX;
    let mut max_row = isize::MIN;
    let mut min_col = isize::MAX;
    let mut max_col = isize::MIN;
    for (i, maybe_line) in lines.enumerate() {
        let row = parse_binary(maybe_line.unwrap());
        for (j, is) in row.iter().enumerate() {
            if *is {
                min_row = min_row.min((i-5) as isize);
                max_row = max_row.max((i+5) as isize);
                min_col = min_col.min((j-5) as isize);
                max_col = max_col.max((j+5) as isize);
                grid.insert((i as isize, j as isize), true);
            }
        }
    }
    assert_ne!(code[0], code[code.len()-1]);
    let mut default = false;
    for _ in 0..50 {
        grid = enhance(&grid, &code, &mut min_row, &mut max_row, &mut min_col, &mut max_col, default);
        if code[0] {
            default = !default;
        }
    }
    println!("{}", grid.iter().filter(|(_, v)| **v).count());
}

fn enhance(grid: &HashMap<(isize, isize), bool>, code: &Vec<bool>, min_row: &mut isize, max_row: &mut isize, min_col: &mut isize, max_col: &mut isize, default: bool) -> HashMap<(isize, isize), bool> {
    let mut new_grid = HashMap::new();
    let row_range = *min_row..=*max_row;
    let col_range =  *min_col..=*max_col;
    for i in row_range {
        for j in col_range.clone() {
            let mut binary = [0; 9];
            for k in [-1isize, 0, 1] {
                for l in [-1isize, 0, 1] {
                    if *grid.get(&(i + k, j + l)).unwrap_or(&default) {
                        let index = ((k + 1) * 3 + (l + 1)) as usize;
                        binary[index] = 1;
                    }
                }
            }
            *min_row = (*min_row).min(i-5);
            *max_row = (*max_row).max(i+5);
            *min_col = (*min_col).min(j-5);
            *max_col = (*max_col).max(j+5);
            new_grid.insert((i, j), code[to_int(binary)]);
        }
    }
    new_grid
}

fn to_int(binary: [usize; 9]) -> usize {
    let s = String::from_iter(binary.iter().map(|n| char::from_digit(*n as u32, 2).unwrap()));
    isize::from_str_radix(&s, 2).unwrap() as usize
}

