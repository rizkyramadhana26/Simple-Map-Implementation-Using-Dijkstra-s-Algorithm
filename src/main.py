from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import my_networkx as mynx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
frm = Frame(root, padx=10)
frm.grid()
Label(frm, text="start node: ").grid(column=0, row=0)
Label(frm, text="   ").grid(column=1, row=0)
Label(frm, text="end node: ").grid(column=2, row=0)
Label(frm, text="   ").grid(column=3, row=0)
Label(frm, text="shortest path length: ").grid(column=4, row=0)
Label(frm, text="   ").grid(column=5, row=0)
Button(frm, text="search !", command=root.destroy).grid(column=6, row=0)

INF = 999
adjacency = [[1,INF,2],[3,2,1],[2,5,INF]]
n = len(adjacency)

G = nx.DiGraph()
f =  plt.Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)
a.margins(0.2)
for i in range(n):
    for j in range(n):
        if(adjacency[i][j]!=INF):
            G.add_weighted_edges_from([(f"N{i:02}",f"N{j:02}",adjacency[i][j])])

pos = nx.spring_layout(G,seed=7)
nx.draw_networkx_nodes(G,pos,node_size=1000,ax=a)
nx.draw_networkx_edges(G,pos,edgelist=G.edges(),edge_color='black',node_size=1000,connectionstyle="arc3, rad = 0.2",ax=a)
nx.draw_networkx_labels(G,pos,ax=a)
mynx.my_draw_networkx_edge_labels(G,pos,nx.get_edge_attributes(G, "weight"),label_pos=0.3,verticalalignment="top",rad=0.2,ax=a)

canvas = FigureCanvasTkAgg(f,root)
canvas.get_tk_widget().grid(column=0,row=2,columnspan=7)



root.mainloop()