import builtins
import psycopg2
from random import choice

from settings import *

conn = psycopg2.connect("BAZA port=5432")
cur = conn.cursor()


def biildings():
    buildings = []
    select = " SELECT names FROM cards"
    cur.execute(select)
    all = cur.fetchall()
    for one in all:
        buildings.append(one)
    return buildings

def randomer(cards):
    random = choice(list(cards))
    return random

def read_baza_money(name):
    select = " SELECT money FROM all_players WHERE player_card = %s or player =%s"
    value = name, name
    cur.execute(select, value)
    balance = cur.fetchone()
    return balance[0]

# давашка денег определенному человку
def get_money(money, player):
    update_money_in_baza = "Update all_players set money = %s where player_card = %s"
    update_money = money, player
    cur.execute(update_money_in_baza, update_money)


def what_player(name):
    select = " SELECT player_card FROM all_players WHERE player = " + "'" + name + "'"
    cur.execute(select)
    who = cur.fetchone()
    print(who)
    return who[0]

class Perks:

    def __init__(self, name, balance=8):
        self.name = name
        self.balance = balance
        self.player_name = what_player(name)
        self.killed = killed
        # self.magic_spisok = magic_spisok

    def perks_of_players(self):
        print(self.name)
        print(f"Ваш баланс: {self.balance}")
        print(self.player_name)
        if self.player_name == 'Ассасин': #1
            for i in names:
                if i != self.name:
                    print(i)   
            self.killed = input('Кого хотите убить: ')
            self.disactivate_one(self.killed)

        elif self.player_name == 'Вор': #2
            thiefed = input('У кого хотите всё украсть: ')
            if what_player(thiefed) != 'Ассасин' and what_player(thiefed) != self.killed:
                self.thief(thiefed)
            else:
                print('К сожалению это невозоможно. Я постарасю и приложу все усилия на то, что бы вы снова были убийцем в следующем раунде и покарали этих говнюков')

        elif self.player_name == 'Чародей': #3
            magic = int(input('Вы хотите поменяться картами с другим игроком или выложить свои любые карты под низ колоды и взять столько же новые:'))
            if magic == 1:
                print(names)
                magic_killed = input('Кто же этот везунчик: ') # здесь в будущем отобразить кнопки с именами игроков
                self.magicer_trade(magic_killed)

            if magic == 2:
                self.print_all_buildings_for_player()

            conn.commit() 

        elif self.player_name == 'Король': #4
            print('Теперь вы - Корона')
            self.colored('жёлтый')

        elif self.player_name == 'Епископ': #5 # bishop у него нельяз сломать кварталы, кондотьер, это тебя касается
            self.colored('синий')

        elif self.player_name == 'Купец':
            print('Вы получаете одно золото за карту Купца')
            balance = read_baza_money(self.player_name)
            get_money(balance+1, self.player_name)
            self.colored('зелёный')

        elif self.player_name == 'Зодчий':
            builders = biildings()
            random = randomer(builders)[0]
            get_to_baza_new_cards(random, self.name)

        elif self.player_name == 'Кондотьер':
            self.colored('красный')
            self.Condottiere()

        conn.commit()


    def dop_colors(self, colors, i):
        select = " SELECT " + "card_names_" + str(i) + " FROM builded WHERE names = " + "'" + self.name + "'"
        cur.execute(select)
        card = cur.fetchone()[0]
        if card:
            selects = " SELECT color FROM cards WHERE names = %s or names = %s "
            value = card, card
            cur.execute(selects, value)
            color = cur.fetchone()[0]
            if color == colors:
                return card

    def colored(self, colors):
        coins = 0
        for i in range(1, 9):
            card = self.dop_colors(colors, i)
            if card:
                coins += 1
                print(f"Вы получаете один золотой за квартал - {card}")
                balance = read_baza_money(self.name)
                
                get_money(balance+1, self.name)
        print(f"Вы получаете {coins} за ваши кварталы")
            # else: print('Кварталов с нужным цветом вы не имеете, а потому больще ничего не получаете')


    def who_are_you(self, name=''):
        if name == '':
            name = self.name
        select = " SELECT player FROM all_players WHERE player_card = " + "'" + name + "'"
        cur.execute(select)
        who = cur.fetchone()
        print(who)
        return who[0]

    # perki_assasin 
    def activate_one(self, killed):
        update = " UPDATE all_players set activate = 1 WHERE player = " + "'" + killed + "'"
        cur.execute(update)

    def disactivate_one(self, killed):
        update = " UPDATE all_players set activate = 0 WHERE player = %s or player = %s"
        value = killed, killed
        print(update)
        cur.execute(update, value)

    # perks_thief
    def thief_dop(self, thief_name=''):
        select = " SELECT money FROM all_players WHERE player = " + "'" + thief_name + "'"
        cur.execute(select)
        get_thief_coins = cur.fetchone()[0]
        return get_thief_coins


    def thief(self, thief_name):
        get_thief_coins = self.thief_dop(thief_name)
        update = " UPDATE all_players set money = 0 WHERE player = " + "'" + thief_name + "'"
        cur.execute(update)    
        
        thief_coins = self.thief_dop(self.name)
        sums = str(thief_coins + get_thief_coins)
        print(sums)
        update = " UPDATE all_players set money = " + sums + " WHERE player_card = " + "'" + self.name + "'"
        cur.execute(update)

    # perks_magic
    def search_card_for(self, name='Чародей'):
        if name == 'Чародей':
            name = self.name

        print(name)
        magic_spisok = []

        for i in range(1, 11):
            
            select = " SELECT card_" + str(i) + " FROM all_players WHERE player = " + "'" + name + "'" # вынести эти штуки потом в кассе инит
            cur.execute(select)
            magic_card = cur.fetchone()[0]
            if magic_card:
 
                magic_spisok.append([magic_card, i])
        print(magic_spisok)
        
        return magic_spisok

    def magicion_for(self, name, magic_spisok):
        nums = 1
        for item in magic_spisok:
            update = " UPDATE all_players set card_" + str(nums) + " = %s WHERE player = %s "
            nums += 1
            value = item[0], name
            cur.execute(update, value)

    def magicer_trade(self, magic_killed):

        magic_spisok = self.search_card_for((self.player_name))

        magic_spisok_for_killed = self.search_card_for(magic_killed)

        self.magicion_for(self.player_name, magic_spisok_for_killed)

        self.magicion_for(magic_killed, magic_spisok)

        conn.commit()

    
    def print_all_buildings_for_player(self): # сделать выбор каких карт я хочу закинуть в колоду и доставние из колоды столько же всё рандом
        p = []
        magic_spisok = self.search_card_for(self.player_name)
        print(magic_spisok) 
        
        while True:
            if x == 'q':
                break
            x = input("Какие карты вы хотите закинуть в колоду: ") # потом убрать int
            p.append(x)

        print(p)
        for i in range(len(p)):
            print(magic_spisok[i][1])
            update = " UPDATE all_players set card_" + str(magic_spisok[i][1]) + " = %s WHERE player_card = %s"
            value = randomer(biildings())[0], self.name
            cur.execute(update, value)

    def king(self):
        pass

    # bishop 5 у него нельяз сломать кварталы, кондотьер, это тебя касается
    def bishop(self):
        pass

    def Condottiere(self):
        buil = []
        select = " SELECT player, player_card FROM all_players "
        cur.execute(select)        
        cards = cur.fetchall()
        print(cards)
        for card, player_card in cards:
            builded_building = self.search_buildeds(card)
            if not builded_building:
                builded_building = 'Пусто'

            else: buil.append(card)

            if card == self.name:
                print(f"Я - {player_card} - {builded_building}")

            elif player_card != 'Епископ':
                print(f"{card.title()} - {player_card} - {builded_building}")

        if buil:    
            fail = self.dop_Condottiere()
            if fail == 'отмена':
                print(fail)
                return 'отмена'
        else: print("Ещё ни у кого нет кварталов")


    def search_buildeds(self, name):
        p = []
        for i in range(1, 8):
            select = " SELECT card_names_" + str(i) + " FROM builded WHERE names = %s or names = %s "
            value = name, name
            cur.execute(select, value)
            item = cur.fetchone()[0]
            if item:
                p.append(item)
            return(item)

    def dop_Condottiere(self):
        p = []
        x = input('Чей квартал вы хотите снести? ').lower()
        if x.lower() == 'свой' or x.lower() == 'я':
            x = self.name
        elif x == 'q':
            return 'отмена'
        for i in range(1, 9):
            select = " SELECT card_names_" + str(i) + " FROM builded WHERE names = %s or names = %s"
            value = x, x
            cur.execute(select, value)
            cards = cur.fetchone()[0]
            if cards:
                select_builded_coins = " SELECT coins FROM cards WHERE names = %s or names = %s "
                value = cards, cards
                cur.execute(select_builded_coins, value)
                builded_coins = cur.fetchone()[0]
                print(f"Снести квартал {cards} будет стоить {builded_coins-1} золотых")
                p.append([cards, i, builded_coins-1])

        self.update_Condottiere(p, x)
        

    def update_Condottiere(self, p='', x=''):
        if not p:
            print('Пусто. Выберите другого игрока!')
            self.dop_Condottiere()
        choice_card = input('Какой квартал вы хотите снести? ')
        for min_p in p:
            if choice_card == min_p[0]:        
                if self.balance >= min_p[2]-1:
                    update = " UPDATE builded set card_names_" + str(min_p[1]) + " = %s WHERE names = %s"
                    value = None, x
                    cur.execute(update, value)
                    print(self.balance-min_p[2]-1)
                    self.minus_money_Condottiere(self.balance-(min_p[2]))
                else: 
                    print('Не хватает денег')
                    self.update_Condottiere(p, x)
                
    def minus_money_Condottiere(self, coins):
        minus = " UPDATE all_players set money = %s WHERE player_card = %s"
        value = coins, self.name
        cur.execute(minus, value)
        print('Удалён')

