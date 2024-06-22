import utils
import interface.meni as meni

if __name__ == '__main__':
    graph = utils.pdf_to_graph()
    
    meni.meni(graph)
    
