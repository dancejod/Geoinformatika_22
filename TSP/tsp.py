import json
from math import sqrt, inf
from json.decoder import JSONDecodeError
import matplotlib.pyplot as plt
import random
import sys

def euclidean_dist(x1, y1, x2, y2):
    """Calculates Euclidean distance using Pythagorean theorem."""
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def nearest_neighbor(coords_list):
    
    # Initialize the length of Hamiltonian circuit to 0
    # Initialize status of all points to "N" (Not Processed)
    W = 0
    status = ["N"] * (len(coords_list))
    
    # Choose random index from the input list of points
    # Then initialize coordinates of starting point using this index
    ui_idx = random.randrange(len(coords_list))
    ui = coords_list[ui_idx]
    
    # Set status of the starting point to "P" (Processed)
    status[ui_idx] = "P"
    
    # Prepare list for visualization of Hamiltonian circuit
    # Append the starting point to this list
    circuit = []
    circuit.append(ui)
    
    # While any Not Processed points exist
    while "N" in status:
        
        # Initialize minimum distance to infinity
        min_dist = inf
        
        # Calculate Euclidean distance between two points
        for point in range(len(coords_list)):
            dist = euclidean_dist(ui[0], ui[1], coords_list[point][0], coords_list[point][1])
            
            # If calculated distance between two points is shorter than current minimum distance
            # and the endpoint is not yet Processed
            if dist < min_dist and status[point] != "P":
                
                # Set minimum distance to current distance and store endpoint and its index
                min_dist = dist
                u_idx = point
                u = coords_list[u_idx]
        
        # Add minimum distance to the current length of Hamiltonian circuit
        # Append endpoint to the Hamiltonian circle
        W += min_dist
        circuit.append(u)
        
        # Set starting point to current endpoint
        ui = u
        
        # Change the status of current endpoint to Processed
        status[u_idx] = "P"
    
    # Add first point to the end of the Hamiltonian circuit list to form a circle
    circuit.append(circuit[0])
    
    plt.plot([coord[0] for coord in circuit], [coord[1] for coord in circuit], c="black", linewidth=1)
    plt.scatter([coord[0] for coord in coords_list], [coord[1] for coord in coords_list], s=20, c = "white", edgecolors = "black")
    plt.scatter(circuit[0][0], circuit[0][1], s=20, c = "red", edgecolors = "red")
    plt.title("Index of starting point (in red): {}".format(ui_idx))
    plt.show()
    
    return W, circuit

def best_insertion(coords_list):
    
    
    # Initialize the length of Hamiltonian circuit to 0
    # Initialize status of all points to "N" (Not Processed)
    W = 0
    status = ["N"] * (len(coords_list))
    
    circuit = []
    dist_list = []
    
    random_indices = random.sample(range(len(coords_list)), 3)
    random_indices.append(random_indices[0])
    
    for idx in random_indices:
        circuit.append(coords_list[idx])
        status[idx] = 'P'
    
    for point, next_point in zip(circuit, circuit[1:]):
        dist = euclidean_dist(point[0], point[1], next_point[0], next_point[1])
        W += dist

    while "N" in status:
        
        u_idx = random.choice([idx for idx in range(len(coords_list)) if status[idx] == "N"])
        u = coords_list[u_idx]
        delta_w = inf
        
        for distance in range(len(circuit) - 2):
            # Vezmem dva za sebou iduce uzly okrem posledneho
            ui = circuit[distance]
            uj = circuit[distance + 1]
            
            # Vypocitam medzi nimi vzdialenost
            ui_uj_dist = euclidean_dist(ui[0], ui[1], uj[0], uj[1])
            
            # Vypocitam sucet odvesien (u plus u1, u+ u1i)
            sum_distances_from_u = euclidean_dist(ui[0], ui[1], u[0], u[1]) + euclidean_dist(uj[0], uj[1], u[0], u[1])
            
            # Ak je sucet odvesien vacsi ako prepona
            if sum_distances_from_u > ui_uj_dist:
                
                # Ak je sucet odvesien mensi ako predosly sucet
                if sum_distances_from_u - ui_uj_dist < delta_w:
                    
                    # Aktualizuj najmensi sucet odvesien, zapamataj si index ui
                    delta_w = sum_distances_from_u - ui_uj_dist
                    ui_idx = distance

        W += delta_w
        
        circuit.insert((ui_idx + 1), u)

        status[u_idx] = "P"
        
    plt.plot([coord[0] for coord in circuit], [coord[1] for coord in circuit], c="black", linewidth=1)
    plt.scatter([coord[0] for coord in coords_list], [coord[1] for coord in coords_list], s=20, c = "white", edgecolors = "black")
    plt.scatter(circuit[0][0], circuit[0][1], s=20, c = "red", edgecolors = "red")
    plt.title("Index of starting point (in red): {}".format(u_idx))
    plt.show()
        
        
        
    

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

#W_NN, NN_h_circuit = nearest_neighbor(coords)

best_insertion(coords)
