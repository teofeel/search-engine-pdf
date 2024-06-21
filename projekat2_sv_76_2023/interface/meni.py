import sys
import algorithms.algorithm as algorithm

def meni(files):
    while True:
        print("#"*20)
        print("1. Find in page")
        print("2. Exit")
        
        inp = input(">>> ")
        
        if not inp.isdigit():
            continue 
        
        if int(inp)==1:
            user_text_input(files)
        
        elif int(inp) == 2:
            break

        else: continue


def user_text_input(files):
    while True:
        print("#"*20)
        print('Input your text in "" to use it as a one expression')
        print('Input your text without anything added to use it as multiple expressions')
        print('Input <# to go back')

        text = input('>>> ')
        if text == '<#':
            return
        
        algorithm.get_results(files, text)

        
        