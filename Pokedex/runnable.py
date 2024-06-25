# encoding: utf-8
# runnable.py

import queue
import requests
import bs4

input_pkm = queue.Queue()
output_pkm = queue.Queue()
fail_pkm = queue.Queue()

class Runnable:
    def __call__(self):
        def process_pkm(pkm):
            try:
                url = pkm["url"]

                response = requests.get(url)
                soup = bs4.BeautifulSoup(response.content, 'lxml')

                name = soup.find('h1').text

                # types
                types_list = soup.find_all('td')[1].text.replace('\n', '')                  # 'type1 type2 '
                types_list = types_list[:-1].split(' ')                                     # 'type1 type2'

                # type1, type2
                type1 = types_list[0]
                
                if (len(types_list) == 2):   # Pokemon mang song hệ
                    type2 = types_list[1]
                else: 
                    type2 = ''              # Pokemon mang 1 hệ

                # species
                species = soup.find_all('td')[2].text

                # height
                height = soup.find_all('td')[3].text.replace('\xa0', '')

                # weight
                weight = soup.find_all('td')[4].text.replace('\xa0', '')

                # ability
                ability = soup.find_all('span', {'class': 'text-muted'})[0].text.replace('1. ', '')

                # extra ability
                if '2. ' in soup.findAll(class_='text-muted')[1].text:
                    ex_ability = soup.findAll(class_='text-muted')[1].text.replace('2. ', '')
                else: 
                    ex_ability = ''
        
    
                # hidden ability
                hid_ability = soup.find_all('small', {'class': 'text-muted'})[0].text.replace(' (hidden ability)', '')
                if '(' in hid_ability:  # Pokemon không có hidden ability nên bị đọc nhầm sang khu vực xuất hiện
                    hid_ability = ''

                # catch_rate
                catch_rate = soup.find_all('td')[8].text.replace('\n', '')

                # base friendship 
                base_fs = soup.find_all('td')[9].text.replace('\n', '')

                # base exp
                base_exp = soup.find_all('td')[10].text.replace('\n', '')

                # growth_rate
                growth_rate = soup.find_all('td')[11].text.replace('\n', '')

                # genders
                genders = soup.find_all('td')[13].text.replace('\n', '')

                # base stats (base, min, max): health point, attack, defense, special attack, special defense, speed, total (base)
                hp = int(soup.find_all('td')[15].text.replace('\n', ''))

                atk = int(soup.find_all('td')[19].text.replace('\n', ''))

                defn = int(soup.find_all('td')[23].text.replace('\n', ''))

                sp_atk = int(soup.find_all('td')[27].text.replace('\n', ''))
                
                sp_def = int(soup.find_all('td')[31].text.replace('\n', ''))

                spd =  int(soup.find_all('td')[35].text.replace('\n', ''))

                total = int(soup.find_all('td')[39].text)


                pkm['Name'] = name
                pkm['Type 1'] = type1
                pkm['Type 2'] = type2
                pkm['Species'] = species
                pkm['Height'] = height
                pkm['Weight'] = weight
                pkm['Ability'] = ability
                pkm['Extra Ability'] = ex_ability
                pkm['Hidden Ability'] = hid_ability
                pkm['Catch Rate'] = catch_rate
                pkm['Base Friendship'] = base_fs
                pkm['Base Exp'] = base_exp
                pkm['Growth Rate'] = growth_rate
                pkm['Gender'] = genders
                pkm['HP'] = hp
                pkm['Attack'] = atk
                pkm['Defense'] = defn
                pkm['Sp. Atk'] = sp_atk
                pkm['Sp. Def'] = sp_def
                pkm['Speed'] = spd
                pkm['Total'] = total

            except:
                fail_pkm.put(pkm)

        while True:

            try:
                pkm = input_pkm.get(timeout=1)
            except Exception as e:
                print(e)
                break

            process_pkm(pkm)