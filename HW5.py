from Binary_search_tree import *
from Splay_tree import *
import random

# Task 1
file = open("sequence.txt", "r")
seq = file.read()
seq = seq.split()
file.close()
print("Sequence:\n", seq, "\n")

# Task 1.1: Implementing BST tree and display tree of the sequence
static_tree = BST()
for i in range(len(seq)):
    if seq[i][-1] == "+":
        static_tree.insert(int(seq[i][:-1]))
    elif seq[i][-1] == "-":
        static_tree.delete(int(seq[i][:-1]))
print("BST tree of the sequence:")
static_tree.show()
print(70*"* ", "\n")
# ------------------------------------
# Task 1.2: Implementing Splay tree and display tree of the sequence
dynamic_tree = SplayTree()
for i in range(len(seq)):
    if seq[i][-1] == "+":
        dynamic_tree.insert(int(seq[i][:-1]))
    elif seq[i][-1] == "-":
        dynamic_tree.delete(int(seq[i][:-1]))
print("Splay tree of the sequence:")
dynamic_tree.show()
print(70*"* ", "\n")
# ------------------------------------
# Task 3: Calculate and compare total cost of
# 3 access lists using BST and Splay tree
file_1 = open("accesslist1.txt", "r")
access_list_1 = file_1.read()
access_list_1 = access_list_1.split()
access_list_1 = [int(i) for i in access_list_1]
# print("First access list:\n", access_list_1, "\n")
file_1.close()

file_2 = open("accesslist2.txt", "r")
access_list_2 = file_2.read()
access_list_2 = access_list_2.split()
access_list_2 = [int(i) for i in access_list_2]
# print("Second access list:\n", access_list_2, "\n")
file_2.close()

file_3 = open("accesslist3.txt", "r")
access_list_3 = file_3.read()
access_list_3 = access_list_3.split()
access_list_3 = [int(i) for i in access_list_3]
# print("Third access list:\n", access_list_3, "\n")
file_3.close()

# A Shuffle of numbers from 1 to 10000
nodes = [i for i in range(1, 10001)]
random.shuffle(nodes)
first_tree = BST()
for i in nodes:
    first_tree.insert(i)
# Let's calculate the total cost of access lists using BST
for i in access_list_1:
    first_tree.search(i)
print("The total cost of first access list using BST:\n", first_tree.cost)
first_tree.cost = 0

for i in access_list_2:
    first_tree.search(i)
print("The total cost of second access list using BST:\n", first_tree.cost)
first_tree.cost = 0

for i in access_list_3:
    first_tree.search(i)
print("The total cost of third access list using BST:\n", first_tree.cost)
print(70*"* ", "\n")
first_tree.cost = 0

# now, it's time to calculate the total cost of access lists using splay tree
tree_1 = SplayTree()
for i in nodes:
    tree_1.insert(i)
tree_1.cost = 0

for i in access_list_1:
    tree_1.search(i)
print("The total cost of first access list using splay tree:\n", int(tree_1.cost))
tree_1.cost = 0
# ------------------------------------------
tree_2 = SplayTree()
for i in nodes:
    tree_2.insert(i)
tree_2.cost = 0

for i in access_list_2:
    tree_2.search(i)
print("The total cost of second access list using splay tree:\n", int(tree_2.cost))
tree_2.cost = 0
# ------------------------------------
tree_3 = SplayTree()
for i in nodes:
    tree_3.insert(i)
tree_3.cost = 0

for i in access_list_3:
    tree_3.search(i)
print("The total cost of third access list using splay tree:\n", int(tree_3.cost))
tree_3.cost = 0
