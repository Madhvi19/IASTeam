import os
import sys
import zipfile



def zipit(folders, zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                        os.path.join(dirpath,filename),
                        os.path.relpath(os.path.join(dirpath,filename),
                        os.path.join(folders[0],'../..')))
                        
    zip_file.close()

cwd = os.getcwd()
path_parent = os.path.dirname(os.getcwd())

#print(path_parent)



folders = [path_parent+"/configFiles",path_parent+"/src"]

zipit(folders,cwd+"/Application_zip.zip")

