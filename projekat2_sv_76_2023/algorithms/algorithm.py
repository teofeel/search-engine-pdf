import re
import algorithms.merge_sort as merge_sort
import algorithms.boyer_moore as boyer_moore

from constants import PAGE_OFFSET


def search_files(files, text, results):
    num_of_result = 0

    for file in files:
        if boyer_moore.find(files[file]['content'], text) == -1: continue

        num_of_result = extract_result_from_file(files[file], text, results, num_of_result)


def extract_result_from_file(file, text, results, num_of_result):
    pattern = re.compile(re.escape(text), re.IGNORECASE)
    matches = list(pattern.finditer(file['content']))

    for match in matches:
        color_start = "\033[31m"
        color_end = "\033[0m"

        start = max(match.start()-5, 0)
        end = min(match.end()+10, len(file['content']))
        
        snippet = file['content'][start:end]
        colored_content = pattern.sub(f"{color_start}{text}{color_end}", snippet)
        
        num_of_result+=1

        results.append({
            'num_result':num_of_result,
            'page_number':file['page_number'],
            'content': colored_content,
            'original_search': text,
            'rang': len(matches)
        })

    
    return num_of_result

def parse_text(text):
    if text[0]=='"' and text[len(text)-1]=='"':
        print(text[1:len(text)-1])
        return text[1:len(text)-1]
    
    return text

def get_results(files, text):
    text = parse_text(text)
    
    results = []
    search_files(files,text,results)

    sort(results)

    for res in results:
        print('#'*10)
        print(f"Number of result: {res['num_result']}\nNumber of page: {res['page_number']}\nContent: {res['content']}")
 
def generate_rang(results, text):
    pass

def sort(results):
    merge_sort.sort(results,0,len(results)-1)
    
        

    



