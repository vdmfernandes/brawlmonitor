import requests
import numpy as np
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from datetime import date

def elo(rating):
    rating = int(rating)
    if rating >= 2000: return 'Diamond'
    elif 1936 <= rating <= 1999: return 'Platinum 5'
    elif 1872 <= rating <= 1935: return 'Platinum 4'
    elif 1808 <= rating <= 1871: return 'Platinum 3'
    elif 1744 <= rating <= 1807: return 'Platinum 2'
    elif 1680 <= rating <= 1743: return 'Platinum 1'
    elif 1622 <= rating <= 1679: return 'Gold 5'
    elif 1564 <= rating <= 1621: return 'Gold 4'
    elif 1506 <= rating <= 1563: return 'Gold 3'
    elif 1448 <= rating <= 1505: return 'Gold 2'
    elif 1390 <= rating <= 1447: return 'Gold 1'
    elif 1338 <= rating <= 1389: return 'Silver 5'
    elif 1286 <= rating <= 1337: return 'Silver 4'
    elif 1234 <= rating <= 1285: return 'Silver 3'
    elif 1182 <= rating <= 1233: return 'Silver 2'
    elif 1130 <= rating <= 1181: return 'Silver 1'
    elif 1086 <= rating <= 1129: return 'Bronze 5'
    elif 1042 <= rating <= 1085: return 'Bronze 4'
    elif 998 <= rating <= 1041: return 'Bronze 3'
    elif 954 <= rating <= 997: return 'Bronze 2'
    elif 910 <= rating <= 953: return 'Bronze 1'
    elif 872 <= rating <= 909: return 'Tin 5'
    elif 834 <= rating <= 871: return 'Tin 4'
    elif 796 <= rating <= 833: return 'Tin 3'
    elif 758 <= rating <= 795: return 'Tin 2'
    elif 720 <= rating <= 757: return 'Tin 1'
    elif 200 <= rating <= 719: return 'Tin 0'

start_time = time.time()
first_page = 4335
last_page = 5341
# for page_number in range(1, 5):
for page_number in range(first_page, last_page + 1):
    percent = round(100*(page_number/last_page), 2) 
    if page_number == last_page: print('Requisitando página {}/{} ({}%)'.format(page_number, last_page, percent))
    else: print('Requisitando página {}/{} ({}%)'.format(page_number, last_page, percent), end='\r')
    
    # requisita html da página
    page = requests.get('https://www.brawlhalla.com/rankings/1v1/brz/{}/'.format(page_number))
    soup = BeautifulSoup(page.content, 'lxml')

    # pega as principais informações da tabela de ranking
    # odds = linhas ímpares, evens = linhas pares
    odds = soup.find_all(class_='odd', id="")
    evens = soup.find_all(class_='even', id="")

    # itera pelos elementos da tabela
    for index in range(len(odds)):
        try:
            odd_infos = odds[index].select('.pcenter')
            odd_position = odd_infos[0].text.replace(',', '')
            odd_server = odd_infos[1].text
            odd_wins = odd_infos[2].text.split('-')[0]
            odd_loses = odd_infos[2].text.split('-')[1]
            odd_rating = odd_infos[3].text
            odd_peak = odd_infos[4].text
            odd_elo = elo(odd_rating)
        except:
            pass

        try:
            even_infos = evens[index].select('.pcenter')
            even_position = even_infos[0].text.replace(',', '')
            even_server = even_infos[1].text
            even_wins = even_infos[2].text.split('-')[0]
            even_loses = even_infos[2].text.split('-')[1]
            even_rating = even_infos[3].text
            even_peak = even_infos[4].text
            even_elo = elo(even_rating)
        except:
            pass

        # abre arquivo, escreve as informações retiradas da tabela e fecha
        filename = date.today().strftime('%Y-%m-%d.csv')
        if os.path.exists(filename):
            f = open(filename, 'a')
        else:
            f = open(filename, 'a+')
            f.write('position,server,wins,loses,rating,elo,peak\n')

        # escreve no arquivo somente se o player tiver jogado 10 partidas ou mais
        if (int(odd_wins) + int(odd_loses)) >= 10: f.write('{},{},{},{},{},{},{}\n'.format(odd_position, odd_server, odd_wins, odd_loses, odd_rating, odd_elo, odd_peak))
        if (int(even_wins) + int(even_loses)) >= 10: f.write('{},{},{},{},{},{},{}\n'.format(even_position, even_server, even_wins, even_loses, even_rating, even_elo, even_peak))
        f.close()

end_time = time.time()
print('Extração dos dados finalizada ({}s).'.format(round(end_time - start_time), 2))

