import pandas as pd
from pytreemap import TreeMap
import Vocab
import random
import os

path = os.getcwd()
sheet = pd.read_excel(path + r'\static\Chinese Vocab Community.xlsx', sheet_name=0)

print(sheet)

vocabs = TreeMap(comparator=None)


for row in sheet.iterrows():
    arr = []
    for i in range(len(row[1])):
        arr.append(row[1][i])
    vc = Vocab.Vocab(arr[0].strip("\t"), arr[1].strip("\t"), arr[2])
    vocabs[row[0]] = vc

user = ""

def flashcardMode():
    print("Starting flashcard mode. Press 'Q' to quit")
    user = input("Presss enter start: ")
    while user.upper() != "Q":
        id = random.randint(0, vocabs.size() - 1)
        print(vocabs[id].getChars(), end=' ')
        user = input()
        print(f"{vocabs[id].getPinyin()}\t{vocabs[id].getDefin()}", end=' ')
        user = input()
        print(user)

def reviewMode():
    print("Starting review mode: Press 'Q' to quit")
    user = input()
    for i in range(len(vocabs.values())):
        print(vocabs[i].getChars(), end=' ')
        user = input()
        print(f"{vocabs[i].getPinyin()}\t{vocabs[i].getDefin()}", end=' ')
        user = input()
        if (user.upper() == 'Q'): return

# while (user.upper() != 'Q'):
#     user = input("What mode would you like:\nFlashcard Mode (F)\nReview Mode (R)\nQuit (Q)\n")
#     if (user.upper() == 'F'): flashcardMode()
#     if (user.upper() == 'R'): reviewMode()
