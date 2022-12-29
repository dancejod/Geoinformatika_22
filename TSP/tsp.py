import json
from math import sqrt, inf
from json.decoder import JSONDecodeError
import matplotlib.pyplot as plt
import random
import sys

def euclid_dist(x1, y1, x2, y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def nearest_neighbor(coords_list):
    W = 0
    status = ["N"] * (len(coords_list))
    
    # get random coord lol
    ui_idx = random.randrange(len(coords_list))
    ui = coords_list[ui_idx]
    
    # Set status of chosen coord to "P"
    status[ui_idx] = "P"
    
    #coords_list.pop(ui_idx)
    # Prepare list for visualization of Hamiltonian circle
    circle = []
    
    circle.append(ui)
    
    
    while "N" in status:
        min_dist = inf
        
        for point in range(len(coords_list)):
            dist = euclid_dist(ui[0], ui[1], coords_list[point][0], coords_list[point][1])
            
            if dist < min_dist and status[point] != "P":
                min_dist = dist
                u_idx = point
                u = coords_list[u_idx]
                
        W += min_dist
        circle.append(u)
        ui = u
        status[u_idx] = "P"
        
    
    circle.append(circle[0])
    plt.scatter([coord[0] for coord in circle], [coord[1] for coord in circle], s=20, c = "white", edgecolors = "black")
    plt.plot([coord[0] for coord in circle], [coord[1] for coord in circle], c="black", linewidth=1)
    plt.show()
    
    return W, circle
        
def load_coordinates(filename):
    try:
        with open(filename, encoding="utf-8") as json_file:
            reader = json.load(json_file)
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

coords = load_coordinates("obce_zemplin.geojson")

nearest_neighbor(coords)

