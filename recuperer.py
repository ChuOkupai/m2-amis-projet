import io
from urllib import request, response
from zipfile import ZipFile
from io import StringIO
from gzip import GzipFile
import gzip
from io import BytesIO
import requests
import shutil
import json

class Recuperer:
    #initialisation
    def __init__(self, json_file_path):
       #chemin du fichier JSON
       self.json_file_path=json_file_path
    
    #Récupération des liens et des noms du fichier à partir de l'utilisateur

        
    def get_url_from_user(self,json_file_path):
            # input
            print("combien de fichier voulez vous télécharger ?")
            nb_f = int(input())
            for i in range(nb_f):
                boolean = True
                while boolean:
                    print("Introduice web url for ",i," folder:  ")
                    string_url = str(input()) 

                    print("Introduice the ",i," folder name : ")
                    string_name = str(input())
                    string_name.replace(" ","") 
                    string_compressed_file="C:/Users/PC/Desktop/ModuleProjet/recuperer/"+string_name+".sdf.gz"
                    string_final_file="C:/Users/PC/Desktop/ModuleProjet/recuperer/"+string_name+".txt"

                    with open(json_file_path, "r") as jsonFile:
                                data = json.load(jsonFile)
                    if string_url not in data["chebi_url"] and string_compressed_file not in data["path_compressed_file"] and string_final_file not in data["path_final_file"]:
                                data["chebi_url"].append(string_url)
                                data["path_compressed_file"].append(string_compressed_file)
                                data["path_final_file"].append(string_final_file)
                                boolean = False
                    else:
                        print("FOLDER URL AND/OR FOLDER NAME ALREADY EXIST ! PLEASE INTRODUCE A NEW ONES \n")
                                

                    with open(json_file_path, "w") as jsonFile:
                            json.dump(data, jsonFile)



    #Récupération du fichier Json contenant les informations sur le site de la bd, path of the commpressed folder & path of the final folder .txt
    def get_info_json(self):
        try:
            with open(self.json_file_path, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
                return json_object
        except Exception:
             print("Error in json file path : ",self.json_file_path)
             pass
    
    #Telecharger le fichier compresser, le decompresser et stocker dans un fichier txt
    # l'url de téléchargement ainsi que les chemins des fichier compressés et décompressés sont spécifiés dans le fichier json
    def download_decompress(self,json_object):
        chebi_url=json_object.get("chebi_url")
        path_gzip=json_object.get("path_compressed_file")
        path_txt=json_object.get("path_final_file")
        paths_folders=[]
        for i_url,i_folderg,i_foldertxt in zip(chebi_url,path_gzip,path_txt):
            try:
                response = requests.get(i_url)
                # 3. Open the response into a new file called instagram.ico
                try:
                    open(i_folderg, "wb").write(response.content)
                    with gzip.open(i_folderg, 'rb') as f_in:
                        with open(i_foldertxt, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    print("succesful download & decompress of the the link : ",i_url)
                    paths_folders.append(i_foldertxt)
                except Exception:
                    print("Error in decompressing file \n")
                    pass
            except Exception:
                print("Error in the chebi url or couldn't begin the download : ",i_url)
                pass   
        return paths_folders



#Main test du telechargement 
json_file_path='download.json'
init_json = Recuperer (json_file_path)
j_object=init_json.get_info_json()
paths = init_json.download_decompress(j_object)

print("PATHS ", paths)

