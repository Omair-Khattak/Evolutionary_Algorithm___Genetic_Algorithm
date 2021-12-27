from matplotlib.patches import Rectangle
import numpy as np
from matplotlib import patches
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import image as img
import random as rm




def initializePop(row,column,popSize):
    popList=[]
    for i in range(popSize):
        Rrows=rm.randint(0,row)
        Rcol=rm.randint(0,column)
        ColRow=[Rrows,Rcol]
        popList.append(ColRow)
    print(popList)
    return popList

def correlation_cofficient(A, B):
    return(np.mean(((A-A.mean())) * (B-B.mean())) /(A.std() * B.std()))


def fitnessValue(image1, image2,pop):
    Fitness= []
    for i in pop:
        x = i[0]
        y = i[1]
        image3 = np.array([image1[y:y+35, x:x+29]])
        correlation= correlation_cofficient(image2, image3)
        Fitness.append(correlation)
    return Fitness


def selection(fitness,population):
    pop = []
    sortt = sorted(zip(fitness, population))
    max_cord = sortt[1]
    for i in sortt:
        pop.append(i[1])
    return pop,max_cord[1]

def crossover(pop):
    for i in range(0,len(pop),2):
        C1= pop[i]
        C2= pop[i+1]
        Xcordnate=np.binary_repr(C1[0],10)
        Ycordnate= np.binary_repr(C1[1], 10)
        stringx= str(Xcordnate) 
        stringy=str(Ycordnate)
        XXcordnate= np.binary_repr(C2[0], 10)
        YYcordnate= np.binary_repr(C2[1],10)
        stringx2= str(XXcordnate)
        stringy2= str(YYcordnate)

        C1= list(stringx+stringy)
        C2=list(stringx2+stringy2)
        k = rm.randint(0, 19)
        for i in range(k, len(C1)):
            C1[i], C2[i] = C2[i], C1[i]
        C1 = ''.join(C1)
        C2 = ''.join(C2)
        pop[i]= (int(C1[0:10],2),int(C1[10:],2))
        pop[i+1]= (int(C2[0:10],2),int(C2[10:],2))
    return pop

def mutation(crossover):
    nextgeneration= [] 
    for i in crossover:
        current = i
        while current[0] > 989:
            a= np.binary_repr(i[0],10)
            a1=str(a)
            a2=list(a1)
            k = rm.randint(0,9) 
            if a2[k]=='0':
                a2[k]='1' 
            else:
                a2[k]='0'
            a2 =''.join(a2)
            a2 = int(a2,2) 
            current= (a2,current[1])
        while current[1] > 476:
            b =np.binary_repr(i[1],10)
            b1=str(b)
            b2=list(b1)
            k = rm.randint(0,9)
            if b2[k]=='0':
                b2[k]='1'
            else:
                b2[k]='0'
            b2 =''.join(b2)
            b2 = int(b2,2)
            current= (current[0],b2)
    nextgeneration.append(current)
    print(nextgeneration)
    return nextgeneration


def main():
    baba_img1 = img.imread('groupGray.jpg')
    gridImg1 = np.array((baba_img1))
    baba_img2 = img.imread('boothiGray.jpg')
    GridImg2 = np.array((baba_img2))    
    draw_fitness = []
    
    
    initialize=initializePop(989,476,100)
    for i in range (1000):
        fitness = fitnessValue(gridImg1, GridImg2,initialize)
        sorted_population,max_c = selection(fitness,initialize)
    
        if max(fitness) > 0.85:
            print(sorted_population[0])
            draw_fitness.append(sorted_population[0])
            break
        crs = crossover(sorted_population)
        mutation(crs)
        
    im = Image.open('groupGray.jpg')
    fig, ax = plt.subplots()
    ax.imshow(im)
    rect = patches.Rectangle((max_c[0],max_c[1]), 29, 35, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    plt.show()

main()



# 1. population = initializepop(row, col, size of pop)
# 2. FitnessValues = FitnessEval(bigimg, templete, population)
# 3. pop = Selection (population, FitnessValues)
# 4. EvolvedPop = Crossover(pop)
# 5. Population = Mutation (EvolvedPop)