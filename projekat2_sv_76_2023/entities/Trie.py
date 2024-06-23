import re
import copy
import algorithms.postfix_equation as postfix_equation
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
    
    
    def search_combinations_advanced(self, text):
        postfix = postfix_equation.infix_to_postfix(text)

        if not postfix: return False
        if not ('AND' in postfix and 'OR' in postfix and 'NOT' in postfix):
            for res in postfix:
                if self.search(res): return True
        try:
            operations = {'AND', 'OR', 'NOT'}
            operations_arr = []
            operators = []

            result = True
            #operators.append(postfix.pop(0))
            i=0

            while i<len(postfix)-1:
                if not postfix[i] in operations:
                    operators.append(postfix[i])
                    i+=1
                    continue

                while len(operators)>1 and postfix[i] in operations:
                    operator1 = operators.pop()
                    operator2 = operators.pop()

                    if postfix[i] == 'AND':
                        if not isinstance(operator1, (bool)):
                            result = self.search(operator2)!=[] and self.search(operator1)!=[]
                        else:
                            result = self.search(operator2)!=[] and operator1
                
                    elif postfix[i]=='OR':
                        if not isinstance(operator1, (bool)):
                            result = self.search(operator2)!=[] or self.search(operator1)!=[]
                        else:
                            result = self.search(operator2)!=[] or operator1

                    elif postfix[i]=='NOT':
                        if not isinstance(operator1, (bool)):
                            result = self.search(operator2)!=[] and not self.search(operator1)!=[]
                        else:
                            result = self.search(operator2)!=[] and not operator1

                    #print(result, operator1, operator2, postfix[i], 'lol')

                    operators.append(result)
                    i+=1    

                #print(result, operator1, operator2, postfix[i], 'l')
                i+=1

            return result
        except:
            return False
        

    def search_combination(self, text, logical_operators):
        operators = copy.deepcopy(logical_operators) 
        result = self.search(text[0])!=[]

        if len(logical_operators)==0: return True


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
    
    
    def find_prefix_node(self, prefix):
        node = self.root

        for char in prefix:
            if char.lower() in node.children:
                node = node.children[char.lower()]
            else:
                return None
            
        return node
    
    def get_words(self, node, prefix):
        words = []

        if node.is_end_of_word:
            words.append(prefix)

        for char, child in node.children.items():
            words.extend(self.get_words(child, prefix + char))

        return words
    
    def extract_words_prefix(self, prefix):
        node = self.find_prefix_node(prefix)

        if not node:
            return []
        
        words = self.get_words(node, prefix)

        return words