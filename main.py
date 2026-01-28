import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv

# Plan du batiment
edges = [
    (1,2), (2,3), (3,4),
    (4,5), (5,6), (6,7), (7,8), (8,4),
    (5,7), (6,8),
    (2,9), (9,10), (10,11), (11,12),
    (10,13), (13,14),
    (12,15), (15,16), (16,12),
    (8,17),
    (17,18), (18,19), (19,20),
    (18,21), (21,22), (22,23),
    (19,22),
    (23,24), (24,25), (25,26), (26,23),
    (24,26),
    (20,27), (27,28), (28,29),
    (29,30), (30,31), (31,29),
    (7,32),
    (25,33),
    (28,34),
]

G =gv.Graph('G', engine='neato')

nodes = set([n for edge in edges for n in edge])

for node in nodes:
    G.node(str(node), shape='square', color='gray')

for u, v in edges:
    G.edge(str(u), str(v))

G.view()



