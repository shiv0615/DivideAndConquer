import copy, os
from collections import OrderedDict
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Graph():
    def __init__(self, nvertices=None, medges=None, inbuilt=None, fpath=None, summary=True, seed=8934):
        self.nvertices = nvertices
        self.medges    = medges
        self.inbuilt   = inbuilt
        self.fpath     = fpath
        self.summary   = summary
        self.vertices  = []
        self.edges     = []
        self.seed      = seed
        self.nvertices_old= self.nvertices
        self.medges_old   = self.medges

        self.fused_vertex_ids = []
        self.fused_edge_ids   = []
        self.fused_vertices   = []
        self.fused_edges      = []
        self.graph_copy       = None
        self.min_cut_graph    = None

        if nvertices is not None:
            self.nvertices = nvertices
            self.vertices  = [Vertex(id=i,status='Actve') for i in range(nvertices)]
        if medges is not None:
            self.medges    = medges
            self.edges     = [Edge(id=i,status='Undefined') for i in range(medges)]
        if self.fpath is None and self.inbuilt is not None:
            if self.inbuilt == 'SquareWithOneDiag': self.build_square_with_one_diag_graph()
        elif self.fpath is not None:
            self.read_from_file()

    def build_square_with_one_diag_graph(self):
        self.create_vertices(nvertices=4)
        self.create_edges(medges=6, status='Undefined')
        ivertex = 0
        for iedge, edge in enumerate(self.edges):
            if iedge < self.medges-2:
                vertex_1 = self.vertices[ivertex]
                vertex_2 = self.vertices[ivertex%(self.nvertices-1) - ivertex//(self.nvertices-1)+1]
                ivertex += 1
            elif iedge == 4:
                vertex_1 = self.vertices[0]
                vertex_2 = self.vertices[2]
            else:
                vertex_1 = self.vertices[1]  
                vertex_2 = self.vertices[3]
            edge.set_vertices(vertices=[vertex_1, vertex_2])
            edge.set_status(status='Active')
            edge.set_direction(direction=1)
            #create vertex connections
            vertex_1.add_edge_connection(edge)
            vertex_2.add_edge_connection(edge)

            con_vert_id = [con_vert.id for con_vert in edge.vertices]
            # print('Vertices connected to this edge: ', con_vert_id)

            con_vert_id = [con_vert.id for con_vert in vertex_1.connected_vertices]
            con_edge_id = [con_edge.id for con_edge in vertex_1.edges]
            # print('vertex_1 with id: ', vertex_1.id)
            # print('vertex_1 status: ', vertex_1.status)
            # print('Vertices connected to this vertex: ', con_vert_id)
            # print('Edges connected to this vertex: ', con_edge_id)

            con_vert_id = [con_vert.id for con_vert in vertex_2.connected_vertices]
            con_edge_id = [con_edge.id for con_edge in vertex_2.edges]
            # print('vertex_2 with id: ', vertex_2.id)
            # print('vertex_2 status: ', vertex_2.status)
            # print('Vertices connected to this vertex: ', con_vert_id)
            # print('Edges connected to this vertex: ', con_edge_id)

        if self.summary: self.print_graph_summary()

    def create_vertices(self, nvertices, status='Active'):
        self.nvertices = nvertices
        self.vertices  = [Vertex(id=i, status=status) for i in range(self.nvertices)]

    def create_edges(self, medges, status='Undefined'):
        self.medges = medges
        self.edges  = [Edge(id=i, status=status) for i in range(self.medges)]

    def read_from_file(self):
        self.create_vertices(nvertices=len(open(self.fpath).readlines(  )))
        self.medges = 0
        for line in open(self.fpath):
            parts = np.array(line.strip().split('\t'), dtype=int)
            parts = parts - 1
            vertex = self.get_vertex(parts[0])
            for nbr_vertex_id in parts[1:]:
                nbr_vertex = self.get_vertex(nbr_vertex_id)
                if nbr_vertex not in vertex.connected_vertices:
                    vertex.add_vertex_connection(nbr_vertex)
                    e = Edge(id=self.medges, status = 'Active', vertices=[vertex,nbr_vertex])
                    self.edges.append(e)
                    vertex.add_edge_connection(e)
                    nbr_vertex.add_edge_connection(e)
                    self.medges+=1
        self.check_for_graph_validity()

    def print_graph_summary(self, print_only_active = True):
        print('Graph with ' + str(self.nvertices) + ' Vertices and ' + str(self.medges) + ' Edges')
        print('--------- Printing Vertex Information ------------')
        for vertex in self.vertices:
            if print_only_active and vertex.status != 'Active': continue
            con_vert_id = [con_vert.id for con_vert in vertex.connected_vertices]
            con_edge_id = [con_edge.id for con_edge in vertex.edges]
            con_vert_stat=[con_vert.status for con_vert in vertex.connected_vertices]
            print('Vertex with id: ', vertex.id)
            print('Vertex status: ', vertex.status)
            print('Vertices connected to this vertex: ', con_vert_id)
            print('Status of connected veritces: ', con_vert_stat)
            print('Edges connected to this vertex: ', con_edge_id)
        print('--------- Printing Edge Information ------------')
        for edge in self.edges:
            if print_only_active and edge.status != 'Active': continue
            con_vert_id = [con_vert.id for con_vert in edge.vertices]
            print('Edge with id: ', edge.id)
            print('Vertices connected to this edge: ', con_vert_id)
            print('Edge status: ', edge.status)
            print('Edge direction: ', edge.direction)

    def determine_karger_min_cut(self):
        # self.graph_copy   = copy.deepcopy(self)
        seed              = np.random.seed(self.seed)
        iloop             = 0
        while (self.nvertices > 2 and iloop < 1000*self.nvertices):
            edge_id = np.random.randint(0, self.medges-1)
            edge    = self.edges[edge_id]
            if edge_id == self.fused_edge_ids or edge not in self.edges:
                iloop = iloop + 1
                continue
            self.fuse_edge(edge)
            # self.add_to_fused_elem_count(edge)
            iloop          += 1
        self.check_for_graph_validity()
        print(f'Number of edges in the min cut is {len(self.vertices[0].edges)} for vertex is: {self.vertices[0].id} ', )

    def add_to_fused_elem_count(self, edge):
        if edge.id not in self.fused_edge_ids:
            self.fused_edge_ids.append(edge.id)
            self.fused_edges.append(edge)
        for vert in self.vertices:
            if vert.status == 'Fused' and vert not in self.fused_vertices:
                self.fused_vertices.append(vert)
                self.fused_vertex_ids.append(vert)

    def visualize(self):
        nxg = nx.Graph()
        for edge in self.edges:
            if edge.status == 'Fused': continue
            nxg.add_edge(edge.vertices[0].id, edge.vertices[1].id)
        nx.draw(nxg, with_labels=True)
        plt.show()

    def fuse_edge(self, edge):
        self.remove_edge(edge)
        self.remove_vertex(edge.vertices[0], par_vertex=edge.vertices[1])
        edge.vertices[1].remove_edge_connection(edge)
        if edge.vertices[1].status == 'Fused':
            self.remove_vertex(edge.vertices[1])
        del(edge.vertices)

    def remove_vertex(self, vertex, par_vertex=None):
        # if vertex not in self.vertices: return
        self.vertices.remove(vertex)
        self.nvertices -= 1
        vertex.set_status('Fused')
        if par_vertex is not None: vertex.parent_vertex = par_vertex
        for con_vert in vertex.connected_vertices:
            con_vert.connected_vertices.remove(vertex)
        if par_vertex is not None:
            nv_edges = len(vertex.edges)
            while nv_edges > 0:
                v_edge   = vertex.edges[nv_edges-1]
                nv_edges-= 1
                if par_vertex in v_edge.vertices:
                    if v_edge in self.edges:
                        self.remove_edge(v_edge)
                    vertex.remove_edge_connection(v_edge)
                    par_vertex.remove_edge_connection(v_edge)
                    continue
                indx = v_edge.vertices.index(vertex)
                v_edge.vertices[indx] = par_vertex
                par_vertex.add_edge_connection(v_edge)
                vertex.remove_edge_connection(v_edge)
        else:
            nv_edges = len(vertex.edges)
            while nv_edges > 0:
                v_edge   = vertex.edges[nv_edges-1]
                vertex.remove_edge_connection(v_edge)
                nv_edges-= 1
        del(vertex.connected_vertices)

    def remove_edge(self, edge):
        # if edge not in self.edges:
        #     print(f'Edge id: {edge.id} and status: {edge.status}')
            # return
        self.edges.remove(edge)
        self.medges -= 1
        edge.set_status('Fused')

    def get_vertex(self, id):
        return self.vertices[id]

    def check_for_graph_validity(self):
        sum_edges = 0
        for vertex in self.vertices:
            sum_edges += len(vertex.edges)
        print(f'Number of edges: {self.medges} is twice the number of all edges connected to vertices: {sum_edges}')
        assert 2*self.medges == sum_edges, 'Number of edges is not twice the number of edges connected to all vertices'

class Edge():
    def __init__(self, id, vertices = None, status = 'Undefined', direction = 1):
        self.id                 = id
        self.parent_edge_id     = id
        self.vertices           = []
        self.direction          = direction    # -1 for vertex_2 to 1 and 0 for degenerate edge
        self.status             = status       # Active, Fused, Looping, Undefined
        if vertices is not None:
            self.vertices = vertices
            self.parent_vertices = vertices

    def set_vertices(self, vertices=[]):
        self.vertices = vertices

    def set_status(self, status):
        self.status = status

    def set_direction(self, direction):
        self.direction = direction

class Vertex():
    def __init__(self, id, edges=None, status = 'Undefined', connected_vertices=None):
        self.id                 = id
        self.parent_vertex      = id
        self.edges              = []
        self.connected_vertices = []
        self.status             = status  # Active, Fused, Looping, Undefined
        if edges is not None:
            self.edges.append(edges)
            self.create_connected_vertex_list_from_edges(edges=edges)

        if connected_vertices is not None:
            self.connected_vertices.append(connected_vertices)

    def set_vertexId(self, id, pVertexId=None):
        self.id = id
        if pVertexId is not None: self.parent_vertex = id

    def set_status(self, status):
        self.status = status

    def set_direction(self, direction):
        self.direction = direction

    def add_edge_connection(self, edge):
        assert edge.status != 'Fused', 'Edge with Fused Status Detected in add_edge_connection'
        if edge in self.edges:return
        self.edges.append(edge)
        vertex_1 = edge.vertices[0]
        vertex_2 = edge.vertices[1]
        vertex_1.add_vertex_connection(vertex_2)
        vertex_2.add_vertex_connection(vertex_1)

    def add_vertex_connection(self, vertex):
        assert vertex.status != 'Fused', 'vertex with Fused Status Detected in add_edge_connection'
        if vertex in self.connected_vertices: return
        self.connected_vertices.append(vertex)

    def remove_edge_connection(self, edge):
        if edge not in self.edges: return
        self.edges.remove(edge)
        self.remove_vertex_connection(edge)

    def remove_vertex_connection(self, edge):
        if edge.vertices[0] != self and edge.vertices[0] in self.connected_vertices:
            self.connected_vertices.remove(edge.vertices[0])
        elif edge.vertices[1] in self.connected_vertices:
            self.connected_vertices.remove(edge.vertices[1])

def main():

    fpath = r'/Users/shivswe/Machine_Learning/Algorithms_Part1/DivideAndConquer/Week4/KagerMincCut.txt'
    # fpath = r'/Users/shivswe/Machine_Learning/Algorithms_Part1/DivideAndConquer/Week4/SimpleInput.txt'
    # g = Graph(inbuilt='SquareWithOneDiag', summary=False)
    g = Graph(fpath=fpath, summary=False)
    # g.visualize()
    g.determine_karger_min_cut()
    # g.print_graph_summary()
    # g.visualize()

if __name__ =='__main__':

    main()
