# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 20:20:59 2019

@author: Vishesh Breja
"""

print('importing libraries.......')
from mpl_toolkits.basemap import Basemap
from geopy.distance import distance # to calculate distance in between the coordinates
import matplotlib.pyplot as plt
import datetime
import time

import numpy as np
#matplotlib inline
plt.style.use('bmh')

import sys
import matplotlib
libraries = (('Matplotlib', matplotlib), ('Numpy', np))




print('importing libraries done!')
###############################################################################
#plotting a particular country-----> Netherlands
###############################################################################
print("Python Version:", sys.version, '\n')
for lib in libraries:
    print('{0} Version: {1}'.format(lib[0], lib[1].__version__))


    

    
    
    
###############################################################################
#defining a function
###############################################################################   
def plot_cities(city_coordinates, annotate=True):
    """
    Makes a plot of all cities.
    Input: city_coordinates; dictionary of all cities and their coordinates in (x,y) format
    """
    names = []
    x = []
    y = []
    plt.figure(dpi=100)
    for ix, coord in city_coordinates.items():
            names.append(ix)
            x.append(coord[0])
            y.append(coord[1])
            if annotate:
                plt.annotate(ix, xy=(coord[0], coord[1]), xytext=(20, -20),
                            textcoords='offset points', ha='right', va='bottom',
                            bbox=dict(boxstyle='round,pad=0.5', fc='w', alpha=0.5),
                            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    plt.scatter(x,y,c='r',marker='o')


###############################################################################
#defining a function
###############################################################################            
from copy import copy
def create_guess(cities):
    """
    Creates a possible path between all cities, returning to the original.
    Input: List of City IDs
    """
    guess = copy(cities)
    np.random.shuffle(guess)
    guess.append(guess[0])
    return list(guess)
###############################################################################
#defining a function
###############################################################################
def plot_guess(city_coordinates, guess, guess_in_title=True):
    """
    Takes the coordinates of the cities and the guessed path and
    makes a plot connecting the cities in the guessed order
    Input:
    city_coordinate: dictionary of city id, (x,y)
    guess: list of ids in order
    """
    plot_cities(city_coordinates)
    for ix, current_city in enumerate(guess[:-1]):
        x = [city_coordinates[guess[ix]][0],city_coordinates[guess[ix+1]][0]]
        y = [city_coordinates[guess[ix]][1],city_coordinates[guess[ix+1]][1]]
        plt.plot(x,y,'c--',lw=1)
    plt.scatter(city_coordinates[guess[0]][0],city_coordinates[guess[0]][1], marker='x', c='b')   
    if guess_in_title:
        plt.title("Best_Route_prediction: [%s]"%(','.join([str(x) for x in guess])))
    else:
        print("Best_Route_prediction: [%s]"%(','.join([str(x) for x in guess])))
###############################################################################
#defining a function
###############################################################################
def create_generation(cities, population=100):
    """
    Makes a list of guessed city orders given a list of city IDs.
    Input:
    cities: list of city ids
    population: how many guesses to make
    """
    generation = [create_guess(cities) for _ in range(population)]
    return generation

###############################################################################
#defining a function
###############################################################################
def distance_between_cities(city1_id, city2_id):
    """
    Given two cities, this calculates this distance between them
    """
    c1 = cities[city1_id]
    c2 = cities[city2_id]
    distance_2 = np.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
    return distance_2

def fitness_score(guess):
    """
    Loops through the cities in the guesses order and calculates
    how much distance the path would take to complete a loop.
    Lower is better.
    """
    score = 0
    for ix, city_id in enumerate(guess[:-1]):
        score += distance_between_cities(city_id, guess[ix+1])
    return score

def check_fitness(guesses):
    """
    Goes through every guess and calculates the fitness score. 
    Returns a list of tuples: (guess, fitness_score)
    """
    fitness_indicator = []
    for guess in guesses:
        fitness_indicator.append((guess, fitness_score(guess)))
    return fitness_indicator
###############################################################################
#defining a function
###############################################################################

def get_breeders_from_generation(guesses, take_best_N=10, take_random_N=5, verbose=False, mutation_rate=0.1):
    """
    This sets up the breeding group for the next generation. You have
    to be very careful how many breeders you take, otherwise your
    population can explode. These two, plus the "number of children per couple"
    in the make_children function must be tuned to avoid exponential growth or decline!
    """
    # First, get the top guesses from last time
    fit_scores = check_fitness(guesses)
    sorted_guesses = sorted(fit_scores, key=lambda x: x[1]) # sorts so lowest is first, which we want
    new_generation = [x[0] for x in sorted_guesses[:take_best_N]]
    best_guess = new_generation[0]
    
    if verbose:
        # If we want to see what the best current guess is!
        print('')
    
    # Second, get some random ones for genetic diversity
    for _ in range(take_random_N):
        ix = np.random.randint(len(guesses))
        new_generation.append(guesses[ix])
        
    # No mutations here since the order really matters.
    # If we wanted to, we could add a "swapping" mutation,
    # but in practice it doesn't seem to be necessary
    
    np.random.shuffle(new_generation)
    return new_generation, best_guess

def make_child(parent1, parent2):
    """ 
    Take some values from parent 1 and hold them in place, then merge in values
    from parent2, filling in from left to right with cities that aren't already in 
    the child. 
    """
    
    list_of_ids_for_parent1 = list(np.random.choice(parent1, replace=False, size=len(parent1)//2))
    #print(len(list_of_ids_for_parent1))
    child = [-99 for _ in parent1]
    #print(child)
   
    for  ix in range(len(list_of_ids_for_parent1)):
        child[ix] = parent1[ix]
    for ix, gene in enumerate(child):
        if gene == -99:
            for gene2 in parent2:
                if gene2 not in child:
                    child[ix] = gene2
                    break
    child[-1] = child[0]
    return child

def make_children(old_generation, children_per_couple=1):
    """
    Pairs parents together, and makes children for each pair. 
    If there are an odd number of parent possibilities, one 
    will be left out. 
    
    Pairing happens by pairing the first and last entries. 
    Then the second and second from last, and so on.
    """
    mid_point = len(old_generation)//2
    next_generation = [] 
    
    for ix, parent in enumerate(old_generation[:mid_point]):
        for _ in range(children_per_couple):
            next_generation.append(make_child(parent, old_generation[-ix-1]))
    return next_generation
###############################################################################
#defining a function
###############################################################################

def evolve_to_solve(current_generation, max_generations, take_best_N, take_random_N,
                    mutation_rate, children_per_couple, print_every_n_generations, verbose=False):
    """
    Takes in a generation of guesses then evolves them over time using our breeding rules.
    Continue this for "max_generations" times.
    Inputs:
    current_generation: The first generation of guesses
    max_generations: how many generations to complete
    take_best_N: how many of the top performers get selected to breed
    take_random_N: how many random guesses get brought in to keep genetic diversity
    mutation_rate: How often to mutate (currently unused)
    children_per_couple: how many children per breeding pair
    print_every_n_geneartions: how often to print in verbose mode
    verbose: Show printouts of progress
    Returns:
    fitness_tracking: a list of the fitness score at each generations
    best_guess: the best_guess at the end of evolution
    """
    fitness_tracking = []
    for i in range(max_generations):
        if verbose and not i % print_every_n_generations and i > 0:
            #print("Generation %i: "%i, end='')
            #print(len(current_generation))
            #print("Current Best Score: ", fitness_tracking[-1])
            is_verbose = True
        else:
            is_verbose = False
        breeders, best_guess = get_breeders_from_generation(current_generation, 
                                                            take_best_N=take_best_N, take_random_N=take_random_N, 
                                                            verbose=is_verbose, mutation_rate=mutation_rate)
        fitness_tracking.append(fitness_score(best_guess))
        current_generation = make_children(breeders, children_per_couple=children_per_couple)
    
    return fitness_tracking, best_guess




plt.figure(figsize=(10,10))


m = Basemap(llcrnrlon=3.3149,llcrnrlat=50.803721015,urcrnrlon= 7.09205325687,urcrnrlat=53.5104033474, resolution = 'h')

m.drawmapboundary(fill_color='aqua')
#Fill the continents with the land color
m.fillcontinents(color='coral',lake_color='aqua')
m.drawcoastlines()
m.drawcountries(linewidth=2)
m.drawstates(color='black')










#plotting the coordinates as per model predictions

print('plotting the coordinates of construction hubs obtained from the trained model.....   \n')
xs= []#empty_list_for x-coordinate
ys= []#empty list for y-coordinate

###############################
hague_lat = 52.3667
hague_lon=  4.8945
x , y = m(hague_lon, hague_lat)
xs.append(x)
ys.append(y)
m.plot(x,y,'^',label= 'Ch_1',markersize= 20,markerfacecolor="g")
###############################
###############################
rotterdam_lat = 51.9244
rotterdam_lon=  4.4777
x , y = m(rotterdam_lon, rotterdam_lat)
xs.append(x)
ys.append(y)
m.plot(x,y,'^',label= 'Ch_2',markersize= 20,markerfacecolor="b")
###############################
###############################
gieten_lat = 52.098836
gieten_lon=  4.259858
x , y = m(gieten_lon, gieten_lat)
xs.append(x)
ys.append(y)
m.plot(x,y,'^',label= 'Ch_3',markersize= 20,markerfacecolor="r")
###############################
###############################
assen_lat = 52.994749
assen_lon=  6.563223
x , y = m(assen_lon, assen_lat)
xs.append(x)
ys.append(y)
m.plot(x,y,'^',label= 'Ch_4',markersize= 20,markerfacecolor="y")
###############################
###############################
bergeijk_lat = 52.2574
bergeijk_lon=   6.7928
x , y = m(bergeijk_lon, bergeijk_lat)
xs.append(x)
ys.append(y)
m.plot(x,y,'^',label= 'Ch_5',markersize= 20,markerfacecolor="m")
###############################

plt.legend(loc = 3)
plt.title('Plotting coordinates of construction hub predicted from trained model')
plt.show()
print('\n')
###############################################################################
#to get the date in table
###############################################################################
x = datetime.datetime.now()

print('Information about our construction hubs! \n')
print('\n')

print('#########################################################################################################################################################')
print('|      Name                |Latitude   |Longitude        |Quantity_of_wood(in KG)    |New_addition     |Date_for_new_material                           |')
print('#########################################################################################################################################################')
construction_hub_list=[['construction_hub_1', 52.3667,4.8945,5,'Plastic',x],
                    ['construction_hub_2',51.9244,4.4777,8,'Plastic',x],
                    ['construction_hub_3',52.0988,4.2598,2,'Plastic',x],
                    ['construction_hub_4',52.9947,6.5632,3,'Plastic',x],
                    ['construction_hub_5',52.2574,6.7928,7.4,'Plastic',x]]

 
for item in construction_hub_list:
    print('|',item[0],' '*(23-len(item[0])), '|',
          item[1],' '*(8-len(str(item[1]))), '|',
          item[2],' '*(14-len(str(item[2]))), '|',
          item[3],' '*(24-len(str(item[3]))), '|',
          item[4],' '*(14-len(str(item[4]))), '|',
          item[5],' '*(26-len(str(item[4]))), '|')
    
print('#########################################################################################################################################################')
print('|                                                                                                                                                       |')
print('#########################################################################################################################################################')
print('\n')
print('\n')

print('Ch_1 contains the material for houses mostly!')
print('Ch_2 contains the material for medical facillity mostly!')
print('Ch_3 contains the material for houses mostly!')
print('Ch_4 contains the material offices mostly!')
print('Ch_5 contains the material for cafes mostly!')


#time.sleep(5)
#print('plotting the coordinates done!')
#asking for user input



i = 1
while i <2:
    ###############################################################################
    #for user input
    ###############################################################################
    
    
    plt.figure(figsize=(10,10))
    
    
    m1 = Basemap(llcrnrlon=3.3149,llcrnrlat=50.803721015,urcrnrlon= 7.09205325687,urcrnrlat=53.5104033474, resolution = 'h')
    
    m1.drawmapboundary(fill_color='aqua')
    #Fill the continents with the land color
    m1.fillcontinents(color='coral',lake_color='aqua')
    m1.drawcoastlines()
    m1.drawcountries(linewidth=3)
    m1.drawstates(color='black')

    name = input("Please enter your name: ")
    try:
        test3num = (name)
        print("This is a valid name! Your good name is: ", test3num)
    except ValueError:
        print("Please enter a string!")
    ###########################################################################
    #taking some user_id as input for verification
    ###########################################################################
    voter_id= input("Please enter your voter_id: ")
    try:
        voter_id = int(voter_id)
        print("You entered: ", voter_id)
    except ValueError:
        print("This is not a valid voter_id. Please try agin later")
    ###########################################################################
    #taking some user_id as input for verification
    ###########################################################################    
    print('Please wait while the authentication is finished....')
    time.sleep(5)
    print('Authentication Finished!')
    ###########################################################################
    #taking construction coordinates by user
    ########################################################################### 
    construction_type = input("Please input the type of your construction (Example: Medical, Commercial, Hotel e.t.c)  :")
    try:
        constructin_type = (construction_type)
        print("You choose: ", construction_type)
    except ValueError:
        print("Please enter a string!")
    ###########################################################################
    #asking for the coordinates of the choosen construction
    ###########################################################################    
    latitude, longitude = [float(s) for s in input('what are the x ()latitude and y (longitude) coordinates you prefer :').split()]
    print(latitude)
    print(longitude)
    ###########################################################################
    #plotting these coordinates on the map
    ###########################################################################
    user_lat_list = []
    user_lon_list = []
    user_lat = latitude
    user_lon=  longitude
    x , y = m(user_lon, user_lat)
    user_lon_list.append(x)
    user_lat_list.append(y)
    m1.plot(x,y,'*',markersize= 20,markerfacecolor="k")
    plt.legend(loc = 3)
    plt.title('Plotting of user coordinate and its distance from already built constructions hub')
    plt.show()
    
    
##############################################################################
#defining the coordinates for the trained locations in a list and passing user input to it
##############################################################################
    user_coord = [latitude, longitude]
    user_coord[0] = latitude
    user_coord[1] = longitude
    cities = {
        'Ch_1': (52.3667,4.8945,),
        'Ch_2': (51.9244,4.4777),
        'Ch_3': (52.0988,4.2598), 
        'Ch_4': (52.9947,6.5632),
        'Ch_5': (52.2574,6.7928)}

###############################################################################
#plotting the distance
###############################################################################
    print('Please wait while the distance is claculated. It may take a while be paitent')
    time.sleep(5)
    for city, coord in cities.items():
        a= coord[0]
        b= coord[1]
        user_lat_list = []
        user_lon_list = []
        user_lat = latitude
        user_lon = longitude
        x , y = m(user_lon, user_lat)
        user_lon_list.append(x)
        user_lat_list.append(y)
        user_lon_list.append(b)
        user_lat_list.append(a)
        d = distance(user_coord, coord)
        
        plt.figure(figsize=(10,10))
        
        m2 = Basemap(llcrnrlon=3.3149,llcrnrlat=50.803721015,urcrnrlon= 7.09205325687,urcrnrlat=53.5104033474, resolution = 'h')
        m2.drawmapboundary(fill_color='aqua')
        #Fill the continents with the land color
        m2.fillcontinents(color='coral',lake_color='aqua')
        m2.drawcoastlines()
        m2.drawcountries(linewidth=3)
        m2.drawstates(color='black')
        m2.plot(user_lon_list,user_lat_list, color = 'k', label= (d), linewidth = 3)
        plt.legend(loc = 3)
        plt.title('Distance between user coordinates and already built construction hub')
        plt.show()
        print("The distance of your choosen coordinates from the %s is : %s" % (city,d))
        
    print('\n')
    print('\n')
    #print('Welcome again.....Please provide details!')
    i = i+1

#city_coordinates = cities()
#print(city_coordinates)
    
# Makes a plot of all cities. Input: city_coordinates; dictionary of all cities and their coordinates in (x,y) format
     
cities = {
        'Ch_1': (52.3667,4.8945,),
        'Ch_2': (51.9244,4.4777),
        'Ch_3': (52.0988,4.2598), 
        'Ch_4': (52.9947,6.5632),
        'Ch_5': (52.2574,6.7928)}

coordinates = cities.values()
plot_cities(cities)

#print(create_guess(list(cities.keys())))
    
path = create_guess(list(cities.keys()))
#print(path)
plot_guess(cities, path,guess_in_title = True)

test_generation = create_generation(list(cities.keys()), population=10)
#print(test_generation)
#print(cities)
#print(check_fitness(test_generation))

breeders, _ = get_breeders_from_generation(test_generation)
#print(breeders)
#print(make_children(breeders, children_per_couple=2))
current_generation = create_generation(list(cities.keys()),population=500)
print_every_n_generations = 5

for i in range(100):
    if not i % print_every_n_generations:
        #print("Generation %i: "%i, end='')
        #print(len(current_generation))
        is_verbose = True
    else:
        is_verbose = False
    breeders, best_guess = get_breeders_from_generation(current_generation, 
                                                        take_best_N=250, take_random_N=100, 
                                                        verbose=is_verbose)
    current_generation = make_children(breeders, children_per_couple=3)
    
    
current_generation = create_generation([ 'Ch_1', 'Ch_2', 'Ch_3', 'Ch_4', 'Ch_5'],population=500)
fitness_tracking, best_guess = evolve_to_solve(current_generation, 100, 150, 70, 0.5, 3, 5, verbose=False)


print(' Plotting the best route in between the construction hubs in case the material needs to be carried from A--> B')
print('\n')
print('If the customer wants to travel in between the construction hubs!')
print('\n')

plot_guess(cities, best_guess)


