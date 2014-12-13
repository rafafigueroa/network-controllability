#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rafa'


import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from IPython.display import Image

class SystemNode(object):
    def __init__(self, i):
        self.index = i
        self.accessible = False
        self.controlled = False
        self.origin = False
        self.layer = None
        self.fork = None
        self.in_cycle = None
        self.in_stem = None
        self.matched = None


class SystemEdge(object):
    def __init__(self, j, i, e):
        self.u = j
        self.v = i
        self.e = e
        self.matched = None

class LtiNetwork(object):

    def __init__(self, A, B = None, sysName = None):

        print A
        self.A = A
        self.B = B
        self.N = len(A)
        self.sn = []  # List of system nodes
        self.sna = []  # List of system nodes for A only
        self.sea = []  # List of system edges for A only
        self.ec = []  # Elementary Cycles
        self.st = []  # List of stems
        self.di = []  # List of dilations
        self.ia = []  # List of inaccessible
        self.um = []  # List of unmatached
        self.visited = []
        self.fork_max = 0
        self.name = sysName

        for i in range(0, self.N):
            n = SystemNode(i)
            self.sn.append(n)
            self.sna.append(n)

        self.Ga = self.create_Ga()
        self.Gbud = self.Ga.copy()
        self.Gec = self.Ga.copy()
        self.Gst = self.Ga.copy()
        self.Gmm = self.Ga.copy()

        if self.B is not None:
            self.M = len(B[0])

            for j in range(0, self.M):
                n = SystemNode(self.N + j)
                n.origin = True
                self.sn.append(n)

            self.Gab = self.create_Gab()

    def create_Ga(self):

        G = pgv.AGraph(strict=False,
                       directed=True,
                       splines=True)

        print self.A
        for i in range(0, self.N):

            G.add_node(i,
                       color='black',
                       size=100,
                       label='X'+str(i+1))

        print self.A
        for i in range(0, self.N):
            for j in range(0, self.N):

                if self.A[i][j] is not 0:
                    G.add_edge(j,
                               i,
                               label=self.A[i][j],
                               color='black')

                    sea = SystemEdge(j, i, G.get_edge(j, i))
                    self.sea.append(sea)

        print 'Ga Nodes:', G.nodes()
        print 'Ga Edges:', G.edges()
        return G

    def create_Gab(self):

        G = self.Ga.copy()

        for j in range(0, self.M):
            G.add_node(self.N + j,
                       style= 'filled',
                       fillcolor='blue',
                       size=100,
                       label='u'+str(j+1))


        for i in range(0, self.N):
            for j in range(0, self.M):
                if self.B[i][j] != 0:
                    G.add_edge(self.N + j,
                               i,
                               label=self.B[i][j],
                               color='blue')
                    self.sn[i].controlled = True
                    self.sn[i].accessible = True

        print 'Gab Nodes:', G.nodes()
        print 'Gab Edges:', G.edges()

        return G

    def draw_Ga(self):
        plt.axis('off')
        G = self.Ga.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Ga.png')
        #G.draw('Ga.eps', prog='circo')
        img=mpimg.imread(self.name + '_Ga.png')
        imgplot = plt.imshow(img)
        plt.show()

    def draw_Gab(self, extra=''):
        plt.axis('off')
        G = self.Gab.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Gab_' + extra +'_.png')
        #G.draw('Gab.eps', prog='circo')
        img=mpimg.imread(self.name + '_Gab_' + extra + '_.png')
        imgplot = plt.imshow(img)
        plt.show()

    def draw_Gbud(self):
        plt.axis('off')
        G = self.Gbud.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Gbud.png')
        #G.draw('Gbud.eps', prog='circo')
        img=mpimg.imread(self.name + '_Gbud.png')
        imgplot = plt.imshow(img)
        plt.show()

    def draw_Gec(self, extra=''):
        plt.axis('off')
        G = self.Gec.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Gec_' + extra + '_.png')
        #G.draw('Gec.eps', prog='circo')
        img=mpimg.imread(self.name + '_Gec_' + extra + '_.png')
        imgplot = plt.imshow(img)
        plt.show()

    def draw_Gst(self):
        plt.axis('off')
        G = self.Gst.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Gst.png')
        #G.draw('Gec.eps', prog='circo')
        img=mpimg.imread(self.name + '_Gst.png')
        imgplot = plt.imshow(img)
        plt.show()

    def draw_Gmm(self):
        plt.axis('off')
        G = self.Gmm.copy()
        G.node_attr['shape'] = 'circle'
        G.layout()
        G.draw(self.name + '_Gmm.png')
        img=mpimg.imread(self.name + '_Gmm.png')
        imgplot = plt.imshow(img)
        plt.show()

    def set_accessible(self, out_sn):
        # RECURSIVE ALGORITHM!
        if out_sn.accessible:
            return True
        else:
            out_sn.accessible = True
            for out_n2 in self.Ga.out_neighbors(out_sn.index):
                out_sn2 = self.sn[int(out_n2)]
                self.set_accessible(out_sn2)

    def inaccessibility_ab(self):
        sn_controlled = [n for n in self.sn if n.controlled]
        for sn in sn_controlled:
            for out_n in self.Ga.out_neighbors(sn.index):
                out_sn = self.sn[int(out_n)]
                self.set_accessible(out_sn)

        sn_inaccessible = []
        for sn in self.sn:
            if (not sn.accessible
                    and not sn.origin):
                print 'inaccesible:', sn.index
                n = self.Gab.get_node(sn.index)
                n.attr['style'] = 'filled'
                n.attr['fillcolor'] = 'yellow'

                sn_inaccessible.append(sn.index)

        self.ia = sn_inaccessible

        return len(sn_inaccessible) > 0

    def find_bud_candidates(self):
        bc = []
        for n in self.Ga:
            sn = self.sn[n]
            n_in = self.Ga.in_neighbors(n)
            n_out = self.Ga.out_neighbors(n)

            if (len(n_in) > 1 or
                    (sn.controlled and len(n_in) > 0)) \
                    and len(n_out) > 0:
                bc.append(n)

        return bc

    def kill_pre_isolated(self, n_pre, n_post):

            # kills any edge where, the starting
            # node or n_pre doesn't have any input
            # keeps going forwards
            sn_pre = self.sn[int(n_pre)]
            sn_post = self.sn[int(n_post)]

            pre_in = self.Gec.in_neighbors(n_pre)
            post_in = self.Gec.in_neighbors(n_post)
            post_out = self.Gec.out_neighbors(n_post)

            pre_isolated = (len(pre_in) == 0)

            post_has_self_edge = self.Gec.has_edge(n_post, n_post)

            if pre_isolated and \
                    not (int(n_pre) == int(n_post)):

                if self.Gec.has_edge(n_pre, n_post):
                    self.Gec.remove_edge(n_pre, n_post)

                # RECURSIVE! keep going forwards
                for n_next in post_out:
                    self.kill_pre_isolated(n_post, n_next)

            else:
                return True

    def kill_post_isolated(self, n_pre, n_post):

            # kills any edge where, the ending
            # node or n_post doesn't have any output
            # keeps going backwards

            post_out = self.Gec.out_neighbors(n_post)
            pre_in = self.Gec.in_neighbors(n_pre)

            post_isolated = (len(post_out) == 0)

            if post_isolated and \
                    not (int(n_pre) == int(n_post)):

                if self.Gec.has_edge(n_pre, n_post):
                    self.Gec.remove_edge(n_pre, n_post)

                # RECURSIVE! keep going backwards
                for n_next in pre_in:
                    self.kill_post_isolated(n_next,
                                            n_pre)
            else:
                return True

    # FIND CYCLES
    def use_acyclic_test(self, n, current_fork, previous):

        n_in = self.Gec.in_neighbors(n)
        n_out = self.Gec.out_neighbors(n)

        sn = self.sn[int(n)]

        if len(self.Gec.edges()) > 0:

            if sn.fork is not None:
                # visited before
                if sn.fork <= current_fork:

                    # Cycle!
                    print 'acyt: found a cycle'
                    print 'current fork', current_fork
                    print 'n start', n

                    #
                    # n_next = None
                    # if len(n_in) == 1:
                    #     # Good, single path
                    #     n_next = n_in[0]
                    #     print 'single path:', n_next
                    #
                    # elif len(n_in) > 1:
                    #     # More complicated, find a path
                    #     # with less or equal fork rank
                    #     # for ccn in n_in:
                    #     #    ccsn = self.sn[int(ccn)]
                    #     #    if ccsn.fork <= sn.fork:
                    #     #        n_next = ccn
                    #     #        print 'mult paths:', n_next
                    #     #        break
                    #     n_next = previous

                    print 'acyt: closing loop'
                    cycle = [n]
                    # Another recursive, but self contained
                    n_next = previous
                    # cycle is going backwards!

                    while True:
                        cycle.append(n_next)
                        # n is not changing on this cycle
                        sn_next = self.sn[int(n_next)]

                        if sn.fork < sn_next.fork:
                            print 'Too far into another cycle!'
                            print 'took a wrong turn'
                            break

                        if n_next == n:
                            # Found it!

                            # The cycle was found going backwards
                            # so they list is reversed. fixing it:
                            cycle.reverse()
                            self.ec.append(cycle)
                            print 'acyt: Elemental Cycle found!'
                            print cycle

                            for nci in range(0, len(cycle) -1):
                                # it includes the first and last
                                # which are the same
                                # remove this cycle from the graph
                                self.Gec.remove_edge(cycle[nci],
                                                     cycle[nci+1])
                            # End recursion
                            print 'acyt: cycle removed'
                            return True

                        n_next_in = self.Gec.in_neighbors(n_next)

                        if len(n_next_in) == 1:
                            # Good, single path
                            n_next = n_next_in[0]

                        elif len(n_in) > 1:
                            # Far tricker
                            for ccn in n_in:
                                ccsn = self.sn[int(ccn)]
                                if ccsn.fork <= sn.fork:
                                    n_next = ccn
                                    break

            elif sn.fork is None and len(n_out) == 1:
                # Easy case, first visited and one output
                sn.fork = current_fork
                n_next = n_out[0]
                # RECURSIVE!
                return self.use_acyclic_test(n_next, current_fork, n)

            elif sn.fork is None and len(n_out) > 1:
                sn.fork = current_fork
                # More complicated, first visited, > 1 output
                # More forks need to be created
                # RECURSIVE!
                for n_next in n_out:
                    self.fork_max += 1
                    return self.use_acyclic_test(n_next, self.fork_max, n)

    def find_elemental_cycles_ab(self):
        sn_controlled = [sn for sn in self.sn if sn.controlled]
        dc = 0  # draw counter
        #self.draw_Gec(str(dc))
        dc += 1

        # Start with controlled nodes and most should go away
        print 'Gec: removing isolated from controlled'
        for sn in sn_controlled:
            for out_n in self.Ga.out_neighbors(sn.index):
                n = sn.index
                self.kill_pre_isolated(n, out_n)

        # Remove self-edges
        # self.draw_Gec(str(dc))
        dc += 1

        print 'Gec: removing self edges'
        edges = self.Gec.edges()
        for e in edges:
            if e[0] == e[1]:
                # Cycle found! (self edge)
                # each EC has beginning == end
                self.ec.append([e[0], e[0]])
                self.Gec.remove_edge(e[0], e[0])

        # Then go to nodes without output
        print 'Gec: removing isolated post'

        edges = self.Gec.edges()
        for e in edges:
            n_pre = self.Gec.get_node(e[0])
            n_post = self.Gec.get_node(e[1])
            # print 'e:', e, 'Nodes:', n_pre, '->', n_post

            self.kill_post_isolated(n_pre, n_post)

        print 'draw: elemental loops and connections'
        # self.draw_Gec(str(dc))
        dc += 1
        # What is left is elemental loops or
        # Connections between elemental loops

        # First, deal with connections between them

        # take the first edge that could be the start
        # of a bud

        edges_left = len(self.Gec.edges()) > 0
        while edges_left:

            # self.draw_Gec(str(dc))
            dc += 1

            for sn in self.sn:
                sn.fork = None

            print '\n\n find and take cycles'
            # find and take out cycles
            edges = self.Gec.edges()
            bud_candidates_found = False
            bud_candidate = None

            for e in edges:
                n = e[1]
                n_in = self.Gec.in_neighbors(n)
                n_out = self.Gec.out_neighbors(n)
                if len(n_in) >= 2 and len(n_out) == 1:
                    bud_candidates_found = True
                    bud_candidate = n

            if not bud_candidates_found:
                for e in edges:
                    n = e[1]
                    if self.use_acyclic_test(n, 0, None):
                        break   # from the for loop
            else:
                n = bud_candidate
                self.use_acyclic_test(n, 0, None)

            # find and take out isolated
            edges = self.Gec.edges()
            for e in edges:
                n_pre = self.Gec.get_node(e[0])
                n_post = self.Gec.get_node(e[1])
                print 'taking post isolated (no IN neighbors)'
                print 'e:', e, 'Nodes:', n_pre, '->', n_post
                self.kill_post_isolated(n_pre, n_post)

            edges = self.Gec.edges()
            for e in edges:
                n_pre = self.Gec.get_node(e[0])
                n_post = self.Gec.get_node(e[1])
                print 'taking pre isolated (no OUT neighbors)'
                print 'e:', e, 'Nodes:', n_pre, '->', n_post
                self.kill_pre_isolated(n_pre, n_post)

            # until every has been taken out
            edges_left = len(self.Gec.edges()) > 0
            print 'edges_left:', edges_left

        # When all is done and done
        # self.Gec will have no edges
        # now is time to reconstruct only the edges
        # with cycles

        for ec in self.ec:
            for ni in range(0, len(ec) - 1):

                # update Gec
                self.Gec.add_edge(ec[ni], ec[ni+1],
                                  color='red')
                n = self.Gec.get_node(ec[ni])
                n.attr['style'] = 'filled'
                n.attr['fillcolor'] = 'green'

                # update Gab
                eab = self.Gab.get_edge(ec[ni], ec[ni+1])
                eab.attr['color'] = 'red'
                nab = self.Gab.get_node(ec[ni])
                nab.attr['style'] = 'filled'
                nab.attr['fillcolor'] = 'green'

                # update Ga

                ea = self.Ga.get_edge(ec[ni], ec[ni+1])
                ea.attr['color'] = 'red'
                na = self.Ga.get_node(ec[ni])
                na.attr['style'] = 'filled'
                na.attr['fillcolor'] = 'green'

                # update Ltis
                self.sn[int(n)].in_cycle = True

    def find_stems_ab(self):
        # After finding elemental cycles

        # Modify a copy of Ga
        self.Gst = self.Ga.copy()

        # Remove distinguished edges
        # loop over elemental cycles
        for ec in self.ec:
            for ni in range(0, len(ec) - 1):
                n = ec[ni]
                n_in = self.Gst.in_neighbors(n)
                if len(n_in) > 1:
                    for nc_de in n_in:
                        if nc_de not in ec:
                            # it is a distinguished edge
                            self.Gst.remove_edge(nc_de, n)

        print 'Distinguished Edges Removed'

        # Remove elemental cycles
        for ec in self.ec:
            for ni in range(0, len(ec) - 1):
                if self.Gst.has_edge(ec[ni], ec[ni+1]):
                    self.Gst.remove_edge(ec[ni], ec[ni+1])

        for ec in self.ec:
            for ni in range(0, len(ec) - 1):
                if self.Gst.has_node(ec[ni]):
                    self.Gst.remove_node(ec[ni])

        print 'Elemental Cycles removed'

        # Remove connections between controlled edges
        sn_controlled = [sn for sn in self.sn if sn.controlled]
        for sn in sn_controlled:
            if self.Gst.has_node(sn.index):
                n = self.Gst.get_node(sn.index)
                out_n = self.Gst.out_neighbors(n)
                for on in out_n:
                    if self.sn[int(on)] in sn_controlled:
                        self.Gst.remove_edge(n, on)

        print 'Connections between controlled nodes removed'

        # Find stems
        # Start backwards

        dilation_found = False
        edges_left = len(self.Gst.edges()) > 0
        while edges_left:
            edges = self.Gst.edges()
            for e in edges:
                n_post = self.Gst.get_node(e[1])
                post_out = self.Gst.out_neighbors(n_post)
                if len(post_out) == 0:
                    print 'found stem top candidate at', n_post
                    # This is the one we want
                    # Last on a possible stem
                    # it needs to be a controlled node
                    # or find a controlled node in the predecessors
                    n_next = self.Gst.get_node(e[0])
                    previous = self.Gst.get_node(e[1])
                    stem = [n_post]

                    # RECURSIVE!
                    while True:
                        if self.sn[int(n_next)].controlled:
                            # break other OUT neighbors
                            # they need their own controlled nodes!

                            n_next_in = self.Gst.in_neighbors(n_next)
                            n_next_out = self.Gst.out_neighbors(n_next)

                            for bn in n_next_out:
                                if bn != previous:
                                    if self.Gst.has_edge(n_next, bn):
                                        self.Gst.remove_edge(n_next, bn)

                            # break other IN neighbors
                            # they need their own controlled nodes!
                            for bni in range(1, len(n_next_in)):
                                bn = n_next_in[bni]
                                if self.Gst.has_edge(bn, n_next):
                                    self.Gst.remove_edge(bn, n_next)

                            # Full stem
                            # since we are going backwards,
                            # needs to be reversed
                            stem.reverse()
                            self.st.append(stem)

                            # Remove from Gst
                            self.Gst.remove_node(n_next)
                            for st in stem:
                                self.Gst.remove_node(st)

                            break

                        else:
                            stem.append(n_next)
                            # keep going down
                            n_next_in = self.Gst.in_neighbors(n_next)
                            if len(n_next_in) == 0:
                                # Didn't find any controlled node!!!
                                # Dilation!
                                dilation_found = True
                                # needs to be reversed
                                stem.reverse()
                                self.di.append(stem) # Not a stem at this point

                                # remove from Gst
                                for st in stem:
                                    self.Gst.remove_node(st)

                                break

                            elif len(n_next_in) == 1:
                                # break other OUT neighbors
                                # they need their own controlled nodes!

                                n_next_out = self.Gst.out_neighbors(n_next)
                                for bn in n_next_out:
                                    if bn != previous:
                                        if self.Gst.has_edge(n_next, bn):
                                            self.Gst.remove_edge(n_next, bn)
                                # keep going down
                                previous = n_next
                                n_next = n_next_in[0]

                            elif len(n_next_in) > 1:

                                # break other IN neighbors
                                # they need their own controlled nodes!
                                for bni in range(1, len(n_next_in)):
                                    bn = n_next_in[bni]
                                    if self.Gst.has_edge(bn, n_next):
                                        self.Gst.remove_edge(bn, n_next)

                                # break other OUT neighbors
                                # they need their own controlled nodes!

                                n_next_out = self.Gst.out_neighbors(n_next)
                                for bn in n_next_out:
                                    if bn != previous:
                                        if self.Gst.has_edge(n_next, bn):
                                            self.Gst.remove_edge(n_next, bn)

                                n_next = n_next_in[0]
                                previous = n_next

                    break  # break from for loop after finding a top candidate

            edges_left = len(self.Gst.edges()) > 0

        # After finding all stems, remove controlled nodes

        controlled_n = [n for n in self.Gst.nodes() if self.sn[int(n)].controlled]
        for n in controlled_n:
            self.Gst.remove_node(n)

        # The only nodes left are also dilations
        # Lastly, find unreachables without current edges
        nodes = self.Gst.nodes()
        for n in nodes:
            # dilation!
            dilation_found = True
            self.di.append([n])

        if dilation_found:
            print 'Dilation found!'

            for di in self.di:
                print 'dilation:', di
                for ni in range(0, len(di) - 1):
                    # update Gab
                    eab = self.Gab.get_edge(di[ni], di[ni+1])
                    eab.attr['color'] = 'darkorange'

                for ni in range(0, len(di)):
                    nab = self.Gab.get_node(di[ni])
                    if self.sn[int(nab)].accessible:
                        nab.attr['style'] = 'filled'
                        nab.attr['fillcolor'] = 'darkorange'

        # update Gab
        for st in self.st:
            for ni in range(0, len(st) - 1):
                eab = self.Gab.get_edge(st[ni], st[ni+1])
                eab.attr['color'] = 'red'

            for ni in range(0, len(st)):
                nab = self.Gab.get_node(st[ni])
                nab.attr['style'] = 'filled'
                nab.attr['fillcolor'] = 'darkgreen'


    def analysis_ab(self):
        self.inaccessibility_ab()
        self.find_elemental_cycles_ab()
        self.find_stems_ab()
        self.draw_Gab()

    def get_sea(self, u, v):
        return [sea for sea in self.sea if (sea.u == u and sea.v == v)][0]

    def matching_a(self):

        print '\n\n ***************** \n\n'

        for sna in self.sna:

            n = self.Gmm.get_node(sna.index)
            n_in = self.Gmm.in_neighbors(n)
            n_out = self.Gmm.out_neighbors(n)

            found_IN_matched = False
            found_OUT_matched = False
            found_IN_free = False
            found_OUT_free = False

            # there can be only one!
            match_in = None
            match_out = None

            # check all IN edges
            for nn in n_in:
                seai = self.get_sea(int(nn), int(n))
                # if one is matched
                if seai.matched:
                    match_in = nn
                    found_IN_matched = True

                if seai.matched is None:
                    found_IN_free = True

            # check all OUT edges
            for nn in n_out:
                seao = self.get_sea(int(n), int(nn))
                # if one is matched
                if seao.matched:
                    match_out = nn
                    found_OUT_matched = True

                if seao.matched is None:
                    found_OUT_free = True

            print '\n *** Checking New Node: ***'
            print 'n', n
            print 'IN_matched', found_IN_matched
            print 'IN_free', found_IN_free
            print 'OUT_matched', found_OUT_matched
            print 'OUT_free', found_OUT_free

            # BINARY COMBINATION

            if (not found_IN_matched) and (not found_IN_free):
                # unmatched
                sna.matched = False
                self.um.append(sna.index)

            if (not found_OUT_matched) and (not found_OUT_free):
                pass

            if (not found_IN_matched) and found_IN_free:
                # match!
                for nn in n_in:
                    seai = self.get_sea(int(nn), int(n))
                    if seai.matched is None:
                        sna.matched = True
                        seai.matched = True
                        break

            if (not found_OUT_matched) and found_OUT_free:
                # match!
                for nn in n_out:
                    seao = self.get_sea(int(n), int(nn))
                    snao = self.sna[int(nn)]
                    print 'in OUT (NO, YES):'
                    print 'seao', seao.e, 'matched:', seao.matched
                    print 'snao', snao.index, 'matched:', snao.matched

                    if seao.matched is None and \
                                    not snao.matched:
                        seao.matched = True
                        # match the node
                        # so no other one grabs it!
                        snao.matched = True
                        break

            if found_IN_matched and (not found_IN_free):
                sna.matched = True

            if found_OUT_matched and (not found_OUT_free):
                pass

            if found_IN_matched and found_IN_free:
                sna.matched = True

            if found_OUT_matched and found_OUT_free:
                pass

            # all undecided connections left
            # are set to False
            for nn in n_in:
                seai = self.get_sea(int(nn), int(n))
                if seai.matched is None:
                    seai.matched = False

            for nn in n_out:
                seao = self.get_sea(int(n), int(nn))
                if seao.matched is None:
                    seao.matched = False


            print '\n----------------'
            print 'sna matched', sna.matched
            for nn in n_out:
                seao = self.get_sea(int(n), int(nn))
                print 'seao', seao.e, 'matched:', seao.matched

            for nn in n_in:
                seai = self.get_sea(int(nn), int(n))
                print 'seai', seai.e, 'matched:', seai.matched


        # update Gmm

        for sna in self.sna:
            n = self.Gmm.get_node(sna.index)
            if sna.matched:
                n.attr['style'] = 'filled'
                n.attr['color'] = 'green'

            elif sna.matched is False:
                n.attr['style'] = 'filled'
                n.attr['color'] = 'gray'

        for sea in self.sea:
            e = self.Gmm.get_edge(sea.u, sea.v)
            if sea.matched:
                e.attr['color'] = 'violet'
            elif sea.matched is False:
                e.attr['color'] = 'gray'

        self.draw_Gmm()

