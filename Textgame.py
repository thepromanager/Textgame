from Drawing import *
from Characters import *
from Items import *
from Map import *


#startGame()
def newPlayer(): 
    inp = input("name:")
    name = colored(inp,colour="blue")
    clear()
    race= chooseTargets(Global.races,name="race")[0]
    player = chooseTargets(Global.classes,name="class")[0](race)
    player.namestandard=name
    player.nameLength = len(inp)
    Global.players.append(player)
    print()
    slowPrint("Good Luck "+player.name,speed=3)
    progress()
    #if(isinstance(player,Sorcerer)):
     #   clear()
      #  print("Unlocked "+player.unlockedSpells[0][0].__name__)
       # progress()
for i in range(int(input("Number of players:"))):
    newPlayer()
cheat=0
#Global.enemies = attack([Witch]*3)

while True:    
    for player in Global.players:
        while cheat>player.level:
            player.levelUp(cheat=True)
            unlockEnemy(player,cheat=True)
    while len(Global.enemies)>0:
        for player in Global.players:
            player.invinsible=0
            if(len(Global.enemies)>0):
                player.passive()
                player.action()
                player.effects()
                if((not Global.players[-1]==player) or (len(Global.enemies)==0)):
                    progress()

        for enemy in Global.enemies:
            enemy.invinsible=0
        i=0
        if(len(Global.enemies)>0):
            while(i<len(Global.enemies)):
                enemy = Global.enemies[i]
                enemy.passive()
                enemy.action()
                enemy.effects()
                if(not enemy in Global.enemies):
                    i-=1
                i+=1
            progress()
    clear()
    for player in Global.players:
        player.levelUp()
    encounter()