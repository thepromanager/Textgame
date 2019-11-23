from Drawing import *
from Characters import *
from Items import *
from Map import *
class Attribute():
    def __init__(self,value,standardValue=None):
        self.value = value
        if(standardValue==None):
            self.standardValue=value
        else:
            self.standardValue=standardValue
    def reset(self):
        self.value = self.standardValue
    def setValue(self,value):
        self.value=value
    def __repr__(self):
        return str(self.value)
    eqlist=["__eq__","__ne__","__lt__","__gt__","__le__","__ge__"]
    for eq in eqlist:
        string="""def {}(self,other):
    if(isinstance(other,int)):
        return int.{}(self.value,other)
    if(isinstance(other,Attribute)):
        return int.{}(self.value,other.value)
        """.format(eq,eq,eq)
        exec(string)
    addlist=["__add__","__sub__","__mul__","__div__","__floordiv__","__mod__","__pow__","__and__","__or__","__xor__"]
    for add in addlist:
        string="""def {}(self,other):
    if(isinstance(other,int)):
        return Attribute(int.{}(self.value,other),self.standardValue)
    if(isinstance(other,Attribute)):
        return Attribute(int.{}(self.value,other.value),self.standardValue)
        """.format(add,add,add)
        exec(string)
    iaddlist=[add[2:] for add in addlist]
    for iadd in iaddlist:
        string="""def __i{}(self,other):
        return self.__{}(other)
        """.format(iadd,iadd)



    

def compose(functions):
    def compose2(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose2, functions, lambda x: x)

a=lambda x:x+2
b=lambda x:x*2
c=lambda x:x**2
print(compose([a,c,a])(3))