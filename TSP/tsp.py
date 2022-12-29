import json
from pyproj import Transformer
from math import sqrt, inf
from json.decoder import JSONDecodeError
import matplotlib.pyplot as plt
import random
import sys

def euclidean_dist(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def nearest_neighbor(coords_list):
    
    # Initialize 
    W = 0
    status = ["N"] * (len(coords_list))
    
    # get random coord lol
    ui_idx = random.randrange(len(coords_list))
    ui = coords_list[ui_idx]
    
    # Set status of chosen coord to "P"
    status[ui_idx] = "P"
    
    #coords_list.pop(ui_idx)
    # Prepare list for visualization of Hamiltonian circle
    circuit = []
    
    circuit.append(ui)
    
    while "N" in status:
        min_dist = inf
        
        for point in range(len(coords_list)):
            dist = euclidean_dist(ui[0], ui[1], coords_list[point][0], coords_list[point][1])
            
            if dist < min_dist and status[point] != "P":
                min_dist = dist
                u_idx = point
                u = coords_list[u_idx]
                
        W += min_dist
        circuit.append(u)
        ui = u
        status[u_idx] = "P"
        
    circuit.append(circuit[0])
    plt.plot([coord[0] for coord in circuit], [coord[1] for coord in circuit], c="black", linewidth=1)
    plt.scatter([coord[0] for coord in coords_list], [coord[1] for coord in coords_list], s=20, c = "white", edgecolors = "black")
    plt.scatter(circuit[0][0], circuit[0][1], s=20, c = "red", edgecolors = "red")
    plt.show()
    
    return W, circuit
        
def load_coordinates(filename):
    try:
        with open(filename, encoding="utf-8") as jsonfile:
            reader = json.load(jsonfile)
            coordinates = []
            
            for coord in reader["features"]:
                coordinates.append(coord["geometry"]["coordinates"])
                
            return coordinates
    
    except FileNotFoundError:
        sys.exit(f"File {filename} not found.")

    except IOError:
        sys.exit(f"{filename}: Incorrect file name or location.")
        
    except PermissionError:
        sys.exit(f"{filename}: Permission denied.")

    except JSONDecodeError:
        sys.exit(f"{filename}: Invalid JSON file.")


coords = load_coordinates("villages_zemplin_sjtsk.json")

W_NN, NN_h_circuit = nearest_neighbor(coords)

