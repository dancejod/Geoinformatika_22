from PIL import Image, ImageOps
import numpy as np
from math import inf
import csv
import sys

# Default settings.
# (Optional) Set THRESHOLD to a higher value for more defined edge points.
# (Optional) Set window_size to an odd number (at least 3) 
THRESHOLD = 3500    
window_size = 9

def create_window(size):
    base_vector_list = [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
    
    # ak je cislo liche
    if (int(size) % 2) == 1 and size >= 3:
        
        # ako musim zvacsit bazove vektory, aby mi opisali cele moje ziadane okno
        vector_multiplier = size // 2
        
        # ak je zvysok po celociselnom deleni dvojkou 1, ide o maticu 3x3, mozem ihned vratit
        if vector_multiplier == 1:
            return base_vector_list
        
        new_vector_list = []
        
        # postupne pridavam do noveho zoznamu vektory ktore su sucinom bazovych vektorov
        for i in range(1, vector_multiplier + 1):
            
            for vector in base_vector_list:
                new_vector = [value * i for value in vector]
                
                if new_vector not in base_vector_list:
                    new_vector_list.append(new_vector)
        
        # rozsirim povodny zoznam vektorov o nove vektory
        base_vector_list.extend(new_vector_list)
        return base_vector_list
            
    elif int(size) <= 3:
        sys.exit("The size of the window has to be at least 3.")

    else:
        sys.exit("The size of the window has to be an odd number (at least 3).")

def convert_image_to_matrix(img):
    try:
        image = Image.open(img)
    except FileNotFoundError:
        sys.exit
    image = ImageOps.grayscale(image)
    image_matrix = np.array(image, dtype="int64")
    return image_matrix

def write_edges_to_file(edges_list, outfilename):
    with open(f"{outfilename}.csv", 'w', newline = '') as out:
        csv.writer(out, delimiter = ',').writerow(["row,column"])
        csv.writer(out, delimiter = ',').writerows(edges_list)
        
def save_edge_map(image_matrix, outimgname):
    # asi to chce sprehladnit
    # ale output sa obmedzuje len na tie pixely na ktorych sa dalo pocitat, tj orezem okraj z povodneho obrazka
    image_matrix = image_matrix[window_size-1:image_matrix.shape[0]-(window_size-1), window_size-1:image_matrix.shape[1]-(window_size-1)]
    edge_map = Image.fromarray((image_matrix * 255).astype(np.uint8))
    edge_map.save(f"{outimgname}.jpg")

def moravec(image_matrix, edges_list, threshold):
    # nic nevraciam lebo len modifikujem povodne premenne 
    # mozem ze ano
    for col in range(window_size - 1, image_matrix.shape[1] - window_size + 1):
        for row in range(window_size - 1, image_matrix.shape[0] - window_size + 1):
    
            min_intensity = inf
            sum_list = []
            
            for pixel in window:
                diff_list = []
                
                for vector in vector_list:
                    offset_y = col + pixel[0] + vector[0]
                    offset_x = row + pixel[1] + vector[1]
    
                    squared_diff = (image_matrix[offset_x, offset_y] - image_matrix[row + pixel[1], col + pixel[0]])**2
                    diff_list.append(squared_diff)
            
                sum_list.append(sum(diff_list))
            min_intensity = min(sum_list)
            
            if min_intensity >= threshold:
                image_matrix[row, col] = 4000
                edges_list.append([row, col])
                
            else:
                image_matrix[row, col] = 0
        
                
edges = []
vector_list = create_window(window_size)
window = vector_list + [[0,0]]
IM = convert_image_to_matrix("lena.jpg")
moravec(IM, edges, THRESHOLD)
edges.sort()
write_edges_to_file(edges, "edges")
save_edge_map(IM, "lena_edges")