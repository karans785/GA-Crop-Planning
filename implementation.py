# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 18:10:44 2018

@author: KARAN
"""
import numpy as np
import pandas as pd
area = int(input('Enter the area : '))
cost = int(input('Enter the money you have : '))

n = int(input('Enter the number of crops you have : '))
crops = []
for i in range(n):
    crops.append(input("Enter crop number : "))
    
data=[[1000,500,10,2],[1200,300,12,3],[500,1000,20,3]] 
class parameters:
    def __init__(self):
        self.mutation_rate  = 0.1
        self.crossover_rate = 0.5
        self.N = 100
    
def is_valid(member):
    a=0
    c=0
    j=0
    for i in member:
        a = a + i
        c = c + (data[j][3]*i)
        j=j+1
    return (a==area) and (not cost<c)
    
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

def roulette_wheel_selection(avg_fitness,fitness_list):    
    probability=[]
    for i in fitness_list:
        probability.append(i/avg_fitness)
    
    
def GA():
    population, params = initialize()
    print('Initial population is : ')
    #for i in population:
    #    print(i," -> ",fitness(i))
    fitness_list=[]
    for i in range(100):
        for i in population:
            mem_fitness = fitness(i)
            fitness.append(mem_fitness)
            avg_fitness = avg_fitness + mem_fitness
        avg_fitness = avg_fitness/params.N
        parents = roulette_wheel_selection(avg_fitness,fitness_list)
    selection(population,fitness)
GA()
