#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" Sanskrit Parser Data Structures

    Author: Karthik Madathil <kmadathil@gmail.com>
"""

import sanskrit_parser.base.sanskrit_base as SanskritBase
import networkx as nx
from itertools import islice
import logging
import operator
import six
from sanskrit_parser.util import lexical_scorer

__all__ = ['SandhiGraph', 'VakyaGraph', 'getSLP1Tagset']


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _console_logging():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)


_console_logging()


class SandhiGraph(object):
    """ DAG class to hold Sandhi Lexical Analysis Results

        Represents the results of lexical sandhi analysis as a DAG
        Nodes are SanskritObjects
    """
    start = "__start__"
    end = "__end__"

    def __init__(self):
        ''' DAG Class Init

        Params:
            elem (SanskritObject :optional:): Optional initial element
            end  (bool :optional:): Add end edge to initial element
        '''
        self.roots = []
        self.G = nx.DiGraph()
        self.scorer = lexical_scorer.Scorer()

    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()

    def hasNode(self, t):
        ''' Does a given node exist in the graph?

            Params:
               t (SanskritObject): Node
            Returns:
               boolean
        '''
        return t in self.G

    def appendToNode(self, t, nodes):
        """ Create edges from t to nodes

            Params:
                t (SanskritObject)      : Node to append to
                nodes (iterator(nodes)) : Nodes to append to t
        """
        # t is in our graph
        assert t in self.G
        for r in nodes:
            self.G.add_edge(t, r)

    def addNode(self, node):
        """ Extend dag with node inserted at root

            Params:
                Node (SanskritObject)      : Node to add
                root (Boolean)             : Make a root node
                end  (Boolean)             : Add an edge to end
        """
        assert node not in self.G
        self.G.add_node(node)

    def addEndEdge(self, node):
        ''' Add an edge from node to end '''
        assert node in self.G
        self.G.add_edge(node, self.end)

    def addRoots(self, roots):
        self.roots.extend(roots)

    def lockStart(self):
        ''' Make the graph ready for search by adding a start node

        Add a start node, add arcs to all current root nodes, and clear
        self.roots
        '''
        self.G.add_node(self.start)
        for r in self.roots:
            self.G.add_edge(self.start, r)
        self.roots = []

    def scoreGraph(self):
        edges = self.G.edges()
        edges_list = []
        edges_to_score = []
        for edge in edges:
            edges_list.append(edge)
            if edge[0] == self.start:
                edges_to_score.append([edge[1]])
            elif edge[1] == self.end:
                edges_to_score.append([edge[0]])
            else:
                edges_to_score.append(edge)
        scores = self.scorer.score_splits(edges_to_score)
        for edge, score in zip(edges_list, scores):
            # Score is log-likelihood, so higher is better.
            # For graph path-finding, smaller weight is better, so use negative
            edges[edge]['weight'] = -score
        for u, v, w in self.G.edges(data='weight'):
            logger.debug("u = %s, v = %s, w = %s", u, v, w)

    def findAllPaths(self, max_paths=10, sort=True, score=True):
        """ Find all paths through DAG to End

            Params:
               max_paths (int :default:=10): Number of paths to find
                          If this is > 1000, all paths will be found
               sort (bool)                 : If True (default), sort paths
                                             in ascending order of length
        """
        if self.roots:
            self.lockStart()
        if score:
            self.scoreGraph()
        # shortest_simple_paths is slow for >1000 paths
        if max_paths <= 1000:
            if score:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end, weight='weight'),
                                                  max_paths)))
                scores = self.scorer.score_splits(paths)
                path_scores = zip(paths, scores)
                sorted_path_scores = sorted(path_scores, key=operator.itemgetter(1), reverse=True)
                logger.debug("Sorted paths with scores:\n %s", sorted_path_scores)
                # Strip the scores from the returned result, to be consistent with no-scoring option
                sorted_paths, _ = zip(*sorted_path_scores)
                return list(sorted_paths)
            else:
                paths = list(six.moves.map(lambda x: x[1:-1],
                                           islice(nx.shortest_simple_paths(
                                                        self.G, self.start, self.end),
                                                  max_paths)))
                return paths
        else:  # Fall back to all_simple_paths
            ps = list(six.moves.map(lambda x: x[1:-1],
                                    nx.all_simple_paths(self.G, self.start, self.end)))
            # If we do not intend to display paths, no need to sort them
            if sort:
                ps.sort(key=lambda x: len(x))
            return ps

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)

    def draw(self, *args, **kwargs):
        _ncache = {}

        def _uniq(s):
            if s not in _ncache:
                _ncache[s] = 0
                return s
            else:
                _ncache[s] = _ncache[s] + 1
                return s + "_" + str(_ncache[s])

        nx.draw(self.G, *args, **kwargs,
                pos=nx.spring_layout(self.G),
                labels={x: _uniq(str(x)) for x in self})

    def write_dot(self, path):
        # H = nx.convert_node_labels_to_integers(G, label_attribute=’node_label’)
        # H_layout = nx.nx_pydot.pydot_layout(G, prog=’dot’)
        # G_layout = {H.nodes[n][‘node_label’]: p for n, p in H_layout.items()}
        nx.drawing.nx_agraph.write_dot(self.G, path)


lakaras = set(['law', 'liw', 'luw', 'lrw', 'low', 'laN', 'liN', 'luN', 'lfN',
               'viDiliN', 'ASIrliN'])
karmani = set(['karmaRi'])

# FIXME - rewrite this as list + list elem assignments + set
_vibhaktis = ['praTamAviBaktiH', 'dvitIyAviBaktiH', 'tftIyAviBaktiH',
              'caturTIviBaktiH', 'paNcamIviBaktiH', 'zazWIviBaktiH',
              'saptamIviBaktiH', 'saMboDanaviBaktiH']
prathama = _vibhaktis[1-1]
dvitiya = _vibhaktis[2-1]
tritiya = _vibhaktis[3-1]
chaturthi = _vibhaktis[4-1]
pancami = _vibhaktis[5-1]
shashthi = _vibhaktis[6-1]
saptami = _vibhaktis[7-1]
sambodhana = _vibhaktis[8-1]
vibhaktis = set(_vibhaktis)
#

# Vacanas
vacanas = set(['ekavacanam', 'dvivacanam', 'bahuvacanam'])
# Puruzas
puruzas = 'praTamapuruzaH', 'maDyamapuruzaH', 'uttamapuruzaH'


class VakyaGraph(object):
    """ DAG class for Sanskrit Vakya Analysis

        Represents Sanskrit Vakya Analysis as a DAG
        Nodes are SanskritObjects with morphological tags
        Edges are potential relationships between them
    """
    def __init__(self, path):
        ''' DAG Class Init

        Params:
             path: Path from SanghiGraph
        '''
        self.roots = []
        self.isLocked = False
        self.G = nx.DiGraph()
        # Need this many nodes in the extracted subgraphs
        self.path_node_count = len(path)
        for sobj in path:
            vnlist = []
            mtags = sobj.getMorphologicalTags()
            for mtag in mtags:
                ncopy = SanskritBase.SanskritObject(sobj.canonical(),
                                                    encoding=SanskritBase.SLP1,
                                                    replace_ending_visarga=None)
                ncopy.setMorphologicalTags(mtag)
                pn = VakyaGraphNode(ncopy)
                vnlist.append(pn)
            for vn in vnlist:
                vn.makeForbidden(vnlist)
                self.addNode(vn)
        self.lock()
        self.addEdges()
        # Remove isolated nodes (with no edges)
        self.G.remove_nodes_from(list(nx.isolates(self.G)))

    def __iter__(self):
        ''' Iterate over nodes '''
        return self.G.__iter__()

    def __str__(self):
        """ Print representation of DAG """
        return str(self.G)

    def lock(self):
        self.isLocked = True

    def addNode(self, node):
        """ Extend dag with node inserted at root

            Params:
                Node (VakyaGraphNode)      : Node to add
        """
        assert node not in self.G
        assert not self.isLocked
        self.G.add_node(node)

    def addEdges(self):
        assert self.isLocked
        bases = self.find_dhatu()
        self.add_karakas(bases)

    def find_dhatu(self):
        ''' Find the ti~Nanta '''
        rlist = []
        for n in self.G:
            if node_is_a(n, lakaras):
                logger.info(f"{n} is a possible Dhatu")
                rlist.append(n)
        return rlist

    def add_karakas(self, bases):
        ''' Add karaka edges from base node (dhatu) base '''
        for d in bases:
            logger.info(f"Processing {d}")
            if node_is_a(d, karmani):
                logger.info("Karmani")
                karta = tritiya
                karma = prathama
            else:
                logger.info("Kartari")
                karta = prathama
                karma = dvitiya
            for n in self.G:
                if not d.isForbidden(n):
                    if node_is_a(n, karta) and match_purusha_vacana(d, n):
                        logger.info(f"Adding kartA edge to {n}")
                        self.G.add_edge(d, n, label="kartA")
                    if node_is_a(n, karma):
                        logger.info(f"Adding karma edge to {n}")
                        self.G.add_edge(d, n, label="karma")
                    if node_is_a(n, tritiya):
                        logger.info(f"Adding karana edge to {n}")
                        self.G.add_edge(d, n, label="karaRa")
                    if node_is_a(n, chaturthi):
                        logger.info(f"Adding sampradana edge to {n}")
                        self.G.add_edge(d, n, label="sampradAna")
                    if node_is_a(n, pancami):
                        logger.info(f"Adding apadana edge to {n}")
                        self.G.add_edge(d, n, label="apAdana")
                    if node_is_a(n, saptami):
                        logger.info(f"Adding adhikarana edge to {n}")
                        self.G.add_edge(d, n, label="aDikaraRa")

    def draw(self, *args, **kwargs):
        _ncache = {}

        def _uniq(s):
            if s not in _ncache:
                _ncache[s] = 0
                return s
            else:
                _ncache[s] = _ncache[s] + 1
                return s + "_" + str(_ncache[s])

        nx.draw(self.G, *args, **kwargs,
                pos=nx.graph_layout(self),
                labels={x: _uniq(str(x)) for x in self})

    def write_dot(self, path):
        nx.drawing.nx_agraph.write_dot(self.G, path)


class VakyaGraphNode(object):
    """ Class for VakyaGraph nodes

        This has pada (a SanskritObject) plus a list of forbidden nodes
        to which edges cannot be created from this node
    """
    def __init__(self, sobj):
        self.pada = sobj
        self.forbiddenNodes = []

    def isForbidden(self, node):
        return node in self.forbiddenNodes

    def makeForbidden(self, nodes):
        self.forbiddenNodes.extend(nodes)

    def getMorphologicalTags(self):
        return self.pada.getMorphologicalTags()

    def __str__(self):
        return str(self.pada) + "=>" + str(self.pada.getMorphologicalTags())

    def __repr__(self):
        return str(self)


def getSLP1Tagset(n):
    return set(map(lambda x: x.canonical(), list(n[1])))


def getNodeTagset(n):
    return getSLP1Tagset(n.getMorphologicalTags())


def node_is_a(n, st):
    if isinstance(st, str):
        return st in getNodeTagset(n)
    elif isinstance(st, set):
        return not st.isdisjoint(getNodeTagset(n))
    else:
        logger.error(f"node_is_a: expecting str or set, got {st}")


def get_vacana(n):
    return getNodeTagset(n).intersection(vacanas)


def get_purusha(n):
    return getNodeTagset(n).intersection(puruzas)


def match_purusha_vacana(d, n):
    n_base = n.getMorphologicalTags()[0]
    if n_base == 'asmad':
        n_purusha = set([puruzas[2]])
    elif n_base == 'yuzmad':
        n_purusha = set([puruzas[1]])
    else:
        n_purusha = set([puruzas[0]])
    return (get_vacana(d) == get_vacana(n)) and (get_purusha(d) == n_purusha)
