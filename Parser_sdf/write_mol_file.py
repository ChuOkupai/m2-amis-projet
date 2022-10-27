def chebi_id_presentation(chebi_id):
  return "CHEBI:"+chebi_id
  
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

def format_filename(name):
    # Retire les caractères spéciaux
    name = name.replace('[','(')
    name = name.replace(']',')')
    name = name.replace('>','-')
    name = name.replace('<','')
    name = name.replace(' ','_')
    name = name.replace('\'','_')
    name = name.replace('\"','_')
    name = name.replace('*','_')
    name = name.replace('?','')
    name = name.replace('\\','')
    name = name.replace('/','')
    name = name[:30]
    return name