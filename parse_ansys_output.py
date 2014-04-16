"""Parse the output of an ANSYS model.

Reads two files in the current working directory:
NLIST.lis
PRNSOL.lis

Author: Perry Roth-Johnson
Last modified: April 15, 2014

"""


import matplotlib.pyplot as plt
import pandas as pd
import ansys_utils as au


# read the node list file, NLIST.lis
nl = au.NodeList(filename='NLIST.lis')
print nl

# read the solution file, PRNSOL.lis
sf = au.SolutionFile(nl.list_of_nodes, filename='PRNSOL.lis')

# convert the list of node objects into a pandas DataFrame
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
df = pd.DataFrame(list_of_dicts)

# sort the DataFrame first by spanwise location, then by chordwise location
dfzx = df.sort(['z','x'])

# TNT: if there are multiple nodes at the same spanwise (z) location, pick only one to plot (either pick LE, TE, or x~0.0 for pitch axis)

# clear all plots
plt.close('all')

# plot the planform of the blade
plt.figure()
plt.plot(dfzx['z'],dfzx['x'],'bx')
plt.xlabel('z, spanwise coordinate [m]')
plt.ylabel('x, chordwise coordinate [m]')

# plot only the LE of the blade
# find nodes that have the same z-coordinate
# pick the node with the min x-coordinate
# save that node to a new list
list_of_LE_nodes = []
for node in dfzx

# plot the nodal y-displacements vs. span
# plt.figure()
# plt.plot(dfzx['z'],dfzx['uy'],'bx-')
# plt.xlabel('z, spanwise coordinate [m]')
# plt.ylabel('uy, nodal y-displacement [m]')

# show all plots
plt.show()
