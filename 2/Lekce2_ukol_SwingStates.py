"""
V souboru 1976-2020-president.csv najdeš historické výsledky amerických prezidentských voleb.

1. Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech (pomocí metody rank()).
   Nezapomeň, že data je před použitím metody nutné seřadit a spolu s metodou rank() je nutné použít metodu groupby().
2. Ponech si v tabulce pouze řádky, které obsahují vítěze voleb v jednotlivých letech v jednotlivých státech.
3. Pomocí metody shift() přidej nový sloupec, abys v jednotlivých řádcích měl(a) po sobě vítězné strany
   ve dvou po sobě jdoucích letech.
4. Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana.
   Můžeš k tomu použít funkci numpy.where a vložit hodnotu 0 nebo 1 podle toho, jestli došlo ke změně vítězné strany.
5. Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
"""

import requests
import pandas as pd
import numpy as np

with requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/1976-2020-president.csv") as r:
  open("1976-2020-president.csv", 'w', encoding="utf-8").write(r.text)

president_elections = pd.read_csv("1976-2020-president.csv")
# Ponechani pouze dulezitych sloupcu
president_elections = president_elections[['year', 'state', 'candidate', 'party_simplified', 'candidatevotes', 'totalvotes']]

# print(president_elections.tail().to_string())
# print(president_elections.info())

# 1. Urči pořadí jednotlivých kandidátů v jednotlivých státech a v jednotlivých letech.
president_elections['candidate_rank'] = president_elections.groupby(['year', 'state'])['candidatevotes'].rank(ascending=False)

# 2. Pouze vitezove v kazdem roku a state.
elections_winners = president_elections[president_elections['candidate_rank'] == 1.0].reset_index(drop=True)

# 3. Pomocí metody shift() přidej nový sloupec,
# abys v jednotlivých řádcích měla po sobě vítězné strany ve dvou po sobě jdoucích letech.
elections_winners = elections_winners.sort_values(['state', 'year'])
elections_winners = elections_winners.rename(columns={'party_simplified': 'winner'})
elections_winners['prev_winner'] = elections_winners['winner'].shift()
elections_winners = elections_winners.drop(['candidate_rank'], axis=1)

# 4. Porovnej, jestli se ve dvou po sobě jdoucích letech změnila vítězná strana.
elections_winners['winner_is_different'] = np.where(elections_winners['winner'] == elections_winners['prev_winner'], 0, 1)
# print('\n',elections_winners.tail(12).to_string())

# 5. Proveď agregaci podle názvu státu a seřaď státy podle počtu změn vítězných stran.
elections_winners_grouped = elections_winners.groupby(['state'])['winner_is_different'].sum()
elections_winners_grouped =pd.DataFrame(elections_winners_grouped)
elections_winners_grouped = elections_winners_grouped.sort_values(['winner_is_different'], ascending=False)
print('\n',elections_winners_grouped.to_string())