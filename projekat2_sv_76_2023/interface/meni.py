import sys
import algorithms.algorithm as algorithm
from utils import save_files, load_files
from prettytable import PrettyTable, ALL
def meni(graph):
    while True:
        print("#"*20)
        print("1. Find in page")
        print("2. Exit")
        
        inp = input(">>> ")
        
        if not inp.isdigit():
            continue 
        
        if int(inp)==1:
            user_text_input(graph)
        
        elif int(inp) == 2:
            save_files(graph)
            break

        else: continue


def user_text_input(graph):
    while True:
        print("#"*20)
        print('Input your text in "" to use it as phrase')#print('Input your text in "" to use it as a one expression')
        print('Input your text without anything added to use it as multiple expressions')
        print('Input <# to go back')

        text = input('>>> ')
        if text == '<#':
            return
        
        text = autocomplete(text, algorithm.autocomplete(graph, text))
        print(text)
        results = algorithm.get_results(graph, text)
        
        paginization(results)

def autocomplete(input_text, suggestions):
    text = input_text

    arr = text.split(' ')
    text_arr = []

    for i in arr:
        if not( i=='' or i==' ' or i=='\\n') and not(i=='AND' or i=='OR' or i=='NOT'):
            text_arr.append(i)
  
    for i in range(len(text_arr)):
        if text_arr[i][len(text_arr[i])-1]=='*' and text_arr[i][:len(text_arr[i])-1] in suggestions:
            text_arr[i]  = change_word(text_arr[i], suggestions[text_arr[i][:len(text_arr[i])-1]])

    return ' '.join(text_arr)

def change_word(original_word, suggestions):
    while True:
        print(f'Do you want to replace word {original_word} with any of the following')
        i=1
        for word in suggestions:
            print(f'{i}. {word}')
            i+=1

        br = input('>>> ')
        if not br.isdigit(): continue
        if int(br)<=0 and int(br)>i: continue

        original_word = suggestions[int(br)-1]
        return original_word

    pass

def paginization(results):
    total_num=0
    num = 0
    paginized_arr=[]
    for result in results:
        if num<10:
            total_num+=1
            num+=1
            paginized_arr.append(result)

        if total_num == len(results):
            print_results(paginized_arr)
            break
        if num>=10:
            print_results(paginized_arr)

            print()
            print('Da li ocete da predjete na sledecu stranicu? (Y/N)')
            inp = input('>>> ')

            if inp.lower()=='y':
                num=0
                paginized_arr = []
            else:
                break
    

def print_results(results):
    table = PrettyTable()
    
    table.field_names = ['Number of Page', 'Number of Result', 'Content']
    table.hrules = ALL

    for res in results:
        table.add_row([res['page_number'],res['num_result'],res['content']])

    print(table)