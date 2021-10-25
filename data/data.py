import json
import os

import pandas as pd
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer

load_dotenv(override=True)

def get_dataframe():
    df = pd.read_csv('data/admitidos.csv')
    return df

def generate_dropdowns_data():
    df = get_dataframe()

    s_periodos = df['cod_periodo'].drop_duplicates().sort_values()
    s_periodos.index = [
        str(periodo)[:-1]+'-I' if str(periodo)[-1]=='1'
        else
        str(periodo)[:-1]+'-II'
        for periodo in s_periodos
    ]

    s_territorial = df['direccion_territorial'].drop_duplicates().sort_values()
    s_territorial.index = s_territorial

    s_cetap = df['cetap'].drop_duplicates().sort_values()
    s_cetap.index = s_cetap

    s_modalidad = df['modalidad'].drop_duplicates().sort_values()
    s_modalidad.index = s_modalidad

    s_metodologia = df['metodologia'].drop_duplicates().sort_values()
    s_metodologia.index = s_metodologia

    s_programa = df['programa'].drop_duplicates().sort_values()
    s_programa.index = s_programa

    dropdowns_dict = {
        'periodo-dropdown': s_periodos.to_dict(),
        'territorial-dropdown': s_territorial.to_dict(),
        'cetap-dropdown': s_cetap.to_dict(),
        'modalidad-dropdown': s_modalidad.to_dict(),
        'metodologia-dropdown': s_metodologia.to_dict(),
        'programa-dropdown': s_programa.to_dict(),
    }

    with open('data/dropdowns_data.json', 'w') as outfile:
        json.dump(dropdowns_dict, outfile, indent=4)
    return 'Dropdowns Created'

def encrypt_dataframe(dataframe: pd.DataFrame):
    """Encrypt the content to be saved on a .imp file.
    """
    s1 = URLSafeSerializer(os.getenv('IMP_SECRET_KEY'), salt=os.getenv('IMP_SECRET_SALT'))
    df_encr = s1.dumps(dataframe.to_dict())
    return df_encr

def decrypt_dataframe(impcontent):
    """Decrypt the content of a .imp file.
    """
    s1 = URLSafeSerializer(os.getenv('IMP_SECRET_KEY'), salt=os.getenv('IMP_SECRET_SALT'))
    df_decrypt = s1.loads(impcontent)
    return df_decrypt

def get_dropdown_data():
    if not os.path.isfile('data\dropdowns_data.json'):
        generate_dropdowns_data()
    with open('data/dropdowns_data.json', 'r') as file:
        dropdowns_data = json.load(file)
    return dropdowns_data