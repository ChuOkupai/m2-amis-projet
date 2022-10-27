# Python[3.10]
# Main, exécution du nettoyage du fichier ChEBI_lite.sdf sous format txt
import sys, os
from os.path import join
projet = os.getcwd()
path = os.path.dirname(projet)
sys.path.append(join(projet, "Parser_sdf"))
from Parser_sdf import parser_first

def main():
    # Ouvrir le fichier en paramètre
    if len(sys.argv) == 2:
        parser_first.interface(sys.argv[1])
    else :
        print("Need one argument")
    # 
    
if __name__=="__main__":
    main()