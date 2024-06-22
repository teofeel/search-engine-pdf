import utils
import interface.meni as meni
from entities.Trie import Trie

if __name__ == '__main__':
    results = utils.pdf_to_hashmap()
    
    

    snippets = results[7]['trie_structure'].search_and_extract_snippets(results[7]['content'], 'undergraduate')
    print(snippets)

    meni.meni(results)
    
