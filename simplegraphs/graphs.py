from abc import ABC, abstractmethod

class Vertice:
    def __init__(self):
        self.edges = set()
        self.incoming = set()
        self.outgoing = set()

    def __iter__(self):
        return _BreadthFirstIterator(self)

    def bfs(self):
        return _DepthFirstIterator(self)
        
    def connect(self, other: Vertice, directed: bool=False, weight: int=0):
        edge = None
        if directed:
            edge = DirectedEdge(self, other, weight)
        else:
            edge = UndirectedEdge(self, other, weight)
            self.incoming.add(edge)
        
        self.edges.add(edge)
        self.outgoing.add(edge)
        other.edges.add(edge)
        other.incoming.add(edge)


class Edge:
    def __init__(self, vertice1: Vertice, vertice2: Vertice, weight: int=0):
        self._vertice1 = vertice1
        self._vertice2 = vertice2
        self.weight = weight

    @abstractmethod
    def traverse(self, origin: Vertice) -> Vertice:
        if origin == self._vertice1:
            return self._vertice2
        elif origin == self._vertice2:
            return self._vertice1


class DirectedEdge(Edge):
    def __init__(self, outgoing: Vertice, incoming: Vertice, weight: int=0):
        Edge.__init__(self, outgoing, incoming)
        self.outgoing = outgoing
        self.incoming = incoming

    def traverse(self) -> Vertice:
        return self.incoming


class UndirectedEdge(Edge):
    def __init__(self, vertice1: Vertice, vertice2: Vertice, weight: int=0):
        Edge.__init__(self, vertice1, vertice2)

    def traverse(self, origin: Vertice) -> Vertice:
        return super().traverse(origin)


class _BreadthFirstIterator():
    def __init__(self, origin: Vertice):
        self._stack = [origin]

    def __iter__(self):
        return self

    def __next__(self):
        if not self._stack:
            raise StopIteration
        next_vertice = self._stack.pop()
        self._stack += next_vertice.outgoing
        return next_vertice


class _DepthFirstIterator():
    def __init__(self, origin: Vertice):
        self._queue = [origin]

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            raise StopIteration
        next_vertice = self._queue.pop(0)
        self._queue += next_vertice.outgoing
        return next_vertice


class Graph:
    def __init__(self):
        self.vertices = set()

    def dfs(self, origin: Vertice):
        return _DepthFirstIterator(origin)

    def bfs(self, origin: Vertice):
        return _BreadthFirstIterator(origin)        

    def edge_set(self):
        raise NotImplementedError

    def add_vertice(self, vertice: Vertice):
        self.vertices.add(vertice)

    def connect(self, vertice1: Vertice, vertice2: Vertice, 
                directed: bool=False, weight: int=0):
        vertice1.connect(vertice1, vertice2, directed, weight)
        