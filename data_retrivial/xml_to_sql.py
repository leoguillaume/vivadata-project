import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from glob import glob
import sqlalchemy as db

def cleaning(data):

    if not data:
        data = 'null'
    else:
        data = ['null' if x == None else x for x in data]
        data = ' '.join(data)
        
    return data

def data(path_in: str, database_out: str):

    DATABASE_URL = 'sqlite:///' + database_out
    engine = db.create_engine(DATABASE_URL, echo = False)
    connection = engine.connect()

    files_list = glob(path_in + '*.xml')
    columns = ['ID', 'NUMERO_AFFAIRE', 'DATE_DEC', 'NATURE', 'SIEGE_APPEL', 'CONTENU', 'SCT']

    for file in files_list:

        tree = ET.parse(file)
        root = tree.getroot()

        row = {}

        for i in columns:

            if i == 'CONTENU':
                data = [[text for text in element.itertext()] for element in root.iter(i)]
                row[i] = cleaning(data[0])
            else:
                data = [element.text for element in root.iter(i)]
                row[i] = cleaning(data)

        pd.DataFrame.from_dict([row]).to_sql('Data', con = engine, if_exists = 'append', index = True)
