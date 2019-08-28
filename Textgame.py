from Drawing import *
from Characters import *
from Items import *
from Map import *
cheat=0
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
#player.enemies=attack(player,[Spirit]*5)

while True:
    while cheat>player.level:
        player.levelUp(cheat=True)
        unlockEnemy(player,cheat=True)
    while len(player.enemies)>0:
        reprint()
        player.action()
        player.effects()
        if(isinstance(player,Sorcerer)):
            player.mana = min(player.maxmana,player.mana+player.managrowth)
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

        progress()
    clear()
    player.levelUp()
    player.enemies = Encounter(player)