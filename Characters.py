import random
from Drawing import *
import math
#Main classes
class Character:
    def __init__(self):
        self.invinsible = 0
        self.nameLength = 0
        self.maxhp = 10
        self.hp = self.maxhp
        self.damage = 4
        self.damageVariance = 2
        self.healing = 2
        self.accuracy = 0.9
        self.healingVariance = 2
        self.messages = []
        self.items = []
        self.name = ""
        self.armor = 0
        self.armorstandard = 0
        self.stun = 0
        self.fire = 0
    def hurt(self, damage):
        if(not self.invinsible):
            self.hp=max(0,self.hp-damage+self.armor)
            if(self.hp==0):
                self.die()
        else:
            self.messages.append(" is invinsible")
    def effects(self):
        if(self.fire>0):
            self.messages.append("takes "+str(self.fire)+" fire damage")
            self.hurt(self.fire)
    def Heal(self):
        heal = self.healing + random.randint(-self.healingVariance, self.healingVariance)
        newhp = min(self.maxhp,self.hp+heal)
        self.messages.append("healed from {}hp to {}hp".format(self.hp, newhp))
        self.hp=newhp
    
    def printMessages(self):
        for message in self.messages:
            slowPrint(self.name+" "+message,speed=4)
        self.messages=[]
        print("")
class Player(Character):
    def __init__(self):       
        Character.__init__(self)
        self.hp = 15
        self.maxhp = 15
        self.level = 0
        self.name = "player"
        self.actions = [self.Heal,self.Attack]
        self.enemies = []
        self.reprint = None
        self.maxAccuracy = 0.9
        self.maxmana = 0
        self.mana = 0
    def returnName(self):
        return self.name
    def hurt(self,damage):
        self.hp=max(0,self.hp-damage+self.armor)

    def die(self):
        slowPrint("You are dead",speed=0.5)
        print("name",self.name,"level",self.level)
        progress()
        exit()
    def action(self):
        if(self.stun==0):
            print("Which action do you want to pursue?")
            didAction = False
            chosenAction = choice(self.actions)
            while didAction == False:            
                if(chosenAction in [str(i) for i in range(0,len(self.actions))]):
                    didAction = True
                    self.actions[int(chosenAction)]()
                else:
                    self.reprint()
                    print("Invalid Input")
                    chosenAction = choice(self.actions)
        else:
            self.stun=self.stun-1
            clear()
            print("You are stunned")
            progress()
        self.mana=min(self.maxmana,self.mana+1)
    def levelUp(self,cheat=False):
        self.level = self.level + 1
        self.armor = self.armorstandard
        if(self.level>1):
            clear()
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
                        self.damage=self.damage+1
                    if(chosenAction=="1"):
                        self.healing=self.healing+1
                    if(chosenAction=="2"):
                        self.maxhp=self.maxhp+2
                        self.hp=self.hp+2
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
            self.accuracy=self.maxAccuracy
            self.fire = 0
            #self.hp=self.maxhp
            if(cheat==False):
                print("Accuracy restored")
                progress()
    def chooseEnemy(self,enemies):
        self.reprint()
        choseEnemy = False
        if(len(enemies)==1):
            choseEnemy = True
            chosenEnemy = 0
        else:
            print("Which enemy do you want to attack?")
            chosenEnemy = choice(enemies)
        while choseEnemy == False:                          
            if(chosenEnemy in [str(i) for i in range(0,len(enemies))]):
                choseEnemy = True
            else:
                self.reprint()
                print("Invalid Input")
                chosenEnemy = choice(enemies)
        chosenEnemy = enemies[int(chosenEnemy)]
        return chosenEnemy
    def Attack(self):
        chosenEnemy = self.chooseEnemy(self.enemies)
        damage = self.damage + random.randint(-self.damageVariance, self.damageVariance)
        if(self.accuracy > random.random()):
            self.messages.append("attacks "+ chosenEnemy.returnName() + " for "+str(damage)+"hp")
            chosenEnemy.hurt(damage)
        else:
            self.messages.append("misses an attack")
