import re
import copy
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
            if char.lower() not in node.children:
                node.children[char.lower()] = TrieNode()
            node = node.children[char.lower()]
        node.is_end_of_word = True
        node.positions.append(position)

    def search(self, word):
        node = self.root
        for char in word:
            if char.lower() not in node.children:
                return []
            node = node.children[char.lower()]
            
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
    
    def search_combination(self, text, logical_operators):
        result = self.search(text[0])!=[]
        operators = copy.deepcopy(logical_operators) 
        if len(operators)==0: return result
        
        for i in range(1,len(text)):
            if len(operators)==0: return result
            operation = operators.pop(0)

            if operation == 'AND':
                result = result and self.search(text[i])!=[]
                
            elif operation=='OR':
                result = result or self.search(text[i])!=[]
                
            elif operation=='NOT':
                result = result and self.search(text[i])==[]
                
        return result