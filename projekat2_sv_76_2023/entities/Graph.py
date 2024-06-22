import re
from algorithms import algorithm

class PageNode:
    def __init__(self, page_id, content, trie_structure,page_rank, next_page):
        self.page_id = page_id
        self.content = content
        self.trie_structure = trie_structure
        self.page_rank = page_rank
        self.next_page = next_page


class Graph:
    def __init__(self):
        self.vertexes = {}
        self.edges = []

    def add_page(self, page):
        if page.page_id not in self.vertexes:
            self.vertexes[page.page_id] = page

    def add_edge(self, start_page_id, end_page_id):
        self.edges.append((start_page_id, end_page_id))
        #self.edges.append((end_page_id, start_page_id))

    def get_outgoing_edges(self, page_id):
        arr = []
        for edge in self.edges:
            if edge[0]==page_id:
                arr.append(edge[1])
        return arr
            
        
    def get_incoming_edges(self, page_id):
        arr = []
        for edge in self.edges:
            if edge[1]==page_id:
                arr.append(edge[0])
    
        return arr


    def add_next_page(self, start_page_id, end_page_id):
        if start_page_id in self.vertexes and end_page_id in self.vertexes:
            self.vertexes[start_page_id].next_page = end_page_id

    def display(self):
        for page_id, page in self.vertexes.items():
            print(f"Page {page_id}:")
            print(f"  Rank: {page.page_rank}")
            print(f"  Outgoing edges: {self.get_outgoing_edges(page_id)}")
            print(f"  Incoming edges: {self.get_incoming_edges(page_id)}")
            print(f"  Next page: {page.next_page}")

    def search_page(self, page_id):
        if page_id in self.vertexes:
            return self.vertexes[page_id]
        return None
    
        
