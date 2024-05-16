import numpy as np


def flattenCells(cells):
    output = []
    if not isinstance(cells[0],float):
        for entry in cells:
                numel = len(entry)
                t = [i for i in entry]
                t.insert(0,numel)
                output += t
    else:
        pass
    return output

def nonhomogenous_shape(a:list):
    "for when you need the maximum shape of an non-homogenous 2D list"
    row = len(a)
    col = 0
    for i in a:
        if len(i) > col:
            col = len(i)
    return (row,col)