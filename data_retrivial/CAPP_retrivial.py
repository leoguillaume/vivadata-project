import os
import shutil

def capp_retrievial(path_in: str, path_out: str):

    filelist = []
    duplicates = 0

    #retrivial xml files
    for root, dirs, files in os.walk(path_in):
        if files != []:
            for file in files:
                filelist.append(file)
                if file not in os.listdir(path_out):
                    shutil.copy2(os.path.join(root, file), path_out)
                else:
                    duplicates += 1

    #delete no xml files
    for file in os.listdir(path_out):
        if file.find('.xml') == -1:
            os.remove(os.path.join(path_out,file))

    print(f'Files: {len(filelist)}\nFiles retrivied: {len(filelist) - duplicates} ({duplicates} duplicates ignored)')

def CAPP_freemium_retrievial(path_in: str, path_out: str):

    filelist = []
    duplicates = 0

    #retrivial xml files
    for root, dirs, files in os.walk(path_in):
        if files != []:
            for file in files:
                filelist.append(file)
                if file not in os.listdir(path_out):
                    shutil.copy2(os.path.join(root, file), path_out)
                else:
                    duplicates += 1

    #delete no xml files
    for file in os.listdir(path_out):
        if file.find('.xml') == -1:
            os.remove(os.path.join(path_out,file))

    print(f'Files: {len(filelist)}\nFiles retrivied: {len(filelist) - duplicates} ({duplicates} duplicates ignored)')
