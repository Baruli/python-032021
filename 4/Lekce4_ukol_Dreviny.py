'''
Tabulka dreviny v naší databázi obsahuje informace o těžbě dřeva podle druhů dřevin a typu těžby.
Objem těžby se nachází ve sloupci hodnota.

1. Pomocí SQL dotazu do databáze si připrav dvě pandas tabulky:
    - tabulka smrk bude obsahovat řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska"
    - tabulka nahodila_tezba bude obsahovat řádky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva"
2. Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk. Pozor, řádky nemusí být seřazené podle roku.
3. Vytvoř graf, který ukáže vývoj objemu těžby pro různé typy nahodilé těžby.
'''

from sqlalchemy import create_engine, inspect
import pandas
import numpy
import matplotlib.pyplot as plt

HOST = "czechitaspsql.postgres.database.azure.com"
PORT = 5432
USER = "barbora3ulicna"
USERNAME = f"{USER}@czechitaspsql"
DATABASE = "postgres"
PASSWORD = "bsc2mqTzVamDNxw2"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=False)

# 1.1. Nacteni tabulky smrk obsahujici jen řádky, které mají v sloupci dd_txt hodnotu "Smrk, jedle, douglaska".
smrk = pandas.read_sql("SELECT * FROM dreviny WHERE dd_txt = 'Smrk, jedle, douglaska'", con=engine)

# 1.2. Nacteni tabulky nahodila_tezba obsahujici radky, které mají v sloupci druhtez_txt hodnotu "Nahodilá těžba dřeva".
nahodila_tezba = pandas.read_sql("SELECT * FROM dreviny WHERE druhtez_txt = 'Nahodilá těžba dřeva'", con=engine)
nahodila_tezba["rok"] = pandas.to_datetime(nahodila_tezba["rok"], format='%Y')

# # 2. Vytvoř graf, který ukáže vývoj objemu těžby pro tabulku smrk.
tezba_po_letech = smrk.groupby(["rok"])["hodnota"].sum()
tezba_po_letech.plot(kind='bar', x='rok', y='hodnota', title='Tezba smrku, jedle, douglasky v letech 2000-2020')
# plt.show()

# 3. Vytvoř graf, který ukáže vývoj objemu těžby pro různé typy nahodilé těžby
pricina_pivot = pandas.pivot_table(nahodila_tezba,
                                   index='rok', columns='prictez_txt',
                                   aggfunc=numpy.sum,
                                   values='hodnota',
                                   margins=False)
pricina_pivot.plot(legend=True)
plt.show()


# Čím je způsobený prudký nárůst těžby jehličnatých stromů cca od roku 2015, který je viditelný v grafu z bodu (2.)?
# Zobrazeni dat za rok 2015
dreviny_2015 = pandas.read_sql('''SELECT rok, hodnota, dd_txt, prictez_txt 
                                  FROM dreviny 
                                  WHERE rok = 2015 
                                  ORDER BY dd_txt
                                  ''', con=engine)
# print(dreviny_2015.to_string())
'''
Odpoved:
Pricinu tezby pro ruzne druhy drevin nelze z tabulky urcit kvuli chybejicim hodnotam (viz. napr. data za rok 2015 vyse). 
Nicmene na zaklade obou grafu, ze kterych lze vycist, ze od r. 2015 stoupa tezba jehlicnatych stromu a soucasne stoupa 
i hodila tezba kvuli hmyzu, lze vyvodit, ze za prudkym narustem tezby jehlicnatych stromu je hmyzova pricina.
'''

# Kolem roku 2007 vidíme v obou grafech krátkodobý nárůst těžby. Čím byl způsobený (můžeš zkusit dohledat konkrétní událost)?
'''Odpoved: Pricinou byl orkan Kyrill, ktery se lesy CR prohnal v noci z 18. na 19.ledna 2007.'''
