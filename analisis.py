import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

def diagramas(datos1,datos2,xlabel="",ylabel="",title="",type_g="lineas"):
    """
    Auxiliar para imprimir graficas de manera facil
    """
    ax=plt.axes()
    if type_g =="lineas":
        plt.plot(datos1,datos2)
    elif type_g == "barras":
        plt.bar(datos1, datos2)
    ax.set_title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

def comparacion_aumento_filosofos():
    """ 
    Compara el aumento de filosofos
    """
    datos=pd.read_csv('comparador.csv', sep=',', header=0).sort_values("num_filosofos")
    print(datos)
    title = 'Grafica de lineas que muesta el tiempo de ejecución en segundos del programa'
    diagramas(datos["num_filosofos"],datos["tiempo"],"filosofos","segundos",title)
    title = 'Grafica de lineas que muestra el total de comidas con diferentes cantidades de filosofos'
    diagramas(datos["num_filosofos"],datos["num_comidas"],"filosofos","numero de comidas",title)
    title = 'Grafica de lineas que muestra el total de pensamientos con diferentes cantidades de filosofos'
    diagramas(datos["num_filosofos"],datos["num_pensamientos"],"filosofos","numero de pensamiento",title)

def comparacion_disminucion_tenedores():
    """ 
    Compara la disminucion de tenedores
    """
    datos=pd.read_csv('comparador.csv', sep=',', header=0).sort_values("num_tenedores")
    print(datos)
    title = 'Grafica de lineas que muesta el tiempo de ejecución en segundos del programa'
    diagramas(datos["num_tenedores"],datos["tiempo"],"tenedores","segundos",title)

def comparacion_dt_af():
    """ 
    Compara la disminucion de tenedores y aumento de filosofos
    """
    datos=pd.read_csv('comparador.csv', sep=',', header=0).sort_values("num_tenedores")
    print(datos)
    title = 'Grafica de lineas que muesta el tiempo de ejecución en segundos del programa'
    diagramas(datos["num_tenedores"],datos["tiempo"],"tenedores","segundos",title)
    datos=datos.sort_values("num_filosofos")
    title = 'Grafica de lineas que muesta el tiempo de ejecución en segundos del programa'
    diagramas(datos["num_filosofos"],datos["tiempo"],"filosofos","segundos",title)

comparacion_dt_af() 
#comparacion_disminucion_tenedores()
#comparacion_aumento_filosofos()