class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.type = "Generic"
        self.typeColor = "red"
        self.name = colored("Enemy",colour="red")
        self.actions = [self.Heal,self.Attack]
        self.player = ""
    def printMessages(self):
        for message in self.messages:
            if(self.type=="Critter"):
                print(self.returnName()+" "+message)
            else:
                slowPrint(self.returnName()+" "+message,speed=4)
        self.messages=[]
        print("")
    def returnName(self):
        return self.name+" ("+colored(self.type,colour=self.typeColor)+")"
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while(self.actions[v]==self.Heal and self.hp==self.maxhp):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            self.messages.append("is stunned")
            self.stun=self.stun-1
    def Attack(self):
        damage = self.damage + random.randint(-self.damageVariance, self.damageVariance)
        if(self.accuracy > random.random()):
            self.messages.append("attacks "+ self.player.name + " for "+str(damage)+"hp")
            self.player.hurt(damage)
        else:
            self.messages.append("misses an attack")
    def die(self):
        self.player.messages.append("kills "+self.returnName())
        self.player.enemies.remove(self)
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
        self.type="Orc"
        self.damage=2
        self.damageVariance=2
        self.accuracy=0.7
        self.actions=[self.Heal,self.Attack,self.Attack,self.Attack]
    
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
        self.level=3
        self.damageVariance=0
        self.accuracy=0.7
        self.actions=[self.Heal,self.Attack,self.FlyAttack]
    def FlyAttack(self):
        if(self.accuracy > random.random()):
            damage = self.damage + random.randint(-self.damageVariance, self.damageVariance) + 2
            self.messages.append("uses flying attack on "+self.player.name+" for "+str(damage)+"hp")
            self.messages.append("and "+self.player.name+" loses accuracy")
            self.accuracy = self.accuracy * 0.7
            self.player.accuracy = self.player.accuracy*0.8
    
            self.player.hurt(damage)
        else:
            self.messages.append("misses flying attack")
    def genName(self):
        nam1=["Wing","Fly","Sky","Night"]
        nam2=["ling","gail","ster"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)        
