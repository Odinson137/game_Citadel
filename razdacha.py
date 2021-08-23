
from collections import Counter
from os import P_OVERLAY
from settings import *


# получение новых карт каждый новый раунд
class Razdacha:
    
    def __init__(self):
        self.new_round_players = []
        self.razdacha_name = []

    def get_name_in_razdacha(self):
        self.print_card_round()
        self.cards_in_game()
        for name in names:
            self.razdacha(name)

    def razdacha(self, name):
        # new_round_players = []
        get_card_to_baza = "Update all_players set player_card = %s where player = %s"
        print(self.new_round_players)
        
        while True:
            # player_name = input("Выберите персножа: ")
            player_name = randomer(self.new_round_players)
            # player_name = input('Имя: ')
            if player_name in self.new_round_players:
                if player_name not in self.razdacha_name:
                    value = player_name, name
                    cur.execute(get_card_to_baza, value)
                    self.razdacha_name.append(player_name)
                    print(self.razdacha_name)
                    break


    def len_open_and_closed_cards(self): # потом сделать здесь разбивку на кол игроков
        if len(names) == 4:
            return 2
        if len(names) == 5:
            return 1
        if len(names) == 6:
            return 1
        if len(names) <= 6:
            return 0

    def print_card_round(self, open_cards=2, closed_cards=1):
        get_card = []
        open_cards = self.len_open_and_closed_cards()
        # CLOSED CARDS
        random = randomer().lower()
        if random != 'король':
            get_card.append(random)
        else:
            self.print_card_round()

        # OPEN CARDS
        while len(get_card)-1 != open_cards:
            random = randomer().title()
            if random != 'король':
                if random not in get_card:
                    get_card.append(random)

    def players(self):
        players_cards=[]
        select = " SELECT names FROM cards_players"
        cur.execute(select)
        all = cur.fetchall()
        for one in all:
            players_cards.append(one)
        return players_cards

    # players - get_card 
    def cards_in_game(self, ): # определяет карты для игроков после print_card_round и return список с игроками
        Bcount = Counter(get_card)
        for item in self.players():
            for i in item:
                if Bcount[i] == 0:
                    self.new_round_players.append(i)
            else:
                Bcount[i] -= 1

# определение порядка вызова игроков
class Vizov:
    def search_number_player(self, name):
        select = " SELECT number FROM cards_players WHERE names = %s OR names = %s"
        value = name, name
        cur.execute(select, value)
        number = cur.fetchone()[0]
        return number

    def number_for_players(self, number, name):
        update = " UPDATE all_players set players_number = %s WHERE player_card = %s"
        value =  number, name
        cur.execute(update, value)

    def vizov_player(self):
        select = " SELECT player_card FROM all_players "
        cur.execute(select)
        pr = cur.fetchall()
        print(pr)

        for p in pr:
            number = self.search_number_player(p)
            self.number_for_players(number, p)
        
class King:
    def update_kinger(self, player):
        update = " UPDATE all_players set king = '+' WHERE player = %s or player = %s"
        value = player, player
        cur.execute(update, value)
        print('ok')

    def update_king(self, player):
        update = " UPDATE all_players set players_number = %s WHERE player = %s"
        value = 0, player
        cur.execute(update, value)
        update = " UPDATE all_players set king = 'None' "
        cur.execute(update)

    def search_kinger(self):
        for i in names:
            select = " SELECT king FROM all_players WHERE player = %s or player = %s "
            value = i, i
            cur.execute(select, value)
            read = cur.fetchone()[0]
            print(read)
            if read == '+':
                update = " UPDATE all_players set players_number = %s WHERE player = %s"
                value = 0, i
                cur.execute(update, value)
                update = " UPDATE all_players set king = 'None' "
                cur.execute(update)
                return
                conn.commit()
            print('ok')


# raz = Razdacha()
# raz.get_name_in_razdacha()
# conn.commit()

# razx = Vizov()
# razx.vizov_player()
# conn.commit()

# king = King()
# king.update_kinger('yura')
# conn.commit()

# king = King()
# king.search_kinger()
# conn.commit()