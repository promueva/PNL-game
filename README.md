# Reasoning About Group Polarization: From Semantic Games to Sequent Systems

We implement the semantic game developed in [this paper](./paper.pdf) using
rewriting logic and
[Maude](http://maude.cs.illinois.edu/w/index.php/The_Maude_System). Besides the
needed Maude theories, a script in Python allows for pretty-printing the trees
and strategies.


## Getting started

The project was tested in [Maude
3.3.1](https://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation).
For using the script in Python, the languages [bidings](https://github.com/fadoss/maude-bindings)
for Maude are needed as well as the library [treelib](https://treelib.readthedocs.io/en/latest/).
Both can be easily installed using [pip](https://pypi.org/project/pip/):

```
pip install maude
pip install treelib
```

## Structure of the project

The needed Maude files are:
- `syntax.maude`: Definition of PNL formulas and game states
- `semantics.maude`: Game rules as rewrite rules. 
- `game.maude`: Maude's strategies to explore the search tree

The directory `examples` contain some examples from the [paper](./paper.pdf)
and some additional ones. See for instance the file `./examples/model-M2.maude`
for the expected way of specifying the PNL model and the needed commands to
check the existence of winning strategies. For instance: 

```
$> maude model-M2.maude

--- I don't have a winning strategy for this game 
Maude> dsrew [1] init using make-me-win .
srewrite [1] in EXAMPLE : init using make-me-win .

No solution.

--- But it is possible to explore the whole search tree
Maude> dsrew [1] init using expand-tree .
srewrite [1] in EXAMPLE : init using expand-tree .

Solution 1
rewrites: 593 in 6ms cpu (5ms real) (89226 rewrites/second)
result YTree: Y< {R+{(a,a), (a,b), (a,c), (b,b), (c,c)},R-{(b,c)}}
...

--- And I have a winning strategy for the negation of this formula
Maude> dsrew [1] < model : ( P @ a : ~ lb(p)) >  using make-me-win .
srewrite [1] in EXAMPLE : < model : P @ a : ~ lb(p) > using make-me-win .

Solution 1
rewrites: 602 in 6ms cpu (4ms real) (90813 rewrites/second)
result ITree: I< {R+{(a,a), (a,b), (a,c), (b,b), (c,c)},R-{(b,c)}} :
...

```

Note that trees of the form `I< ...>` are trees where *I* win and trees
of the form `Y<...>` are trees where *You* win. 

## Python Interface

Instead of executing the above Maude commands, it is possible to use [this](./main.py)
Python script. Here some example of executing the same commands above: 

```
$> python main.py examples/model-M2.maude a "lb(p)"

No solution.

$> python main.py examples/model-M2.maude a "lb(p)"  --tree

[❌,Y] : P @ a : (¬ (◆ ◆ p ∨ ◇ ◇ p) ∨ ◆ p) ∧ ¬ (◆ ◇ p ∨ ◇ ◆ p) ∨ ◇ p
├── [❌,I] : P @ a : ¬ (◆ ◇ p ∨ ◇ ◆ p) ∨ ◇ p
│   ├── [❌,I] : P @ a : ¬ (◆ ◇ p ∨ ◇ ◆ p)
│   │   └── [❌,Y] : O @ a : ◆ ◇ p ∨ ◇ ◆ p
│   │       ├── [❌,Y] : O @ a : ◆ ◇ p
│   │       │   ├── [❌,Y] : O @ c : ◇ p
│   │       │   │   └── [❌,Y] : O @ b : p
│   │       │   ├── [✔,Y] : O @ a : ◇ p
│   │       │   └── [✔,Y] : O @ b : ◇ p
│   │       │       └── [✔,Y] : O @ c : p
│   │       └── [✔,Y] : O @ a : ◇ ◆ p
│   └── [❌,I] : P @ a : ◇ p
└── [✔,I] : P @ a : ¬ (◆ ◆ p ∨ ◇ ◇ p) ∨ ◆ p
    ├── [❌,I] : P @ a : ¬ (◆ ◆ p ∨ ◇ ◇ p)
    │   └── [❌,Y] : O @ a : ◆ ◆ p ∨ ◇ ◇ p
    │       ├── [❌,Y] : O @ a : ◆ ◆ p
    │       │   ├── [❌,Y] : O @ a : ◆ p
    │       │   │   ├── [❌,Y] : O @ b : p
    │       │   │   ├── [✔,Y] : O @ a : p
    │       │   │   └── [✔,Y] : O @ c : p
    │       │   ├── [❌,Y] : O @ b : ◆ p
    │       │   │   ├── [❌,Y] : O @ b : p
    │       │   │   └── [✔,Y] : O @ a : p
    │       │   └── [✔,Y] : O @ c : ◆ p
    │       │       ├── [✔,Y] : O @ a : p
    │       │       └── [✔,Y] : O @ c : p
    │       └── [✔,Y] : O @ a : ◇ ◇ p
    └── [✔,I] : P @ a : ◆ p
        ├── [❌,I] : P @ a : p
        ├── [❌,I] : P @ c : p
        └── [✔,I] : P @ b : p

$> python main.py examples/model-M2.maude a "~ lb(p)"
[✔,I] : P @ a : ¬ ((¬ (◆ ◆ p ∨ ◇ ◇ p) ∨ ◆ p) ∧ ¬ (◆ ◇ p ∨ ◇ ◆ p) ∨ ◇ p)
└── [✔,I] : O @ a : (¬ (◆ ◆ p ∨ ◇ ◇ p) ∨ ◆ p) ∧ ¬ (◆ ◇ p ∨ ◇ ◆ p) ∨ ◇ p
    └── [✔,Y] : O @ a : ¬ (◆ ◇ p ∨ ◇ ◆ p) ∨ ◇ p
        ├── [✔,I] : O @ a : ¬ (◆ ◇ p ∨ ◇ ◆ p)
        │   └── [✔,I] : P @ a : ◆ ◇ p ∨ ◇ ◆ p
        │       └── [✔,I] : P @ a : ◆ ◇ p
        │           └── [✔,I] : P @ c : ◇ p
        │               └── [✔,I] : P @ b : p
        └── [✔,Y] : O @ a : ◇ p

```
