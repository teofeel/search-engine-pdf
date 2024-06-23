import json
import fitz
from entities.Trie import Trie
import re
from constants import PAGE_OFFSET
from entities import Graph
import pickle

def pdf_to_graph():
    pdf_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    graph = Graph.Graph()

    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        page_text = page.get_text()

        page = Graph.PageNode(page_num+1, page_text, Trie().insert_words_trie(page_text), 0)
        graph.add_page(page)
        graph.add_next_page(page.page_id, min(page_num+2, len(pdf_doc)))

    create_page_links(graph)
    
    #graph.display()

    return graph


def convert_hashmap_to_graph(hashmap):
    graph = Graph.Graph()
    for page_id, page_details in hashmap.items():
        page = Graph.PageNode(
            page_id=page_details['page_number'],
            content=page_details['content'], 
            trie_structure = Trie().insert_words_trie(page_details['content']),
            page_rank=0,
            next_page = min(page_details['page_number']+1, len(hashmap))
        )
        graph.add_page(page)

        for connected_page in page_details['page_connected']:
            graph.add_edge(page_id, connected_page)

        graph.add_next_page(page_id, page.next_page)

    return graph

def create_page_links(graph):
    for page in graph.vertexes:
        text = graph.vertexes[page].content

        page_links = extract_page_link(text)

        for connected_page in page_links:
            graph.add_edge(page, connected_page+PAGE_OFFSET)


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
    try:
        with open('data', 'rb') as file:
            graph = pickle.load(file)
        return graph
    except:
        return False

def save_files(graph):
    try:
        with open('data', 'wb') as file:
            pickle.dump(graph, file)
    except:
        return False
        
    
def save_pages_pdf(graph, results, original_search):
    new_doc = fitz.open()
    old_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    if original_search[0] =='"' or original_search[-1] =='"':
        path = f'results/{original_search[1:-1]}_phrase.pdf'
    else:
        path = f'results/{original_search}.pdf'

    for result in results:
        new_doc.insert_pdf(old_doc, from_page=result['page_number']+1, to_page=result['page_number']+1)
    

    new_doc.save(path)
    new_doc.close()    
    