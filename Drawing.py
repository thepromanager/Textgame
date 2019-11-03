import shutil
import time
import re

class Global():
    enemies = []
    players = []

def reprint():
    clear()
    arts=[]
    for enemy in Global.enemies:
        arts.append(enemy.art)
    for i in range(5):
        s=""
        for art in arts:
            s+=art[i]+" "
        print(s)
   
    print("\n"*3)
    for player in Global.players:
        drawHP(player)
        if(player.__class__.__name__=="Sorcerer"):
            drawHP(player,"blue",True)
    print("")
    for enemy in Global.enemies:
        drawHP(enemy,"red") 
    print("")


def drawHP(character,colour="green",mana=False):
    hp = character.hp
    diff = (character.maxhp-character.hp)
    filled = ucode("25A0")
    unfilled = ucode("25A1")
    name = character.returnName()
    if(mana):
        hp = character.mana
        diff = (character.maxmana-character.mana)
        filled = ucode("25CF")
        unfilled = ucode("25CB")
        name = character.nameLength*" "
    print(name, colored(filled*hp+unfilled*diff,colour=colour), hp, "/", hp+diff,"🔥"*character.fire,("("+colored("stun "+str(character.stun),colour="yellow")+")")*(not not character.stun))

def progress():
    input("Press Enter to continue: ")
    pass
def block():
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    return ("."*columns+"\n")*(rows-1)
def clear():
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    print("\n"*(rows-1))
def slowPrint(string,speed=4,end="\n"):
    colorchange = re.compile(r"(\x1b\[[0-9][0-9]*;[0-9][0-9]*;[0-9][0-9]*m)")
    stringList = re.split(colorchange,string)
    for strg in stringList:
        if(colorchange.match(strg)):
            print(strg,end="")
        else:
            for character in strg:
                print(character,end="",flush=True)
                time.sleep((1/speed)/10)
    print("",end=end)
def changeColor(colour="green",bcolor="black",style="no effect",returnString=False):
    colors = ["black","red","green","yellow","blue","purple","cyan","white"]
    styles = ["no effect", "bold", "underline"]
    colour = 30 + colors.index(colour)
    bcolor = 40 + colors.index(bcolor)
    style = styles.index(style)
    string = "\033[{};{};{}m".format(style,colour,bcolor)
    if(returnString): return string
    print(string,end="")
def colored(string,colour="green",bcolor="black",style="no effect"):
    return changeColor(colour=colour,bcolor=bcolor,style=style,returnString=True)+string+changeColor(returnString=True)
    pass
def ucode(character):
    return chr(int(character,base=16))
    pass
def choice(actions):
    if(len(actions)==1):
        return "0"
    for action in actions:
        actionName=action
        if(callable(action)):
            actionName = action.__name__
        elif(isinstance(action,tuple)):
            actionName = action[0].__name__
        elif(not isinstance(action,str)):
            if("name" in action.__dict__):
                actionName = action.__dict__["name"]
            else:
                actionName=action.__class__.__name__          
        print(colored(str(actions.index(action))+":",colour="blue"),actionName)
    return input(colored("choose: ",colour="blue"))

def chooseTargets(targets,number=1,name="target",action="choose"):
    targets = targets[:]
    targetsSelected = 0
    if(len(targets)<=number):
        targetsSelected = number
        chosenTargets = targets
    else:
        chosenTargets=[]
        reprint()
        while targetsSelected < number:
            print("Which "+name+" do you want to "+action+"?")
            chosenTarget = choice(targets)                          
            if(chosenTarget in [str(i) for i in range(0,len(targets))]):
                targetsSelected+=1
                chosenTargets.append(targets[int(chosenTarget)])
                targets.remove(targets[int(chosenTarget)])
                reprint()
            else:
                reprint()
                print("Invalid Input")
    clear()        
    return chosenTargets
def startGame():
    clear()
    changeColor(colour="blue")
    print(" _______ _            ____            _     _______        _                             ")
    print("|__   __| |          |  _ \          | |   |__   __|      | |                            ")
    print("   | |  | |__   ___  | |_) | ___  ___| |_     | | _____  _| |_ __ _  __ _ _ __ ___   ___ ")
    print("   | |  | '_ \ / _ \ |  _ < / _ \/ __| __|    | |/ _ \ \/ / __/ _` |/ _` | '_ ` _ \ / _ \ ")
    print("   | |  | | | |  __/ | |_) |  __/\__ \ |_     | |  __/>  <| || (_| | (_| | | | | | |  __/")
    print(r"   |_|  |_| |_|\___| |____/ \___||___/\__|    |_|\___/_/\_\\__\__, |\__,_|_| |_| |_|\___|")
    print("                                                               __/ |                     ")
    print("                                                              |___/                      ")
    changeColor()
    slowPrint("Welcome to The Best Textgame\n",speed=1)
    slowPrint("In this game you play as an adventurer on a mission to kill all the monsters in this grim world\nTo start the game enter your name",speed=1.5)