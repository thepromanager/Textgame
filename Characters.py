import random
from Drawing import *
import math

#Main classes
class Character:
    def __init__(self):
        self.itemLimits={"hand":2,"head":1,"body":1,"legs":1,"feet":2,"eye":2,"neck":1,"arm":2,"fingers":10}
        self.armorPierce = 0
        self.invincible = 0
        self.nameLength = 0
        self.maxhpstandard = 10
        self.maxhp = 10
        self.hp = self.maxhp
        self.damage = 4
        self.damagestandard=4
        self.damageVariance = 2
        self.healing = 2
        self.accuracy = 0.9
        self.accuracystandard = 0.9
        self.healingVariance = 2
        self.messages = []
        self.items = []
        self.name = ""
        self.armor = 0
        self.armorstandard = 0
        self.stun = 0
        self.fire = 0
        self.fireResistance=0
        self.magicDamage = 2
        self.magicDamagestandard = 2
        self.fireDamage = 1
        self.passives=[]
        self.realDamage = lambda damage:damage
        self.damageFunctions=[self.realDamage]
        self.flying = False
        self.holy=False
        self.evil=False
        self.morphs=0
    def hurt(self, damage,armorPierce=0):
        if(not self.invincible):
            self.hp=max(0,self.hp-max(0,damage-max(self.armor-armorPierce,0)))
            if(self.hp==0):
                self.die()
        else:
            slowPrint(self.name+"  is invincible")
    def passive(self):
        for Passive in self.passives:
            Passive()
    def effects(self):
        self.morphs=0
        if(self.fire>self.fireResistance and not self.invincible):
            slowPrint(self.name+" takes "+str(self.fire-self.fireResistance)+" fire damage")
            self.hp=max(0,self.hp-max(0,self.fire-self.fireResistance))
            if(self.hp==0):
                self.die()
    def Heal(self):
        heal = self.healing + random.randint(-self.healingVariance, self.healingVariance)
        newhp = min(self.maxhp,self.hp+heal)
        slowPrint(self.name+" healed from {}hp to {}hp".format(self.hp, newhp))
        self.hp=newhp
class Player(Character):
    def __init__(self):       
        Character.__init__(self)
        self.maxhpstandard = 15 
        self.level = 0
        self.name = "player"
        self.namestandard = "player"
        self.actions = [self.Heal,self.Attack]
        self.ai=False
    def setStats(self):
        self.realDamage=compose(self.damageFunctions)
        self.maxhp=self.maxhpstandard
        self.hp=self.maxhp
        self.armor=self.armorstandard
        self.accuracy=self.accuracystandard
        self.damage=self.damagestandard
        self.magicDamage=self.magicDamagestandard
        self.fire = 0
        self.name = self.namestandard
    def Use(self):
        pass
    def returnName(self):
        return self.name
    def hurt(self,damage,armorPierce=0):
        self.hp=max(0,self.hp-max(0,damage-max(self.armor-armorPierce,0)))
        if(self.hp==0):
            self.die()

    def die(self):
        slowPrint("You are dead "+self.name,speed=0.5)
        for player in Global.players:
            print("name",player.name,"level",player.level)
        progress()
        exit()
    def action(self): 
        if(self.stun==0):
            chooseTargets(self.actions,name="action",action="pursue, "+self.name,ai=self.ai)[0]()
        else:
            self.stun=self.stun-1
            clear()
            print("You are stunned")
            progress()
    def levelUp(self,cheat=False):
        self.setStats()
        self.level+=1
        if(self.level>1):
            clear()
            print(self.returnName())
            print("damage:",self.damage)
            print("healing:",self.healing)
            print("maxhp:",self.maxhp)
            print("You leveled up from",self.level-1,"to",self.level)
            print("What do you want to level up?")
            didAction = False
            traits=["damage","healing","maxhp"]
            chosenAction = choice(traits)
            while didAction == False:            
                if(chosenAction in [str(i) for i in range(0,len(traits))]):
                    didAction = True
                    if(chosenAction=="0"):
                        self.damagestandard=self.damagestandard+1
                    if(chosenAction=="1"):
                        self.healing=self.healing+1
                    if(chosenAction=="2"):
                        self.maxhpstandard=self.maxhpstandard+1
                else:
                    clear()
                    print("damage:",self.damage)
                    print("healing:",self.healing)
                    print("maxhp:",self.maxhp)
                    print("You leveled up from",self.level-1,"to",self.level)
                    print("What do you want to level up?")
                    print("Invalid Input")
                    chosenAction = choice(traits)
            clear()
            self.setStats()
    def Attack(self):
        chosenEnemy = chooseTargets(Global.enemies,name="enemy",action="attack",ai=self.ai)[0]
        damage = self.realDamage(self.damage) + random.randint(-self.damageVariance, self.damageVariance)

        if(self.accuracy > random.random()):
            
            
            if(self.holy and chosenEnemy.evil):
                damage*=2
                slowPrint("Faithful players are super effective against evil types")
            slowPrint(self.name+" attacks "+ chosenEnemy.returnName() + " for "+str(damage)+"hp")
            chosenEnemy.hurt(damage)
        else:
            slowPrint(self.name+" misses an attack")
