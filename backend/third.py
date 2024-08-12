import cv2
import sys
import numpy as np
import os
import matplotlib.pyplot as plt

def checkFingerPrint(test_path, database_path):
    def load_image(image_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise Exception(f"Error: Unable to load image at {image_path}")
            return image
        except Exception as e:
            print(f"Error: {e}")
            return None


    # Load the test image
    sample = load_image(test_path)

    if sample is None:
        exit()

    # Initialize variables
    best_score = 0
    filename = None
    image = None
    kp1, kp2, mp = None, None, None


    # Check if the database directory exists
    if not os.path.exists(database_path) or not os.path.isdir(database_path):
        print(f"Error: The specified database path '{database_path}' does not exist or is not a directory.")
        exit()

    # Loop through each file in the database
    for file in os.listdir(database_path):
        # Construct the full path to the image in the database
        database_image_path = os.path.join(database_path, file)
        
        # Load the database image
        fingerprint_database_image = load_image(database_image_path)

        if fingerprint_database_image is None:
            continue

        # Create SIFT detector
        sift = cv2.SIFT_create()

        # Detect and compute keypoints and descriptors
        keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_database_image, None)

        # FLANN based matching
        matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(descriptors_1, descriptors_2, k=2)

        # Apply ratio test
        match_points = [p for p, q in matches if p.distance < 0.1 * q.distance]

        # Calculate the matching score
        keypoints = min(len(keypoints_1), len(keypoints_2))
        matching_score = len(match_points) / keypoints * 100

        # Update the best match if the current one is better
        if matching_score > best_score:
            best_score = matching_score
            filename = file
            image = fingerprint_database_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    # Draw and display the matches
    # if image is not None:
    #     result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
    #     result = cv2.resize(result, None, fx=4, fy=5)
    #     plt.imshow(result)
    #     plt.show()
        
    # Print the best match and score
    if filename is not None:
        return str(best_score)
    else:
        return "Not found"
    




__all__ = checkFingerPrint