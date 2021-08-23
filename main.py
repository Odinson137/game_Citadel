import builtins

from razdacha import Razdacha, Vizov, King
from perks import Perks
from random import choice
from collections import Counter
import random, psycopg2
from starting_game import Start_game
from settings import *


class cycle_game():
    def __init__(self):
        self.names = names
        
    # главный цикл
    def cycle(self, ):
        kings = []
        while True:
            razdacha_name = []
            new_round_players = []
            
            raz = Razdacha() # выбор игральной карты для игрока 
            raz.get_name_in_razdacha()  

            number_vizov = Vizov() # каждому игроку присваивается номер, по которому он будет вызываться по номеру его карты
            number_vizov.vizov_player()



            if kings:
                print('kings = ' + kings[0])
                # king.update_kinger(kings[0])
                king = King()
                print('Так как в прошлой игре вы были королём!')
                king.update_king(kings[0])
                kings = []

            conn.commit()
            self.activate_all()
            for player, player_card in self.sort_players():
                print(player)
                if self.search_activate(player) == 1:
                    print(f"{player.title()} - {player_card}, твой ход")
                    if player_card == 'Король':
                        print('Вы - корона')
                        kings.append(player)
                        print(kings)

                    print(f"Способность карты:\n{self.dop_info(player_card)}")
                    self.ifers(player, player_card)
                # ДАЛЬШЕ СДЕЛАТЬ ПРОСТО ФУНКЦИЮ И В НЕЙ МНОЖЕСТВО IF
                conn.commit() # потом удалить возможно для ускорений
                # добаить поле возможностей игрока цифрами 


            if self.len_builded(2):
                    conn.commit()
                    cur.close()
                    conn.close()
                    break

    def dop_info(self, player_card):
        select = " SELECT cards FROM cards_players WHERE names = %s or names = %s "
        value = player_card, player_card
        cur.execute(select, value)
        info = cur.fetchone()
        return info[0]

