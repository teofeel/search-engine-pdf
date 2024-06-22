import json
import fitz
from entities.Trie import Trie
import re
from constants import PAGE_OFFSET
from entities import GraphV1
from entities import Graph


def pdf_to_graph():
    pdf_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    graph = Graph.Graph(directed=True)
    hashmap = {}
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        page_text = page.get_text()

        hashmap[page_num+1] = {
            'page_id': page_num+1,
            'content': page_text,
            'trie': Trie().insert_words_trie(page_text),
            'connections': [],
            'next': min(page_num+2, len(pdf_doc))
        }

    graph, vertex_map = convert_hashmap_to_graph(hashmap) 
    #graph.display()

    return graph

def convert_hashmap_to_graph(hashmap):
    graph = Graph.Graph(directed=True)
    vertex_map = {}

    for i in hashmap:
        vertex_map[i] = graph.insert_vertex(hashmap[i]['page_id'], hashmap[i]['content'], hashmap[i]['trie'], 0)
    
    for i in hashmap:
        graph.set_next_page(vertex_map[i], vertex_map[hashmap[i]['next']])

        page_links = extract_page_link(hashmap[i]['content'])

        for link in page_links:
            graph.insert_edge(vertex_map[i], vertex_map[link+PAGE_OFFSET])
    
    return graph, vertex_map


def create_page_links(graph):
    for page in graph.vertices():
        text = page.content

        page_links = extract_page_link(text)

        for connected_page in page_links:
            graph.insert_edge(page, graph.get)
            graph.add_edge(graph.pages[page].page_id, connected_page+PAGE_OFFSET)


def extract_page_link(text):
    patterns = [
        r'see page (\d+)',
        r'on page (\d+)',
        r'see pages (\d+) and (\d+)',
        r'on pages (\d+) and (\d+)',
        r'see page (\d+) and (\d+)'
    ]

    page_links = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            if(isinstance(match, tuple)):
                page_links.extend(match)
            else:
                page_links.append(match)

    try:
        return list(map(int, page_links))
    except:
        return []
    
        

def load_files():
    pass  

def save_files():
    pass
