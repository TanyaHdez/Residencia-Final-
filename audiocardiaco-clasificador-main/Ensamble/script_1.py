import matplotlib.pyplot as plt # pip install matplotlib
import audiofile  # pip install audiofile  #instalar ffmpeg y media info #para fmpeg agregar la carpeta de los programas descargados al entorno de variables
import numpy as np
import math
from scipy import signal #pip install scipy
from statistics import mode
import statistics
import librosa
import csv
import pandas as pd
import pickle
import sys 
import os
import json

if len(sys.argv) < 2:
    print("Uso: python script_1.py <ruta_archivo>")
    sys.exit(1)

ruta_archivo = sys.argv[1]

if not os.path.exists(ruta_archivo):
    print(f"El archivo no existe: {ruta_archivo}")
    sys.exit(1)

try:
    x, fs = audiofile.read(ruta_archivo)
    # Procesamiento...
    print("Archivo procesado correctamente")  # Opcional: puedes imprimir JSON aquí si se necesita
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    sys.exit(1)
#Read audio file
#x, fs = audiofile.read('../Michigan_Heart_Sounds/04 Apex, Mid Sys Click, Supine, Bell.mp3')

#x,fs = audiofile.read('../the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data/13918_TV.wav')

#Normalization of the signal -1 to 11
a=-1
b=1
normalized_x = x/np.linalg.norm(x)  #normalize 0 to 1
x = (((x - min(x)) / ( max(x) - min(x) ))*(b-a))+a  #normalize -1 to 1


#Create time vector
t = np.arange(0,len(x))/fs
#plt.plot(t,x)
#plt.show()

E0=[]
E=[]

#Shannon Energy
for i in range(len(x)):
    if x[i] != 0:
        E0=-abs(x[i])*math.log10(abs(x[i]))
        E.append(E0)
    else:
        E0=0
        E.append(E0)

#plt.plot(t,E)
#plt.show()

#Mean of the Shannon Energy 
m=sum(E)/len(E)

#Standard Deviation of the Shannon Energy 
standard_deviation = np.std(E) 

#Standardized Shannon Energy
En = (E-m)/standard_deviation
         
#plt.plot(t,En)
#plt.show()

#Normalize to 1 the envelope
En = En/max(En)
#plt.plot(t,x)
#plt.plot(t,En)
#plt.show()



#Filter for the envelope
sos = signal.butter(4, 10, btype='low', analog=False, output='sos', fs=fs)
#sos = signal.cheby2(4, 80, 20, btype='low', analog=False, output='sos', fs=fs)
En_filtered = signal.sosfiltfilt(sos, En)

#En_filtered_smooth = signal.savgol_filter(En_filtered, 200, 3, delta=1000)


#Normalize 0 to 1 the envelope
En_filtered_normalized = (En_filtered-np.min(En_filtered))/(np.max(En_filtered)-np.min(En_filtered))

#plt.plot(t,x)
#plt.plot(t,En_filtered_normalized)
#plt.show()

#Derivate of the envelope
derivate=np.diff(En_filtered_normalized)

#Algoritmo para detectar cambios de pendiente en la envolvente
cambios_de_pendiente = []
min_and_max= []

for i in range(len(derivate)-1):
    v1=derivate[i]
    v2=derivate[i+1]

    if v1<0 and v2>0: #Detecta si es un mínimo
        indice_muestra = i+1
        cambios_de_pendiente.append(indice_muestra)
        min_and_max.append(1) #1-> mínimo; 2-> máximo;

    
    elif v1>0 and v2<0: #Detecta si es un máximo
        indice_muestra = i+1
        cambios_de_pendiente.append(indice_muestra)
        min_and_max.append(2) #1-> mínimo; 2-> máximo;


#fig, ax = plt.subplots()
#ax.plot(t,x)
#ax.plot(t,En_filtered_normalized)
#ax.plot(t[cambios_de_pendiente],En_filtered_normalized[cambios_de_pendiente], 'o')
#plt.show()






min1=[]
max=[]
min2=[]
min1_max_min2_1=[]
min1_max_min2_2=[]
min1_max_min2_3=[]


#Loop to find ones and twos
for i in range(len(min_and_max)-2):
    #Ones and twos searching
    v1=min_and_max[i]  #minimum 1 
    v2=min_and_max[i+1] #max
    v3=min_and_max[i+2] #minimum 2

    if v1==1 and v2==2 and v3==1: #Once we find the ones and twos searching for minimum1, max, minimum2 in samples
        min1=cambios_de_pendiente[i]
        max=cambios_de_pendiente[i+1]
        min2=cambios_de_pendiente[i+2]
        

        min1_max_min2_in_samples=[min1, max, min2]
        min1_max_min2_in_amplitude=[En_filtered_normalized[min1], En_filtered_normalized[max], En_filtered_normalized[min2]]
        min1_max_min2_in_time=[min1/fs, max/fs, min2/fs]


        min1_max_min2_1.append(min1_max_min2_in_samples)
        min1_max_min2_2.append(min1_max_min2_in_amplitude)
        min1_max_min2_3.append(min1_max_min2_in_time)
        

