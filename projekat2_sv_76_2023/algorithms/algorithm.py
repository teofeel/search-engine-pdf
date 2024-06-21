import re
import algorithms.merge_sort as merge_sort
import algorithms.boyer_moore as boyer_moore
import itertools
from constants import PAGE_OFFSET


def search_files(files, text, results):
    num_of_result = 0

    for file in files:
        words = []
        for word in text:
            if boyer_moore.find(files[file]['content'].lower(), word.lower()) != -1: 
                words.append(word)

        if len(words) == 0: continue


        num_of_result = extract_result_from_file(files[file], words, text, results, num_of_result)


def extract_result_from_file(file, text, original_text, results, num_of_result):
    
    for word in text:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        matches = list(pattern.finditer(file['content']))

        print(len(matches), file['page_number'])
        for match in matches:
            color_start = "\033[31m"
            color_end = "\033[0m"

            i = match.start()
            while i>1:
                if file['content'][i]=='.' or file['content'][i]=='\n':
                    break
                i-=1
            start = max(i, 0)

            i = match.end()
            while i<len(file['content'])-1:
                if file['content'][i]=='.'  or file['content'][i]=='\n':
                    break
                i+=1
            end = min(i, len(file['content']))

            snippet = file['content'][start:end]

            for w in text:
                pattern_temp = re.compile(re.escape(w), re.IGNORECASE)
                snippet = pattern_temp.sub(f"{color_start}{w}{color_end}", snippet) 


            num_of_result+=1

            results.append({
                'num_result':num_of_result,
                'page_number':file['page_number'],
                'content': snippet,
                'original_search': word,
                'rang': generate_rang(file, text, original_text) #len(matches) 
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
    print('#'*20)

    for res in results:
        print('#'*10)
        print(f"Number of result: {res['num_result']}\nNumber of page: {res['page_number']}\nContent: {res['content']}")


 
def generate_rang(file, text, original_text):
    rang = 0

    for word in text:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        matches = list(pattern.finditer(file['content']))

        rang += len(matches)

    word_in_text = []
    
    for w in original_text:
        if(boyer_moore.find(file['content'].lower(), w.lower())) != -1:
            word_in_text.append(w)

    if(len(word_in_text)==len(original_text)):
        rang*=2 

    return rang

def sort(results):
    merge_sort.sort(results,0,len(results)-1)
    
        

    



