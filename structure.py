from os import listdir
from os.path import isfile, join
import os

def remake_number(numbers):

    numbers = int(numbers)
    table = (1000,100,10,1)
    new_number = ""

    for i in table:
        division = int(numbers/i)
        new_number += str(division)
        numbers -= division * i

    return str(new_number)

def rename_files_by_dir(filedir):

    list_files = listdir(filedir)

    for i in list_files:
        old_name = os.path.join(filedir, i)
        aux = i.split()
        aux[1] = remake_number(aux[1])
        aux = ' '.join(aux)
        new_name = os.path.join(filedir, aux)
        os.rename(old_name, new_name)

if __name__=="__main__":

    dir = [fr"D:\Livros\.LIGHTNOVEL\Nine Star Hegemon Body Art\Volume {i}" for i in range(1,11)]

    for i in dir:
        onlyfiles = [f for f in listdir(i) if isfile(join(i, f))]
        for j in onlyfiles:
            old_name = os.path.join(i, j)
            aux = '1' + j
            new_name = os.path.join(i, aux)
            os.rename(old_name, new_name)