import re

def search_files(files, text, results):
    num_of_result = 0

    for file in files:
        if boyer_moore(files[file]['content'], text) == -1: continue

        num_of_result = extract_result_from_file(files[file], text, results, num_of_result)


def extract_result_from_file(file, text, results, num_of_result):
    color_start = "\033[31m"
    color_end = "\033[0m"

    pattern = re.compile(re.escape(text), re.IGNORECASE)
    match = pattern.search(file['content'])
    
    if match:
        start = max(match.start()-5, 0)
        end = min(match.end()+10, len(file['content']))
        
        snippet = file['content'][start:end]
        colored_content = pattern.sub(f"{color_start}{text}{color_end}", snippet)
        
        num_of_result+=1
        print(file)
        results[num_of_result] = {
            'num_result':num_of_result,
            'page_number':file['page_number'],
            'content': colored_content
        }
    
    return num_of_result


def get_results(files, text):
    results = {}
    search_files(files,text,results)


    for res in results:
        print('#'*10)
        print(f"Number of result: {results[res]['num_result']}\nNumber of page: {results[res]['page_number']}\nContent: {results[res]['content']}")
        pass

def boyer_moore(T, P):
    n, m = len(T), len(P)
    num = 0
    if m == 0:
        return 0
    last = {}

    for k in range(m):
        last[ P[k] ] = k

    i = m-1 
    k = m-1 
    while i < n:
        if T[i] == P[k]:
            if k == 0:
                return i
            else:
                i -= 1
                k -= 1
        else:
            j = last.get(T[i], -1)
            i += m - min(k, j + 1)
            k = m - 1

    return -1

if __name__ == '__main__':
    print(boyer_moore('ovo je tekst za pretragu', 'ovo'))
    pass