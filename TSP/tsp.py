import json
from math import sqrt, inf
from json.decoder import JSONDecodeError
import matplotlib.pyplot as plt
import random
import sys

def euclidean_dist(x1, y1, x2, y2):
    '''Calculates Euclidean distance using Pythagorean theorem.'''
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def nearest_neighbor(coords_list, reps, starting_node, separate_plots):
    '''
    Nearest Neighbor algorithm.

        Parameters:
            coords_list (list): List of coordinations of nodes.
            reps (int): Number of repetitions of the algorithm. If starting node is specified,
                        repetitions will not yield different results.
            starting_node (int): Index of the starting node.
            separate_plots (bool): Specifies whether to draw separate plots for this algorithm.

        Returns:
            results (list): List of Hamiltonian circuits and their lengths.
    '''
    
    # Prepare results list
    results = []
        
    # Repeat the algorithm number of reps times
    for rep in range(reps):
        
        # Initialize the length of Hamiltonian circuit to 0
        # Initialize status of all points to "N" (Not Processed)
        W = 0
        status = ["N"] * (len(coords_list))
        
        # Choose random index from the input list of points
        # Then initialize coordinates of starting point using this index
        if starting_node == "unspecified":
            ui_idx = random.randrange(len(coords_list))
            ui = coords_list[ui_idx]
        
        # If starting node was specified, initialize its coordinates
        else:
            ui_idx = starting_node
            ui = coords_list[starting_node]
            
        # Set status of the starting point to "P" (Processed)
        status[ui_idx] = "P"
        
        # Prepare list for visualization of Hamiltonian circuit
        # Append the starting point to this list
        circuit = []
        circuit.append(ui)
        
        # While any Not Processed nodes exist
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
        # Calculate the remaining distance between two last points
        W += euclidean_dist(ui[0], ui[1], circuit[0][0], circuit[0][1])
        circuit.append(circuit[0])
        
        # Append length W and Hamiltonian circuit
        results.append([W, circuit])
        
        if separate_plots:
            plt.plot([coord[0] for coord in circuit], [coord[1] for coord in circuit], c="black", linewidth=1)
            plt.scatter([coord[0] for coord in coords_list], [coord[1] for coord in coords_list], s=20, c = "white", edgecolors = "black")
            plt.scatter(circuit[0][0], circuit[0][1], s=40, c = "red", edgecolors = "red")
            plt.title("Nearest Neighbor method, W = {} km".format(round(W/1000, 2)))
            plt.show()
    
    return results

def best_insertion(coords_list, reps, starting_node, separate_plots):
    '''
    Best Insertion algorithm.

        Parameters:
            coords_list (list): List of coordinations of nodes.
            reps (int): Number of repetitions of the algorithm. If starting node is specified,
                        repetitions will not yield different results.
            starting_node (int): Index of the starting node.
            separate_plots (bool): Specifies whether to draw separate plots for this algorithm.

        Returns:
            results (list): List of Hamiltonian circuits and their lengths.
    '''
    
    # Prepare results list
    results = []
    
    # Repeat the algorithm number of reps times
    for rep in range(reps):
        
        # Initialize the length of Hamiltonian circuit to 0
        # Initialize status of all points to "N" (Not Processed)
        W = 0
        status = ["N"] * (len(coords_list))
        
        # Prepare list for visualization of Hamiltonian circuit
        circuit = []
        
        # If starting node was not specified
        if starting_node == "unspecified":
            
            # Get random indices of three nodes
            # Append the first index again to form a circle
            random_indices = random.sample(range(len(coords_list)), 3)
            random_indices.append(random_indices[0])
        
        # If starting node was specified
        else:
            
            # Get random indices of three nodes again but replace the first index
            # with starting node index
            random_indices = random.sample(range(len(coords_list)), 3)
            random_indices[0] = starting_node
            random_indices.append(starting_node)
        
        # Append nodes to Hamiltonian circuit using prepared indices
        # Set their status to Processed
        for idx in random_indices:
            circuit.append(coords_list[idx])
            status[idx] = 'P'
        
        # Calculate the length of the circle
        for point, next_point in zip(circuit, circuit[1:]):
            dist = euclidean_dist(point[0], point[1], next_point[0], next_point[1])
            W += dist
            
        # While any Not Processed nodes exist 
        while "N" in status:
            
            # Select random Not Processed node
            # Initialize the minimum length increment to infinity
            u_idx = random.choice([idx for idx in range(len(coords_list)) if status[idx] == "N"])
            u = coords_list[u_idx]
            delta_w = inf
            
            # For all nodes except last two (to avoid working with the starting node)
            for distance in range(len(circuit) - 2):
                
                # Get two consecutive nodes
                ui = circuit[distance]
                uj = circuit[distance + 1]
                
                # Calculate their distance
                ui_uj_dist = euclidean_dist(ui[0], ui[1], uj[0], uj[1])
                
                # Calculate and sum their distance from the current node
                sum_distances_from_u = euclidean_dist(ui[0], ui[1], u[0], u[1]) + euclidean_dist(uj[0], uj[1], u[0], u[1])
                
                # If this sum is greater than the distance between two consecutive nodes (hypotenuse)
                if sum_distances_from_u > ui_uj_dist:
                    
                    # And if this sum minus hypotenuse is smaller than the minimum length increment
                    if sum_distances_from_u - ui_uj_dist < delta_w:
                        
                        # Set the minimum length increment to this sum minus hypotenuse
                        # Store index of the first node of the created 3-node-path
                        delta_w = sum_distances_from_u - ui_uj_dist
                        ui_idx = distance
            
            # Add minimum length increment to W
            W += delta_w
            
            # Insert current node between nodes forming the selected path
            circuit.insert((ui_idx + 1), u)
            
            # Set the status of current node to Processed
            status[u_idx] = "P"
        
        # Append length W and Hamiltonian circuit
        results.append([W, circuit])

        if separate_plots:
            plt.plot([coord[0] for coord in circuit], [coord[1] for coord in circuit], c="black", linewidth=1)
            plt.scatter([coord[0] for coord in coords_list], [coord[1] for coord in coords_list], s=20, c = "white", edgecolors = "black")
            plt.scatter(circuit[0][0], circuit[0][1], s=40, c = "red", edgecolors = "red")
            plt.title("Best Insertion method, W = {} km".format(round(W/1000, 2)))
            plt.show()
    
    return results
        
