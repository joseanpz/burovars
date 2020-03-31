import pandas as pd

from features import FeaturesBuro
from controlador import VariablesBuro
from buro.client import configura_cuentas_buro

feature_names = [
    'num_d_pmt_to_dlq_bal_tu_all_op_acc',
    'max_d_pmt_to_dlq_bal_au_op_acc'
]

features = FeaturesBuro(feature_names)
variables = VariablesBuro(features)

folios = [2346338, 2377725]

df = pd.read_csv('data/cuentas.csv')

df_folio = df.loc[df['cufFolio'] == folios[0]]

cuentas_folio = df_folio.to_dict(orient='records')

lista_cuentas_buro = configura_cuentas_buro(cuentas_folio)

variables_cuentas = variables.controlador_cuentas(lista_cuentas_buro)

print('finish!')