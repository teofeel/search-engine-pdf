import re
import algorithms.merge_sort as merge_sort
import algorithms.boyer_moore as boyer_moore
import itertools
from constants import PAGE_OFFSET
from prettytable import PrettyTable, ALL
        
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
                i+=1
                break
            i-=1
        start = max(i, 0)

        i = match.end()
        while i<len(graph_page.content):
            if graph_page.content[i]=='.'  or graph_page.content[i]=='\n':
                i-=1
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
    if text[0]=='"' and text[len(text)-1]=='"':
        return text[1:len(text)-1], True, None


    text_arr = text.split(' ')
    new_text = []
    logical_operators = []
    for i in text_arr:
        if not( i=='' or i==' ' or i=='\\n') and not(i=='AND' or i=='OR' or i=='NOT'):
            new_text.append(i)
        
        if i=='AND' or i=='OR' or i=='NOT':
            logical_operators.append(i)

    
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

    for page_link in graph.get_incoming_edges(id):
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

    for word in text:
        if (boyer_moore.find(snippet.lower(), word.lower())) != -1:
            rang+=1

    return rang

def sort(results):
    merge_sort.sort(results,0,len(results)-1)
    
        
def dfs_get_results_test(graph, text, results):
    visited = set()
    num_of_result = 0 
    text, phrase, logical_operators = parse_text(text)

    def dfs(page_num, num_of_result):
        if page_num in visited:
            return
        visited.add(page_num)
        
        next_pages = graph.get_outgoing_edges(page_num)
        next_pages.append(graph.vertexes[page_num].next_page)
        
        if phrase==False and graph.vertexes[page_num].trie_structure.search_combination(text, logical_operators):
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

def paginization():
    pass

def print_results(results):
    table = PrettyTable()
    
    table.field_names = ['Number of Page', 'Number of Result', 'Content']
    table.hrules = ALL

    for res in results:
        table.add_row([res['page_number'],res['num_result'],res['content']])

    print(table)
    
def get_results(graph,text):
    results = []
    
    dfs_get_results_test(graph, text, results)
    sort(results)
    print_results(results)
    

    
