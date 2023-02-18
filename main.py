from datetime import datetime
now = datetime.now()

desde = now
hasta = 23

desde_mes = desde.month
desde_dia = desde.day
desde_hora = 0

import pandas as pd

df_cot = pd.read_csv('tabla-cot-resumen.csv')

df_cot["mesDia"] = df_cot.Mes.astype(str)+'.'+df_cot.Dia.astype(str)
df_cot.loc[df_cot.Dia.astype(str).str.len() == 1,'mesDia'] = df_cot.Mes.astype(str)+'.0'+df_cot.Dia.astype(str)

df_cot = df_cot[(df_cot.Descripcion == 'XYZ') & (df_cot.mesDia.astype(float) > 2.06)] 

df_stat = df_cot.copy()

df_cot = df_cot[(df_cot.Mes >= desde_mes) & (df_cot.Dia >= desde_dia) ]

maxMesCot = df_cot.Mes.max()

df_cot.loc[df_cot.Hora.astype(str).str.len() == 1,'Hora'] = '0'+df_cot.Hora.astype(str)


df_cot['Orden'] = df_cot["Dia"].astype(str)+'.'+df_cot["Hora"].astype(str)
maxOrden = df_cot.Orden.astype(float).max()

data = []
for dia in range(df_cot.Dia.min(),df_cot.Dia.max()+1):
    for hora in range(24):
        if len(str(hora)) == 1:
            data.append(str(dia)+'.0'+str(hora))
        if len(str(hora)) == 2:       
            data.append(str(dia)+'.'+str(hora))       
d = pd.Series(data)
d.name = 'Orden'
df_cot = pd.merge(df_cot,d,left_on="Orden",right_on="Orden",how='right')
df_cot.fillna(0,inplace=True)

df_cot.Dia = df_cot.Orden.str.extract('(..?)\.')
df_cot.Hora = df_cot.Orden.str.extract('\.(..)')
df_cot.Anio = 2023
df_cot.Descripcion = 'XYZ'

arr = df_cot[df_cot.Mes == 0].Dia.unique().copy()

for MesesCero in arr:
    if(desde_dia == int(MesesCero)):
        df_cot.loc[df_cot.Dia == MesesCero, 'Mes'] = desde.month
    if((desde_dia < int(MesesCero)) & (int(MesesCero)>2) & (int(MesesCero)<32)):    
        df_cot.loc[df_cot.Dia == MesesCero, 'Mes'] = desde.month
    if((desde_dia > int(MesesCero)) & (int(MesesCero)<3)):   
        df_cot.loc[df_cot.Dia == MesesCero, 'Mes'] = desde.month+1

df_cot=df_cot[(df_cot.Orden.astype(float) <= maxOrden) & (df_cot.Mes.astype(int) <= maxMesCot)]

df_cot["NombreDia"] = df_cot.Anio.astype(str)+'-'+df_cot.Mes.astype(int).astype(str)+'-'+df_cot.Dia.astype(str) 
df_cot["NombreDia"]=pd.to_datetime(df_cot["NombreDia"]).dt.day_name()
df_cot.loc[df_cot["NombreDia"]=='Monday','NombreDia'] = 'Lun'
df_cot.loc[df_cot["NombreDia"]=='Tuesday','NombreDia'] = 'Mar'
df_cot.loc[df_cot["NombreDia"]=='Wednesday','NombreDia'] = 'Mie'
df_cot.loc[df_cot["NombreDia"]=='Thursday','NombreDia'] = 'Jue'
df_cot.loc[df_cot["NombreDia"]=='Friday','NombreDia'] = 'Vie'
df_cot.loc[df_cot["NombreDia"]=='Saturday','NombreDia'] = 'Sab'
df_cot.loc[df_cot["NombreDia"]=='Sunday','NombreDia'] = 'Dom'

