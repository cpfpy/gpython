"""
制作人：盖房子的猫熊
模拟运动。这是注释
"""
import rhinoscriptsyntax as rs #调入rhino基本的库函数，函数是想象过程的，所以很简单。
import random as r #调入随机函数
import math 
from  scriptcontext import sticky as st

class Mover(object):
    """定义一个Mover类,继承于新式类。并初始化，
       定义位置以及运动方向。
    """
    def __init__(self):
        self.pos=[0,0,0]  #定义基本类的位置属性。
        self.vec=[0,0,0]  #速度
        self.acc=[0,0,0]  #加速度

    #定义一个函数更新物体的运动状态
    def update(self):
        self.vec=rs.VectorAdd(self.vec,self.acc) #速度公式：V = Vo +a * t  时间为1.
        self.pos=rs.VectorAdd(self.pos,self.vec) #位移公式：S = So + V * t 

    #定义一个恒定力，让物体运动有一个方向。
    def force(self,force,mass):
        scale=1/mass #加速度公式：F = a * m
        self.acc=rs.VectorScale(force,scale)

    #定义一个变化力，让物体运动方向产生一定的随机波动
    def wind(self):
        a=r.randint(-5,5) #这个函数是产生-5到5之间的随机数。
        b=r.randint(-5,5)
        c=r.randint(-5,5)
        vec=rs.VectorCreate([0,0,0],[a/4,b/4,c/4])
        self.vec=rs.VectorAdd(self.vec,vec)

    #将物体的运动速度限制在一定的范围之内
    def limited(self,max):  
        if rs.VectorLength(self.vec)>max:
            self.vec=rs.VectorUnitize(self.vec) #单位化向量。
            self.vec=rs.VectorScale(self.vec,max)
            self.acc=[0,0,0]
            

class OtMover(Mover):
    """
    定义了一个追随排斥的类，继承于Mover类。继承的优势在于
    父类的方法函数不用再写一遍可以直接调用。
    """
    def attraction(self,sca,otpos):
        #吸引力，这里你可以理解为追随头羊
        distance=rs.Distance(self.pos,otpos)
        vector=(rs.VectorCreate(otpos,self.pos))*sca
        self.vec=rs.VectorAdd(self.vec,vector)

    def reject(self,otpos):
        #排斥力当两个物体相距小于50时，排除力产生，理解为躲避狼
        distance=rs.Distance(self.pos,otpos)
        if distance<50: #这里进行判断在50这个范围内是否有危险
            vector=rs.VectorCreate(otpos,self.pos)
            vector=(rs.VectorUnitize(vector))*(distance-50) 
            #如果有危险，距离危险越近，逃离的速度越快。
            self.vec=rs.VectorAdd(self.vec,vector) #位移公式：S = So + V * t 
    def checkEdges(self,x,y,z): 
    #检查边界例如：当物体超越顶面时，从地面出现。
        if self.pos[0] < 0:
            self.pos[0] = x
        if self.pos[0] > x:
            self.pos[0] = 0
        if self.pos[1] < 0:
            self.pos[1] = y
        if self.pos[1] > y:
            self.pos[1] = 0
        if self.pos[2] < 0:
            self.pos[2] = z
        if self.pos[2] > z:
            self.pos[2] = 0

    def display(self): #函数可以调用函数，这样更易简化代码
        self.wind()
        self.force(force,10)
        self.limited(10)
        self.checkEdges(x,y,z)
        self.update()

class MiMover(Mover):
    #定义一个运动的类，继承于Mover类
    
    #在一定范围内运动，如果到达边界，运动方向进行方向，弹回来了。
    def checkEdges(self,x,y,z):
        if self.pos[0]<0 or self.pos[0]>x:
            self.vec[0]*=-1
        if self.pos[1]<0 or self.pos[1]>y:
            self.vec[1]*=-1
        if self.pos[2]<0 or self.pos[2]>z:
            self.vec[2]*=-1
            
    def display(self):
        self.wind()
        self.force(force,10)
        self.limited(8)
        self.checkEdges(x,y,z)
        self.update()
c=[]
d=[]
op=[]
ov=[]

if "move" not in st:
    st["move"]=MiMover()  #初始化一个头羊。
    r.seed(seed)
if Toogle:
    st["move"].display() #更新斗羊位置
    point=st["move"].pos   #得到头羊的位置
    vector=st["move"].vec #得到头羊的运动方向。
else:
    del st["move"]

for i in range(num): #初始化一群大灰狼
    names='move%d'%i 
    if names not in st:
        st[names]=OtMover()
    if Toogle:
        st[names].display() #更新狼的位置
        a=st[names].pos #得到狼的位置
        b=st[names].vec #得到狼的方向
        op.append(a) #把每一头狼的位置放在一起
        ov.append(b) #把每一头狼的方向放在一起


for item in range(number):
    name='otmove%d'%item
    if name not in st: #初始化基本物体。。。
        st[name]=OtMover()
    if Toogle:
        st[name].attraction(sca,st["move"].pos)#追随头羊
        for i in range(num):
            names="move%d"%i
            st[name].reject(st[names].pos) #逃避每一头狼。
        st[name].display()
        a=st[name].pos  
        b=st[name].vec
        c.append(a) #把每一羊的位置放在一起
        d.append(b) #把每一羊的方向放在一起
    else:
        del st[name]
