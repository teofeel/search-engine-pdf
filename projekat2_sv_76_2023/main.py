import utils
import interface.meni as meni

import time

if __name__ == '__main__':
    start = time.time()
    graph = utils.load_files()
    print(time.time()-start)

    
    if graph == False:
        print('Loading. Please wait')
        start = time.time()
        graph = utils.pdf_to_graph()
        print(time.time()-start)
    
    meni.meni(graph)
    