#Getting the total length of a min1_max_min2 array
# The number of rows
rows = len(min1_max_min2_1)

# The number of columns
cols = len(min1_max_min2_1[0])

# The number of total elements
total_length = rows * cols

#Resahpe the min1_max_min2 array
min1_max_min2_1=np.reshape(min1_max_min2_1, total_length)
min1_max_min2_2=np.reshape(min1_max_min2_2, total_length)
min1_max_min2_3=np.reshape(min1_max_min2_3, total_length)






coordinates_min1=[]
coordinates_min1_1=[]
coordinates_max=[]
coordinates_max_1=[]
coordinates_min2=[]
coordinates_min2_1=[]

#Loop to obtain the coordinates of min1 max and min2
for i in range(0,len(min1_max_min2_1),3):
    coordinates_min1=[min1_max_min2_3[i],min1_max_min2_2[i]]
    coordinates_max=[min1_max_min2_3[i+1],min1_max_min2_2[i+1]]
    coordinates_min2=[min1_max_min2_3[i+2],min1_max_min2_2[i+2]]

    coordinates_min1_1.append(coordinates_min1)
    coordinates_max_1.append(coordinates_max)
    coordinates_min2_1.append(coordinates_min2)


#Getting the total length of coordinates of min1 max and min2 array
# The number of rows
rows = len(coordinates_min1_1)

# The number of columns
cols = len(coordinates_min1_1[0])

# The number of total elements
total_length = rows * cols

#Resahpe the coordinates of min1 max and min2 array
coordinates_min1_1=np.reshape(coordinates_min1_1, total_length)
coordinates_max_1=np.reshape(coordinates_max_1, total_length)
coordinates_min2_1=np.reshape(coordinates_min2_1, total_length)



V_Area=[]

#Loop to calculate the area of Heron
for i in range(0,len(coordinates_min1_1),2):
    a=math.sqrt((pow(coordinates_max_1[i]-coordinates_min1_1[i], 2))+(pow(coordinates_max_1[i+1]-coordinates_min1_1[i+1], 2)))
    b=math.sqrt((pow(coordinates_max_1[i]-coordinates_min2_1[i], 2))+(pow(coordinates_max_1[i+1]-coordinates_min2_1[i+1], 2)))
    c=math.sqrt((pow(coordinates_min2_1[i]-coordinates_min1_1[i], 2))+(pow(coordinates_min2_1[i+1]-coordinates_min1_1[i+1], 2)))
    S=(a+b+c)/2

    Area=math.sqrt(S*((S-a)*(S-b)*(S-c)))

    V_Area.append(Area)

M=statistics.mean(V_Area)


contador1=0
contador2=1
contador3=2
vectorfinal_en_muestras=[]
contador=[]


#In this loop, the average of the area vector is taken and it is compared with each value of the V_Area vector
for i in range (len(V_Area)): 

    if i==0  and V_Area[i]>M:
        contador1=0
        contador2=1
        contador3=2
        contador.append(contador1)
        contador.append(contador2)
        contador.append(contador3)

    
    if i>0:
        contador1+=3
        contador2+=3
        contador3+=3

        if i>0 and V_Area[i]>M:
            contador.append(contador1)
            contador.append(contador2)
            contador.append(contador3)



vectorfinal_en_muestras=min1_max_min2_1[contador]


"""fig, ax = plt.subplots()
ax.plot(t,x)
ax.plot(t,En_filtered_normalized)
ax.plot(t[vectorfinal_en_muestras],En_filtered_normalized[vectorfinal_en_muestras], 'o')
plt.show()"""



indicesmin1_vector=[]
for i in range(0,len(vectorfinal_en_muestras),3):
    for j in range(3,len(vectorfinal_en_muestras),3):
        minimum2=vectorfinal_en_muestras[i+2]
        minimum1=vectorfinal_en_muestras[j]

        if minimum1==minimum2:
            indicesbuenos=np.array([j, j+1, j+2])
            vectorfinal_en_muestras[indicesbuenos]=1


vectorfinal_en_muestras = [elemento for elemento in vectorfinal_en_muestras if elemento !=1]          

"""fig, ax = plt.subplots()
ax.plot(t,x)
ax.plot(t,En_filtered_normalized)
ax.plot(t[vectorfinal_en_muestras],En_filtered_normalized[vectorfinal_en_muestras], 'o')
plt.show()"""

maximum=[]


for i in range(0,len(vectorfinal_en_muestras),3):
    maximum.append(vectorfinal_en_muestras[i+1])


maximum_in_time=np.array(maximum)
maximum_in_time=maximum_in_time/fs


