import random
from Drawing import *
from Characters import *

enemyTypes = [Critter,Bat,Orc,Robotum,Roc,Vampire,Spirit,Summoner]
unlockedEnemyTypes=[]
def generateEnemy(player,type):
    enemy = type()
    enemy.genName()
    enemy.player=player
    slowPrint("Suddenly "+"a"+" wild "+enemy.type+" appear!",speed=4)
    return enemy
def unlockEnemy(player,cheat=False):
    if(len(enemyTypes)>0):
        for enemyType in enemyTypes:
            if(enemyType().level<=player.level):
                if(not enemyType in unlockedEnemyTypes):
                    unlockedEnemyTypes.append(enemyType)
def Encounter(player):
    unlockEnemy(player)
    enemies=[]
    clear()
    enemy = generateEnemy(player,random.choice(unlockedEnemyTypes))
    if(player.level%5==0):
        enemy.bossify()
        slowPrint("This enemy has enhanced strength, be careful",speed=1.5)
    enemies.append(enemy)
    for i in range(player.level//5):
        enemy = generateEnemy(player,random.choice(unlockedEnemyTypes))
        enemies.append(enemy)      
    progress()    
    return enemies
def attack(player,enemiesTypes):
    enemies=[]
    for enemyType in enemiesTypes:
        enemy = enemyType()
        enemy.genName()
        enemy.player=player
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
        self.enemies = []
    def encounter(self):
        pass
    def reward(self):
        pass