import shutil
import time
import re
def drawHP(character,colour="green"):
    hp = character.hp
    diff = (character.maxhp-character.hp)
    print(character.returnName(), colored(ucode("25A0")*hp+ucode("25A1")*diff,colour=colour), hp, "/", hp+diff)
def progress():
    input("Press Enter to continue: ")
    pass
def block():
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    return ("."*columns+"\n")*(rows-1)
def clear():
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    print("\n"*(rows-1))
def slowPrint(string,speed=1,end="\n"):
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
    for action in actions:
        actionName=action
        if(callable(action)):
            actionName = action.__name__
        elif(not isinstance(action,str)):
            actionName = action.__dict__["name"]          
        print(colored(str(actions.index(action))+":",colour="blue"),actionName)
    return input(colored("choose: ",colour="blue"))
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
    slowPrint("Welcome to The Best Textgame\n")
    slowPrint("In this game you play as an adventurer on a mission to kill all the monsters in this grim world\nTo start the game enter your name",1.5)