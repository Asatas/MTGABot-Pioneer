#importing the module cv2 and numpy
import cv2
import numpy as np

# Reading the image
imagergb = cv2.imread(r"G:\Games\MTGABot-main\hand.png")

# Convert the image to HSV color space
imagehsv = cv2.cvtColor(imagergb, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for the blue tint in HSV (allowing slightly darker shades)
lower_bound = np.array([90, 90, 150])  # Lowered Value to 150 to include slightly darker shades
upper_bound = np.array([135, 255, 255])  # Still allows brighter and more saturated blue

# Mask the image to isolate the blue-tinted outline
imagemask = cv2.inRange(imagehsv, lower_bound, upper_bound)

# Save the resulting masked image
cv2.imwrite(r"G:\Games\MTGABot-main\handmask.png", imagemask)