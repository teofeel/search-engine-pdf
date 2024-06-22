import utils
import interface.meni as meni

if __name__ == '__main__':
    results = utils.pdf_to_hashmap()

    meni.meni(results)
    
