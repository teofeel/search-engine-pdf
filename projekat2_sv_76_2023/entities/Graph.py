import re
from algorithms import algorithm

class PageNode:
    def __init__(self, page_id, content, trie_structure,page_rank, next_page):
        self.page_id = page_id
        self.content = content
        self.trie_structure = trie_structure
        self.page_rank = page_rank
        self.outgoing_edges = []
        self.incoming_edges = []
        self.next_page = next_page


class Graph:
    def __init__(self):
        self.pages = {}

    def add_page(self, page):
        if page.page_id not in self.pages:
            self.pages[page.page_id] = page

    def add_edge(self, start_page_id, end_page_id):
        if start_page_id in self.pages and end_page_id in self.pages:
            self.pages[start_page_id].outgoing_edges.append(end_page_id)
            self.pages[end_page_id].incoming_edges.append(start_page_id)

    def add_next_page(self, start_page_id, end_page_id):
        if start_page_id in self.pages and end_page_id in self.pages:
            self.pages[start_page_id].next_page = end_page_id

    def display(self):
        for page_id, page in self.pages.items():
            print(f"Page {page_id}:")
            print(f"  Rank: {page.page_rank}")
            print(f"  Outgoing edges: {page.outgoing_edges}")
            print(f"  Incoming edges: {page.incoming_edges}")
            print(f"  Next page: {page.next_page}")

    def search_page(self, page_id):
        if page_id in self.pages:
            return self.pages[page_id].content
        return None
    

    