df_cot['DiaHora'] = df_cot.NombreDia+'/'+df_cot.Dia.astype(str)+' ('+df_cot.Hora.astype(str)+' hrs)'

df_stat["NombreDia"] = df_stat.Anio.astype(str)+'-'+df_stat.Mes.astype(int).astype(str)+'-'+df_stat.Dia.astype(str) 
df_stat["NombreDia"]=pd.to_datetime(df_stat["NombreDia"]).dt.day_name()
df_stat.loc[df_stat["NombreDia"]=='Monday','NombreDia'] = 'Lun'
df_stat.loc[df_stat["NombreDia"]=='Tuesday','NombreDia'] = 'Mar'
df_stat.loc[df_stat["NombreDia"]=='Wednesday','NombreDia'] = 'Mie'
df_stat.loc[df_stat["NombreDia"]=='Thursday','NombreDia'] = 'Jue'
df_stat.loc[df_stat["NombreDia"]=='Friday','NombreDia'] = 'Vie'
df_stat.loc[df_stat["NombreDia"]=='Saturday','NombreDia'] = 'Sab'
df_stat.loc[df_stat["NombreDia"]=='Sunday','NombreDia'] = 'Dom'

df_stat = df_stat[['NombreDia','Hora','mesDia','CotizacionesUnicas']]

#### --> linea siguiente inserta obervaciones que falten (porque son cero)

df_stat.loc[len(df_stat.index)] = ['Vie', 4, 2.17,0] 

import scipy.stats
  
n=round(len(df_stat[df_stat["NombreDia"] == df_cot.NombreDia[0]])/24)

alpha = 0.1
nivel_de_confianza=(1-alpha/2)*100
t_stu = scipy.stats.t.ppf(q=nivel_de_confianza/100,df=n)



g=df_stat.groupby(["NombreDia","Hora"]).agg(['mean','std'])

g.reset_index(inplace=True)
g.loc[:,('CotizacionesUnicas','mean')].fillna(0,inplace=True)
g.loc[:,('CotizacionesUnicas','std')].fillna(0,inplace=True)

g["li"] = g.loc[:,('CotizacionesUnicas','mean')]-(1.886*g.loc[:,('CotizacionesUnicas','std')])/(2**0.5)
g["ls"] = g.loc[:,('CotizacionesUnicas','mean')]+(1.886*g.loc[:,('CotizacionesUnicas','std')])/(2**0.5)

g["li"] = g["li"].astype(int)
g["ls"] = g["ls"].astype(int)

g=g[g["NombreDia"] == df_cot.NombreDia[0]]

g.loc[g.li <0,'li'] = 0

nivel_confianza = '80'
n = '2'

# pip install Jinja2
from jinja2 import Environment, FileSystemLoader
import os
 
root = os.path.dirname(os.path.abspath('templates'))
print(root)
print('#'*30)
templates_dir = os.path.join(root+'\\Jinja2', 'templates')
print(templates_dir)
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('template.html')
 
 
filename = os.path.join(root+'\\Jinja2', 'html', 'index.html')
with open(filename, 'w') as fh:
    fh.write(template.render(
        li = g.li.to_list(),
        ls = g.ls.to_list(),
        prom = g.loc[:,('CotizacionesUnicas','mean')].to_list(),
        orden = ['00:00', '01:00', '02:00', '03:00', '04:00','05:00', '06:00', '07:00', '08:00', '09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00'],
        data = df_cot['CotizacionesUnicas'].to_list(),
        labeltext1 = f"'Cotizaciones {df_cot.NombreDia[0]} {df_cot.Dia[0]}/{desde_mes}/{desde.year}'",
        labeltext2 = "'Limite Superior'",
        labeltext3 = "'Limite Inferior'",
        labeltext4 = "'Valor medio'",
        h1_title_text = f"Proyecci&oacute;n Cotizaciones - XYZ - [ confianza = {int(nivel_de_confianza)}% ; n = {n} ]"
    ))