class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.type = "Generic"
        self.typeColor = "red"
        self.name = colored("Enemy",colour="red")
        self.actions = [self.Heal,self.Attack]
        self.art = ["??"]*5
    def Morph(self):
        if(self.morphs==0):
            chosenType=random.choice(Global.enemyTypes)
            while(chosenType==Shapeshifter):
                chosenType=random.choice(Global.enemyTypes)
            slowPrint(self.name+" morphs into a "+chosenType.__name__)
            hp=self.hp
            maxhp=self.maxhp
            name=self.name
            morph=self.Morph
            new=chosenType()
            new.hp=hp
            new.maxhp=maxhp
            new.name=name
            new.type="Shapeshifter "+new.type
            new.morphs=1
            new.passives.append(new.Morph)
            Global.enemies[Global.enemies.index(self)]=new
    def returnName(self):
        return self.name+" ("+colored(self.type,colour=self.typeColor)+")"
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while(self.actions[v]==self.Heal and self.hp==self.maxhp):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            slowPrint(self.name+" is stunned")
            self.stun=self.stun-1
    def Attack(self):
        damage = self.damage + random.randint(-self.damageVariance, self.damageVariance)
        if(self.accuracy > random.random()):
            player = random.choice(Global.players)

            slowPrint(self.name+" attacks "+ player.name + " for "+str(damage)+"hp")
            player.hurt(damage,armorPierce=self.armorPierce)
        else:
            slowPrint(self.name+" misses an attack")
    def die(self):
        slowPrint(self.name+" dies")
        Global.enemies.remove(self)
    def description(self):
        slowPrint("Generic Monster found nowhere")
    def gname(self,name):
        self.name = colored(name,colour="red")
    def bossify(self):
        self.maxhp = self.maxhp*2
        self.hp = self.hp*2
        self.damage = self.damage*2
        self.healing = self.healing*2
        self.type = self.type+" boss"
        self.typeColor = "purple"

