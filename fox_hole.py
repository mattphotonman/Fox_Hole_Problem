#!/usr/bin/env python
"""
Solves the Fox in a Hole problem from
http://gurmeet.net/puzzles/
Solves it for N holes, where N is set below.
"""

#Imports
import copy

#Global variables
N=7

#Functions

#Evolves the set of possible fox locations given an initial
#set of possible locations and a hole that is checked.
def evolve(config_in,guess):
    config=copy.copy(config_in)
    
    if len(config)!=N:
        print "Error in evolve: config has wrong length."
        exit(1)
    
    if guess<0 or guess>=N:
        print "Error in evolve: guess out of range."
        exit(1)

    config[guess]=False
    new_config=range(N)
    for i in range(N):
        val1=val2=False
        if i>0:
            val1=config[i-1]
        if i<N-1:
            val2=config[i+1]
        new_config[i]=val1 or val2

    return new_config

#Converts a set of possible fox locations to an integer
#by treating the set as a binary number.
def config_to_int(config_in):
    config=copy.copy(config_in)
    
    if len(config)!=N:
        print "Error in config_to_int: config has wrong length."
        exit(2)

    #Change the True and False to 1 and 0.
    new_config=range(N)
    for i in range(N):
        if config[i]:
            new_config[i]=1
        else:
            new_config[i]=0

    #Convert binary to base 10.
    intval=0
    for i in range(N):
        intval+=new_config[i]*2**i

    return intval

#Inverse of the above
def int_to_config(intval):
    if intval<0 or intval>=2**N:
        print "Error in int_to_config: intval out of range."
        exit(3)

    new_config=range(N)
    for i in range(N-1,-1,-1):
        if intval/2**i==1:
            new_config[i]=True
        elif intval/2**i==0:
            new_config[i]=False
        else:
            print "Error in int_to_config: Something wrong with logic of function."
            exit(3)
        intval-=(intval/2**i)*2**i

    return new_config

#Initially the fox could be anywhere
start_config=range(N)
for i in range(N):
    start_config[i]=True

#List of lists of paths taken to get to a given
#configuration once it has been visited.  Configurations in
#the list are represented as integers.  If a config hasn't
#been visited then the list will just contain [] for that
#config.
path_to_config=range(2**N)
for i in range(2**N):
    if i==config_to_int(start_config):
        path_to_config[i]=[[i]]
    else:
        path_to_config[i]=[]

#List of lists of guesses that were taken to get to a
#configuration, with order matching up to path_to_config.
guess_to_config=range(2**N)
for i in range(2**N):
    guess_to_config[i]=[[]]

#Go through generating new configurations until no new ones
#are generated.
last_configs=[copy.copy(start_config)]
while True:
    new_configs=[]
    for i in range(len(last_configs)):
        for j in range(N):
            possible_new=evolve(last_configs[i],j)
            #Is it really new?
            int_old=config_to_int(last_configs[i])
            int_new=config_to_int(possible_new)
            if path_to_config[int_new]==[]:
                #This is a genuinely new config
                path_to_config[int_new]=copy.deepcopy(path_to_config[int_old])
                for k in range(len(path_to_config[int_new])):
                    path_to_config[int_new][k].append(int_new)
                guess_to_config[int_new]=copy.deepcopy(guess_to_config[int_old])
                for k in range(len(guess_to_config[int_new])):
                    guess_to_config[int_new][k].append(j)
                new_configs.append(copy.copy(possible_new))
            else:
                #Config has already been visited
                #Check if this config was just added in this iteration
                if possible_new in new_configs:
                    #Add alternate path information
                    for k in range(len(path_to_config[int_old])):
                        path_to_config[int_new].append(copy.copy(path_to_config[int_old][k]))
                        path_to_config[int_new][-1].append(int_new)
                    for k in range(len(guess_to_config[int_old])):
                        guess_to_config[int_new].append(copy.copy(guess_to_config[int_old][k]))
                        guess_to_config[int_new][-1].append(j)
            
            #If the config is not new at all, nothing is done.

    #If there were no new configs generated then we've reached
    #the end.
    if new_configs==[]:
        break
    #Otherwise, copy new configs to last_configs and continue.
    last_configs=copy.deepcopy(new_configs)

#If we never got to a configuration with all False
#(configuration 0), then there is no solution for N fox holes.
#If we did get to this configuration, then display the
#paths that get there.
if path_to_config[0]==[]:
    print "There is no solution for", N, "fox holes."
else:
    for i in range(len(path_to_config[0])):
        print "Path", i+1
        print ""
        for j in range(len(path_to_config[0][i])):
            print int_to_config(path_to_config[0][i][j])
            if j<len(path_to_config[0][i])-1:
                print "Check hole:", guess_to_config[0][i][j]+1
        print ""

