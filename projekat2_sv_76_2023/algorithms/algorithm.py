import re
import algorithms.merge_sort as merge_sort
import algorithms.boyer_moore as boyer_moore
import itertools
from constants import PAGE_OFFSET

def search_files(files,text,results):
    num_of_result = 0

    for file in files:
        if(len(text)>1): 
            num_of_result = search_words_seperated(files[file], text, results, num_of_result)
            generate_page_rank(files[file], text)
            continue
        
        if boyer_moore.find(files[file]['content'].lower(), text[0]) == -1:  
            continue


        num_of_result = extract_phrase_from_file(files[file], text[0], results, num_of_result)
        generate_page_rank(files[file], text)

def search_words_seperated(file, text, results, num_of_result):
    for word in text:
        snippets = file['trie_structure'].search_and_extract_snippets(file['content'], word)
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
                'page_number':file['page_number'],
                'content': colored_snippet,
                'original_search': word,
                'rang': generate_rang_result(file, text, snippet) 
            })
    return num_of_result
            



#def search_files(files, text, results):
#    num_of_result = 0
#
#    for file in files:
#        words = []
#        for word in text:
#            if boyer_moore.find(files[file]['content'].lower(), word.lower()) != -1: 
#                words.append(word)
#
#        if len(words) == 0: continue
#
#
#        num_of_result = extract_result_from_file(files[file], words, text, results, num_of_result)
#        generate_page_rank(files[file], text)


def extract_phrase_from_file(file, word, results, num_of_result):
    pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) # rf'\b{re.escape(word)}\b'
    matches = list(pattern.finditer(file['content']))

    for match in matches:
        color_start = "\033[31m"
        color_end = "\033[0m"

        i = match.start()
        while i>0:
            if file['content'][i]=='.' or file['content'][i]=='\n':
                break
            i-=1
        start = max(i, 0)

        i = match.end()
        while i<len(file['content']):
            if file['content'][i]=='.'  or file['content'][i]=='\n':
                break
            i+=1
        end = min(i, len(file['content']))

        snippet = file['content'][start:end]

        colored_snippet = snippet

        pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) # re.escape(word)
        colored_snippet = pattern.sub(f"{color_start}{word}{color_end}", colored_snippet) 
        
        num_of_result+=1

        results.append({
            'num_result':num_of_result,
            'page_number':file['page_number'],
            'content': colored_snippet,
            'original_search': word,
            'rang': generate_rang_result(file, [word], snippet) 
        })

    return num_of_result

def parse_text(text):
    if text[0]=='"' and text[len(text)-1]=='"':
        return text[1:len(text)-1]
    
    return text.split(' ')


def get_results(files, text):
    text = parse_text(text)
    
    if not isinstance(text, (list,tuple)):
        text = [text]

    results = []
    search_files(files,text,results)

    sort(results)

    for res in results:
        print('#'*10)
        print(f"Number of result: {res['num_result']}\nNumber of page: {res['page_number']}\nContent: {res['content']}")

def generate_page_rank(file, original_text):
    page_rang = 0
    for w in original_text:
        if(boyer_moore.find(file['content'].lower(), w.lower())) != -1:
            page_rang+=1
    file['rang'] = page_rang

def generate_rang_result(file, text, snippet):
    rang = 0

    for word in text:
        pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) # re.escape(word)
        matches = list(pattern.finditer(file['content']))

        rang += len(matches)

    for word in text:
        if (boyer_moore.find(snippet.lower(), word.lower())) != -1:
            rang+=1

    return rang

def sort(results):
    merge_sort.sort(results,0,len(results)-1)
    
        

    



