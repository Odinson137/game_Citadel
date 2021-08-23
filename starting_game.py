import random, psycopg2
from random import choice
from collections import Counter
from settings import *

from bot import start

class Start_game:
    def __init__(self):
        self.num = 0


    def game(self, ):
        for name in names:
            self.get_name(name)
            self.print_in_builded(name)

        self.get_start_money()
        self.get_random_start_card()

        
        conn.commit()

    def players(self):
        players_cards=[]
        select = " SELECT names FROM cards_players"
        cur.execute(select)
        all = cur.fetchall()
        for one in all:
            players_cards.append(one)
        return players_cards

    def randomer(self, players = ["ассасин", "вор", "чародей", "король", "епископ", "купец", "зодчий", "кондотьер"]):
        random = choice(list(players))
        return random

    def biildings(self, ):
        buildings = []
        select = " SELECT names FROM cards"
        cur.execute(select)
        all = cur.fetchall()
        for one in all:
            buildings.append(one)
        return buildings

        
    # давашка денег всем в начале а может и не только
    def get_start_money(self, id_money=0, money=10):
        while id_money != 5:
            id_money += 1
            update_money_in_baza = "Update all_players set money = %s where id = %s"
            update_money = money, id_money
            cur.execute(update_money_in_baza, update_money)

    in_players_cards = []


    def get_random_start_card(self, middle_card = 'card'):
        first_part_card = "Update all_players set "
        last_part_card = " = %s where id = %s"
        num_card = 1
        while num_card != 5:
            for i in range(len(names)+1):
                random = self.randomer(self.biildings())
                full_card = first_part_card + middle_card + '_' + str(num_card) + last_part_card
                update = random, i
                cur.execute(full_card, update) # загрузка в базу данных
                self.in_players_cards.append(random) # загрузка в cписок для подсчета в ostatok_card

            num_card += 1

    
    def ostatok_card(self, ):
        Bcount = Counter(self.in_players_cards)
        C = []
        for item in self.biildings():
            if Bcount[item] == 0:
                ready_spisok.append(item[0])
            else:
                Bcount[item] -= 1




        print(len(self.biildings()))

    
    def get_name(self, name):
        global num
        self.num += 1
        start(name)
        print(name)
        search_name = " INSERT INTO all_players (player, id) VALUES (%s, %s)"
        values = name, self.num
        cur.execute(search_name, values)


        
    def print_in_builded(self, name):
        insert = " INSERT INTO builded (names) VALUES (" + "'" + name + "'" +  ")"
        cur.execute(insert)

def delete():
    delete = " DELETE FROM all_players"
    cur.execute(delete)
    delete_builded = " DELETE FROM builded "
    cur.execute(delete_builded)

delete()
game = Start_game()
game.game()