def load_coordinates(filename):
    '''
    Loads coordinates (nodes) from input JSON file.

        Parameters:
            filename (file): A JSON file containing geographical coordinates.

        Returns:
            coordinates (list): List of oordinates from input file.
    '''
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

def visualize_comparison(NN_results, BI_results, reps):
    '''
    Visualize both NN and BI algorithms next to each other for comparison.

        Parameters:
            NN_results (list): List of results of NN algorithm.
            BI_results (list): List of results of BI algorithm
    '''
    
    # Create comparison plots for each repetition
    for rep in range(reps):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle("Travelling Salesman Problem, repetition number: {}".format(rep + 1), fontsize = 20)
        ax1.plot([coord[0] for coord in NN_results[rep][1]], [coord[1] for coord in NN_results[rep][1]], c="black", linewidth=1)
        ax1.scatter([coord[0] for coord in NN_results[rep][1]], [coord[1] for coord in NN_results[rep][1]], s=20, c = "white", edgecolors = "black")
        ax1.scatter(NN_results[rep][1][0][0], NN_results[rep][1][0][1], s=40, c = "red", edgecolors = "red")
        ax1.set_title("Nearest Neighbor method, W = {} km".format(round(NN_results[rep][0]/1000, 2)))
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        ax2.plot([coord[0] for coord in BI_results[rep][1]], [coord[1] for coord in BI_results[rep][1]], c="black", linewidth=1)
        ax2.scatter([coord[0] for coord in BI_results[rep][1]], [coord[1] for coord in BI_results[rep][1]], s=20, c = "white", edgecolors = "black")
        ax2.scatter(BI_results[rep][1][0][0], BI_results[rep][1][0][1], s=40, c = "red", edgecolors = "red")
        ax2.set_title("Best Insertion method, W = {} km".format(round(BI_results[rep][0]/1000, 2)))
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        plt.show()

def TSP(coords_list, reps = 10, algorithm = "all", starting_node = "unspecified", separate_plots = False):
    '''
    Specifies conditions on which the script runs.

        Parameters:
            coords_list (list): List of geographical coordinates.
            reps (int): Number of repetitions. DEFAULT = 10
            algorithm (str): Specifies which algorithm is used to solve the Travelling Salesman Problem.
                             DEFAULT = "all" (both) OPTIONAL = "NN" (Nearest Neighbor); "BI" (Best Insertion)
            starting_node (int): Specifies the starting node. DEFAULT = "unspecified".
            separate_plots (bool): Specifies whether to draw separate plots for NN and BI algorithms.
                                   DEFAULT = False

        Returns:
            DEFAULT
            NN_results, BI_results (tuple): Tuple containing all results from both algorithms.
            
            OPTIONAL
            NN_results (list): List of results of all repetitions of NN algorithm.
            BI_results (list): List of results of all repetitions of BI algorithm.
    '''
    
    if algorithm == "all":
        NN_results = nearest_neighbor(coords_list, reps, starting_node, separate_plots)
        BI_results = best_insertion(coords_list, reps, starting_node, separate_plots)
        visualize_comparison(NN_results, BI_results, reps)
        return NN_results, BI_results
    
    elif algorithm == "NN":
        NN_results = nearest_neighbor(coords, reps, starting_node, separate_plots)
        return NN_results
    
    elif algorithm == "BI":
        BI_results = best_insertion(coords, reps, starting_node, separate_plots)
        return BI_results
    
    else:
        sys.exit("Unknown parameters. The script will now terminate.")

# Load coordinates
coords = load_coordinates("villages_zemplin_sjtsk.json")

# Save results of TSP with (un)specified arguments
tsp = TSP(coords, starting_node=7)