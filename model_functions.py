import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def set_up_city(population_size, empty_ratio):
    # Ratio of races (-1, 1) and empty houses (0)
    p = [(1-empty_ratio)/2, (1-empty_ratio)/2, empty_ratio]
    city_size = int(np.sqrt(population_size))**2
    city = np.random.choice([-1, 1, 0], size=city_size, p=p)
    city = np.reshape(city, (int(np.sqrt(city_size)), int(np.sqrt(city_size))))
    
    return city


def run_simulation(city, n_neighbors, similarity_threshold):
    for (row, col), value in np.ndenumerate(city):
        race = city[row, col]
        if race != 0:
            neighborhood = city[row-n_neighbors:row+n_neighbors, col-n_neighbors:col+n_neighbors]
            neighborhood_size = np.size(neighborhood)
            n_empty_houses = len(np.where(neighborhood == 0)[0])
            if neighborhood_size != n_empty_houses + 1:
                n_similar = len(np.where(neighborhood == race)[0]) - 1
                similarity_ratio = n_similar / (neighborhood_size - n_empty_houses - 1.)
                is_unhappy = (similarity_ratio < similarity_threshold)
                if is_unhappy:
                    empty_houses = list(zip(np.where(city == 0)[0], np.where(city == 0)[1]))
                    random_house = random.choice(empty_houses)
                    city[random_house] = race
                    city[row,col] = 0   
                    
    return city


def get_mean_similarity_ratio(city, n_neighbors):
    count = 0
    similarity_ratio = 0
    for (row, col), value in np.ndenumerate(city):
        race = city[row, col]
        if race != 0:
            neighborhood = city[row-n_neighbors:row+n_neighbors, col-n_neighbors:col+n_neighbors]
            neighborhood_size = np.size(neighborhood)
            n_empty_houses = len(np.where(neighborhood == 0)[0])
            if neighborhood_size != n_empty_houses + 1:
                n_similar = len(np.where(neighborhood == race)[0]) - 1
                similarity_ratio += n_similar / (neighborhood_size - n_empty_houses - 1.)
                count += 1
    return similarity_ratio / count


def plot_city(city):
    cmap = ListedColormap(['red', 'white', 'royalblue'])

    plt.figure(figsize=(8, 8))

    plt.axis('off')
    plt.pcolor(city, cmap=cmap, edgecolors='w', linewidths=1)