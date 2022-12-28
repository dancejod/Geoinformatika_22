from PIL import Image, ImageOps
import numpy as np
from math import inf
import csv
import sys

# Default settings.
# (Optional) Set THRESHOLD to a higher value for more refined edge points.
# (Optional) Set window_size to an odd number greater than 3 to get more pronounced edges.
# WARNING: Setting window_size to a high value will lead to decreased performance.
THRESHOLD = 3500    
WINDOW_SIZE = 3

def generate_vectors(size):
    '''
    Generates vectors to access all pixels in a convolution window.

        Parameters:
            size (int): Size of the convolution window (size x size).

        Returns:
            base_vector_list (list): List of vectors to be used in edge calculation.
    '''
    
    # Create base vector list of all directions for minimum window size of 3
    base_vector_list = [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
    
    # If the selected window size is an odd number (at least 3), proceed
    if (int(size) % 2) == 1 and size >= 3:
        
        # Find the size of convolution window (number of pixels surrounding the central pixel from all directions)
        vector_multiplier = size // 2
        
        # If the vector multiplier is 1, the selected size is 3, therefore no need to generate more vectors
        if vector_multiplier == 1:
            return base_vector_list
        
        # Create empty list for new vectors
        new_vector_list = []
        
        # Compute all required vectors by multiplying base vector list
        for i in range(2, vector_multiplier + 1):
            
            for vector in base_vector_list:
                new_vector = [value * i for value in vector]
                new_vector_list.append(new_vector)
        
        # Extend the original vector list by new vectors
        base_vector_list.extend(new_vector_list)
        return base_vector_list
    
    # If the selected window size is less than 3, terminate script 
    elif int(size) <= 3:
        sys.exit("The size of the window has to be at least 3.")

    # If the size input is not convertible to int or is an even number, terminate script
    else:
        sys.exit("The size of the window has to be an odd number (at least 3).")

def create_convolution_window(vector_list):
    '''
    Creates convolution window used in detecting edges on source image.

        Parameters:
            vector_list (list): List of vectors covering the convolution window.

        Returns:
            window (list): List of vectors making up the window with added origin.
    '''
    window = vector_list + [[0,0]]
    return window

def convert_image_to_matrix(img):
    '''
    Converts source image to numpy matrix.

        Parameters:
            img (Image object): Source image.

        Returns:
            image_matrix (array): Image matrix.
    '''
    
    try:
        image = Image.open(img)
        
    except FileNotFoundError:
        sys.exit(f"The image {img} could not be found.")
    
    # Convert image to grayscale
    image = ImageOps.grayscale(image)
    image_matrix = np.array(image, dtype="int64")
    return image_matrix

def write_edges_to_file(edges_list, outfilename):
    '''
    Writes computed edges to a csv file.

        Parameters:
            edges_list (list): List of detected edges.
            outfilename (str): Name of the output file.
    '''
    
    with open(f"{outfilename}.csv", 'w', newline = '') as out:
        csv.writer(out, delimiter = ',').writerow(["row,column"])
        csv.writer(out, delimiter = ',').writerows(edges_list)
        
def save_edge_map(image_matrix, window_size, outimgname):
    '''
    Saves the detected edges to a tif image.

        Parameters:
            image_matrix (array): Image matrix.
            window_size (int): Size of the convolution window (size x size).
    '''
    
    # Crop the matrix in order to get rid of pixels not used in edge computation (source image bounds)
    image_matrix = image_matrix[window_size-1:image_matrix.shape[0]-(window_size-1), window_size-1:image_matrix.shape[1]-(window_size-1)]
    # Convert image matrix to Image object with adjusted values for increased performance
    edge_map = Image.fromarray((image_matrix * 255).astype(np.uint8))
    edge_map.save(f"{outimgname}.tif")

def moravec(image_matrix, threshold, window_size):
    '''
    An edge detection algorithm.
    The algorithm moves the convolution window around one pixel in all directions
    and assigns new value to this pixel based on finding whether it is an edge point or not.
    This implementation therefore modifies the original image matrix.

        Parameters:
            image_matrix (array): Image matrix.
            threshold (int): Threshold value from which the pixel is considered an edge point.
            window_size (int): Size of the convolution window (size x size).

        Returns:
            edges_list (list): List of detected edges.
    '''
    
    edges_list = []
    
    # Iterate over each pixel in the array except those not accessible with convolution window
    for col in range(window_size - 1, image_matrix.shape[1] - window_size + 1):
        for row in range(window_size - 1, image_matrix.shape[0] - window_size + 1):
            
            # Initialize minimum intensity value for current pixel to infinity 
            min_intensity = inf
            sum_list = []
            
            # Iterate over each pixel in the convolution window
            for pixel in window:
                diff_list = []
                
                # Get squared difference of two corresponding pixels in all directions
                for vector in vector_list:
                    offset_y = col + pixel[0] + vector[0]
                    offset_x = row + pixel[1] + vector[1]
    
                    squared_diff = (image_matrix[offset_x, offset_y] - image_matrix[row + pixel[1], col + pixel[0]])**2
                    
                    # Append the squared difference to a list
                    diff_list.append(squared_diff)
            
                # Append and evaluate the squared differences list to a sum list
                sum_list.append(sum(diff_list))
            
            # Select the lowest sum from sum list and declare it as minimum intensity value
            min_intensity = min(sum_list)
            
            # If minimum intensity value is greater than or equal to threshold,
            # the currently iterated pixel is declared an edge point and is appended to edges list
            if min_intensity >= threshold:
                # The matrix is modified in order to visualize the edge map
                image_matrix[row, col] = 4000
                edges_list.append([row, col])
            
            # If minimum intensity value is lower than threshold,
            # change its value to 0 as it is not an edge point (for visualization purposes)
            else:
                image_matrix[row, col] = 0
        
    return edges_list
        
# Execute the script with default file names
vector_list = generate_vectors(WINDOW_SIZE)
window = create_convolution_window(vector_list)
IM = convert_image_to_matrix("lena.tif")
edges = moravec(IM, THRESHOLD, WINDOW_SIZE)
edges.sort()
write_edges_to_file(edges, "edges")
save_edge_map(IM, WINDOW_SIZE, "lena_edges")