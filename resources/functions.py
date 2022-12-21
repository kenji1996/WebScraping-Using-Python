from os import listdir
from os import rename
from os.path import isfile, join
from itertools import tee
from random import choices, choice
from itertools import takewhile
import string

from src.model.elem import Element

def get_common_xpath(*args : list[Element], sep=r"/"):

    """ Given >=2 Element objects, finds the common xpath between them. """

    # Check if all args are type Element 

    condition = all([isinstance(x, Element) for x in args])

    if not condition:
        return print("Invalid argument. Make sure every object is of Element type.")
    
    list_xpath = []
    list_size = len(args)

    if list_size < 2:

        return print("Function only works with 2 or more elements.")
        
    else:

        # Transforms all xpaths into list of strings
        # '/html/body/div/header/div/nav/ul' -> ['', 'html', 'body', 'div', 'header', 'div', 'nav', 'ul']
        list_xpath = [el.property['xpath'].split(sep=sep) for el in args]

    elements_size = [len(x) for x in list_xpath]

    # *list unpacks list
    list_xpath_zip = list(zip(*list_xpath))    
    
    # takewhile() applies a condition to a iterable and only stops when it returns False to said conditions
    # n = tuple of string
    # n[0] = string itself
    # the condition is lambda x: returns true if all elements are equal to first element of x

    common_xpath = list(
                        n[0] for n in takewhile
                                                (
                                                lambda x: all(m == x[0] for m in x)
                                                , list_xpath_zip
                                                )
                        )

    elements_size = list(x - len(common_xpath) for x in elements_size)
    common_xpath = '/'.join(common_xpath)

    return common_xpath, elements_size

def rename_files_numbers(dir: str, limit = 1000):

    """ Given a certain directory, scan all files and, if there's a number,
    
        reformat the file's name's number(s) given certain limit.

        if limit is 1000:
        
        name1 -> name0001

        name14 -> name0014

        Limit 10

        name9 -> name09

        name100 -> name100 (unchanged)
        
        :param dir: Directory. 
        :param limit: Default 1000 """
    
    def file_number_index(name: str) -> list:
        return [[index, number] for index, number in enumerate(name) if number.isdigit()]

    def combine_numbers(lista: list):
        
        #efficient way to handle iterators (NOT WORKING FOR NOW)
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            iter = []
            for i in iterable:
                a, b = tee(iterable)
                next(b, None)
                iter.append(list(zip(a,b)))
            return iter

        #For each number found, pair it with the next one
        # if list = [ 1,2,3,4,5.. ], zip will be [ (1,2),(2,3),(3,4)... ]
        def pair(iterable):
            lista = []
            for i in iterable:
                lista.append(list(zip(i, i[1:])))
            return lista

        #Will be used to hold the numbers during the algorithm usage
        str_temp = ''

        # Each sequence of numbers found will be stored here.
        num_temp = []


        each_file = []

        # Algorithm to separate single-digit numbers from multiple-digit.
        # Check if the next number found belongs to a sequence or is a separated entity.
        # For example, if file is named foo123a1b12..
        # The generated paired list is : [ [index, number], [index, number], [index, number] ] so:
        # [ [3,1], [4,2], [5,3], [7,1], [9,1], [10,2] ]
        paired_lists = pair(lista)
        for par in paired_lists:
            for n, (previous, current) in enumerate(par):
                # Checking if its the first number found, to serve as the base.
                if n == 0:
                    str_temp += str(previous[1])+str(current[1])

                # Checking if the next number belongs to the same sequence as the previous one.
                # foo123 should result in [123] and not [1,2,3] / [12,3] ..
                elif previous[0] == current[0]-1:
                    str_temp += current[1]

                # Finally, checks if the next current number should belong to the current sequence
                # Avoids having the last digit of a multiple-digit number being considered out of it.
                elif par[n][0][0] != (par[n][0][0]+2):
                    num_temp.append(str_temp)
                    str_temp = ''
                    str_temp += current[1]
            if str_temp != "":
                num_temp.append(str_temp)
                str_temp = ""
            each_file.append(num_temp.copy())
            num_temp.clear()

        return each_file
    
    # How many digits should the numbers have i.e if limit = 10000 then 143 -> 00143
    digits = len(str(limit))

    # Find all files in dir
    files = [f for f in listdir(rf'{dir}') if isfile(join(rf'{dir}', f))]
    onlyfiles = files.copy()

    # Find the numbers's index from each file
    indexes = [file_number_index(file) for file in onlyfiles]

    # Separate each number
    numbers = combine_numbers(indexes)

    # Replace old number with new
    for (n,file), numbers_found in zip(enumerate(onlyfiles), numbers):
        
        # Creating random sequence to avoid conflicts when replacing numbers
        random_char = [f'{number}'.join(choices(string.ascii_uppercase)) * 5 for number in numbers_found]
        new_set_numbers = [f"{int(number):0{digits}d}" for number in numbers_found]

        # First replace all numbers found to random sequence of chars to avoid
        #   having the algortihm apply the conversions more than once to the same number.
        for numb,random in zip(numbers_found, random_char):
            onlyfiles[n] = onlyfiles[n].replace(numb, random)

        # Convert the random chars to the desired numbers.
        for random, new_number in zip(random_char, new_set_numbers):
            onlyfiles[n] = onlyfiles[n].replace(random, new_number)

    # Apply the changed numbers to the file itself.
    for old_name, new_name in zip(files, onlyfiles):
        rename(rf'{dir}/{old_name}', rf'{dir}/{new_name}')

def random_name(n=10, upper = True, lower = True, numbers = True):

    """ Generates string of random characters.
        
        :param n: Number of characters (default 10).

        :param upper: Uppercase letters (default True). 
        
        :param lower: Lowercase letters (default True). """

    dicionario = {
                    ('upper', upper) : string.ascii_uppercase,
                    ('lower', lower) : string.ascii_lowercase,
                    ('numbers', numbers) : string.digits
                }

    characters = ""

    for key, value in dicionario.items():
        if key[1]:
            characters += value

    seq = ''.join([choice(characters) for x in range(0,n)])
    
    return seq

if __name__=="__main__":

    seq = random_name(20)
    print(seq,len(seq))