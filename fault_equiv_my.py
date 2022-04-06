# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:35:40 2022

@author: Rajesh
"""

import pandas as pd
df = pd.read_csv ("Fault equivalence.txt", sep = " ")
print (df)

#finding the primary outputs
po = []
pi = []
for i in range (len(df)):
    if (df.loc[i]["fanout"] == 0):
        po.append(df.loc[i]["node"])
    
    if (df.loc[i]["typ"] == "inpt"):
        pi.append(df.loc[i]["node"])
print ("Primary outputs : ",po)
print ("Primary outputs : ",pi)

#initializing the stuck at faults at each node
dict = {} #declared globally
#dict = {node: [s_a_0, s_a_1]}
for i in range (len(df)):
    dict [df.loc[i, "node"]] = [True, True]
print ("Initialized faults : ",dict)
print ("-----------------------------------------------------\n")
#main
'''
for i in range (len(po)):
        if 
        
        if (df.loc[po[i]-1, "typ"] == "or"):
            print ("OR")
            print ("-----")
            print ()
            key1 = df.loc[po[i]-1, "fin1"]
            print (key1)
            dict[key1] = [False, False]
            key2 = df.loc[po[i]-1, "fin2"]
            print (key2)
            dict[key2][0] = False
            
        elif (df.loc[po[i]-1, "typ"] == "or"):
            print ("AND")
print("**********")
print ("Updated fault list : ",dict)'''

def fault_equi (node):
    print ("\n****************************************************")
    print ("Node : ", node)
    if (node in pi):
        print ("Reached PI")
        return
    
    #check the faults available at that node
    s_a_0 = dict[node][0]
    s_a_1 = dict[node][1]
    print ("\nFaults available -")
    print ("s_a_0 : ", s_a_0)
    print ("s_a_1 : ", s_a_1)
    
    c = 0
    
    #if the node is a branch, then assign same faults to its stem
    #problem when both the branches have different faults****************
    if (df.loc[node-1, "con"] == 'fan'):
        c = 1
        print ("\nType - Branch")
        stem = df.loc[node, 'fanout']
        print ("Stem : ", stem)
        dict[df.loc[node-1, 'fanout']] = dict[node]
        print ("Fault assigned at stem - ", dict[stem])
        #call the function for its stem
        fault_equi(stem)
        
    
    #check only for nand and and gate in case of s_a_0 fault
    gate = df.loc[node-1, 'typ']
    fin1 = df.loc[node-1, 'fin1']
    fin2 = df.loc[node-1, 'fin2']
    print ("\nGate : ", gate)
    print ("Fanin in 1 : ", fin1)
    print ("Fanin in 2 : ", fin2)
    
    #not using 'else' includes the case when both the faults are present in a line
    if (s_a_0):
        if (gate == 'and' or gate == 'nand'):
            #cancel the s_a_0 at both the fanins
            dict[fin1][0] = False
            dict[fin2][0] = False
            print (f"\nFault assigned to {fin1} : ", dict[fin1])
            print (f"Fault assigned to {fin2} : ", dict[fin2])
        else if (gate == 'not'):
            c = 2
            dict[fin1][1] = False
            print (f"\nFault assigned to {fin1} : ", dict[fin1])
    
    if (s_a_1):
        if (gate == 'or' or gate == 'nor'):
            #cancel the s_a_0 at both the fanins
            dict[fin1][1] = False
            dict[fin2][1] = False
            print (f"\nFault assigned to {fin1} : ", dict[fin1])
            print (f"Fault assigned to {fin2} : ", dict[fin2])
        else if (gate == 'not'):
            c = 2
            dict[fin1][0] = False
            print (f"\nFault assigned to {fin1} : ", dict[fin1])
    
    if (c==0):
        #if the current node is not a branch i.e. its a gate, then call the 
        #function for both the fanins
        fault_equi(fin1)
        fault_equi(fin2)
    else if (c==2):
        #if its a not gate, then call the function for fin1
        fault_equi(fin1)

#dict[4] = [True, False]
for primary_op in po:
    fault_equi(primary_op)

print ("\n####################################################")
print ("Updated Fault list: ")
print (dict)

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
    outfile.write (str(dict[node][0]))
    outfile.write ("  ")
    outfile.write (str(dict[node][1]))
    outfile.write ("\n")