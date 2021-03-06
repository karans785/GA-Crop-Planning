# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:10:44 2018

@author: KARAN
"""
import numpy as np
import pandas as pd
import copy

#inputs
area = int(input('Enter the area : '))
cost = int(input('Enter the money you have : '))
n = int(input('Enter the number of crops you have : '))
crops = []
for i in range(n):
    name=input("Enter crop name : ")
    crops.append(name)

#Read xls
xls_file=pd.ExcelFile('data.xls')
df = xls_file.parse('Sheet1')
DB=df.values
data=[]
for i in range(0,n):
    found=False
    for j in range(0,len(DB)):
        if crops[i]==DB[j][0]:
            info = [DB[j][1],DB[j][2],DB[j][3],DB[j][4]]
            data.append(info)
            found=True
    if not found:
        print(crops[i],' not found in the DB!!')


class parameters:
    def __init__(self):
        self.mutation_rate  = 0.2
        self.crossover_rate = 0.8
        self.N = 100

crossover_rate = 0.8
mutation_rate  = 0.2

def is_valid(member):
    a=0
    c=0
    j=0
    for i in member:
        a = a + i
        c = c + (data[j][3]*i)
        j=j+1
    return ((a==area) and (not cost<c))
    
def cover():
    member = [0 for i in range(n)]
    while(not is_valid(member)):
        member = [np.random.randint(0,10) for i in range(n)]
    return member

def initialize():
    param = parameters()
    population = []
    
    while len(population)<param.N:
        population.append(cover())
    return population, param

def fitness(member):
    fitness = 0
    for i in range(len(member)):
        #(productivity*Area) *(sp-cp/cp)
        fitness = fitness + ((data[i][0]/data[i][1])*member[i]*((data[i][2]-data[i][3])/data[i][3]));
    return fitness

def roulette_wheel_selection(avg_fitness,fitness_list,population):    
    probability=[]
    x = len(fitness_list)
    for i in fitness_list:
        probability.append(i/avg_fitness)
    cum_probab=[]
    for i in range(x):
        if i == 0:
            cum_probab.append(probability[i])
        else:
            cum_probab.append(cum_probab[i-1]+probability[i])
    new_pop=[]
    for i in range(x):
        rand = np.random.randint(0,100)
        closest_diff_so_far = 10000
        closest_j_so_far=-1
        for j in range(x):   
            if cum_probab[i]>rand:
                diff = abs(cum_probab[i]-rand)
                if diff < closest_diff_so_far  :
                    closest_diff_so_far = diff    
                    closest_j_so_far = j
                if closest_j_so_far >-1:                   
                    found = False
                    for k in new_pop:
                        if  k == population[j]:
                            found=True    
                    if not found:
                        new_pop.append(population[j])                      
    return new_pop

def cross(p1,p2):
    point1 = np.random.randint(0,n) 
    point2 = np.random.randint(0,n)
    p1[point1],p2[point2] = p2[point1],p1[point2]
    return p1,p2

def crossover(mating_pool):
    new_pop=[]
    for i in mating_pool:
        new_pop.append(i)
    temp_1 = np.random.randint(len(mating_pool))
    temp_2 = np.random.randint(len(mating_pool))
    rand = np.random.uniform(0,1)
    parent_1 = copy.deepcopy(mating_pool[temp_1])
    parent_2 = copy.deepcopy(mating_pool[temp_2])
    if rand < crossover_rate:    
        new1,new2 = cross(parent_1,parent_2) 
        new_pop.append(new1)
        new_pop.append(new2)
    else:
        new_pop.append(parent_1)
        new_pop.append(parent_2)
    return new_pop

def mutation(population):
    n = len(population)
    rand = np.random.uniform(0,1)
    if rand < mutation_rate:            
        rand_parents= [np.random.randint(0,n) for i in range(5)]
        for i in rand_parents:
            population[i]=cover()
    return population

def find_best(fitness_list):
    max_so_far = -1
    for i in range(len(fitness_list)):
        if fitness_list[i] >max_so_far:
            max_so_far = fitness_list[i]
    return max_so_far
        
iter=100     
def GA():
    population, params = initialize()
    print('Initial population is : ')
    for i in population:
        print(i," with fitness ",fitness(i))
    ans=-100
    ans_Chromosome=[]
    avg_fitness_list = []
    best_fitness_list =[]
    for i in range(iter):
        fitness_list=[]
        avg_fitness=0
        for j in population:
            mem_fitness = fitness(j)
            fitness_list.append(mem_fitness)
            avg_fitness = avg_fitness + mem_fitness
        avg_fitness = avg_fitness/(params.N)
        avg_fitness_list.append(avg_fitness)
        print("Average fitness of population in generation ",i+1," is ",avg_fitness,".")
        mating_pool = roulette_wheel_selection(avg_fitness,fitness_list,population)
        population=crossover(mating_pool)
        if i%15==0:
            population=mutation(population)
        best_fitness_list.append(find_best(fitness_list))
        if i ==iter-1:
            p=0
            for k in (fitness_list):
                if k>ans:
                    ans=k
                    ans_Chromosome=population[p]
                p=p+1
    return ans,ans_Chromosome,avg_fitness_list,best_fitness_list

#Printing the results:-
answer,ans_Chromosome,avg_fitness_list,best_fitness_list=GA()    
print("Answer is : ",ans_Chromosome," with fitness ",answer,".")


print("The genetic algorithm suggests that you should plant  :- \n")
for i in range(n):
    print(crops[i]," in ",ans_Chromosome[i]," hectares of your farm.")

#plotting the results
import matplotlib.pyplot as plt
x = np.arange(0,iter,1)
y = avg_fitness_list
plt.plot(x,y)
plt.xlabel('Number of Generation')
plt.ylabel('Avg Fitness Of Population')
plt.title('Avg fitness curve')
plt.show()

x = np.arange(0,iter,1)
z = best_fitness_list
plt.plot(x,z,"red")
plt.xlabel('Number of Generation')
plt.ylabel('Best Fitness Of Population')
plt.title('Best fitness curve')
plt.show()

plt.plot(x,y,"blue",label='Avg')
plt.plot(x,z,"red",label="Best")
plt.xlabel('Number of Generation')
plt.ylabel('Fitness ')
plt.legend(loc="upper left")
plt.show()
