"""Parse the output of an ANSYS model.

Reads two files in the current working directory:
NLIST.lis
PRNSOL.lis

Author: Perry Roth-Johnson
Last modified: April 16, 2014

"""


import matplotlib.pyplot as plt
import pandas as pd
import ansys_utils as au
from operator import attrgetter
# helps to sort lists of objects by their attributes
# ref: https://wiki.python.org/moin/HowTo/Sorting#Operator_Module_Functions


# read the node list file, NLIST.lis
nl = au.NodeList(filename='NLIST.lis')
# print nl

# read the solution file, PRNSOL.lis
sf = au.SolutionFile(nl.list_of_nodes, filename='PRNSOL.lis')

# sort the nodes first by spanwise location (z), then by chordwise location (x)
nl.list_of_nodes.sort(key=attrgetter('z', 'x'))
# assemble the node objects into a dictionary format
list_of_dicts = []
for node in nl.list_of_nodes:
    d = {
        'node_num' : node.node_num,
        'x' : node.x,
        'y' : node.y,
        'z' : node.z,
        'uy' : node.uy
    }
    list_of_dicts.append(d)
# convert the list of node dictionairies into a pandas DataFrame
df = pd.DataFrame(list_of_dicts)

# plot only the nodes near the pitch axis (x=0) of the blade
list_of_PA_nodes = []
for node in nl.list_of_nodes:
    # only add nodes that are near x=0 to the list
    if abs(node.x) < 0.01:
        list_of_PA_nodes.append(node)
list_of_dicts_PA = []
# convert the list of nodes near the pitch axis to a dictionary format
for node in list_of_PA_nodes:
    d = {
        'node_num' : node.node_num,
        'x' : node.x,
        'y' : node.y,
        'z' : node.z,
        'uy' : node.uy
    }
    list_of_dicts_PA.append(d)
# convert the list of node dictionairies into a pandas DataFrame
df_PA = pd.DataFrame(list_of_dicts_PA)

# clear all plots
plt.close('all')

# plot the planform of the blade
fig,ax = plt.subplots()
ax.set_aspect('equal')
plt.plot(df['z'],df['x'],'bx',label='all nodes')
plt.plot(df_PA['z'],df_PA['x'],'ro--',label='nodes near pitch axis')
plt.xlabel('z, spanwise coordinate [m]')
plt.ylabel('x, chordwise coordinate [m]')
plt.ylim([-1,2])
plt.legend()

# plot the nodal y-displacements vs. span
plt.figure()
plt.plot(df['z'],df['uy'],'bx-',label='all nodes')
plt.plot(df_PA['z'],df_PA['uy'],'ro--',label='nodes near pitch axis')
plt.xlabel('z, spanwise coordinate [m]')
plt.ylabel('uy, nodal y-displacement [m]')
plt.legend(loc='upper left')

# show all plots
plt.show()
