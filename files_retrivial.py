import os
import shutil

from dila_path import *

def capp_retrivial(dila_path: str = dila_path):

    path_files = os.path.join(dila_path, 'files')
    path_extract = os.path.join(dila_path, 'extract')

    if not os.path.exists(path_files):
        os.mkdir(os.path.join(dila_path, 'files'))

    nb_retrivied_before = len(os.listdir(path_files))

    filelist = []

    for root, dirs, files in os.walk(path_extract):
        if files != []:
            for file in files:
                filelist.append(file)
                if file not in os.listdir(path_files):
                    shutil.copy2(os.path.join(root, file), path_files)
                else:
                    continue

    for file in os.listdir(path_files):
        if file.find('.xml') == -1:
            os.remove(os.path.join(path_files,file))

    shutil.rmtree(path_extract, ignore_errors=True)

    nb_files = len(filelist)
    nb_retrivied_after = len(os.listdir(path_files))

    nb_duplicates = (nb_files + nb_retrivied_before) - nb_retrivied_after
    nb_retrivied = nb_files - nb_duplicates

    print(f'Files: {nb_files}\nFiles retrivied: {nb_files_retrivied} ({nb_duplicates} duplicates ignored)')

def freemium_capp_retrivial(freemium_path: str = freemium_path, dila_path: str = dila_path):

    path_freemium_extract = os.path.join(dila_path, 'freemium_extract')
    path_files = os.path.join(dila_path, 'files')

    file_name = '20180315-170000'

    if not os.path.exists(os.path.join(path_freemium_extract, file_name)):
        os.mkdir(os.path.join(dila_path, 'freemium_extract'))
        shutil.move(os.path.join(freemium_path), path_freemium_extract)

    nb_retrivied_before = len(os.listdir(path_files))

    filelist = []

    for root, dirs, files in os.walk(path_freemium_extract):
        if files != []:
            for file in files:
                filelist.append(file)
                if file not in os.listdir(path_files):
                    shutil.copy2(os.path.join(root, file), path_files)
                else:
                    continue

    shutil.rmtree(path_freemium_extract, ignore_errors=True)

    nb_files = len(filelist)
    nb_retrivied_after = len(os.listdir(path_files))

    nb_duplicates = (nb_files + nb_retrivied_before) - nb_retrivied_after
    nb_retrivied = nb_files - nb_duplicates

    print(f'Files: {nb_files}\nFiles retrivied: {nb_files_retrivied} ({nb_duplicates} duplicates ignored)')