resta_vector=[]
for i in range(0,len(maximum_in_time)):
    if i>=1:
        resta= abs(maximum_in_time[i]-maximum_in_time[i-1])
        resta_vector.append(resta)

resta_vector=np.array(resta_vector)

if len(resta_vector) % 2 == 0:
    resta_vector=resta_vector
else:
    resta_vector=np.delete(resta_vector, -1, None)




valor_primerS1_maximo_array=[]
valor_primerS1_maximo_vector=[]
valor_primerS1_maximo_vector_2=[]

valor_segundoS1_maximo_array=[]
valor_segundoS1_maximo_vector=[]
valor_segundoS1_maximo_vector_2=[]




for i in range(1,len(resta_vector),2):
    actual=resta_vector[i]
    anterior=resta_vector[i-1]

    if actual>anterior:
        valor_primerS1_maximo=maximum[i-1]
        valor_primerS1_maximo_vector=np.array(valor_primerS1_maximo)
        posiciones = np.where(vectorfinal_en_muestras == valor_primerS1_maximo_vector)
        valor_primerS1_maximo_vector_2.append(posiciones)

        valor_segundoS1_maximo=maximum[i+1]
        valor_segundoS1_maximo_vector=np.array(valor_segundoS1_maximo)
        posiciones2 = np.where(vectorfinal_en_muestras == valor_segundoS1_maximo_vector)
        valor_segundoS1_maximo_vector_2.append(posiciones2)



#Getting the total length of coordinates of min1 max and min2 array
# The number of rows
rows = len(valor_primerS1_maximo_vector_2)

# The number of columns
cols = len(valor_primerS1_maximo_vector_2[0])

# The number of total elements
total_length = rows * cols

#Resahpe the coordinates of min1 max and min2 array
valor_primerS1_maximo_vector_2=np.reshape(valor_primerS1_maximo_vector_2, total_length)
valor_segundoS1_maximo_vector_2=np.reshape(valor_segundoS1_maximo_vector_2, total_length)



valor_primerS1_indice_min1=[]
valor_segundoS1_indice_min1=[]

for i in range(len(valor_primerS1_maximo_vector_2)):
    indice_min1=valor_primerS1_maximo_vector_2[i]

    indice_min1_1=valor_segundoS1_maximo_vector_2[i]
    

    valor_primerS1_indice_min1.append(vectorfinal_en_muestras[indice_min1-1]) 
    valor_segundoS1_indice_min1.append(vectorfinal_en_muestras[indice_min1_1-1]) 


valor_primerS1_indice_min1_np_array=[]
valor_segundoS1_indice_min1_np_array=[]

valor_primerS1_indice_min1_np_array=np.array(valor_primerS1_indice_min1)
valor_segundoS1_indice_min1_np_array=np.array(valor_segundoS1_indice_min1)

# Obtener la ruta absoluta al archivo del modelo en la misma carpeta que el script
script_dir = os.path.dirname(os.path.realpath(__file__))  # Directorio donde está el script
filename = os.path.join(script_dir, 'finalized_model_murmur_classification.sav')



loaded_model = pickle.load(open(filename, 'rb'))


predicciones_del_modelo=[]
for i in range(len(valor_segundoS1_indice_min1_np_array)): #Se calculan los coeficientes mfcc de cada ciclo y se pasan al modelo para clasificar cada ciclo de la señal
    ciclo = x[valor_primerS1_indice_min1_np_array[i]:valor_segundoS1_indice_min1_np_array[i]]
    mfccs=np.mean(librosa.feature.mfcc(y=ciclo, sr=fs,n_mfcc=13).T, axis=0)

    
    #results = loaded_model.predict([[mfccs[0],mfccs[1],mfccs[2],mfccs[3],mfccs[4],mfccs[5],mfccs[6],mfccs[7],mfccs[8],mfccs[9],mfccs[10],mfccs[11],mfccs[12]]])
    results = loaded_model.predict([mfccs])
    predicciones_del_modelo=np.concatenate((results,predicciones_del_modelo),axis=None)


moda_de_vector_prediccion=mode(predicciones_del_modelo)

if moda_de_vector_prediccion == 0:
    print(', el registro de fonocardiograma está en estado normal')
if moda_de_vector_prediccion == 1:
    print(', el registro de fonocardiograma muestra clic')
if moda_de_vector_prediccion == 2:
    print(', el registro de fonocardiograma presenta soplo temprano')
if moda_de_vector_prediccion == 3:
    print(', el registro de fonocardiograma presenta soplo moderado')
if moda_de_vector_prediccion == 4:
    print(', el registro de fonocardiograma muestra soplo tardio')
if moda_de_vector_prediccion == 5:
    print(', el registro de fonocardiograma muestra soplo completo')
    
"""fig, ax = plt.subplots()
ax.plot(ciclo)
plt.show()"""

