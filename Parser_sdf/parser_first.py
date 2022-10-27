from os import mkdir, getcwd
from os.path import join, isfile, isdir
from Parser_sdf import write_mol_file as WMF

def search_balise(fl, text, first_index, limit):
  i = first_index
  while text not in fl[i] and i<limit:
    i += 1
  return i

# lecture des nombre de sommets et de liaisons
# gestion des cas d'erreur par le remplacement par None (comportement adapté par la suite)
def read_numbers(f, numbers_balise):
  tab_numbers = f[numbers_balise].split()
  nb_nodes = None
  nb_edges = None
  if len(tab_numbers) >= 2 :
    if tab_numbers[0].isnumeric():
      nb_nodes = int(tab_numbers[0])
      if nb_nodes <=1 :
        nb_nodes = None
    if tab_numbers[1].isnumeric():
      nb_edges = int(tab_numbers[1])
    if nb_nodes != None and nb_edges != None :
      if nb_edges < nb_nodes-1:
        nb_edges = None
  return nb_nodes, nb_edges

def read_nodes(f, nodes_balise, nb_nodes):
  tab_nodes = []
  if nb_nodes != None:
    for i in range(nodes_balise, nodes_balise+nb_nodes):
      line = f[i].split()
      #print(line)
      if len(line)>=13:
        tab_nodes.append(line[3])
      else :
        print("error 1", line)
        break
  else :
    i = nodes_balise
    line = f[i].split()
    while len(line)>=13:
      tab_nodes.append(line[3])
      i += 1
      line = f[i].split()
  return tab_nodes

def read_edges(f, edges_balise, nb_edges):
  tab_edges = []
  if nb_edges != None:
    for i in range(edges_balise, edges_balise+nb_edges):
      line = f[i].split()
      if len(line)>=6:
        tab_edges.append(line[0:3])
      else :
        print("error 2", line)
        break
  else :
    i = edges_balise
    line = f[i].split()
    while len(line)>=6:
      tab_edges.append(line[0:3])
      i += 1
      line = f[i].split()
  return tab_edges

def write_file(name, chebi_id, nb_nodes, tab_nodes, nb_edges, tab_edges):
  if not isdir("files"):
    mkdir("files")
  if name!=None and chebi_id!=None and len(tab_nodes)!=0 and len(tab_edges)!=0:
    f_out = open(join("files", str(chebi_id)+'_'+WMF.format_filename(name)+".txt"), "w")
    f_out.write(WMF.chebi_id_presentation(chebi_id)+'\n') # IDs
    f_out.write(name+'\n') # Name
    f_out.write(str(nb_nodes)+'\n') # nombre de sommet
    f_out.write(WMF.liste_presentation(tab_nodes,' ')+'\n') # liste des sommets
    f_out.write(str(nb_edges)+'\n') # nombre de liaisons
    f_out.write(WMF.matrice_c_presentation(tab_edges,' ')) # matrice creuse des adjacences
    f_out.close()
  else :
    print("Erreur Manque de données", name, 'CHEBI:'+str(chebi_id), str(len(tab_nodes))+' atomes', str(len(tab_edges))+' liaisons')

def interface(name_file):
  # ouvre le fichier
  if not isfile(name_file):
    print("Erreur", "Lecture fichier impossible :", name_file)
    print("Localisation", getcwd())
  else:
    f = open(name_file, "r").readlines()
    
    #number of molecule parsed
    number_extracted = 0
    begin_balise = -1
    next_balise = 0
    i = 0
    
    while next_balise < len(f) and number_extracted < 1000:
      # repère de début de la prochaine molécule
      next_balise = search_balise(f, "$$$$", begin_balise+1, len(f))
      if next_balise == len(f) :
        print("Suivant à la fin")
      #print(begin_balise, next_balise)
      
      # informations globales
      numbers_balise = begin_balise+4
      nb_nodes, nb_edges = read_numbers(f, numbers_balise)
      
      # sommets
      nodes_balise = numbers_balise+1
      if nb_nodes!= None and nodes_balise+nb_nodes>next_balise-10:
        nb_nodes = None
        tab_nodes = read_nodes(f, nodes_balise, nb_nodes)
      else :
        tab_nodes = read_nodes(f, nodes_balise, nb_nodes)
      nb_nodes = len(tab_nodes)
      
      # liaisons simples et doubles
      edges_balise = nodes_balise+nb_nodes
      if nb_edges!= None and edges_balise+nb_edges>=next_balise-10:
        nb_edges = None
        tab_edges = read_edges(f, edges_balise, nb_edges)
      else :
        tab_edges = read_edges(f, edges_balise, nb_edges)
      nb_edges = len(tab_edges)
      
      i = edges_balise+nb_edges
      # recherche Chebi ID
      chebi_id = None
      chebi_balise = search_balise(f, "> <ChEBI ID>", i, next_balise)
      if chebi_balise < next_balise:
        line = f[chebi_balise+1].split()
        line = line[0].split(":")
        chebi_id = line[1]
      else :
        print("error 3", begin_balise, f[i])
        break
      # recherche Chebi Name
      name = None
      name_balise = search_balise(f, "> <ChEBI Name>", i, next_balise)
      if name_balise < next_balise:
        name = f[name_balise+1][:-1]
      else :
        print("error 4", begin_balise, f[i])
        break
          
      # écrire le fichier de sortie
      write_file(name, chebi_id, nb_nodes, tab_nodes, nb_edges, tab_edges)
      
      # passer au suivant (etcs)
      begin_balise = next_balise
      number_extracted += 1