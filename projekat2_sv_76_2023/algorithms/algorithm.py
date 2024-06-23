import re
import algorithms.merge_sort as merge_sort
import algorithms.boyer_moore as boyer_moore
import itertools
from constants import PAGE_OFFSET
from prettytable import PrettyTable, ALL
import copy

def extract_words(graph_page, text, results, num_of_result):
    for word in text:
        snippets = graph_page.trie_structure.search_and_extract_snippets(graph_page.content, word)
        color_start = "\033[31m"
        color_end = "\033[0m"

        for snippet in snippets:
            colored_snippet = snippet

            for w in text:
                pattern_temp = re.compile(rf'\b{re.escape(w)}\b', re.IGNORECASE) # re.escape(word)
                colored_snippet = pattern_temp.sub(f"{color_start}{w}{color_end}", colored_snippet)

            num_of_result+=1
            results.append({
                'num_result':num_of_result,
                'page_number':graph_page.page_id,
                'content': colored_snippet,
                'original_search': word,
                'rang': generate_rang_result(graph_page, text, snippet, False) 
            })
    return num_of_result


def extract_phrase(graph_page, word, results, num_of_result):
    pattern = re.compile(re.escape(word), re.IGNORECASE) # rf'\b{re.escape(word)}\b'
    matches = list(pattern.finditer(graph_page.content))

    for match in matches:
        color_start = "\033[31m"
        color_end = "\033[0m"

        i = match.start()
        while i>0:
            if graph_page.content[i]=='.' or graph_page.content[i]=='\n':
                break
            i-=1
        start = max(i, 0)

        i = match.end()
        while i<len(graph_page.content):
            if graph_page.content[i]=='.'  or graph_page.content[i]=='\n':
                break
            i+=1
        end = min(i, len(graph_page.content))

        snippet = graph_page.content[start:end]

        colored_snippet = snippet

        pattern = re.compile(re.escape(word), re.IGNORECASE) # re.escape(word)
        colored_snippet = pattern.sub(f"{color_start}{word}{color_end}", colored_snippet) 

        num_of_result+=1

        results.append({
            'num_result':num_of_result,
            'page_number':graph_page.page_id,
            'content': colored_snippet,
            'original_search': word,
            'rang': generate_rang_result(graph_page, [word], snippet, True) 
        })

    return num_of_result

def parse_text(text):
    if text[0]=='"' or text[len(text)-1]=='"':
        return text[1:-1], True, None

    text_arr = copy.deepcopy(text.split(' '))
    new_text = []
    logical_operators = []
    
    for i in text_arr:
        if not( i=='' or i==' ' or i=='\\n') and not (i=='AND' or i=='OR' or i=='NOT'):
            word = i
            new_text.append(word)
        
        if i=='AND' or i=='OR' or i=='NOT':
            logical = i
            logical_operators.append(logical)


    return new_text, False, logical_operators


def generate_page_rank(graph, id, original_text, phrase):
    page_rang = 0

    for w in original_text:
        if not phrase and graph.vertexes[id].trie_structure.search(w) != []: 
            page_rang+=1
        if phrase and boyer_moore.find(graph.vertexes[id].content.lower(), w.lower()) != -1:
            pattern = re.compile(re.escape(w), re.IGNORECASE) 
            matches = list(pattern.finditer(graph.vertexes[id].content))
            
            page_rang+=len(matches)

    for page_link in graph.get_linked_pages_edges(id):
        page_rang +=1
        page_rang += get_rang_linked_page(graph.vertexes[page_link], original_text, phrase)

    graph.vertexes[id].rang = page_rang

def get_rang_linked_page(graph_page, text, phrase):
    rang = 0
    for word in text:
        if not phrase and graph_page.trie_structure.search(word) != []:
            rang+=1
        if phrase and boyer_moore.find(graph_page.content.lower(), word.lower()) != -1:
            rang+=1

    return rang

def generate_rang_result(graph_page, text, snippet, phrase):
    rang = graph_page.page_rank

    for word in text:
        if not phrase:
            pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) 
        else:
            pattern = re.compile(re.escape(word), re.IGNORECASE) 
            
        matches = list(pattern.finditer(graph_page.content))
        rang += len(matches)

    #for word in text:
    #    if (boyer_moore.find(snippet.lower(), word.lower())) != -1:
    #        rang+=1

    return rang

def sort(results):
    merge_sort.sort(results)
    
        
def dfs_get_results_test(graph, text_original, results):
    visited = set()
    num_of_result = 0 
    text, phrase, logical_operators = parse_text(copy.deepcopy(text_original))

    def dfs(page_num, num_of_result):
        if page_num in visited:
            return
        visited.add(page_num)
        
        next_pages = graph.get_outgoing_edges(page_num)
        
        if phrase==False and graph.vertexes[page_num].trie_structure.search_combinations_advanced(text_original):
            generate_page_rank(graph, page_num, text, phrase) 
            num_of_result = extract_words(graph.vertexes[page_num], text, results, num_of_result)
            for page in next_pages:
                dfs(page, num_of_result)
    
        elif phrase and boyer_moore.find(graph.vertexes[page_num].content.lower(), text.lower()) != -1:  
            generate_page_rank(graph, page_num, [text], phrase) 
            num_of_result = extract_phrase(graph.vertexes[page_num], text, results, num_of_result)

        for page in next_pages:
            dfs(page, num_of_result)

    dfs(1, num_of_result)

def sort_common_words(words):
    words_arr = []

    for word in words:
        words_arr.append((word, words[word]))

    words_arr.sort(key=lambda tup:tup[1], reverse=True)

    sorted_words = []
    for i in range(3):
        sorted_words.append(words_arr[i][0])

    return sorted_words
    

def find_common_words_prefix(graph, prefix):
    visited = set()

    words = {}
    
    def dfs(page_num):
        if page_num in visited:
            return
        visited.add(page_num)

        next_pages = graph.get_outgoing_edges(page_num)

        extracted_words = graph.vertexes[page_num].trie_structure.extract_words_prefix(prefix)

        for word in extracted_words:
            if not word in words:
                words[word] = 1
            elif word in words:
                words[word] += 1

        for page in next_pages:
            dfs(page)

    dfs(1)

    most_common_words = sort_common_words(words) 
    
    return most_common_words    

def autocomplete(graph, original_text):
    if original_text[0]=='"' or original_text[len(original_text)-1]=='"':
        return original_text
    
    text, _, _ = parse_text(original_text)
    
    suggestions = {}
    for word in text:

        if word[len(word)-1] == '*':
            shorten_word = word[:len(word)-1]

            if not shorten_word in suggestions:
                suggestions[shorten_word] = find_common_words_prefix(graph, word[:-1])
    
    return suggestions

def alternative_keywords(graph, text):
    pass

import algorithms.postfix_equation as postfix_equation   
def get_results(graph,text):
    results = []
    

    dfs_get_results_test(graph, text, results)
    sort(results)

    

    #print(graph.vertexes[720].trie_structure.search_combinations_advanced(text))
    
    return results
    

    
