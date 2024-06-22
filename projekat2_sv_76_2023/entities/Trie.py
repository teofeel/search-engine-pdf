import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.positions = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, position):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.positions.append(position)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]
            
        return node.positions if node.is_end_of_word else []

    def extract_words_with_positions(self,text):
        words_with_positions = []
        for match in re.finditer(r'\b\w+\b', text.lower()):
            word = match.group()
            start_pos = match.start()
            words_with_positions.append((word, start_pos))
        return words_with_positions

    def insert_words_trie(self, text):
        word_with_position = self.extract_words_with_positions(text)
        for word, pos in word_with_position:
            self.insert(word, pos)

        return self

    def get_snippet(self, text, position):
        i = position
        while i>0:
            if text[i]=='.' or text[i]=='\n':
                i+=1
                break
            i-=1
        start = max(i, 0)

        i = position
        while i<len(text):
            if text[i]=='.' or text[i]=='\n':
                break
            i+=1
        end = min(i, len(text))
        
        return text[start:end]

    def search_and_extract_snippets(self,text, word):
        positions = self.search(word)
        snippets = [self.get_snippet(text, pos) for pos in positions]
        return snippets