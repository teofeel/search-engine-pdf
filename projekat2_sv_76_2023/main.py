import parse_txt_files
import meni


if __name__ == '__main__':
    in_path = 'Data Structures and Algorithms in Python.pdf'
    out_path = 'Data Structures and Algorithms in Python'
    results = parse_txt_files.read_results_from_files(out_path)
    #parse_txt_files.print_dict(results)

    meni.meni()
    
