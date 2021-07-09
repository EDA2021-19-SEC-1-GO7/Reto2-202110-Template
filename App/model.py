"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import time
assert cf
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos
def initialize():
    Data={
        "videos":None,
        "categorias_id":None,
        "categorias":None
    }
    Data["videos"]=lt.newList("ARRAY_LIST")#Todos los videos
    Data["categorias_id"]=mp.newMap(44,47,'CHAINING',2,None)#Parejas id_categoria-Nombre categoria
    Data["categorias"]=mp.newMap(44,47,'CHAINING',2,None)#Videos ordenados por categoria
    
    return Data
# Funciones para agregar informacion al catalogo
def add_video(Data, video):
    lt.addLast(Data["videos"],video)
    add_categoria_vid(video,Data)

def add_categoria_id(Data, categoria):
    mp.put(Data["categorias_id"],categoria["id"],categoria["name"])
    cat=new_categoria(categoria["name"],categoria["id"])
    mp.put(Data["categorias"],categoria["name"],cat)

def new_categoria(name,id):
    cat={"name":name,"id":id,'videos':lt.newList(datastructure='ARRAY_LIST')}
    return cat

def add_categoria_vid(video,Data):
    nombre_cat=me.getValue(mp.get(Data["categorias_id"],video["category_id"]))
    categoria=me.getValue(mp.get(Data["categorias"],nombre_cat))
    lt.addLast(categoria["videos"],video)

# Funciones para creacion de datos

# Funciones de consulta

def filtrar_cat_n(categories, categoria_name,n)->list:
    """ Retorna una lista ordenada de los videos con más views de una categoría """
    videos=me.getValue(mp.get(categories,categoria_name))["videos"]
    tiempo,vids_sorted=sort_vids_by_views(videos)
    list_new=lt.newList()
    titulos=lt.newList()
    i=1
    while lt.size(list_new)<n and i<=lt.size(vids_sorted):
        tit=lt.getElement(vids_sorted,i)["title"]
        if lt.isPresent(titulos,tit):
            pass
        else:
            lt.addLast(titulos,tit)
            lt.addLast(list_new,lt.getElement(vids_sorted,i))
        i+=1
    return tiempo,list_new 

def filtrar_count_cat(videos:list, categories, categoria:str, pais:str)->tuple:
    """ Retorna una lista ordenada de los videos con más likes de una categoría y 
    un país en específico """
    vids_cat=lt.newList()
    cat_id=None
    j=1
    search=True
    while j<=lt.size(mp.keySet(categories)) and search:
        nombre_cat=me.getValue(mp.get(categories,lt.getElement(mp.keySet(categories),j)))
        if nombre_cat==categoria:
            search=False
            cat_id=me.getKey(mp.get(categories,lt.getElement(mp.keySet(categories),j)))
        j+=1
    for i in range(lt.size(videos)):
        video_i=lt.getElement(videos,i)
        if video_i["category_id"]==cat_id and video_i["country"]==pais:
            lt.addLast(vids_cat,video_i)
    return sort_vids_by_likes(vids_cat)

def filtrar_count_tag(videos, pais, tag)->list:
    """ Retorna una lista ordenada de los videos con más comentarios de un país 
    y con un tag en específico. En este caso se incluyen todos aquellos tags que 
    incluyan la palabra ingresada por el usuario como subcadena """
    vid_filtrados=lt.newList()#Lista en la que poner los videos filtrados
    for i in range(lt.size(videos)):#Proceso de filtrado
        video=lt.getElement(videos, i)
        if video["country"]==pais and (tag in video["tags"]):
            lt.addLast(vid_filtrados, video)
    return sort_vids_by_comments(vid_filtrados)

