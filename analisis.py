import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
import csv

# datos=pd.read_csv('comidas.csv', sep=',', header=0)
# otro = datos.copy()

def diagrama_lineas(datos1,datos2,xlabel="",ylabel="",title=""):
    ax=plt.axes()
    plt.plot(datos1,datos2)
    ax.set_title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()


def comparacion_aumento_filosofos():
    datos=pd.read_csv('comparador.csv', sep=',', header=0)
    if len(datos["num_filosofos"])==len(datos["num_tenedores"]):
        title = 'Grafica de lineas que muesta el tiempo de ejecución en segundos del programa'
        diagrama_lineas(datos["num_filosofos"],datos["tiempo"],"filosofos","segundos",title)
        title = 'Grafica de lineas que muestra el total de comidas con diferentes cantidades de filosofos'
        diagrama_lineas(datos["num_filosofos"],datos["num_comidas"],"filosofos","numero de comidas",title)
        title = 'Grafica de lineas que muestra el total de pensamientos con diferentes cantidades de filosofos'
        diagrama_lineas(datos["num_filosofos"],datos["num_pensamientos"],"filosofos","numero de pensamiento",title)
        
comparacion_aumento_filosofos()

#1) EXPLORACION DE DATOS(ESTADISTICAS DESCRIPTIVAS) 
#ANALISIS DESCRIPTIVO DE LA VARIABLE tiempo(tiempo)
# x=datos['tiempo'].describe()
# print("")
# print("Estadisticas descriptivas para la variable tiempo:")
# print(x)
# print("")
# y=datos['tiempo'].value_counts()
# print("Cantidad de elementos por columnas:")
# print(y)
# #Moda
# print("")
# modaE=datos['tiempo'].mode()
# print("Moda")
# print("Tiempo que mas se repite:")
# print(modaE)
# #Mediana
# print("")
# medianaE=datos['tiempo'].median()
# print("Mediana:")
# print(medianaE)
# #representacion grafica para la variable tiempo con histograma
# ax=plt.axes()
# tiempo=plt.hist(datos['tiempo'],20,color="mediumvioletred",ec="black",lw=2)
# ax.set_title('HISTOGRAMA PARA LA VARIABLE "tiempo"')
# plt.ylabel("Frecuencia")
# plt.xlabel("tiempo")
# plt.show()

# def comidas():
#     comidas=[]
#     with open('comparador.csv', mode='r') as comp:
#         reader = csv.DictReader(comp)
#         for row in reader:   
#             comidas.append(row)
#     info = []     