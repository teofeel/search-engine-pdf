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
        
        results = algorithm.get_results(graph, text)
        paginization(results)

        
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