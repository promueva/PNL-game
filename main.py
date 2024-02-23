'''
 Python script to pretty-print the output of the Maude specification 
'''

import maude
import re
from treelib import Node, Tree
import argparse


def getSolution(file, modulename="MODEL", initialterm="init", strategy='expand-tree'):
    '''
    Returns the representation of the resulting tree
    '''

    maude.init()
    maude.load(file)
    modsys = maude.getModule(modulename)
    tinit = modsys.parseTerm(initialterm)

    result = tinit.srewrite(modsys.parseStrategy(strategy))

    try:
        return next(result)[0] 
    except StopIteration:
        return None 


def winner(term):
    '''Printing a tree with the winner'''
    symbol = str(term.symbol())

    if "I<" in symbol: return '\033[32m' + '✔' + '\033[0m'
    else: return '\033[31m' + '❌' + '\033[0m'

def choice(term):
    '''Returning the player that wins the state'''
    symbol = str(term.symbol())

    if "I" in symbol: return "I"
    else: return "Y"

def labelnode(term, child, formula):
    '''Label used in the tree (the winner and how has to choose)'''
    return f'[{winner(term)},{choice(child)}] : {prettyPrint(formula.prettyPrint(maude.PRINT_MIXFIX))}'

def prettyPrint(formula:str):
    '''replacing some ASCII symbols with UTF ones'''
    translation = {"<+>" : "◆" , "<->" : '◇', '/\\': '∧', '\\/' : '∨', "~" : '¬'}
    for x in translation:
        formula = formula.replace(x, translation[x])

    return formula


def outputTree(term):

    def outputChildren(parent, term, tree):
        ''' Recursively adding the children'''

        symbol = str(term.symbol())
        i = 0

        if "I<" in symbol or "Y<" in symbol:
            # A single node
            _,F,newlevel = tuple(term.arguments())
            idtree = f'{parent}.{str(i)}'
            tree.create_node(labelnode(term, newlevel,F), idtree, parent)
            children = tuple(newlevel.arguments())[0] #Eliminating I(...) and Y(...)
            outputChildren(idtree, children, tree)
        else:
            # A ;-separated set
            for x in term.arguments():
                i+= 1
                _,F,newlevel = tuple(x.arguments())
                idtree = f'{parent}.{str(i)}'
                tree.create_node(labelnode(x,newlevel,F), idtree, parent)
                children = tuple(newlevel.arguments())[0] #Eliminating I(...) and Y(...)
                outputChildren(idtree, children, tree)
                


    # Root I< REL , FORMULA ,  I/Y(...) >
    tree = Tree() 
    _,F,children = tuple(term.arguments())
    win = winner(term)

    tree.create_node(labelnode(term, children, F), "0")

    children = tuple(children.arguments())[0] #Eliminating I(...) and Y(...)
    outputChildren('0', children, tree)

    print(tree.show(stdout=False))

if __name__ == "__main__":


    example_text = '''
                    
                    Examples of use: 

                    python main.py examples/model-M1.maude a "<+> p"  
                    python main.py examples/model-M1.maude a "<-> p"  
                    python main.py examples/model-M1.maude a "<-> p"  --tree
                    python main.py examples/model-M1.maude a "lb(p)"  
                    python main.py examples/model-M1.maude a "lb(p)"  --tree
                   '''

    parser = argparse.ArgumentParser(description='Game Semantics for the logic PNL', epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("file", help="Maude file with the model to be analyzed")
    parser.add_argument("world", help="Initial World")
    parser.add_argument("formula", help="Formula to be verified")
    parser.add_argument("--tree", help="Compute the whole tree of the game", action="store_true")

    args = parser.parse_args()

    # Strategy to be used 
    strategy = 'make-me-win'
    if args.tree:
        strategy = 'expand-tree'

    term = getSolution(args.file, initialterm=f'< model : ( P @ {args.world} : {args.formula} ) >', strategy=strategy) 
    if term:
        outputTree(term)
    else:
        print("No solution.")

