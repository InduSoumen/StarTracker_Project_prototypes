import cv2
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

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

# Initialize a list to hold centroids
centroids = []
for contour in contours:
    # Draw bounding rectangles around each star (as in the original code)
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image_with_stars, (x, y), (x + w, y + h), (0, 255, 0), 1)

    # Calculate the centroid of each contour
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        centroids.append((cx, cy))

        # Draw a small circle at the centroid position
        cv2.circle(image_with_stars, (cx, cy), 3, (0, 0, 255), -1)  # blue circle for centroids
        for i in range(len(centroids) - 1):
            # Draw a line between consecutive centroids
            cv2.line(image_with_stars, centroids[i], centroids[i + 1], (255, 255, 0), 1)  # yellow line
# Display the result
plt.subplot(144)
plt.imshow(image_with_stars)
plt.title("Detected Stars with Centroids")
plt.axis("off")
plt.subplot(141)
plt.imshow(image, cmap="gray")
plt.title("Gray Scale")
plt.axis("off")
plt.subplot(142)
plt.imshow(blurred_image, cmap="gray")
plt.title("Blurred Image")
plt.axis("off")
plt.subplot(143)
plt.imshow(thresholded_image, cmap="gray")
plt.title("Threshold Image")
plt.axis("off")

plt.show()
