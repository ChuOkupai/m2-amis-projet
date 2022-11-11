import recuperer as p


#Main test du telechargement 
json_file_path='download.json'

recup = p.Recuperer (json_file_path)
recup.get_url_from_user(recup.json_file_path)

j_object=recup.get_info_json()
paths = recup.download_decompress(j_object)

print("PATHS ", paths)