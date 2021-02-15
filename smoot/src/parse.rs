use nom::{
    IResult,
    Err
};

pub struct Program {
    signature: Signature,
    statements: Vec<Statement>,
    return_value: Expression
}

pub struct Signature {
    inputs: Vec<Variable>,
}

pub struct Variable {
    name: String,
    unit: Unit,
}

pub struct Unit {
    name: String,
}

pub struct Statement {
    lhs: Expression,
    rhs: Expression
}

enum Expression {
    BinaryOp(Op, Box<Expression>, Box<Expression>),
    Value(Unit, Number)
}

enum Op {
    Mul,
    Add,
    Sub,
    Div
}

enum Number {
    Float(f64),
    Int(i64)
}

fn parse_signature(line: String) -> Result<Signature, Err> {
    println!("Signautre: {}", line);
    let inputs = Vec::new();
    return Signature{inputs};
}

pub fn parse_program(program: Vec<String>) -> Result<Program, Err> {
    if program.len() < 2 {
        return Err("A program must have at least 2 lines (signature, return value)");
    }
    let signature = parse_signature(program[0])?;
    // let return_value = parse_return_value(program[program.len()-1])?;
    // let statements = Vec::new();
    // for line in program.into_iter() {
    //     let statement = parse_statement(line)?;
    // }
    
    let statements = Vec::new();
    let return_value = Expression::Value(Unit{name: "nm"}, Number::Float(1.0));

    return Ok(Program{signature, statements, return_value});
}
