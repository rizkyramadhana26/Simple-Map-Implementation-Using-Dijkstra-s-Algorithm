from tkinter import *
from turtle import end_fill
import networkx as nx
import matplotlib.pyplot as plt
from numpy import True_
import my_networkx as mynx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
INF = 999

#Read adjacency matrix from config.txt
with open("test/test1.txt") as f :
    lines = f.readlines()
    lines = [x.strip().split(" ") for x in lines]
    adjacency = [[int(y) if y.isnumeric() else INF for y in x] for x in lines]
    n = len(adjacency)

#GUI
root = Tk()
frm = Frame(root, padx=10)
frm.grid()
Label(frm, text="start node: ").grid(column=0, row=0)
start_node = Entry(frm)
start_node.grid(column=1, row=0)
Label(frm, text="end node: ").grid(column=2, row=0)
end_node = Entry(frm)
end_node.grid(column=3, row=0)

#Method for getting the input
def on_click():
    global start,end,spl,sp
    start = start_node.get()
    end = end_node.get()
    if(start in list(G)) and (end in list(G)):
        shortest_path.config(text=" ")
        shortest_path_length.config(text=" ")
        desc.config(text=f"Shortest path from {start} to")
        i=list(G).index(start)
        spl[i]=0
        sp[i]=start
        update_spl(1)
    else:
        shortest_path.config(text="NOT VALID")
        shortest_path_length.config(text="NOT VALID")

def update_spl(mode):
    global display_spl,display_sp
    if(mode==1):  
        for i in range(n):
            display_spl.append(Label(frm,text=spl[i]))
            display_spl[i].grid(row=1,column=6+i) 
            display_sp.append(Label(frm,text=sp[i]))
            display_sp[i].grid(row=2,column=6+i)
    else:
        for i in range(n):
            display_spl[i].config(text=spl[i])
            display_sp[i].config(text=sp[i])

def next_step():
    global expand,sp
    #find next node to be expanded
    min=999
    for i in range(n):
        if spl[i]<min and not visited[i]:
            expand=list(G)[i]
            min = spl[i]

    if min==999 :
        expand=""
        update_graph()
        show_answer()
        return

    update_graph()

    for edge in list(G.out_edges(expand,data="weight")):
        src = list(G).index(edge[0])
        dest = list(G).index(edge[1])
        if(spl[src]+edge[2] < spl[dest]):
            spl[dest] = spl[src]+edge[2]
            sp[dest] = sp[src]+f"-{edge[1]}"

    visited[src] = True

    update_spl(2)
    
def show_answer():
    i = list(G).index(end)
    shortest_path.config(text=sp[i])
    shortest_path_length.config(text=spl[i])

def update_graph():

    visited_nodes = []
    not_visited_nodes = []
    for i in range(n):
        if visited[i]:
            visited_nodes.append(list(G)[i])
        else:
            not_visited_nodes.append(list(G)[i])

    out_edge_from_expand_node = []
    else_edge = []
    for edge in list(G.edges.data("weight")):
        if edge[0]==expand :
            out_edge_from_expand_node.append(edge)
        else:
            else_edge.append(edge)

    pos = nx.spring_layout(G,seed=7)
    nx.draw_networkx_nodes(G,pos,node_size=1000,ax=a,nodelist=visited_nodes,node_color="green")
    nx.draw_networkx_nodes(G,pos,node_size=1000,ax=a,nodelist=not_visited_nodes,node_color="blue")
    if(expand!=""):
        nx.draw_networkx_nodes(G,pos,node_size=1000,ax=a,nodelist=[expand],node_color="red")
    nx.draw_networkx_edges(G,pos,node_size=1000,connectionstyle="arc3, rad = 0.2",ax=a,edgelist=out_edge_from_expand_node,edge_color="red")
    nx.draw_networkx_edges(G,pos,node_size=1000,connectionstyle="arc3, rad = 0.2",ax=a,edgelist=else_edge,edge_color="black")
    nx.draw_networkx_labels(G,pos,ax=a)
    mynx.my_draw_networkx_edge_labels(G,pos,nx.get_edge_attributes(G, "weight"),label_pos=0.3,verticalalignment="top",rad=0.2,ax=a)

    canvas = FigureCanvasTkAgg(f,root)
    canvas.get_tk_widget().grid(column=0,row=2,columnspan=3)

Button(frm, text="search !", command=on_click).grid(column=4, row=0)
Button(frm, text="next step", command=next_step).grid(column=4, row=1)

Label(frm,text="shortest path: ").grid(row=1,column=0)
shortest_path = Label(frm,text="   ")
shortest_path.grid(row=1,column=1)
Label(frm,text="shortest path length: ").grid(row=1,column=2)
shortest_path_length = Label(frm,text="   ")
shortest_path_length.grid(row=1,column=3)

desc = Label(frm,text="Shortest path from _ to")
desc.grid(row=1,column=5)


#Djikstra

G = nx.DiGraph()
f =  plt.Figure(figsize=(6,6), dpi=100)
a = f.add_subplot(111)

for i in range(n):
    for j in range(n):
        if(adjacency[i][j]!=INF):
            G.add_weighted_edges_from([(f"N{i:02}",f"N{j:02}",adjacency[i][j])])

for i in range(n):
    Label(frm,text=list(G)[i]).grid(row=0,column=6+i)

visited = [False for i in range(n)]
spl = [INF for i in range(n)]
sp = ["" for j in range(n)]
expand = ""
display_spl=[]
display_sp=[]
update_graph()




root.mainloop()