def max_vids_count(videos:list,pais:str)->dict:
    """ Retorna una tupla que contiene 
            El título del video que fue tendencia por más días en un país específico
            El ratio de likes/dislikes para el video que fue tendencia por más días en un país específico
            El canal del video que fue tendencia por más días en un país específico
            El numero de días que el video fue tendencia
            El país en donde el video fue tendencia"""
    registro={}#Diccionario de listas vacio, tendra como llave los titulos de los videos; en las listas se anotaran los valores solicitados por el usuario.
    for i in lt.iterator(videos):#Recorrer cada video de la lista principal.
        titulo=i["title"]
        if titulo in registro.keys() and i["country"]==pais: #Si el video ya ha aparecido para el pais requerido, entonces se suma uno al contador y se comparan los likes.
            lista=registro[titulo]#[numero de apariciones, likes maximos, dislikes maximos,titulo del canal]
            record=lt.getElement(lista,1)
            lt.changeInfo(lista,1,record+1)#Suma 1 al contador
            likes_i=int(i["likes"])
            dislikes_i=int(i["dislikes"])
            if likes_i>lt.getElement(lista,2):#Asumimos que la relacion likes/dislikes es la de la ultima fecha, y que en esta ultima fecha hay más likes que en las otras posibles.
                lt.changeInfo(lista,2,likes_i)
                lt.changeInfo(lista,3,dislikes_i)
        elif titulo not in registro.keys() and i["country"]==pais:#Si el video no esta registrado ya, entonces se añade su entrada y se inicializa con sus valores.
            registro[titulo]=lt.newList()
            lt.addLast(registro[titulo],1)
            lt.addLast(registro[titulo],int(i["likes"]))
            lt.addLast(registro[titulo],int(i["dislikes"]))
            lt.addLast(registro[titulo],i["channel_title"])
        else:
            pass #Caso en el que el video no corresponde al pais
    #Para este punto nuestro diccionario tiene que tener todos los videos unicos de la lista para el pais seleccionado, y con los likes/dislikes más actuales.         
    respuesta=None
    ratio=None
    for j in registro.keys():#Se recorre cada video unico.
        apariciones_j=lt.getElement(registro[j],1)
        likes=lt.getElement(registro[j],2)
        dislikes=lt.getElement(registro[j],3)
        if dislikes!=0 and likes/dislikes<10:
            pass
        elif respuesta!=None and (apariciones_j>lt.getElement(registro[respuesta],1)) and j!="Deleted video":
            respuesta=j
            if dislikes>0:
                ratio=likes/dislikes
            else:
                ratio=likes #si hay 0 dislikes, entonces se toma el ratio como el numero de likes.
        elif respuesta==None:
            respuesta=j
            if dislikes>0:
                ratio=likes/dislikes
            else:
                ratio=likes
    return respuesta, ratio, lt.getElement(registro[respuesta],4), lt.getElement(registro[respuesta],1), pais


