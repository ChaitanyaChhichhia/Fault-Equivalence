# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 06:40:30 2022

@author: Chaitanya
Modifications : in case of branches, the stems r visited twice as both the 
branch call the func for stem. Due to this the entire path from stem to PI
is covered twice. In case of multiple branches, this path will be visited
multiple times
sol-maintain a list to check whether the node is already visited or not
MODIFICATION done
"""
import pandas as pd
df = pd.read_csv ("c17.txt", sep = " ")
print (df)

node_dict = {}  #dictionary 
def preprocessor (df):
    #function to map the netlist node no.s in sequence  
    for i in range (len(df)):
        node_dict[df['node'][i]] = i
preprocessor(df)
print (node_dict)

#finding the primary outputs
po = []
pi = []
visited = []
for i in range (len(df)):
    if (df.loc[i]["fanout"] == 0):
        po.append(df.loc[i]["node"])
    
    if (df.loc[i]["typ"] == "inpt"):
        pi.append(df.loc[i]["node"])
print ("Primary outputs : ",po)
print ("Primary outputs : ",pi)

#initializing the stuck at faults at each node
dictf = {} #declared globally
#dict = {node: [s_a_0, s_a_1]}
for i in range (len(df)):
    dictf [df.loc[i, "node"]] = [True, True]
print ("Initialized faults : ",dictf)
print ("-----------------------------------------------------\n")

def fault_equi (node):
    print ("\n****************************************************")
    print ("Node : ", node)
    if (node in visited):
        print ("Node already visited")
        return
    visited.append(node)
    if (node in pi):
        print ("Reached PI")
        return   
    
    #check the faults available at that node
    s_a_0 = dictf[node][0]
    s_a_1 = dictf[node][1]
    print ("\nFaults available -")
    print ("s_a_0 : ", s_a_0)
    print ("s_a_1 : ", s_a_1)
    
    c = 0
    
    #if the node is a branch, then assign same faults to its stem
    #problem when both the branches have different faults****************
    if (df.loc[node_dict[node], "con"] == 'fan'):
        c = 1
        print ("\nType - Branch")
        stem = df.loc[node_dict[node], 'fanout']
        print ("Stem : ", stem)
        #dict[df.loc[node-1, 'fanout']] = dict[node]
        print ("Fault assigned at stem - ", dictf[stem])
        #call the function for its stem
        fault_equi(stem)
        
    
    #check only for nand and and gate in case of s_a_0 fault
    gate = df.loc[node_dict[node], 'typ']
    fin1 = df.loc[node_dict[node], 'fin1']
    fin2 = df.loc[node_dict[node], 'fin2']
    print ("\nGate : ", gate)
    print ("Fanin in 1 : ", fin1)
    print ("Fanin in 2 : ", fin2)
    
    if ((gate == 'and' and s_a_0) or (gate == 'nand' and s_a_1)):
            #cancel the s_a_0 at both the fanins
        dictf[fin1][0] = False
        dictf[fin2][0] = False
        print (f"\nFault assigned to {fin1} : ", dictf[fin1])
        print (f"Fault assigned to {fin2} : ", dictf[fin2])  

    if ((gate == 'or'and s_a_1) or (gate == 'nor' and s_a_0)):
        #cancel the s_a_0 at both the fanins
        dictf[fin1][1] = False
        dictf[fin2][1] = False
        print (f"\nFault assigned to {fin1} : ", dictf[fin1])
        print (f"Fault assigned to {fin2} : ", dictf[fin2])
    elif (gate == 'not'):
        c = 2
        dict[fin1][0] = False
        print (f"\nFault assigned to {fin1} : ", dictf[fin1])
    
    if (c==0):
        #if the current node is not a branch i.e. its a gate, then call the 
        #function for both the fanins
        fault_equi(fin1)
        fault_equi(fin2)
    elif (c==2):
        #if its a not gate, then call the function for fin1
        fault_equi(node_dict[fin1])

#dict[4] = [True, False]
for primary_op in po:
    fault_equi(primary_op)

print ("\n####################################################")
print ("Updated Fault list: ")
print (dictf)

#print the contents into a file
#node s_a_0 s_a_1
#1    True  False
outfile = open ("reduced fault list.txt", 'w')
#outfile.write ('%5s'%('NODE ') '%5s' %(' s_a_0 ')'%5s'(' s_a_1\n'))
node_str = 'NODE'
s0 = 's_a_0'
s1= 's_a_1'
outfile.write (f'{node_str} {s0} {s1}\n')
outfile.write ("-----------------\n")
for node in df['node']:
    outfile.write (str(node))
    outfile.write ("    ")
    outfile.write (str(dictf[node][0]))
    outfile.write ("  ")
    outfile.write (str(dictf[node][1]))
    outfile.write ("\n")