class Robotum(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=10
        self.level=4
        self.maxhp=10
        self.healing=4
        self.type="Robotum"
        self.damage=3
        self.damageVariance=0
        self.accuracy=1
        self.actions=[self.Heal,self.Attack,self.Laser]
        self.laserPower = 0
    def Laser(self):
        self.messages.append("uses LASER")
        if(self.laserPower==0):
            self.messages.append("charges LASER")
            self.laserPower=1
        else:
            self.messages.append("shoots LASER at "+self.player.name+" for "+str(self.damage*2)+"hp")
            self.player.hurt(self.damage*2)
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
        self.level=6
        self.type="Spirit"
        self.damage=2
        self.damageVariance=1
        self.accuracy=0.9
        self.actions=[self.Heal,self.Attack,self.Buff]
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while((self.actions[v]==self.Heal and self.hp==self.maxhp) or (self.actions[v]==self.Buff and len(self.player.enemies)== 1)):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            self.messages.append("is stunned")
            self.stun=self.stun-1
    def Buff(self):
        for ally in self.player.enemies:
            if(ally != self):
                if(self.accuracy > random.random()):
                    self.messages.append("blesses "+ally.returnName())
                    ally.maxhp = ally.maxhp+1
                    ally.damage = ally.damage+1
                    ally.hp = ally.hp+1
                    ally.accuracy = math.sqrt(ally.accuracy)
                    if(ally.type[0:6]!="Blesse"):
                        ally.type = "Blessed "+ally.type
                        ally.typeColor = "cyan"
                else:
                    self.messages.append("misses blessing")

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
        self.level=7
        self.type="Roc"
        self.damage=3
        self.damageVariance=2
    def genName(self):
        nam1=["Wing","Fly","Sky","Sly","Fur"]
        nam2=["dun","rier","con","vin"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Vampire(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=18
        self.maxhp=18
        self.level=9
        self.type="Vampire"
        self.damage=4
        self.damageVariance=1
        self.accuracy=0.8
        self.actions=[self.Heal,self.Attack,self.Drain]
    def Drain(self):
        if(self.accuracy > random.random()):
            self.messages.append("uses drain on "+self.player.name+" for "+str(self.damage//2)+"hp")
            self.messages.append("gains "+str(self.damage//2)+"hp")

            self.player.hurt(self.damage//2)
            self.hp = min(self.maxhp,self.hp+self.damage//2)
        else:
            self.messages.append("misses drain")

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
        self.level=10
        self.type="Summoner"
        self.summonTarget = Critter
        self.damage = 5
        self.damageVariance = 1
        self.accuracy = 0.7
        self.actions = [self.Heal,self.Summon]
    def Summon(self):
        enemy=self.summonTarget()
        enemy.player=self.player
        enemy.genName()
        self.player.enemies.append(enemy)
        self.messages.append("summons a Critter")
    def genName(self):
        nam1=["Vale","Virium","Elmor","Goldior","Lance","Osum"]
        nam2=[" Orium"," Podem"," Lance"," Greenheart"," Mountainrise"," Evergreen"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
class Pyromancer(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=15
        self.maxhp=self.hp
        self.level=8
        self.type="Pyromancer"
        self.damage = 4
        self.damageVariance = 2
        self.accuracy = 0.7
        self.actions = [self.Heal,self.Attack,self.Burn]
    def Burn(self):
        self.messages.append("burns "+self.player.returnName()+" for "+str(self.damage//4))

        self.player.fire+=self.damage//4
    def genName(self):
        nam1=["Bale","Adria","Vic","Kon","Lance","Osum"]
        nam2=[" of the Flame"," Nalaar"," Ablaze",", Flamecaller"," Ash",", Infernal Seeker"]
        name = random.choice(nam1)+random.choice(nam2)
        self.gname(name)
#class Witch
class Demon(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.hp=20
        self.maxhp=self.hp
        self.level=8
        self.type="Pyromancer"
        self.damage = 4
        self.damageVariance = 2
        self.accuracy = 0.7
        self.actions = [self.Heal,self.Attack,self.Burn]
class Mechanum(Robotum):
    def __init__(self):
        Robotum.__init__(self)
        self.hp=20
        self.level=15
        self.maxhp=self.hp
        self.healing=6
        self.type="Mechanum"
        self.damage=4
        self.damageVariance=0
        self.accuracy=1
        self.actions=[self.Heal,self.Attack,self.Laser,self.Barrier]
        self.laserPower = 0
    def action(self):
        if(self.stun==0):
            v = random.randint(0,len(self.actions)-1)
            while((self.actions[v]==self.Heal and self.hp==self.maxhp) or (self.actions[v]==self.Barrier and len(self.player.enemies)== 1)):
                v = random.randint(0,len(self.actions)-1)
            self.actions[v]()
        else:
            self.messages.append("is stunned")
            self.stun=self.stun-1
    def Barrier(self):
        allies = self.player.enemies[:]
        allies.remove(self)
        ally = random.choice(allies)
        ally.invinsible = 1
        self.messages.append("shields "+ally.returnName()+" for 1 turn")

    def genName(self):
        nam1=["A","B","C","X","Y","Z"]
        nam2=[str(i) for i in range(10)]
        name = random.choice(nam1)
        for i in range(random.randint(3,4)):
            name = name + random.choice(nam1+nam2)
        self.gname(name)


#Player types
class Warrior(Player):
    def __init__(self):
        Player.__init__(self)
        self.damage=5
        self.damageVariance=3
        self.hp = 13
        self.maxhp = 13
        self.maxAccuracy = 0.8
        self.accuracy = self.maxAccuracy
        self.actions = [self.Heal,self.Attack,self.Fury]
    def Fury(self):
        self.messages.append("starts fury")
        i=0
        while(i<len(self.enemies)):
            enemy=self.enemies[i]
            damage = self.damage + random.randint(-self.damageVariance, self.damageVariance)
            if(self.accuracy**len(self.enemies) > random.random()):
                self.messages.append("attacks "+ enemy.returnName() + " for "+str(damage)+"hp")
                enemy.hurt(damage)
                if(not enemy in self.enemies):
                    i-=1
                self.messages.append("is hurt for 1hp")
                self.hurt(1)
            else:
                self.messages.append("misses an attack")
                self.messages.append("is hurt for 1hp")
                self.hurt(1)
            i+=1
class Paladin(Player):
    def __init__(self):
        Player.__init__(self)
        self.damage=4
        self.damageVariance=1
        self.hp = 16
        self.maxhp = 16
        self.maxAccuracy = 0.9
        self.accuracy = self.maxAccuracy
        self.armor = 1
        self.armorstandard = self.armor
        self.actions = [self.Heal,self.Attack,self.Stun]
    def Stun(self):
        enemy = self.chooseEnemy(self.enemies)
        if(self.accuracy > random.random()):
            self.messages.append("stuns "+ enemy.returnName() + " for "+str(len(self.enemies))+" turns")
            enemy.stun = len(self.enemies)
        else:
            self.messages.append("misses stun")
class Sorcerer(Player):
    def __init__(self):
        Player.__init__(self)
        self.damage = 2
        self.damageVariance = 1
        self.hp = 16
        self.maxhp = 16
        self.maxAccuracy = 0.9
        self.accuracy = self.maxAccuracy
        self.armor = 0
        self.armorstandard = 0
        self.magicDamage = 4
        self.mana = 5
        self.maxmana = 5
        self.managrowth = 1
        self.fireDamage = 1
        self.bolts = 2
        self.regain = 1
        self.spells = [(self.TwinFlame,3),(self.Ignite,2),(self.Bolt,2),(self.Regain,1)]
        initialSpell = (self.TwinFlame,3) #random.choice(self.spells)
        self.spells.remove(initialSpell)
        self.unlockedSpells = [initialSpell]
        
        self.actions = [self.Heal,self.Attack,self.Spell]
    def Spell(self):
        noSpellsCastable = True
        for spell in self.unlockedSpells:
            if(self.mana>=spell[1]):
                noSpellsCastable = False
        if( noSpellsCastable == True):
            self.messages.append("does not have enough mana to cast any spells")
            return None
        self.reprint()
        choseSpell = False
        if(len(self.unlockedSpells) == 1):
            choseSpell = True
            chosenSpell = "0"
            self.mana=self.mana - self.unlockedSpells[int(chosenSpell)][1]
        else:
            print("Which spell do you want to cast?")
            chosenSpell = choice(self.unlockedSpells)
        while choseSpell == False:                          
            if(chosenSpell in [str(i) for i in range(0,len(self.unlockedSpells))]):
                if( self.unlockedSpells[int(chosenSpell)][1]<=self.mana):
                    choseSpell = True
                    self.mana=self.mana - self.unlockedSpells[int(chosenSpell)][1]
                else: 
                    self.reprint()
                    print("Not enough Mana")
                    chosenSpell = choice(self.unlockedSpells)

            else:
                self.reprint()
                print("Invalid Input")
                chosenSpell = choice(self.unlockedSpells)
        chosenSpell = self.unlockedSpells[int(chosenSpell)][0]
        chosenSpell()
    
    def TwinFlame(self):
        enemies = self.enemies[:]
        chosenEnemies = []
        if(len(enemies) == 1 or len(enemies) == 2):
            chosenEnemies = enemies
        else:
            chosenEnemies.append(self.chooseEnemy(enemies))
            enemies.remove(chosenEnemies[0])
            chosenEnemies.append(self.chooseEnemy(enemies))
        i=0
        while(i<len(chosenEnemies)):
            index = self.enemies.index(chosenEnemies[i])             
            enemy = self.enemies[index]
            damage = self.magicDamage
            fire = self.fireDamage
            if(self.accuracy > random.random()):
                self.messages.append("uses TwinFlame on "+ enemy.returnName() + " for "+str(damage)+"hp and "+str(fire)+" fire")
                enemy.fire+=fire
                enemy.hurt(damage)
            else:
                self.messages.append("misses TwinFlame")
            i+=1
    def Ignite(self):
        for enemy in self.enemies:
            if(enemy.fire>0):
                self.messages.append("ignites "+enemy.returnName())
                enemy.fire *= (self.fireDamage+1)
                enemy.fire += (self.fireDamage)
                if(self.accuracy*0.9 < random.random()):
                     self.messages.append("accidentaly sets self on fire")
                     self.fire += self.fireDamage
    def Bolt(self):
        bolts = self.bolts+random.randint(-self.damageVariance,self.damageVariance)
        for i in range(bolts):
            if(self.enemies != []):
                enemy = random.choice(self.enemies)
                if(self.accuracy > random.random()):
                    self.messages.append("shoots bolt at "+enemy.returnName())
                    enemy.hurt(self.magicDamage)
    def Regain(self):
        self.messages.append("regains health, mana, fire")
        self.hp   = min(self.maxhp,self.hp+self.regain)
        self.mana = min(self.maxmana,self.mana+self.regain+self.managrowth)
        self.fire = max(0,self.fire-self.regain)
