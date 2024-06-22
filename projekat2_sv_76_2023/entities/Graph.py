import entities.Trie as Trie
from algorithms import algorithm
import re
from constants import PAGE_OFFSET

class PageNode:
    def __init__(self, page_number, content, rang, trie, next_page):
        self._page_number = page_number
        self._content = content
        self._rang=rang
        self._trie_structure = trie
        self._page_connected = []
        self._next_page = next_page


    @property
    def page_number(self):
        return self._page_number
    @property
    def content(self):
        return self._content
    @property
    def rang(self):
        return self._rang
    @property
    def trie_structure(self):
        return self._trie_structure
    @property
    def page_connected(self):
        return self._page_connected
    @property
    def next_page(self):
        return self._next_page

    @page_number.setter
    def page_number(self, value):
        self._page_number = value

    @content.setter
    def content(self, value):
        self._content = value

    @rang.setter
    def rang(self, value):
        self._rang = value

    @trie_structure.setter
    def trie_structure(self, value):
        self._trie_structure = value

    @page_connected.setter
    def page_connected(self, value):
        self._page_connected.append(value)

    @next_page.setter
    def next_page(self, value):
        self._next_page = value

class Graph:
    def __init__(self):
        self.pages = {}

    def add_page(self, page):
        if page.page_number not in self.pages:
            self.pages[page.page_number] = page

    def add_edge(self, start_page_num, end_page_num):
        if start_page_num in self.pages and end_page_num in self.pages:
            self.pages[start_page_num].page_connected.append(end_page_num)

    def display(self):
        for page_num, page in self.pages.items():
            print(f"Page {page_num}: connected to {page.next_page}")

    def search_page(self, page_number):
        if page_number in self.pages:
            return self.pages[page_number].content
        return None

    def dfs_get_results(self, start_page_num, text, results):
        visited = set()
        num_of_result=0

        text, phrase = algorithm.parse_text(text)

        def dfs(page_num, num_of_result):
            if page_num in visited:
                return
            visited.add(page_num)

            if(not phrase):
                algorithm.generate_page_rank(self.pages, self.pages[page_num], text, phrase) 
                num_of_result = algorithm.extract_words(self.pages[page_num], text, results, num_of_result)
                dfs(self.pages[page_num].next_page, num_of_result)

            elif phrase and algorithm.boyer_moore.find(self.pages[page_num].content.lower(), text) == -1:  
                dfs(self.pages[page_num].next_page, num_of_result)

            elif phrase:
                algorithm.generate_page_rank(self.pages, self.pages[page_num], text, phrase)
                num_of_result = algorithm.extract_phrase(self.pages[page_num], text, results, num_of_result)

            dfs(self.pages[page_num].next_page, num_of_result)

        dfs(start_page_num,num_of_result)

    def dfs_create_page_links(self, start_page_num):
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
        visited = set()

        def dfs(page_num):
            if page_num in visited:
                return
            visited.add(page_num)

            text = self.pages[page_num].content

            page_links = extract_page_link(text)

            for link in page_links:
                self.pages[link+PAGE_OFFSET].page_connected = link

            dfs(self.pages[page_num].next_page)

        dfs(start_page_num)
        
    

    