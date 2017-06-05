'''
This module contains classes for representing semigroups.
'''
# pylint: disable = no-member, protected-access, invalid-name, len-as-condition
# pylint: disable = cell-var-from-loop

import networkx

class CayleyGraph:
    """
    A class for representing right and left Cayley graphs of semigroups.
    """

    def __init__(self):
        self._label_edge_list = []
        self._graph = networkx.classes.multidigraph.MultiDiGraph()

    def __eq__(self, other):
        return self.ordered_adjacencies() == other.ordered_adjacencies()

    def __ne__(self, other):
        return not self == other

    def _add_node(self, node):
        self._graph.add_node(node)

    def _add_edge_with_label(self, label, edge):
        self._graph.add_edge(*edge)
        self._label_edge_list.append((label, edge))

    def ordered_adjacencies(self):
        return self._adjacencies_list

    def edges(self):
        return list(map(lambda x: x[1], self._label_edge_list))

    def nodes(self):
        return self._graph.nodes()

    def strongly_connected_components(self):
        return list(networkx.strongly_connected_components(self._graph))
