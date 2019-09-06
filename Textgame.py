from Drawing import *
from Characters import *
from Items import *
from Map import *

classes=[Warrior,Paladin,Sorcerer]

def reprint():
    clear()
    drawHP(player)
    if(isinstance(player,Sorcerer)):
        drawHP(player,"blue",True)
    print("")
    for enemy in player.enemies:
        drawHP(enemy,"red")
    print("")

#startGame()
inp = input("name:")
name = colored(inp,colour="blue")
clear()
print("Which class do you choose?")
player = classes[int(choice(classes))]()
player.reprint = reprint
player.name=name
player.nameLength = len(inp)
print()
slowPrint("Good Luck "+player.name,speed=3)
progress()
if(isinstance(player,Sorcerer)):
    clear()
    print("Unlocked "+player.unlockedSpells[0][0].__name__)
progress()

cheat=0
player.enemies = attack(player,[Mechanum]*3)

while True:
    while cheat>player.level:
        player.levelUp(cheat=True)
        unlockEnemy(player,cheat=True)
    while len(player.enemies)>0:
        reprint()
        player.invinsible=0
        player.action()
        for enemy in player.enemies:
            enemy.invinsible=0
        clear()
        player.printMessages()
        i=0
        while(i<len(player.enemies)):
            enemy = player.enemies[i]
            enemy.action()
            enemy.effects()
            enemy.printMessages()
            if(player.hp==0):
                player.die()
            if(not enemy in player.enemies):
                i-=1
                player.printMessages()
            i+=1
        player.effects()
        player.printMessages()

        progress()
    clear()
    player.levelUp()
    player.enemies = Encounter(player)