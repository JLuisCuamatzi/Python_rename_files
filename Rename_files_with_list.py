# How execute:
# python3 Rename_files_with_list.py -d /path/where/files/to/rename/are/saved -l /path/to/csv/file/with/info/about/names

#python3 /mnt/c/Users/SilverStone/OneDrive/2020_Jorge/Tuto_python/Rename_files/Rename_files_with_list.py -d /mnt/c/Users/SilverStone/OneDrive/2020_Jorge/Tuto_python/Rename_files/Files_example/Try_3 -l /mnt/c/Users/SilverStone/OneDrive/2020_Jorge/Tuto_python/Rename_files/Files_example/Try_3/List.csv   

import os
import argparse
#
# Agregando argumentos
ag = argparse.ArgumentParser()
ag = argparse.ArgumentParser(description = "Python program to rename files")
ag.add_argument("-d", "--directory", default = "", help = "directory where are the files to rename")
ag.add_argument("-l", "--list", default = "", help = "csv file with old and new names")

args = vars(ag.parse_args())
wd_path = str(args["directory"])
list_names = str(args["list"])

## Funciones para abrir y leer las columnas en un .csv
def opencsv (csv_file):
    arr = []
    csv_file = open(csv_file,"r",encoding = "utf-8")
    for line in csv_file:
        arr.append(line.strip().split(","))
    csv_file.close
    return arr
# Function to look at info from the header
# This is a generic function in order to look at the header (first row) of any csv file
def extindex (row,header):
    col_ID = 0
    for col in row:
        if header in col:
            break
        else:
            col_ID += 1        
    return col_ID
# Function to extract info from the column at a specific header
# This function employ the extindex function
def extcol (array, header):
    index = extindex(array[0], header)
    arr = []
    for i in range(1, len(array)):
        for j in range(0, len(array[0])):
            if j == index:
                arr.append(array[i][j])
            else:
                pass
    return arr
## Acá terminan las funciones para abrir y leer las columnas en un .csv

##### MAIN #####
os.chdir(wd_path)
old_new_name = opencsv(list_names) # Aquí abro el archivo con los nombres
old_names = extcol(old_new_name, "Old_name") # Extraigo la columna con los antiguos nombres
new_names = extcol(old_new_name, "New_name") # Extraigo la columna con los nuembros nombres
for i in range(0, len(old_names)):
    old_name = old_names[i]
    new_name = new_names[i]
    os.rename(old_name, new_name)