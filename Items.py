from Drawing import *
import random
Global.items=[]


class Item():
    def __init__(self):
        self.itemClass = None
        self.level = 1
        self.type = "Item"
        self.weight = 1
        self.name = "Item"
        self.element = None
        self.usable=False
        self.typeColor="yellow"
    def equip(self,player):
        slowPrint(player.name+" equips "+self.name)
        player.items.append(self)
    def pickup(self,player):

        weight=0
        for item in player.items:
            if(item.itemClass==self.itemClass):
                weight+=item.weight
        if(weight+self.weight<=player.itemLimits[self.itemClass]):
            self.equip(player)
        else:
            slowPrint(player.name+", you are carrying too many "+self.itemClass+" items")
            progress()
            a=binary(first="unequip some items",ai=player.ai)
            if(a=="0"):
                while(weight>player.itemLimits[self.itemClass]):
                    items = [item for item in player.items if item.itemClass==self.itemClass]
                    item = choosetargets(items,action="discard",name="item")
                    weight-=item.weight
                    item.remove()
            else:
                slowPrint(player.name+" discards "+self.name)

    def Use(self):
        pass
    def remove(self,player):
        slowPrint(player.name+" discards "+self.name)
        player.items.remove(self)
    def genName(self):
        self.gname(self.name)
    def returnName(self):
        return self.name+" ("+colored(self.type,colour=self.typeColor)+")"
    def gname(self,name):
        self.name = colored(name,colour="yellow")

class Sword(Item):
    def __init__(self):
        Item.__init__(self)
        self.itemClass = "hand"
        self.type = "Sword"
        self.weight = 2
        self.genName()
        self.modifier = 3
    def equip(self,player):
        slowPrint(player.name+" equips "+self.returnName())
        player.damagestandard+=self.modifier
        player.items.append(self)
    def Use(self):
        pass
    def remove(self,player):
        slowPrint(player.name+" discards "+self.returnName())
        player.damagestandard-=self.modifier
        player.items.remove(self)
    def genName(self):
        name="Sword of generic Nonsense"
        self.gname(name)