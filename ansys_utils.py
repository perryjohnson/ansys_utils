"""Create entities for an ANSYS shell model.

Author: Perry Roth-Johnson
Last modified: April 22, 2014

"""


import re
import numpy as np
import matplotlib.pyplot as plt


class Node:
    number_of_nodes = 0
    def __init__(self, node_num, x, y, z):
        """Create a node object.

        Parameters
        ----------
        node_num : int, the ID number of this node
        x : float, the (chordwise) x-coordinate of this node
        y : float, the (flapwise) y-coordinate of this node
        z : float, the (spanwise) z-coordinate of this node
        coords : tuple of floats, the (x,y,z) coordinates of this node
        ux : float, the x-displacement of this node (from postprocessing)
        uy : float, the y-displacement of this node (from postprocessing)
        uz : float, the z-displacement of this node (from postprocessing)

        """
        Node.number_of_nodes += 1
        self.node_num = int(node_num)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.coords = (self.x,self.y,self.z)
        self.ux = None  # assign an empty value for now, fill it later
        self.uy = None  # assign an empty value for now, fill it later
        self.uz = None  # assign an empty value for now, fill it later

    def __str__(self):
        return "Node #{0}: ({1:10.8f}, {2:10.8f}, {3:10.8f})".format(
            self.node_num,
            self.x, self.y, self.z)


class NodeList:
    def __init__(self, filename='NLIST.lis'):
        """Read in a node list file into memory.

        Parameters
        ----------
        filename : str, the filename of the node list text file
        _ansys_file : file obj, the node list file in memory
        _node_pattern : str, a regular expression to identify nodes
        number_of_nodes : int, the number of nodes in this model
        list_of_nodes : list, a list of node objects in this model

        """
        self.filename = filename
        f = open(self.filename, 'r')
        self._ansys_file = f.readlines()
        f.close()
        self._node_pattern = re.compile(
            r'[ ]+[0-9]+(\s+-*[0-9]+\.[0-9]*E*[+-]*[0-9]*){6}\n')
        # explanation of the _node_pattern regex:
        #   [ ]+ : leading spaces
        #   [0-9]+ : node number
        #   (\s+-*[0-9]+\.[0-9]*E*[+-]*[0-9]*){6} : x, y, z, thxy, thyz, thzx
        #   \n : endline (carriage return)
        #   note: coords may be in decimal or scientific notation
        self.number_of_nodes = 0
        self.list_of_nodes = []
        self.parse_nodes()

    def __str__(self):
        node_preview = ''
        for node in self.list_of_nodes[:10]:
            node_preview += node.__str__() + '\n'
        return node_preview

    def parse_nodes(self):
        """Save the nodes in a list of Node objects.

        Saves:
        self.number_of_nodes
        self.list_of_nodes

        """
        for line in self._ansys_file:
            node_match = self._node_pattern.match(line)
            if node_match: # if we find a node
                # save the first 4 entries (drop last 3: thxy, thyz, thzx)
                (node_num, x, y, z) = line.strip().split()[:-3]
                n = Node(node_num, x, y, z)
                self.list_of_nodes.append(n)
        self.number_of_nodes = len(self.list_of_nodes)


class SolutionFile:
    def __init__(self, list_of_nodes, filename='PRNSOL.lis'):
        """Read in a solution file into memory.

        Parameters
        ----------
        list_of_nodes : list, list of node objects to assign node displacements to
        filename : str, the filename of the solution text file
        _ansys_file : file obj, the solution file in memory
        _disp_pattern : str, a regular expression to identify node displacements

        """
        self.filename = filename
        f = open(self.filename, 'r')
        self._ansys_file = f.readlines()
        f.close()
        self._disp_pattern = re.compile(
            r'[ ]+[0-9]+(\s+-*[0-9]+\.[0-9]*E*[+-]*[0-9]*)\n')
        # explanation of the _disp_pattern regex:
        #   [ ]+ : leading spaces
        #   [0-9]+ : node number
        #   (\s+-*[0-9]+\.[0-9]*E*[+-]*[0-9]*) : uy
        #   \n : endline (carriage return)
        #   note: coords may be in decimal or scientific notation
        self.list_of_nodes = list_of_nodes
        self.parse_displacements()

    def parse_displacements(self):
        """Save the displacements of each node.

        Saves:
        self.list_of_nodes[i].uy

        """
        for line in self._ansys_file:
            disp_match = self._disp_pattern.match(line)
            if disp_match: # if we find a node
                # save the 2 entries
                (node_num, uy) = line.strip().split()
                try:
                    self.list_of_nodes[int(node_num)-1].uy = uy
                except IndexError:
                    n = int(node_num)
                    print 'index {0} (node_num={1}) is out of range'.format(n-1, n)
