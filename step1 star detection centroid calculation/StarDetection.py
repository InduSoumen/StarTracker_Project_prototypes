import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image in grayscale
image = cv2.imread("night_sky_image_3.jpg", cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

# Use thresholding to isolate bright spots (stars)
_, thresholded_image = cv2.threshold(blurred_image, 170, 200, cv2.THRESH_BINARY)

# Detect contours, which represent the stars
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Show the detected stars on the image
image_with_stars = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2RGB)

for contour in contours:

     x, y, w, h = cv2.boundingRect(contour)
     cv2.rectangle(image_with_stars, (x, y), (x + w, y + h), (0, 255, 0), 1)

# Display the result
plt.subplot(144)
plt.imshow(image_with_stars)
plt.title("Detected Stars")
plt.axis("off")
plt.subplot(141)
plt.imshow(image)
plt.title("Grey Scale")
plt.axis("off")
plt.subplot(142)
plt.imshow(blurred_image)
plt.title("Blurred Image")
plt.axis("off")
plt.subplot(143)
plt.imshow(thresholded_image)
plt.title("Threshold Image")
plt.axis("off")

plt.show()