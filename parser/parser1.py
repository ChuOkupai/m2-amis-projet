import sys, os
doc = os.getcwd()
path = os.path.dirname(doc)
from os import mkdir
from os.path import join, isfile, isdir

def search_balise(fl, text, first_index, limit):
  i = first_index
  while text not in fl[i] and i<limit:
    i += 1
  return i

def chebi_id_presentation(chebi_ids):
  s = "CHEBI:"+chebi_ids[0]
  if len(chebi_ids)>1:
    s+= ","+chebi_ids[1]
  return s

def liste_presentation(tab, sep):
  s = ""
  for elem in tab:
    s+= str(elem) + sep
  return s

def matrice_c_presentation(tab, sep):
  s = ""
  for line in tab:
    for elem in line:
      s+= str(elem) + sep
    s+= '\n'
  return s

# ouvre le fichier
if isfile("ChEBI_complete.txt"):
  f = open("ChEBI_complete.txt", "r").readlines()
  
  #number of molecule parsed
  number_extracted = 0
  next_balise = 0
  i = 693393
      
  while next_balise < len(f):
    # repère de début d'une description de molécule
    marvin_balise = search_balise(f, "Marvin", i, len(f))
    if marvin_balise==len(f):
      print("Fichier fini")
      break
    
    next_balise = search_balise(f, "Marvin", marvin_balise+1, len(f))
    if next_balise == len(f) :
      print("suivant à la fin")
      break
    print(marvin_balise, next_balise)
    
    # informations globales
    numbers_line = marvin_balise+2
    tab_numbers = f[numbers_line].split()
    nb_nodes = int(tab_numbers[0])
    nb_edges = int(tab_numbers[1])
    
    # sommets
    tab_nodes = []
    nodes_balise = numbers_line+1
    for i in range(nodes_balise, nodes_balise+nb_nodes):
      line = f[i].split()
      #print(line)
      if len(line)>=4:
        tab_nodes.append(line[3])
      else :
        print("error 1", line)
        break
      
    # liaisons simples et doubles
    tab_edges = []
    edges_balise = nodes_balise+nb_nodes
    for i in range(edges_balise, edges_balise+nb_edges):
      line = f[i].split()
      if len(line)>=3:
        tab_edges.append(line[0:3])
      else :
        print("error 2", line)
        break
    
    i = edges_balise+nb_edges
    # recherche Chebi ID
    chebi_ids = []
    chebi_balise = search_balise(f, "> <ChEBI ID>", i, next_balise)
    if chebi_balise < next_balise:
      line = f[chebi_balise+1].split()
      line = line[0].split(":")
      chebi_ids.append(line[1])
      # recherche Chebi secondary ID
      second_balise = search_balise(f, "> <Secondary ChEBI ID>", i, next_balise)
      if chebi_balise < next_balise:
        line = f[second_balise+1].split()
        line = line[0].split(":")
        chebi_ids.append(line[1])
      else :
        print("error 3", f[i])
        break
    else :
      print("error 4", f[i])
      break
    # recherche Chebi Name
    name_balise = search_balise(f, "> <ChEBI Name>", i, next_balise)
    name = None
    if name_balise < next_balise:
      name = f[name_balise+1][:-1]
    else :
      print("error 5", f[i])
      break
        
    # écrire le fichier de sortie
    if not isdir("data"):
      mkdir("data")
    if name!=None and len(chebi_ids)!=0 and len(tab_nodes)!=0:
      f_out = open(join("data", str(chebi_ids[0])+'_'+name+".txt"), "w")
      f_out.write(chebi_id_presentation(chebi_ids)+'\n') # IDs
      f_out.write(name+'\n') # Name
      f_out.write(str(nb_nodes)+'\n') # nombre de sommet
      f_out.write(liste_presentation(tab_nodes,' ')+'\n') # liste des sommets
      f_out.write(str(nb_edges)+'\n') # nombre de liaisons
      f_out.write(matrice_c_presentation(tab_edges,' ')) # matrice creuse des adjacences
      f_out.close()
    else :
      print("rien à imprimer")
    # passer au suivant (etcs)
    number_extracted += 1