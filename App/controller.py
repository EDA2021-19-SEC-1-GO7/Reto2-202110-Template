﻿"""
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
 """

from os import sep
import config as cf
import model 
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initialize():
    Datos=model.initialize()
    return Datos 

# Funciones para la carga de datos
def Load_Data(storage:dict):

    Load_cetegories(storage)
    Load_videos(storage)
    

def Load_videos(storage:dict):
    videos_File = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(videos_File, encoding='utf-8'))
    for video in input_file:
        model.add_video(storage, video)

def Load_cetegories(storage:dict):
    cat_File = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(cat_File, encoding='utf-8'), delimiter='\t')
    for cat in input_file:
        model.add_categoria_id(storage, cat)

# Funciones de ordenamiento


# Funciones de consulta sobre el catálogo
def filtrar_count_cat(videos:list, categories:list, categoria:str, pais:str)->list:
    return model.filtrar_count_cat(videos, categories, categoria, pais)

def filtrar_cat_n(categories, categoria:str,n:int)->list:
    return model.filtrar_cat_n(categories, categoria,n)

def filtrar_count_tag(videos, pais, tag)->list:
    return model.filtrar_count_tag(videos, pais, tag)

def max_vids_count(vids:list,pais:str):
    return model.max_vids_count(vids,pais)

def max_vids_cat(videos:list, categories:list, categoria:str):
    return model.max_vids_cat(videos, categories, categoria)
