# Moravec edge detector

## About

This operator detects the corners of objects in an image by observing changes in intensity around one pixel in all directions.

## Usage

Put `moravec.py` in the same directory as your image. Execute the script.  
If needed, rewrite the default string `lena.tif` on line 186 to the title of your image (with an extension).  

The script returns a `.csv` file containing coordinates of detected edge points and a `.tif` file of the image's edge map.

### Customization

Variables in `UPPERCASE` can be edited. It is not recommended to set them to high values as it greatly decreases the script's performance.  
Output file names can also be edited by rewriting the default strings in functions `write_edges_to_file` and `save_edge_map` (lines 189 and 190).


<p align="center">
<img src="https://user-images.githubusercontent.com/90621465/209814062-4c0391a3-9f36-4c33-bd09-2d77671b559b.png" width="600">
</p>


## References
* H. Moravec, “Obstacle Avoidance and Navigation in the Real World by a Seeing Robot Rover”, technical report, Carnegie–Mellon University, Robotics Institute, 1980.
* V. Mazet, “Corner detection – Basics of Image Processing”, 2022, https://vincmazet.github.io/bip/detection/corners.html (26. 12. 2022).
