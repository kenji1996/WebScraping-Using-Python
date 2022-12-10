from os import listdir
from os import rename
from os.path import isfile, join
from itertools import tee
from random import choices
import string
from lxml.html import HtmlElement

def get_common_xpath(elemento1 : str, elemento2 : str) -> str:
    
    """ Finds out the common xpath between 2 given xpaths."""

    # Transforming xpath string into list of components and zipping both lists into one
    el1_xpath = elemento1.split(sep=r'/')
    el2_xpath = elemento2.split(sep=r'/')

    el_zipped = list(zip(el1_xpath, el2_xpath))

    # Looping through zipped list to check what components are identical    
    el_equal_comp = [i for i,j in el_zipped if i == j]

    # Joining all equal components, separating then with /
    el_equal_comp = '/'.join(el_equal_comp)

    return el_equal_comp

def is_same_div(elemento1 : HtmlElement, elemento2 : HtmlElement):
    return elemento1.getparent() == elemento2.getparent()

def check_instance_iterable(var) -> bool:

    """ Check if variable is an iterable. 
        
        Return True if var is a list/tuple/set, otherwise False. """

    conditions = (isinstance(var, list), 
                isinstance(var, tuple),
                isinstance(var, set))

    return any(conditions)

def reformat_all_files_numbers(dir: str, limit = 1000):

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