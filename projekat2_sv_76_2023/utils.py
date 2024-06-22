import json
import fitz
from entities.Trie import Trie
import re
from constants import PAGE_OFFSET
from entities import Graph

def pdf_to_hashmap():
    pdf_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    hashmap = {}
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        page_text = page.get_text()

        #page = Graph.PageNode(page_num+1, page_text, Trie().insert_words_trie(page_text), 0, min(page_num+2, len(pdf_doc)))
        
        hashmap[page_num + 1] = {
            'content':page_text,
            'page_number':page_num + 1,
            'trie_structure': Trie().insert_words_trie(page_text),
            'page_connected': []
        }
    
    create_page_links(hashmap)

    graph = convert_hashmap_to_graph(hashmap)

    #graph.display()

    return hashmap, graph


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
            graph.add_edge(page_id, connected_page, page.next_page)

        graph.add_next_page(page_id, page.next_page)

    return graph

def create_page_links(files):
    for file in files:
        text = files[file]['content']

        page_links = extract_page_link(text)

        for link in page_links:

            files[file]['page_connected'].append(link+PAGE_OFFSET)


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
