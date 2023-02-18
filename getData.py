import pandas
import psycopg2
import credentials

database = credentials.database
user = credentials.user
password = credentials.password
host = credentials.host


conn = psycopg2.connect(database=database, user=user, password=password, host=host)
cursor = conn.cursor()

cursor.execute('SELECT "Anio", "Mes", "Dia", "Hora", "Descripcion",\
       "CotizacionesUnicas", "Cotizaciones" \
               FROM dbo."CotizacionUsuarioResumen"') 



df_cotizaciones = pandas.DataFrame(cursor)
col_names = []
for e in cursor.description:
    col_names.append(e[0])
df_cotizaciones.columns = col_names

df_cotizaciones.to_csv('tabla-cot-resumen.csv',index=False)

import runpy
import os 
root = os.path.dirname(os.path.abspath('main.py'))
root=root+"\\Jinja2\\main.py"

runpy.run_path(path_name=root)
