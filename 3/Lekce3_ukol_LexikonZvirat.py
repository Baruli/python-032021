'''
LEXIKON ZVIRAT 1:
Dataset obsahuje sloupec image_src, který má jako hodnoty odkazy na fotky jednotlivých zvířat.
Napiš funkci check_url, která bude mít jeden parametr radek.

Funkce zkontroluje, jestli je odkaz v pořádku podle několika pravidel:
1. datový typ je řetězec: isinstance(radek.image_src, str),
2. hodnota začíná řetězcem "https://zoopraha.cz/images/",
3. hodnota končí buďto JPG nebo jpg.

Zvol si jeden ze způsobů procházení tabulky, a na každý řádek zavolej funkci check_url.
Pro každý řádek s neplatným odkazem vypiš název zvířete (title).


LEXIKON ZVIRAT 2:
Chceme ke každému zvířeti vytvořit popisek na tabulku do zoo.
Popisek bude využívat sloupců:
- title (název zvířete),
- food (typ stravy),
- food_note (vysvětlující doplněk ke stravě),
- description (jak zvíře poznáme).

Napiš funkci popisek, která bude mít jeden parametr radek. Funkce spojí informace dohromady.
Následně použijte metodu apply, abyste vytvořili nový sloupec s tímto popiskem.
'''

import requests
import pandas
desired_width = 1000
pandas.set_option('display.width', desired_width)
pandas.options.display.max_columns = 100

with requests.get("https://raw.githubusercontent.com/lutydlitatova/czechitas-datasets/main/datasets/lexikon-zvirat.csv") as r:
    open("lexikon-zvirat.csv", "wb").write(r.content)

zviratka = pandas.read_csv("lexikon-zvirat.csv", delimiter=";")

# zbaveni se posledniho sloupce a posledniho radku, ktere obsahuji samé nulové hodnoty.
zviratka.dropna(how="all", axis="columns", inplace=True)
zviratka.dropna(how="all", axis="rows", inplace=True)


print("\n-------  LEXIKON ZVIRAT 1 ----------------------------------------------------\n")

# Napiš funkci check_url, která bude mít jeden parametr radek.
# Funkce zkontroluje, jestli je odkaz v pořádku podle několika pravidel.
def check_url(radek):
    # 1. datový typ je řetězec: isinstance(radek.image_src, str)
    is_retezec = isinstance(radek.image_src, str)
    # 2. hodnota začíná řetězcem "https://zoopraha.cz/images/"
    has_correct_start = radek.image_src.startswith("https://zoopraha.cz/images/")
    # 3. hodnota končí buďto JPG nebo jpg
    is_jpg = radek.image_src.lower().endswith("jpg")
    if is_retezec == False or has_correct_start == False or is_retezec is False:
        print (radek.title)
        # print(radek.id, radek.title, is_retezec, has_correct_start, is_jpg, radek.image_src)


# nahrazeni null hodnot ve sloupci image_scr, aby u nich vytvorena funkce nevyhazovala chybu ("Kaloň rodriguezský")
zviratka['image_src'].fillna('', inplace=True)

# Zavolani funkci check_url na každý řádek DataFramu
print("Zvirata, u kterych je uvedena neplatna URL obrazku:")
zviratka.apply(check_url, axis=1)

# Ve vysledku je duplikovane informace - "Kaloň rodriguezský" -> hledani chyby:
# r = zviratka[zviratka['id'] == '160']         # Check radky s nahrazenou NaN hodnotou -> OK
r = zviratka.iloc[151:153,]
print(f"\nZ puvodniho souboru se nacita chybne vstup: 'Kaloň rodriguezský'\n{r}")
# Chyba je v puvodnim csv souboru, pravdepodobne dva znaky ";" jduci po sobe, ktere rozdelily info do 2 radku 151 a 152.
# Bylo by potreba puvodni soubor opravit.


print("\n-------  LEXIKON ZVIRAT 2 ----------------------------------------------------\n")

# Zkouknuti prikladu, jak ma vypadat cilovy vystup
examples = zviratka.iloc[[320, 300], :]
print(examples[['title', 'food', 'food_note', 'description']].head(), '\n')

'''
Zvíře na pozici 320:
  {Zoborožec rýhozobý} preferuje následující typ stravy: {plody}. 
  Konkrétně ocení když mu do misky přistanou {převážně plody, příležitostně bezobratlí (včetně rojících se mravenců)}. 
  Jak toto zvíře poznáme: {Tento malý zoborožec je nápadný výraznou pohlavní dvojtvárností. 
  Samec má krémovou hlavu a krk, bílou hruď a rezavé břicho a nadocasní krovky. 
  Ocas je béžový, s širokým koncovým pruhem. Samice je téměř celá černá a má modré pole kolem očí}.

Zvíře na pozici 300:
  {Ústřičník velký} preferuje následující typ stravy: {bezobratlí}. Konkrétně ocení když mu do misky přistanou {mlži, 
  korýši a další bezobratlí.}
  Jak toto zvíře poznáme: {Díky kontrastnímu zbarvení a pronikavému hlasu je nezaměnitelný. 
  Je téměř celý černý, jen hruď a břicho má bílé. Typický je svítivě oranžový zobák a růžové nohy. 
  V letu je patrný bílý křídelní pásek. Samec a samice vypadají stejně, mláďata mají hnědočerný hřbet, 
  šedé nohy a černou špičku zobáku.}
'''

# Definice funkce, ktera vytvori popisek
def popisek(radek):
    text1 = f"{radek.title} preferuje následující typ stravy: {radek.food}. "
    text2 = f"Konkrétně ocení když mu do misky přistanou {radek.food_note}. "
    text3 = f"Jak toto zvíře poznáme: {radek.description}."
    return text1 + text2 + text3

# Pouziti vytvorene funkce k vytvoreni noveho sloupce "popisek"
zviratka["popisek"] = zviratka.apply(popisek, axis=1)
# print(zviratka[['title', 'food', 'food_note', 'description', 'popisek']],'\n')

# Kontrola toho, ze dosazeny vystup odpovida vzorovemu vystupu pro popisek
with pandas.option_context('display.max_colwidth', None):
     print(zviratka.iloc[[320,300], :].popisek)




