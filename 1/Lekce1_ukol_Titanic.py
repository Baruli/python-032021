"""
Zakladni zadani:
Vytvoř kontingenční tabulku, která porovná závislost mezi
pohlavím cestujícího (sloupec Sex), třídou, ve které cestoval (sloupec Pclass),
a tím, jestli přežil potopení Titanicu (sloupec Survived).

Rozsireni:
Z dat vyfiltruj pouze cestující, kteří cestovali v první třídě.
Dále použij metodu cut na rozdělení cestujících do věkových skupin.
Urči relativní počet přeživších pro jednotlivé kombinace pohlavní a věkové skupiny.

"""

import requests
import pandas as pd
import numpy as np

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/titanic.csv")
with open("titanic.csv", 'w', encoding='utf8') as file:
    file.write(r.text)
titanic = pd.read_csv('titanic.csv')

# Rychla kontrola dat
# print(titanic.tail().to_string(),'\n')
# print(titanic.info(),'\n')

# Jsou v datasetu duplicity? => vysledek: OK, zadne duplicity
# print(f'\nJsou v datech duplicity? {titanic.duplicated().any()}\n')


# ZAKLADNI ZADANI:
# Závislost mezi pohlavím cestujícího, třídou, ve které cestoval, a tím, jestli přežil. (kontingenční tabulka)
print('\nPocet prezivsich pasazeru Titaniku podle pohlavi a tridy, kterou cestovali: ')
titanic_pivot = pd.pivot_table(titanic,
                               index='Sex', columns='Pclass',
                               values='Survived',
                               aggfunc=np.sum,
                               margins=True,
                               margins_name='Survived')
print(titanic_pivot)


# ROZSIRENE ZADANI:
# Pouze cestujici v 1. tride
titanic_1stClass = titanic[titanic['Pclass'] == 1].reset_index(drop=True)

# To check the result
# print(titanic_1stClass.count())
# print(titanic.groupby(['Pclass']).size())

# # Rozdeleni cestujicich podle vekovych skupin
titanic_1stClass["age_group"] = (pd.cut(titanic_1stClass["Age"],
                                        bins=[0,12,19,65,99],
                                        labels=['child', 'adolescent', 'adult', 'elderly']))
# print(titanic_1stClass.tail().to_string())

# Relativni pocet prezivcich 1. tridy podle pohlavi a vekove skupiny
print('\nRelativni pocet prezivsich pasazeru 1. tridy podle pohlavi a vekove skupiny: ')
titanic_1stClass_pivot = pd.pivot_table(titanic_1stClass,
                                        index='Sex', columns='age_group',
                                        values='Survived',
                                        aggfunc=np.mean,
                                        margins=True,
                                        margins_name='1st class survivors')

print(titanic_1stClass_pivot)