# давашка денег определенному человку
    def get_money(self, money, player):
        update_money_in_baza = "Update all_players set money = %s where player = %s"
        update_money = money, player
        cur.execute(update_money_in_baza, update_money)

    def activate_all(self):
        update = " UPDATE all_players set activate = 1 "
        cur.execute(update)


    def print_all_buildings_for_player(): # сделать выбор каких карт я хочу закинуть в колоду и доставние из колоды столько же всё рандом
        pass

    def sort_players(self, ):
        select = " SELECT player, player_card FROM all_players ORDER BY players_number "
        cur.execute(select)
        all = cur.fetchall()
        return all


    def read_baza_money(self, name):
        select = " SELECT money FROM all_players WHERE player = %s or player =%s"
        value = name, name
        cur.execute(select, value)
        balance = cur.fetchone()
        return balance[0]


    # ifers 2
    def get_cards_for_colods(self, name=None):
        spisok_for_ostatok = []
        print(ready_spisok)
        for i in range(2):
            
            random = randomer(ready_spisok)
            print(random)
            spisok_for_ostatok.append(random)
        print(spisok_for_ostatok)
        inp = input("Что выбираете? ")

        if inp == spisok_for_ostatok[0]:
            card =  spisok_for_ostatok[0]
            print(card)
            get_to_baza_new_cards(spisok_for_ostatok[0], name)
            ready_spisok.remove(spisok_for_ostatok[0])

        elif inp == spisok_for_ostatok[1]:
            card = spisok_for_ostatok[1]
            print(card)
            get_to_baza_new_cards(spisok_for_ostatok[1], name)
            ready_spisok.remove(spisok_for_ostatok[1])

        else: 
            print('Не выёживайся и выбирай нормально')
            self.get_cards_for_colods(name)


    def coins_for_kvartal(self, name):
        select = " SELECT coins FROM cards WHERE names = %s or names = %s "
        value = name, name
        cur.execute(select, value)
        coins = cur.fetchone()
        if coins:
            return coins


    def search_occupied_cards(self, name): # потом сделать как-то рефакторинг этой и той одинаковой части
        p = []
        for i in range(1, 10):
           
            
            first_select = " SELECT card_" + str(i) + " FROM all_players WHERE player = %s or player = %s "
            value = name, name
            cur.execute(first_select, value)
            item = cur.fetchone()[0]

            if item:
                select = " SELECT color FROM cards WHERE names = %s or names = %s "
                values = item, item
                cur.execute(select, values)
                color = cur.fetchone()
                p.append([item, i, color]) # пото сделать из i элемент в init для всеобщих пользований
                
        return p
        
    def search_free_site_in_builded(self, name):
        for i in range(1, 8):
            first_select = " SELECT card_names_" + str(i) + " FROM builded WHERE names = %s or names = %s "
            value = name, name
            cur.execute(first_select, value)
            item = cur.fetchone()[0]
            
            if item == None:
                return i
        

    # ifers 3
    def build_kvartal(self, name):
        balance = self.read_baza_money(name)
        print(f"Баланс: {balance}")
        name_cards = self.search_occupied_cards(name)
        for name_card in name_cards:
            prise = self.coins_for_kvartal(name_card[0])
            print(f"{name_card[0]} ({name_card[2][0]}) - {prise[0]}")


        x = input('Что вы хотите построить: ')
        # if x in name_cards:
        prise_card = self.coins_for_kvartal(x)[0]
        if prise_card <= balance:
            balance -= prise_card
            update = " UPDATE all_players set money = %s WHERE player = %s"
            value = balance, name
            cur.execute(update, value)
            update = " UPDATE builded set card_names_" + str(self.search_free_site_in_builded(name)) + " = %s WHERE names = %s"
            values = x, name
            cur.execute(update, values)
            print(f"Баланс: {balance}")
            for i in name_cards:
                if i[0] == x:

                    del_card = " UPDATE all_players set card_" + str(i[1]) + " = %s WHERE player = %s "
                    value = None, name
                    cur.execute(del_card, value)
            print('ok')

        else: 
            print('Не хватает денег')
            self.build_kvartal(name)


    def ifers(self, name='name_player', name_card='name_card_player'):
        actvacion = 2
        spisok = ['1) сбор ресурсов \n', '2) сбор карт\n' ,'3) Строительство\n', '4) Способность карты']
        while actvacion != 0:
            print(spisok)
            x = int(input('Что вы хотите сделать: '))
            balance = self.read_baza_money(name)
            
            if x == 1:
                self.get_money(balance+2, name)
                actvacion -= 1
                del spisok[0]
                del spisok[0]
                del spisok[0]

            elif x == 2:
                self.get_cards_for_colods(name)
                actvacion -= 1
                del spisok[0]
                del spisok[0]
                del spisok[0]


            elif x == 3:
                if name_card == 'Зодчий':
                    print('Можете построить сразу три здания!')
                    for i in range(3):
                        self.build_kvartal(name)
                else: self.build_kvartal(name)
                actvacion -= 1
                del spisok[0]
                del spisok[0]
                del spisok[0]

            if x == 4:
                print('Здесь будет способность карт которая потом возвражает в это же меню')
                perk = Perks(name, balance)
                perk.perks_of_players()
                conn.commit()
                actvacion -= 1
                if len(spisok) == 4:
                    del spisok[3]
                else: spisok[0]

            conn.commit()

            # потом сделать передачу остатка карт в 4

        else:
            pass

    def len_builded(self, number=7):
        lens = len(names)
        print(lens)
        if lens <= 4:
            nums = number #7
        
        dop = str(nums)
        select = " SELECT card_names_" + dop + " FROM builded" #  WHERE names = %s or names = %s 
        cur.execute(select)
        lensing = cur.fetchall()
        for lenes in lensing:
            if lenes[0]:
                return  1
        return

                
            

    def search_activate(self, name):
        select = " SELECT activate FROM all_players WHERE player = %s or player = %s"
        value = name, name
        cur.execute(select, value)
        status = cur.fetchone()
        return status[0]


        
def delete():
    delete = " DELETE FROM all_players"
    cur.execute(delete)
    delete_builded = " DELETE FROM builded "
    cur.execute(delete_builded)

def starts():
    delete() # очищения базы от всей лишней фигни от прошой игры

    starting = Start_game() # получение начальной инфы для игры(начальные деньги и тд)
    starting.game()

    start_cycle = cycle_game() # начало полноценной игры с раунздами
    start_cycle.cycle()
    # conn.commit()
    # cur.close()
    # conn.close()

starts()

