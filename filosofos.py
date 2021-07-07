
import time
import random
import threading
import csv
import traceback

N = 10                     # Número de filosofos y tenedores
MAXIMUM_NUMBER_MEALS = 2   # Representa el número maximo de comidas por filosofo
# Tiempo de espera entre las comidas y pensamientos 
# --Este en una lista de dos numeros que representa un intervalo que se utilizará para generar una
# --cantidad de segundos aleatorios (en caso de ser iguales el número de segundos es constante)
STANDBY_TIME = [1,1]       
TENEDR = 6                  # Número de tenedores
# Almacena la información de los pensamientos - quien estaba pensando y cuanto duro
pensamientos=[]
# Almacena la información de las comidas - quien estaba comiendo y cuanto duro
comidas=[]
# Almacena la información de cada corrida para ser comparada despues
comparador=[{
    "num_filosofos":N, 
    "num_tenedores":TENEDR,
    "tiempo":"",
    "num_comidas":0,
    "num_pensamientos":0
}]

# Leemos la información del archivo que sirve para comparar las corridas
with open('comparador.csv', mode='r') as comp:
    reader = csv.DictReader(comp)
    for row in reader:   
        comparador.append(row)     

class Filosofo(threading.Thread):
    """ 
    Clase Filosofo, actua como un Thread que necesita dos tenedores adyacentes para comer()
    """
    semaforo = threading.Lock()     # SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = []                     # PARA CONOCER EL ESTADO DE CADA FILOSOFO
    tenedores = []                  # ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count=0
    food=[]
    thoughts=[]

    def __init__(self):
        super().__init__()          # HERENCIA
        self.id=Filosofo.count      # DESIGNA EL ID AL FILOSOFO
        Filosofo.count+=1           # AGREGA UNO A LA CANT DE FILOSOFOS
        Filosofo.estado.append('PENSANDO')                # EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        Filosofo.tenedores.append(threading.Semaphore(0)) # AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        self.food.append(0)
        self.thoughts.append(0)
        print("Filosofo {0} - PENSANDO".format(self.id))

    def __del__(self):
        print("Filosofo {0} - Se para de la mesa".format(self.id))  #NECESARIO PARA SABER CUANDO TERMINA EL THREAD

    def pensar(self):
        inicio = time.time()
        time.sleep(random.randint(STANDBY_TIME[0],STANDBY_TIME[1])) #CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO
        fin = time.time()
        pensamientos.append({"id_filosofo":self.id, 
        "id_pensamiento":self.thoughts[self.id],
        "tiempo":str(fin-inicio)})

    def derecha(self,i):
        return (i-1)%N  # BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N   # BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        inicio = time.time()
        if Filosofo.estado[i] == 'HAMBRIENTO' and (Filosofo.estado[self.izquierda(i)] != 'COMIENDO' and Filosofo.estado[self.derecha(i)] != 'COMIENDO'):
            Filosofo.estado[i]='COMIENDO'
            Filosofo.tenedores[i].release()  # SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO
            fin = time.time()
            self.food[self.id]+=1
            comidas.append({"id_filosofo":self.id, 
            "id_comida":self.food[self.id],
            "tiempo":str(fin-inicio)})

    def tomar(self):
        Filosofo.semaforo.acquire()             # SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        Filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id)                 # VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        Filosofo.semaforo.release()             # SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        Filosofo.tenedores[self.id].acquire()   # SOLO SI PODIA TOMARLOS SE BLOQUEARA CON ESTADO COMIENDO

    def soltar(self):
        Filosofo.semaforo.acquire()             # SEÑALA QUE SOLTARA LOS TENEDORES
        Filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        Filosofo.semaforo.release()             # YA TERMINO DE MANIPULAR TENEDORES

    def comer(self):
        print("Filosofo {} COMIENDO".format(self.id))
        time.sleep(random.randint(STANDBY_TIME[0],STANDBY_TIME[1])) # TIEMPO ARBITRARIO PARA COMER
        print("Filosofo {} TERMINO DE COMER".format(self.id))
        
    def run(self):
        for i in range(MAXIMUM_NUMBER_MEALS):
            self.pensar()   # EL FILOSOFO PIENSA
            self.tomar()    # AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer()    # COME
            self.soltar()   # SUELTA LOS TENEDORES


def main():
    """ 
    Ejecuta los filosofos
    """
    if TENEDR == N:
        lista=[Filosofo() for i in range(N)]    # AGREGA UN FILOSOFO A LA LISTA
        for f in lista:
            f.start()                           # ES EQUIVALENTE A RUN()
        for f in lista:
            f.join()                            # BLOQUEA HASTA QUE TERMINA EL THREAD
    else:
        if TENEDR >= 2:
            m=0
            div=int(N/2)
            lista=[Filosofo() for i in range(N)]    # AGREGA UN FILOSOFO A LA LISTA
            for i in range(0,int(len(lista)/(div))):
                for f in range(m,(div)+m):
                    lista[f].start()                           # ES EQUIVALENTE A RUN()
                for f in range(m,(div)+m):
                    lista[f].join()                            # BLOQUEA HASTA QUE TERMINA EL THREAD
                m+=div
            if len(lista)%2 !=0:
                lista[len(lista)-1].start()
                lista[len(lista)-1].join()


def documentar():
    """ 
    Guardar la información de la corrida.
    """
    with open('comidas.csv', 'w') as c:
        fieldnames_c = ["id_filosofo", "id_comida","tiempo"]
        writer_c = csv.DictWriter(c,fieldnames=fieldnames_c)
        writer_c.writeheader()
        writer_c.writerows(comidas)
    with open('pensamientos.csv', 'w') as p:
        fieldnames_p = ["id_filosofo", "id_pensamiento","tiempo"]
        writer_p = csv.DictWriter(p,fieldnames=fieldnames_p)
        writer_p.writeheader()
        writer_p.writerows(pensamientos)
    with open('comparador.csv', 'w') as compar:
        fieldnames_comp = ["num_filosofos", "num_tenedores","tiempo","num_comidas","num_pensamientos"]
        writer_comp = csv.DictWriter(compar,fieldnames=fieldnames_comp)
        writer_comp.writeheader()
        writer_comp.writerows(comparador)   


if __name__=="__main__":
    try:
        inicio = time.time()
        main()
        fin = time.time()
        comparador[0]["tiempo"]=str(fin-inicio)
        comparador[0]["num_comidas"],comparador[0]["num_pensamientos"] = len(comidas),len(pensamientos)
        # Guardamos la información de la corrida
        documentar()
    except (KeyboardInterrupt, SystemExit):
        fin = time.time()
        comparador[0]["tiempo"]=str(fin-inicio)
        comparador[0]["num_comidas"],comparador[0]["num_pensamientos"] = len(comidas),len(pensamientos)
        # Guardamos la información de la corrida
        documentar()
        print("exit")
    except Exception as e:
        # En caso de que ocurra una excepcion se guarda la información de la Excepción en un archivo llammado error.csv
        error = [str(traceback.format_exc())]
        with open('error.csv', 'w') as er:
            spamwriter = csv.writer(er)
            spamwriter.writerow(error)
    finally:  
        print("los filosofos han termiando")
