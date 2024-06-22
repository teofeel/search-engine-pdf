class Graph:

    """ Simple graph representation """

    class Vertex:
        """ Vertex structure for the graph. """
        __slots__ = '_element', '_content', '_trie_structure', '_page_rank', '_next_page'

        def __init__(self, page_id, content, trie_structure, page_rank):
            self._element = page_id
            self._content = content
            self._trie_structure = trie_structure
            self._page_rank = page_rank
            self._next_page = None

        def element(self):
            """ Returns the element (page_id) associated with this vertex. """
            return self._element

        def content(self):
            """ Returns the content of the page. """
            return self._content

        def trie_structure(self):
            """ Returns the trie structure of the page. """
            return self._trie_structure

        def page_rank(self):
            """ Returns the page rank. """
            return self._page_rank

        def set_next_page(self, next_page):
            """ Sets the next page. """
            self._next_page = next_page

        def get_next_page(self):
            """ Gets the next page. """
            return self._next_page

        def __hash__(self):         # allows Vertex to be a map key
            return hash(id(self))

        def __str__(self):
            return str(self._element)

    class Edge:
        """ Edge structure for the graph """
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, origin, destination, element=None):
            self._origin = origin
            self._destination = destination
            self._element = element

        def endpoints(self):
            """ Returns the endpoints of the edge as a tuple (u,v). """
            return self._origin, self._destination

        def opposite(self, v):
            """ Returns the vertex opposite v on this edge. """
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v must be a Vertex instance')
            return self._destination if v is self._origin else self._origin

        def element(self):
            """ Returns the element associated with this edge. """
            return self._element

        def __hash__(self):         # allows Edge to be a map key
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    def __init__(self, directed=False):
        """ Create an empty graph (undirected by default).

        If directed is True, creates a directed graph.
        """
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def _validate_vertex(self, v):
        """ Verify that v is a Vertex of this graph. """
        if not isinstance(v, self.Vertex):
            raise TypeError('Expected a Vertex instance')
        if v not in self._outgoing:
            raise ValueError('Vertex does not belong to this graph.')

    def is_directed(self):
        """ Return True if this is a directed graph; False if undirected. """
        return self._incoming is not self._outgoing

    def vertex_count(self):
        """ Return the number of vertices in the graph. """
        return len(self._outgoing)

    def vertices(self):
        """ Return an iteration of all vertices of the graph. """
        return self._outgoing.keys()

    def edge_count(self):
        """ Return the number of edges in the graph. """
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        """ Return a set of all edges of the graph. """
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """ Return the edge from u to v, or None if not adjacent. """
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """ Return the number of (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to count incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """ Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, page_id, content, trie_structure, page_rank):
        """ Insert and return a new Vertex with element x. """
        v = self.Vertex(page_id, content, trie_structure, page_rank)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """ Insert and return a new Edge from u to v with auxiliary element x.

        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:
            return
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def set_next_page(self, v, next_page):
        """ Set the next page for a vertex v. """
        self._validate_vertex(v)
        self._validate_vertex(next_page)
        v.set_next_page(next_page)

    def display(self):
        """ Display the graph vertices and edges. """
        for v in self.vertices():
            print(f"Page {v.element()}:")
            print(f"  Content: {v.content()}")
            #print(f"  Trie Structure: {v.trie_structure()}")
            #print(f"  Rank: {v.page_rank()}")
            print(f"  Next page: {v.get_next_page()}")
            outgoing_edges = ', '.join(str(e.opposite(v)) for e in self.incident_edges(v))
            print(f"  Outgoing edges: {outgoing_edges}")
            incoming_edges = ', '.join(str(e.opposite(v)) for e in self.incident_edges(v, outgoing=False))
            print(f"  Incoming edges: {incoming_edges}")
            print()

    def get_first_vertex(self):
        for v in self.vertices():
            return v
        
    def dfs(self):
        self._validate_vertex(self.get_first_vertex())
        visited = set()
        

<<<<<<< Updated upstream
    
=======
        def _dfs(v):
            visited.add(v)
            print(v.content())
            for edge in self.incident_edges(v):
                neighbor = edge.opposite(v)
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(self.get_first_vertex())
>>>>>>> Stashed changes
