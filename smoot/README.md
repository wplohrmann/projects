# Smoot programming language

The purpose of this repo is to play around with some ideas for a programming language with a strong emphasis
on terseness and correctness. The name is from the unit of length Smoot (TODO: link).

Not all of these features may be implemented but we should at least get started with a basic roadmap:

## Features (Done/Not done):
- [ ] A single file corresponds to a single function, which can then be called by another language. Will probably start with Rust.
- [ ] Only number types to begin with, as well as tensors (represented internally as vectors).
- [ ] All numbers have units - different units can be multiplied / divided but not added or set equal to each other. It is possible to relate units through linear relationships, in which case one is converted before the operations.
- [ ] All loops are implicit using something like indexing / Einstein summation notation.
