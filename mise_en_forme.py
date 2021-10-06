# coding:utf-8

"""
Mise en forme pour la sortie console
liste des codes https://askcodez.com/liste-de-sequences-dechappement-couleur-ansi.html
"""

def bleu(texte):
    START = "\033[34m"
    END = "\033[0m"
    texte = START + texte + END
    return texte

def rouge(texte):
    START = "\033[31m"
    END = "\033[0m"
    texte = START + texte + END
    return texte

def italique(texte):
    START = "\033[3m"
    END = "\033[0m"
    texte = START + texte + END
    return texte