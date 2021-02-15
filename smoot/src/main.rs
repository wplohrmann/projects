use std::fs::File;
use std::io::{BufRead, self};
use clap::{App, Arg};

use parse::parse_program;

fn main() {
    // let opts = Opts::parse();
    let matches = App::new("Smoot compiler")
        .author("William Lohrmann <willia2501@gmail.com>")
        .about("Compile a program")
        .arg(Arg::with_name("file")
            .required(true))
        .get_matches();

    let file = matches.value_of("file").unwrap();
    let handle = File::open(file).expect(&format!("Unable to open file {}", file));
    let reader = io::BufReader::new(handle).lines();
    println!("Reading file:");
    let mut lines = Vec::new();
    for maybe_line in reader {
        if let Ok(line) = maybe_line {
            if line.len() > 0 {
                println!("{}", line);
                lines.push(line);
            }
        }
    }
    let maybe_program = parse_program(lines);
}
