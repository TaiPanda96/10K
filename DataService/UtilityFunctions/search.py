import UtilityFiles
from UtilityFiles.tickers import tickers

class Node:
    def __init__(self,ticker):
        self.ticker = ticker 
        self.left   = None 
        self.right  = None 


def BST(array):
    if not array:
        return None 
    
    # split the length of array
    mid = (len(array))//2

    # assign root node as middle of the array
    root = Node(array[mid])

    # left of the array is < root Node
    root.left = BST(array[:mid])

    # right of the array is > root Node
    root.right = BST(array[mid+1:])

    return root

def preorder(node):
    if not node:
        return None 

    
    print(node.ticker)
    preorder(node.left)
    preorder(node.right)
    
tickerArray = sorted(tickers)
array = [1, 2, 3, 4, 5, 6, 7]

tree = BST(array)
tickerTree = BST(tickerArray)
preorder(tree)
preorder(tickerTree)