#Enemy types
class Critter(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.level=1
        self.hp=3
        self.maxhp=3
        self.type="Critter"
        self.damage=1
        self.damageVariance=1
        self.accuracy=0.8
        self.actions=[self.Heal,self.Heal,self.Attack]
        self.art = [" "*5]*4+["(⸪)< "]
    
    def genName(self):
        nam1=["Meini","Mouni","Bilou","Borel","Binkel"]
        nam2=["","mo","mi","dou"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Orc(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=8
        self.level=2
        self.maxhp=8
        self.evil=True
        self.type="Orc"
        self.damage=2
        self.damageVariance=2
        self.accuracy=0.7
        self.actions=[self.Heal,self.Attack,self.Attack,self.Attack]
        self.art = [" "*7]*2+[r"(\) O  ",r"  \/|\ ",r"   / \ "]

    
    def genName(self):
        nam1=["Brag","Krau","Brak","Vra","Sig","Daug","Dig","Big","Jag"]
        nam2=["lug","vort","oum","ump","rog","og"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Bat(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=6
        self.maxhp=6
        self.type="Bat"
        self.damage=1
        self.level=2
        self.damageVariance=0
        self.accuracy=0.7
        self.flying = True
        self.actions=[self.Heal,self.Attack,self.FlyAttack]
        self.art = [" "*10]*2+[" ,  _  ,  ",r"/|\(⸪)/|\ ","   ^ ^    "]
    def FlyAttack(self):
        if(self.accuracy > random.random()):
            damage = self.damage + random.randint(-self.damageVariance, self.damageVariance) + 2
            player = random.choice(Global.players)
            slowPrint(self.name+" uses flying attack on "+player.name+" for "+str(damage)+"hp")
            slowPrint(self.name+" and "+player.name+" loses accuracy")
            self.accuracy = self.accuracy * 0.7
            player.accuracy = max(0.5,player.accuracy*0.8)
    
            player.hurt(damage)
        else:
            slowPrint(self.name+" misses flying attack")
    def genName(self):
        nam1=["Wing","Fly","Sky","Night"]
        nam2=["ling","gail","ster"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)        
class Faerie(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=2
        self.level=2
        self.maxhp=2
        self.type="Faerie"
        self.damage=3
        self.damageVariance=1
        self.accuracy=0.9
        self.flying=True
        self.actions=[self.Heal,self.Attack]
        self.art=[" "*4]*4+["^l^ "]
    def hurt(self, damage,armorPierce=0):
        if(not self.invincible):
            if(random.random()>0.5):
                self.hp=max(0,self.hp-max(0,damage-max(self.armor-armorPierce,0)))
                if(self.hp==0):
                    self.die()
            else:
                slowPrint(self.name+" evades the attack")
        else:
            slowPrint(self.name+" is invincible")
    def genName(self):
        nam1=["Lou","Lio","Vou","Fou","Fau","Sy","Ly"]
        nam2=["voun","fo","se","ni","mmel","dius"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Robotum(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=8
        self.level=3
        self.maxhp=self.hp
        self.healing=4
        self.type="Robotum"
        self.damage=3
        self.damageVariance=0
        self.accuracy=1
        self.armor=1
        self.actions=[self.Heal,self.Attack,self.Laser]
        self.laserPower = 0
        self.art = [" "*7]*2+[" [..]  "," =-|-  ","  o^o  "]
    def Laser(self):
        slowPrint(self.name+" uses LASER")
        if(self.laserPower==0):
            slowPrint(self.name+" charges LASER")
            self.laserPower=1
        else:
            player = random.choice(Global.players)
            slowPrint(self.name+" shoots LASER at "+player.name+" for "+str(self.damage*2)+"hp")
            player.hurt(self.damage*2)
            self.laserPower=0    
    def genName(self):
        nam1=["A","B","C","X","Y","Z"]
        nam2=[str(i) for i in range(10)]
        name = random.choice(nam1)
        for i in range(random.randint(1,2)):
            name = name + random.choice(nam1+nam2)
        self.gname(name)
class Spirit(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=12
        self.maxhp=12
        self.level=5
        self.type="Spirit"
        self.damage=2
        self.damageVariance=1
        self.accuracy=0.9
        self.actions=[self.Heal,self.Attack,self.Buff]
        self.flying=True
        self.art=[" "*9]+[
            r"  /,,\   ",
            r"'\|^ \/' ",
            r"   \\\   ",
            r"   '' '  "]
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while((self.actions[v]==self.Heal and self.hp==self.maxhp) or (self.actions[v]==self.Buff and len(Global.enemies)== 1)):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            slowPrint(self.name+" is stunned")
            self.stun=self.stun-1
    def Buff(self):
        for ally in Global.enemies:
            if(ally != self):
                if(self.accuracy > random.random()):
                    slowPrint(self.name+" blesses "+ally.returnName())
                    ally.maxhp = ally.maxhp+1
                    ally.damage = ally.damage+1
                    ally.hp = ally.hp+1
                    ally.accuracy = math.sqrt(ally.accuracy)
                    if(not "Blessed" in ally.type):
                        ally.type = "Blessed "+ally.type
                        ally.typeColor = "cyan"
                else:
                    slowPrint(self.name+" misses blessing")

    def genName(self):
        nam1=["Val","Vir","Vis","Nor","Vul","Dir"]
        nam2=["'ahr","hs","'aryh","'h","'arhium"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Roc(Bat):
    def __init__(self):
        Bat.__init__(self)
        self.hp=14
        self.maxhp=14
        self.level=5
        self.type="Roc"
        self.damage=3
        self.damageVariance=2
        self.art = [
        r"  _   ,____   ",
        r"<'') /|\ \ \  ",
        r"  \\/)) \ \ \ ",
        r"  / /         ",
        r" ^ ^          "]
    def genName(self):
        nam1=["Wing","Fly","Sky","Sly","Fur"]
        nam2=["dun","rier","con","vin"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Wolf(Enemy):
    def __init__(self,leader=True):
        Enemy.__init__(self)
        self.hp=4+leader*2
        self.level=6
        self.maxhp=self.hp
        self.evil=False
        self.type=leader*"Alpha "+"Wolf"
        self.damage=1+1*leader
        self.damageVariance=1
        self.accuracy=0.7
        self.actions=[self.Attack]
        self.art = [
        r"        ",
        r"        ",
        r" ʌʌ     ",
        r'<"====/ ',
        r"  // \\ ",
        ]
        

        if(leader):
            self.passives.append(self.action)
            for i in range(2):
                wolf = Wolf(leader=False)
                wolf.genName()
                Global.enemies.append(wolf)
            self.art = [
                r"        ",
                r"        ",
                r" ʌ ʌ    ",
                r"≤'')⊪)⊰ ",
                r" // \\  ",
                ]

    
    def genName(self):
        nam1=["Kroo","Fojo","Graud","Maul","Rah","Rok","Revoo","Morre","Johgot"]
        nam2=[", the Savage",", the Wicked",", leader of the pack",", fearsome predatory",",the Untamed",", adept stalker"]
        name = random.choice(nam1)#+random.choice(nam2)*(self.type=="Alpha Wolf")
        self.gname(name)
class Vampire(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=18
        self.maxhp=18
        self.level=7
        self.type="Vampire"
        self.evil=True
        self.damage=5
        self.damageVariance=1
        self.accuracy=0.8
        self.actions=[self.Heal,self.Drain]
        self.art = [
        r"      ",
        r"\ ⟅O⟆ ",
        r" X/|\ ",
        r"   |  ",
        r"  / \ ",
        ]
    def die(self):
        if("Vampire" in self.type):
            slowPrint(self.name+" turns into a bat")
            enemy=Bat()
            enemy.evil=True
            enemy.name=self.name
            enemy.type = self.type+" Bat"
            Global.enemies[Global.enemies.index(self)]=enemy
        else:
            slowPrint(self.name+" dies")
            Global.enemies.remove(self)


        
    def Drain(self):
        if(self.accuracy > random.random()):
            player = random.choice(Global.players)
            slowPrint(self.name+" uses drain on "+player.name+" for "+str(self.damage//2)+"hp")
            slowPrint(self.name+" gains "+str(self.damage//2)+"hp")

            player.hurt(self.damage//2)
            self.hp = min(self.maxhp,self.hp+self.damage//2)
        else:
            slowPrint(self.name+" misses drain")

    def genName(self):
        nam1=["Christopher","Rodriguez","Alexander","Abigale","Akesta","Olivia","Drakula","Abigail"]
        nam2=[" van Hoffel"," II"," III",", Lord of Darkness",", Count of the Castle"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Summoner(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=16
        self.maxhp=16
        self.level=6
        self.type="Summoner"
        self.evil=True
        self.summonTarget = Critter
        self.damage = 5
        self.damageVariance = 1
        self.accuracy = 0.7
        self.actions = [self.Heal,self.Summon,self.Summon]
        self.art=[
        r"         ",
        r" .O. /|  ",
        r" /|\/ |  ",
        r"  |/ (⸪) ",
        r" / \     ",
        ]
    def Summon(self):
        enemy=self.summonTarget()
        enemy.genName()
        Global.enemies.append(enemy)
        slowPrint(self.name+" summons a Critter")
    def genName(self):
        nam1=["Vale","Virium","Elmor","Goldior","Lance","Osum"]
        nam2=[" Orium"," Podem"," Lance"," Greenheart"," Mountainrise"," Evergreen"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Pyromaniac(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=15
        self.maxhp=self.hp
        self.level=7
        self.evil=True
        self.type="Pyromaniac"
        self.damage = 4
        self.damageVariance = 2
        self.accuracy = 0.7
        self.fireResistance=1
        self.actions = [self.Heal,self.Attack,self.Burn,self.Burn]
        self.art = [
        r"      ",
        r"(=)   ",
        r"/|\🔥 ",
        r" |    ",
        r"/ \   ",
        ]
    def Burn(self):
        player = random.choice(Global.players)
        slowPrint(self.name+" burns "+player.returnName()+" for "+str(self.damage//3))

        player.fire+=self.damage//3
    def genName(self):
        nam1=["Bale","Adria","Vic","Kon","Lance","Osum"]
        nam2=[" of the Flame"," Nalaar"," Ablaze",", Flamecaller"," Ash",", Infernal Seeker"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Mechanum(Robotum):
    def __init__(self):
        Robotum.__init__(self)
        self.hp=16
        self.level=8
        self.maxhp=self.hp
        self.healing=6
        self.type="Mechanum"
        self.armor=2
        self.damage=4
        self.damageVariance=0
        self.accuracy=1
        self.actions=[self.Heal,self.Attack,self.Laser,self.Barrier]
        self.laserPower = 0
        self.art = [" "*8]*1+[
        r"  [..]  ",
        r" o=-|-  ",
        r"    |   ",
        r"   O^O  ",
        ]
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while((self.actions[v]==self.Heal and self.hp==self.maxhp) or (self.actions[v]==self.Barrier and len(Global.enemies)== 1)):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            slowPrint(self.name+" is stunned")
            self.stun=self.stun-1
    def Barrier(self):
        allies = Global.enemies[:]
        allies.remove(self)
        ally = random.choice(allies)
        ally.invincible = 1
        slowPrint(self.name+" shields "+ally.returnName()+" for 1 turn")

    def genName(self):
        nam1=["A","B","C","X","Y","Z"]
        nam2=[str(i) for i in range(10)]
        name = random.choice(nam1)
        for i in range(random.randint(3,7)):
            name = name + random.choice(nam1+nam2)
        self.gname(name)
class Demon(Pyromaniac,Vampire):
    def __init__(self):
        Pyromaniac.__init__(self)
        self.hp=25
        self.maxhp=self.hp
        self.level=10
        self.evil=True
        self.type="Demon"
        self.damage = 6
        self.damageVariance = 2
        self.accuracy = 0.8
        self.actions = [self.Attack,self.Burn,self.Drain]
        self.art = [
        r"  , ⟅🔥⟆,  ",
        r" /|\ | /|\ ",
        r"🔥   |   🔥",
        r"    / \    ",
        r"   /   \   ",
        ]

    def genName(self):
        nam1=["Argon","Felgar","Razaketh","Krav","Nefarex","Lucius"]
        nam2=[", Soulhoarder",", Regent of Hell",", Devourer"," Duskseer"," Axkrand",", Tyrant of Chaos"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Witch(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=17
        self.evil=True
        self.maxhp=self.hp
        self.level=8
        self.type="Witch"
        self.accuracy = 0.85
        self.actions = [self.Heal,self.Curse]
        self.curses = ["Curse of strength","Curse of memory","Curse of protection","Curse of health",]
        self.art = [
        r"  ʌ      ",
        r" /⸪\ ()> ",
        r"\/|\/    ",
        r"/_|_\    ",
        r" / \     "]
    def Curse(self):
        player = random.choice(Global.players)
        if(self.accuracy > random.random()):
            cursed = False
            if(player.name != colored("???",colour="blue") or (player.damage > 3) or (player.armor > 0) or (player.maxhp > 5)):
                while(cursed==False):
                    selectedCurse=random.choice(self.curses)
                    if(selectedCurse=="Curse of memory" and player.name != colored("???",colour="blue")):
                        slowPrint(self.name+" casts Curse of memory on "+player.name)
                        slowPrint(player.name+" forgets their name")           
                        player.name=colored("???",colour="blue")
                        cursed=True
                    elif(selectedCurse=="Curse of strength" and (player.damage > 3)):
                        slowPrint(self.name+" casts Curse of strength on "+player.name)
                        slowPrint(player.name+" loses 1 damage")          
                        player.damage-=1
                        cursed=True
                    elif(selectedCurse=="Curse of protection" and (player.armor > 0)):
                        slowPrint(self.name+" casts Curse of protection on "+player.name)
                        slowPrint(player.name+" loses all armor")           
                        player.armor=0
                        cursed=True
                    elif(selectedCurse=="Curse of health" and (player.maxhp > 5)):
                        slowPrint(self.name+" casts Curse of health on "+player.name)
                        slowPrint(player.name+" loses 1 maxhp")           
                        player.maxhp-=1
                        player.hp-=1
                        if(player.hp==0):
                            player.die()
                        cursed=True
            else:
                self.Attack()

            
        else:
            slowPrint(self.name+" misses Curse")
    def genName(self):
        nam1=["Baba","Toad","Razi","Bubo","Fili"]
        nam2=["do","duck","bum","sim","po","i","e"]
        name = random.choice(nam1)+random.choice(nam2)+random.choice(nam2+[""]*7)
        self.gname(name)
class Hydra(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.level=9
        self.type="Hydra"
        self.nam=random.choice(["Kirgi","Zerk","Klow","Varge","Maxaj","Joffers","Wilkk","Xukh"])
        self.heads=1
        self.hp=6
        self.damage=2
        self.heal=2
        self.damageVariance=1
        self.maxhp=self.hp
        self.accuracy = 0.65
        self.actions = [self.Heal,self.Attack,self.Grow]
        self.passives.append(self.Grow)
        self.generateArt()
    def generateArt(self):
        spaces=math.ceil(self.heads/2)
        self.art=[
        " "*spaces+
        r"     ",
        " "*spaces+
        r"     ",
        "O"*spaces+
        r"     ",
        (" "*(self.heads%2==1))+("O"*(self.heads//2))+
        r"\__p ",
        " "*spaces+
        r" /\  ",
        ]
    def Grow(self):
        self.damage+=1
        self.hp+=2
        self.maxhp+=2
        self.heads+=1
        slowPrint(self.name+" grows another head")
        if(not "Shapeshifter" in self.type):
            self.genName()
        self.generateArt()
    def genName(self):
        name = self.nam+", the "+str(self.heads)+"-headed"
        self.gname(name)
class Troll(Enemy):
    pass #throws critters
class Dragon(Bat):
    pass #DragonBreath fly attack scales
class Progenitor(Summoner):
    pass # creates bats every turn
class Shapeshifter(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=10
        self.maxhp=10
        self.level=6
        self.type="Shapeshifter"
        self.damage=3
        self.damageVariance=1
        self.accuracy=0.9
        self.actions=[self.Attack,self.Heal]
        self.passives.append(self.Morph)
    def genName(self):
        nam1=["Paradox","Form","Shape","Illusion"]
        nam2=["ium"," Enigma"," of the Realms",",the Hidden"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name) 



#caller of Cthulu


#Player races
class Human(Player):
    def __init__(self):
        Player.__init__(self)
        self.maxhpstandard+=1
        self.accuracystandard+=0.05
        self.damagestandard+=1
class Flamekin(Player):
    def __init__(self):
        Player.__init__(self)
        self.fireResistance+=2
        self.fireDamage+=1
        self.magicDamagestandard-=1
        self.maxhpstandard-=1
        f=lambda damage:damage+self.fire
        self.damageFunctions.append(f)
        self.actions.append(self.Flame)
    def Flame(self):
        enemy=chooseTargets(Global.enemies,name="enemy",action="burn with Flame",ai=self.ai)[0]
        if(self.accuracy> random.random()):
            damage = (self.realDamage(self.damage) + self.magicDamage)
            enemy.fire += damage            
            slowPrint(self.name+" burns "+enemy.returnName()+" for "+str(damage)+"hp and "+str(damage)+" fire")
            slowPrint(self.name+" burns self for "+str(damage//2)+" fire")
            enemy.hurt(damage)
            self.fire += (damage//2)
        else:
            slowPrint(self.name+" misses Flame")
class Elf(Player):
    def __init__(self):
        Player.__init__(self)
        #self.magicDamagestandard+=1
        self.healing+=2
        self.maxhpstandard-=2
        
        self.actions.append(self.Bless)
    def Bless(self):
        ally=chooseTargets(Global.players,action="bless",name="player",ai=self.ai)[0]
        if(self.accuracy > random.random()):
            slowPrint(self.name+" blesses "+ally.returnName())
            ally.damage = ally.damage+2
            ally.magicDamage = ally.magicDamage+2
            ally.maxhp = ally.maxhp+2
            ally.hp = ally.hp+2
            ally.accuracy = math.sqrt(ally.accuracy)
        else:
            slowPrint(self.name+" misses blessing") 
class Fae(Player):
    def __init__(self):
        Player.__init__(self)
        self.magicDamagestandard+=1
        self.maxhpstandard-=6
        self.flying=True
        self.actions.append(self.Weaken)
        self.hurt=self.evade
    def Weaken(self):
        enemy = chooseTargets(Global.enemies,action="weaken",name="enemy",ai=self.ai)[0]
        if(self.accuracy > random.random()):

            if(not "Weak" in enemy.type):
                slowPrint(self.name+" weakens "+ enemy.returnName())
                enemy.damage = int(enemy.damage*0.7)
                weak = int(enemy.maxhp*0.35)
                enemy.maxhp -= weak
                enemy.hp-=weak
                enemy.type = "Weak "+enemy.type
                enemy.typeColor = "yellow"
            else:
                slowPrint(self.name+"uses weaken, "+enemy.returnName()+" is already Weak") 
        else:
            slowPrint(self.name+" misses weaken") 
    def evade(self, damage,armorPierce=0):
        if(not self.invincible):
            if(random.random()>0.5):
                self.hp=max(0,self.hp-max(0,damage-max(self.armor-armorPierce,0)))
                if(self.hp==0):
                    self.die()
            else:
                slowPrint(self.name+" evades the attack")
        else:
            slowPrint(self.name+" is invincible")
class Dwarf(Player):
    def __init__(self):
        Player.__init__(self)
        self.damagestandard+=2
        self.healing-=1
        self.armorstandard+=1
        self.fireResistance+=1
class Dryad(Player):
    pass
class Undead(Player):
    pass
class Robotkin(Player):
    pass # armor


Global.races = [Human,Flamekin,Elf,Fae,Dwarf]

#Player class
class Shaman(*Global.races):
    pass
class Wizard(*Global.races):
    pass #Lightning strike
class Necromancer(*Global.races):
    pass #

class Engineer(*Global.races):
    pass # Make Turrets from armor
class Beastmaster(*Global.races):
    pass # Create Allies evolve allies
class Nomad(*Global.races):
    def hurt(self,damage,armorPierce=0):
        pass
        #hurt enemies when damaged, double damage against evil, Selfhurt, Share with allies 

class Druid(*Global.races):
    pass
class Warrior(*Global.races):
    def __init__(self,chosenRace):
        chosenRace.__init__(self)
        self.damagestandard += 1
        f = lambda damage:damage + int(damage*(1-self.hp/self.maxhp))
        self.damageFunctions.append(f)
        self.damageVariance += 1
        self.accuracystandard -= 0.1
        self.actions.append(self.Fury)
        self.setStats()
    def Fury(self):
        slowPrint(self.name+" starts fury")
        i=0
        while(i<len(Global.enemies)):
            enemy=Global.enemies[i]
            damage = (self.realDamage(self.damage) + random.randint(-self.damageVariance, self.damageVariance))//2
            if(self.accuracy > random.random()):
                slowPrint(self.name+" attacks "+ enemy.returnName() + " for "+str(damage)+"hp")
                enemy.hurt(damage)
                if(not enemy in Global.enemies):
                    i-=1
                slowPrint(self.name+" is hurt for 1hp")
                self.hurt(1)
            else:
                slowPrint(self.name+" misses an attack")
                slowPrint(self.name+" is hurt for 1hp")
                self.hurt(1)
            i+=1
class Paladin(*Global.races): 
    def __init__(self,chosenRace):
        chosenRace.__init__(self)
        self.holy=True
        self.damageVariance -=1
        self.maxhpstandard += 1
        self.armorstandard +=1
        self.actions.append(self.Stun)
        f = lambda damage:damage + len(Global.players)-1
        self.damageFunctions.append(f)
        self.setStats()
    def Stun(self):
        enemy = chooseTargets(Global.enemies,action="stun",name="enemy",ai=self.ai)[0]
        if(self.accuracy > random.random()):
            slowPrint(self.name+" stuns "+ enemy.returnName() + " for "+str(len(Global.enemies))+" turns")
            enemy.stun = len(Global.enemies)
        else:
            slowPrint(self.name+" misses stun") 
class Sorcerer(*Global.races):
    def __init__(self,chosenRace):
        chosenRace.__init__(self)
        self.damagestandard -= 2
        self.damageVariance -= 1
        self.maxhpstandard -= 2
        self.magicDamagestandard += 2
        self.spells = [self.TwinFlame,self.Ignite,self.Bolt,self.Regain]
        self.unlockedSpells = []
        for i in range(2):
            initialSpell = chooseTargets(self.spells,action="unlock",name="spell",ai=self.ai)[0]#random.choice(self.spells)
            self.spells.remove(initialSpell)
            self.unlockedSpells.append(initialSpell)
        
        self.actions.append(self.Spell)
        self.setStats()
    def Spell(self):        
        chooseTargets(self.unlockedSpells,name="spell",action="cast, "+self.name,ai=self.ai)[0]()
    
    def TwinFlame(self):
        chosenEnemies=chooseTargets(Global.enemies,name="enemy",action="burn with TwinFlame",number=2,ai=self.ai)
        i=0
        while(i<len(chosenEnemies)):
            index = Global.enemies.index(chosenEnemies[i])             
            enemy = Global.enemies[index]
            damage = self.magicDamage
            fire = self.fireDamage
            if(self.accuracy > random.random()):
                slowPrint(self.name+" uses TwinFlame on "+ enemy.returnName() + " for "+str(damage)+"hp and "+str(fire)+" fire")
                enemy.fire+=fire
                enemy.hurt(damage)
            else:
                slowPrint(self.name+" misses TwinFlame")
            i+=1
    def Ignite(self):
        for enemy in Global.enemies:
            slowPrint(self.name+" ignites "+enemy.returnName())
            enemy.fire *= (self.fireDamage+1)
            if(self.accuracy*0.9 < random.random()):
                slowPrint(self.name+" accidentaly sets self on fire")
                self.fire += self.fireDamage
    def Bolt(self):
        for i in range(3):
            if(Global.enemies != []):
                enemy = random.choice(Global.enemies)
                if(self.accuracy > random.random()):
                    slowPrint(self.name+" shoots bolt at "+enemy.returnName()+" for "+str(self.magicDamage)+"hp")
                    enemy.hurt(self.magicDamage)
                else:
                    slowPrint(self.name+" misses bolt")
    def Regain(self):
        slowPrint(self.name+" regains "+str(self.magicDamage)+" health and fire and increases damage by "+str(self.magicDamage//2))
        self.hp   = min(self.maxhp,self.hp+self.magicDamage)
        self.damage+=self.magicDamage//2
        self.fire = max(0,self.fire-self.magicDamage)
class Cleric(*Global.races):
    def __init__(self,chosenRace):
        chosenRace.__init__(self)
        self.healing +=2
        self.maxhpstandard+=1
        self.healingVariance-=1
        self.damagestandard-=1
        self.holy=True
        self.actions.append(self.Remedy)
        self.actions.append(self.Cure)
        self.setStats() 
    def Heal(self):
        ally=chooseTargets(Global.players,name="player",action="heal",ai=self.ai)[0]
        heal = self.healing + random.randint(-self.healingVariance, self.healingVariance)
        newhp = min(ally.maxhp,ally.hp+heal)
        slowPrint(self.name+" healed "+ally.name+" from {}hp to {}hp".format(ally.hp, newhp))
        ally.hp=newhp
    def Remedy(self):
        if(self.accuracy > random.random()):
            healing = self.healing + random.randint(-self.healingVariance, self.healingVariance)
            healing = int(healing*0.4)
            message=self.name+" heals "
            for i in range(len(Global.players)):
                ally = Global.players[i]
                message+=ally.returnName()+" for "+str(healing)+"hp"
                if(i<len(Global.players)-2):
                    message+=", "
                if(i==len(Global.players)-2):
                    message+=" and "
            slowPrint(message)
            for ally in Global.players:
                ally.hp=min(ally.maxhp,ally.hp+healing)
        else:
            slowPrint(self.name+" misses Remedy")
    def Cure(self):
        ally=chooseTargets(Global.players,ai=self.ai)[0]
        slowPrint(self.name+" cures "+ally.name)
        if(ally.maxhp<ally.maxhpstandard):
            diff=ally.maxhpstandard-ally.maxhp
            ally.maxhp+=1+diff//2
            ally.hp+=1+diff//2
        if(ally.damage<ally.damagestandard):
            diff=ally.ally.damagestandard-ally.damage
            ally.damage+=1+diff//2
        if(ally.magicDamage<ally.magicDamagestandard):
            diff=ally.magicDamagestandard-ally.magicDamage
            ally.magicDamage+=1+diff//2
        if(ally.fire>0):
            ally.fire=0
         #Heal all allies protect certain ally heal fungerar på vem som helst, double damage against evil #Ressurect
class Knight(*Global.races):
    def __init__(self,chosenRace):
        chosenRace.__init__(self)
        self.damagestandard +=1
        self.accuracystandard+=0.03
        self.healing+=1
        self.actions.append(self.Pierce)
        self.actions.append(self.Slash)
        self.holy=True
        self.setStats() #Pierce hurt flying enemies 3*40%  more Slash enemies next to each other        
    def Pierce(self):
        enemy = chooseTargets(Global.enemies,name="enemy",action="Pierce",ai=self.ai)[0]
        if(enemy.flying):
                slowPrint("Pierce is super effective against flying types")
        for i in range(3):           
            if(enemy in Global.enemies):
                damage = self.realDamage(self.damage) + random.randint(-self.damageVariance, self.damageVariance)
                damage = int(damage*0.4)
                damage *= 1+enemy.flying
                if(self.accuracy > random.random()):                   
                    slowPrint(self.name+" pierces "+enemy.returnName()+" for "+str(damage)+"hp")
                    enemy.hurt(damage)
                else:
                    slowPrint(self.name+" misses pierce")
    def Slash(self):
        chosenEnemies = chooseTargets(Global.enemies,name="enemy",action="slash (also hits neighbours)",ai=self.ai)
        chosenEnemyIndex = Global.enemies.index(chosenEnemies[0])
        if(chosenEnemyIndex>0):
            chosenEnemies.append(Global.enemies[chosenEnemyIndex-1])
        if(chosenEnemyIndex<len(Global.enemies)-1):
            chosenEnemies.append(Global.enemies[chosenEnemyIndex+1])
        if(self.accuracy > random.random()):
            damage = self.realDamage(self.damage) + random.randint(-self.damageVariance, self.damageVariance)
            damage = int(damage*0.5)
            message=self.name+" slashes "
            for i in range(len(chosenEnemies)):
                enemy = chosenEnemies[i]
                message+=enemy.returnName()+" for "+str(damage)+"hp"
                if(i<len(chosenEnemies)-2):
                    message+=", "
                if(i==len(chosenEnemies)-2):
                    message+=" and "
            slowPrint(message)
            for i in range(len(chosenEnemies)):
                enemy = chosenEnemies[i]
                enemy.hurt(damage)
        else:
            slowPrint(self.name+" misses Slash")
Global.classes=[Warrior,Paladin,Cleric,Sorcerer,Knight]


# // Human magic