def max_vids_cat(videos:list, categories:list, categoria:str)->dict:
    """ Retorna una tupla que contiene 
            El título del video que fue tendencia por más días de una categoría específica
            El ratio de likes/dislikes para el video que fue tendencia por más días de una categoría específica
            El canal del video que fue tendencia por más días de una categoría específica
            El numero de días que el video fue tendencia
            La categoría del video fue tendencia por más días"""
    registro={} #Diccionario de listas vacio, tendra como llave los titulos de los videos; en las listas se anotaran los valores solicitados por el usuario.
    cat_id=None
    j=1
    encontro=False
    while j<lt.size(categories) and encontro == False: #Busca el id de la categoria que se desea consultar
        categ=lt.getElement(categories, j)
        if categ["name"]==categoria:
            search = True
            cat_id = categ["id"]
        j+=1

    for i in lt.iterator(videos):#Recorrer cada video de la lista principal.
        titulo=i["title"]
        if titulo in registro.keys() and i["category_id"]==cat_id: #Si el video ya ha aparecido para la categoria requerida, entonces se suma uno al contador y se comparan los likes.
            lista=registro[titulo]#[numero de apariciones, likes maximos, dislikes maximos,titulo del canal]
            record=lt.getElement(lista,1)
            lt.changeInfo(lista,1,record+1)#Suma 1 a la cantidad de días en tendencia
            likes_i=int(i["likes"])
            dislikes_i=int(i["dislikes"])
            if likes_i>lt.getElement(lista,2):#Asumimos que la relacion likes/dislikes es la de la ultima fecha, y que en esta ultima fecha hay más likes que en las otras posibles.
                lt.changeInfo(lista,2,likes_i)
                lt.changeInfo(lista,3,dislikes_i)
        elif titulo not in registro.keys() and i["category_id"]==cat_id:#Si el video no esta registrado ya, entonces se añade su entrada y se inicializa con sus valores.
            registro[titulo]=lt.newList()
            lt.addLast(registro[titulo],1)
            lt.addLast(registro[titulo],int(i["likes"]))
            lt.addLast(registro[titulo],int(i["dislikes"]))
            lt.addLast(registro[titulo],i["channel_title"])
        else:
            pass #Caso en el que el video no corresponde al pais
    #Para este punto nuestro diccionario tiene que tener todos los videos unicos de la lista para la categoria seleccionada, y con los likes/dislikes más actuales.         
    respuesta=None
    ratio=None
    for j in registro.keys():#Se recorre cada video unico.
        apariciones_j=lt.getElement(registro[j], 1)
        likes=lt.getElement(registro[j], 2)
        dislikes=lt.getElement(registro[j], 3)
        if dislikes!=0 and likes/dislikes<20:
            pass
        elif respuesta!=None and (apariciones_j>lt.getElement(registro[respuesta],1)) and j!="Deleted video":
            respuesta=j
            if dislikes>0:
                ratio=likes/dislikes
            else:
                ratio=likes#si hay 0 dislikes, entonces se toma el ratio como el numero de likes.
        elif respuesta==None:
            respuesta=j
            if dislikes>0:
                ratio=likes/dislikes
            else:
                ratio=likes
    return respuesta, ratio, lt.getElement(registro[respuesta], 4), lt.getElement(registro[respuesta],1), categoria, cat_id

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByLikes(video1, video2): 
    """ Devuelve verdadero (True) si los likes de video1 son mayores que los del video2 
    Args: video1: informacion del primer video que incluye su valor 'likes' 
    video2: informacion del segundo video que incluye su valor 'likes' """
    return (float(video1['likes']) > float(video2['likes']))

def cmpVideosByComments(video1, video2):
     """ Devuelve verdadero (True) si los la cantidad de comentarios del 
     video 1 es mayores que la cantidad del video2 Args: 
     video1: informacion del primer video que incluye su valor 'likes' 
     video2: informacion del segundo video que incluye su valor 'likes' """
     return (float(video1['comment_count'])) > float(video2['comment_count'])

def cmpVideosByViews(video1, video2):
     """ Devuelve verdadero (True) si los la cantidad de comentarios del 
     video 1 es mayores que la cantidad del video2 Args: 
     video1: informacion del primer video que incluye su valor 'likes' 
     video2: informacion del segundo video que incluye su valor 'likes' """
     return (float(video1['views'])) > float(video2['views'])

# Funciones de ordenamiento

def sort_vids_by_likes(Data:list):
    """ Retorna la lista ordenada por medio de merge sort y el tiempo que 
    tardó en realizar esta operación. Utiliza la función cmpVideosByLikes 
    como función de comparación"""
    start_time = time.process_time()
    sorted_list = merge.sort(Data, cmpVideosByLikes)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sort_vids_by_comments(Data:list):
    """ Retorna la lista ordenada por medio de merge sort y el tiempo que 
    tardó en realizar esta operación. Utiliza la función cmpVideosByCommesnts 
    como función de comparación"""
    start_time = time.process_time()
    sorted_list = merge.sort(Data, cmpVideosByComments)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sort_vids_by_views(Data:list):
    """ Retorna la lista ordenada por medio de merge sort y el tiempo que 
    tardó en realizar esta operación. Utiliza la función cmpVideosByCommesnts 
    como función de comparación"""
    start_time = time.process_time()
    sorted_list = merge.sort(Data, cmpVideosByViews)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list