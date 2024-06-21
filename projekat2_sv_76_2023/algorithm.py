import re

def search_files(files, text):
    bold_start = "\033[31m"
    bold_end = "\033[0m"

    for file in files:
        if boyer_moore(files[file]['content'], text) == -1: continue

        pattern = re.compile(re.escape(text), re.IGNORECASE)
        bolded_content = pattern.sub(f"{bold_start}{text}{bold_end}", files[file]['content'])

        print(bolded_content)
    

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