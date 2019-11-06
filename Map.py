import random
from Drawing import *
from Characters import *

Global.enemyTypes = [Critter,Bat,Faerie,Orc,Robotum,Wolf,Roc,Vampire,Spirit,Summoner,Pyromaniac,Mechanum,Witch,Hydra,Demon]
Global.enemyTypes.sort(key=lambda x:(x().level))
Global.enemies=[]

def generateEnemy(type):
    enemy = type()
    enemy.genName()
    slowPrint("Suddenly a wild "+enemy.type+" appears!",speed=4)
    return enemy
def encounter():
    level=sum([player.level for player in Global.players])
    level = level + 5*len(Global.players)
    levelList = [enemy().level for enemy in Global.enemyTypes]
    Global.enemies=[]
    enemies=[]
    clear()
    while level>0:
        availableEnemies = [element for element in levelList if element<=level]
        chosenIndex = random.randint(0,len(availableEnemies)-1)
        level-=availableEnemies[chosenIndex] 
        enemy = generateEnemy(Global.enemyTypes[chosenIndex])
        enemies.append(enemy)
    

    if(sum([player.level for player in Global.players])%6==0):
        enemies[0].bossify()
        slowPrint("One of the enemies has enhanced strength, be careful",speed=1.5)    
    progress()
    random.shuffle(enemies)
    Global.enemies = Global.enemies+enemies

def attack(enemiesTypes):
    enemies=[]
    for enemyType in enemiesTypes:
        enemy = enemyType()
        enemy.genName()
        enemies.append(enemy)
    return enemies

def town(player):
    pass
    # Information
    # Inventory
    # Rest
    # Quests
    # Event
    # Dungeon
    # Shop
    # Boss
    # Adventure
    # time
    # Money
class Event():
    def __init__(self):
        self.level = 1
    def encounter(self):
        pass
    def reward(self):
        pass
