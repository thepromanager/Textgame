from Drawing import *
from Characters import *
from Items import *
from Map import *
cheat=60
classes=[Warrior,Paladin]

def reprint():
    clear()
    drawHP(player)
    for enemy in player.enemies:
        drawHP(enemy,"red")

#startGame()
name = colored(input("name:"),colour="blue")
clear()
print("Which class do you choose?")
player = classes[int(choice(classes))]()
player.reprint = reprint
player.name=name
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
        clear()
        player.printMessages()
        for enemy in player.enemies:
            enemy.action()
            enemy.printMessages()
            if(player.hp==0):
                player.die()
        progress()
    clear()
    player.levelUp()
    player.enemies = Encounter(player)