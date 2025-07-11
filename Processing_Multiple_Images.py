import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import queue
import time

# Queue to process images
image_queue = queue.Queue()
output_folder = "C:/Users/manoj/PycharmProjects/StarTracker/output"  # Output folder for processed images

# Create output folder if not exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def process_image_in_main_thread():
    """Process images from the queue."""
    while True:
        image_path = image_queue.get()  # Get the next image path
        if image_path is None:
            break  # Exit the loop if None is received
        process_image(image_path)
        image_queue.task_done()


def process_image(image_path):
    """Detect stars in the image and save the processed output."""
    print(f"Processing image: {image_path}")
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Could not read image {image_path}")
        return

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

    # Save the processed output
    output_path = os.path.join(output_folder, f"processed_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, image_with_stars)
    print(f"Processed image saved to {output_path}")


class ImageHandler(FileSystemEventHandler):
    """Watchdog event handler to monitor directory for new files."""
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"New image detected: {file_path}")
            image_queue.put(file_path)  # Add the file to the queue


def monitor_directory(directory_to_watch, monitor_time=30):
    """Monitor directory for new images and fallback to existing ones."""
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()
    print(f"Monitoring directory: {directory_to_watch}")

    # Monitor for new images for a specified time
    start_time = time.time()
    try:
        while True:
            time.sleep(1)  # Keep the script running
            if time.time() - start_time > monitor_time:
                break
    except KeyboardInterrupt:
        observer.stop()
    observer.stop()
    observer.join()


def fallback_to_existing_images(directory):
    """Fallback to process existing images if no new ones are available."""
    print("No new images detected. Falling back to existing images.")
    existing_images = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not existing_images:
        print("No existing images to process.")
        return

    # Sort images by modification time (most recent first)
    existing_images.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Add existing images to the processing queue
    for image_path in existing_images:
        image_queue.put(image_path)


if __name__ == "__main__":
    directory_to_watch = "C:/Users/manoj/PycharmProjects/StarTracker"  # Change this to your folder path

    if not os.path.exists(directory_to_watch):
        os.makedirs(directory_to_watch)

    # Start a thread to process images in the main thread
    processing_thread = threading.Thread(target=process_image_in_main_thread, daemon=True)
    processing_thread.start()

    # Start monitoring the directory for a defined time
    monitor_directory(directory_to_watch, monitor_time=30)

    # If no images were added, process existing images
    fallback_to_existing_images(directory_to_watch)

    # Wait for the queue to process all images
    image_queue.join()
