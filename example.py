import pandas as pd

from caracteristicas.buro import FeaturesBuro
from controladores.buro import ControladorBuro
from buro.client import configura_cuentas_buro, configura_consultas_buro, configura_score_buro

df_cuentas = pd.read_csv('data/cuentas.csv')
df_consultas = pd.read_csv('data/consultas.csv')
df_score = pd.read_csv('data/score.csv')

folios = [2346338, 2377725]

feature_names = [
    'sum_d_pmt_to_dlq_bal_tu_all_op_acc',
    'max_d_pmt_to_dlq_bal_au_op_acc',
    'avg_d_pmt_to_dlq_bal_tu_all_op_acc',
    'pct_num_iq_06m_r',
    'num_iq_12m_r',
    'val_score_prod',
]

features = FeaturesBuro(feature_names)
controladores = ControladorBuro(features)

df_cuentas_folio = df_cuentas.loc[df_cuentas['cufFolio'] == folios[0]]
df_consultas_folio = df_consultas.loc[df_consultas['cofFolio'] == folios[0]]
df_score_folio = df_score.loc[df_score['scfFolio'] == folios[0]]

lista_cuentas_buro = configura_cuentas_buro(df_cuentas_folio.to_dict(orient='records'))
lista_consultas_buro = configura_consultas_buro(df_consultas_folio.to_dict(orient='records'))
lista_score_buro = configura_score_buro(df_score_folio.to_dict(orient='records'))

variables_cuentas = controladores.controlador_cuentas(lista_cuentas_buro)
variables_consultas = controladores.controlador_consultas(lista_consultas_buro)
variables_score = controladores.controlador_score(lista_score_buro)

print('finish!')