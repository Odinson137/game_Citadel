import psycopg2
from random import choice


conn = psycopg2.connect("dbname=ddqjssbfv2l586 user=esglikdemrphdb host=ec2-44-196-250-191.compute-1.amazonaws.com password=2f1d952066d22ec58acd197f13a434b1f948e45dbd3344e2fbff7f243a81d089 port=5432")
cur = conn.cursor()

names = ['Maz', 'Jeck']

num = 0

ready_spisok = []

killed = ''

get_card=[]


def biildings():
    buildings = []
    select = " SELECT names FROM cards"
    cur.execute(select)
    all = cur.fetchall()
    for one in all:
        buildings.append(one)
    return buildings

def randomer(players = ["ассасин", "вор", "чародей", "король", "епископ", "купец", "зодчий", "кондотьер"]):
    random = choice(list(players))
    return random

def search_in_baza_free_dop_card(name):
    for i in range(1, 10):
        first_select = " SELECT card_" + str(i) + " FROM all_players WHERE player = %s or player = %s "
        value = name, name
        cur.execute(first_select, value)
        item = cur.fetchone()[0]
        
        if not item:
            return i
            
def get_to_baza_new_cards(card, name):
    print(len(ready_spisok))
    number = search_in_baza_free_dop_card(name)
    update = " UPDATE all_players set card_" + str(number) +  " = %s WHERE player = %s "
    value = card, name 
    cur.execute(update, value)
    conn.commit()

def search_free_site_in_builded(name):
    for i in range(1, 8):
        first_select = " SELECT card_names_" + str(i) + " FROM builded WHERE names = %s or names = %s "
        value = name, name
        cur.execute(first_select, value)
        item = cur.fetchone()[0]
        
        if item == None:
            return i
