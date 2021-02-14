use clap::{App, Arg, SubCommand};

fn main() {
    // let opts = Opts::parse();
    let matches = App::new("Smoot compiler")
        .author("William Lohrmann <willia2501@gmail.com>")
        .subcommand(SubCommand::with_name("compile")
            .about("Compile a program")
            .arg(Arg::with_name("file")
                .required(true))
            .help("File to compile"))
        .subcommand(SubCommand::with_name("run")
            .about("Run a program")
            .arg(Arg::with_name("file")
                .required(true)
                .help("File to run")))
        .get_matches();

    match matches.subcommand() {
        ("run", Some(args)) => {
            let file = args.value_of("file").unwrap();
            println!("Running file: {:?}", file);
        },
        ("compile", Some(args)) => {
            let file = args.value_of("file").unwrap();
            println!("Compiling file: {:?}", file);
        }
        _ => {
            println!("Unable to parse matches: {:?}", matches);
        }
    };
}
