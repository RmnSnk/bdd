# coding:utf-8

import re

def siren_check(siren):
    pattern = '[0-9]'
    test_string = str(siren)
    if len(test_string) != 9:
        print("Un Siren comporte exactement 9 chiffres")
        return 0
    else:
        flag = 0
        for c in test_string:
            result = re.match(pattern, c)
            if not result:
                flag += 1
        if flag != 0:
            print("La chaines doit contenir que des chiffres")
            return 0
        else:
            print("Numero siren valide")
            return 1

siren = input("S : ")
siren_check(siren)