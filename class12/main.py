import cv2
import numpy as np
import argparse

# Function to detect Aruco markers
def detect_aruco_markers(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at the path: {image_path}")

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the dictionary and parameters for Aruco detection
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    # Detect markers
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    if ids is not None:
        print(f"Detected Aruco markers with IDs: {ids.flatten()}")
        for corner in corners:
            # Draw detected markers
            cv2.aruco.drawDetectedMarkers(image, corner)
    else:
        print("No Aruco markers detected.")
        return None, None

    return corners, ids

# Function to apply perspective transformation
def apply_perspective_transform(image, corners):
    # Define the destination points (assuming a rectangular shape)
    width, height = 400, 400  # Desired output size
    destination_points = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
    ], dtype='float32')

    # Get the four corners from the detected markers
    src_points = np.array(corners[0].reshape(4, 2), dtype='float32')  # Using the first marker's corners

    # Calculate the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, destination_points)

    # Apply the perspective transformation
    transformed_image = cv2.warpPerspective(image, matrix, (width, height))

    return transformed_image

# Function to find obstacles in the transformed image
def find_obstacles(transformed_image_path, obstacle_output_path):
    image = cv2.imread(transformed_image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at the path: {transformed_image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use edge detection to find obstacles (you can choose a different method)
    edges = cv2.Canny(gray, 50, 150)

    # Find contours of the obstacles
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    obstacle_count = len(contours)
    total_area = 0

    with open(obstacle_output_path, 'w') as f:
        f.write(f"Number of obstacles detected: {obstacle_count}\n")
        for contour in contours:
            area = cv2.contourArea(contour)
            total_area += area

    # Append total area to the output file
    with open(obstacle_output_path, 'a') as f:
        f.write(f"Total area covered by obstacles: {total_area}\n")

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--output", required=True, help="Path to output transformed image")
    parser.add_argument("--obstacle_output", required=True, help="Path to output obstacles text file")
    args = parser.parse_args()

    # Detect Aruco markers
    corners, ids = detect_aruco_markers(args.image)

    if corners is not None:
        # Apply perspective transform if markers are detected
        image = cv2.imread(args.image)
        transformed_image = apply_perspective_transform(image, corners)

        # Save the transformed image
        cv2.imwrite(args.output, transformed_image)
        print(f"Transformed image saved at: {args.output}")

        # Find obstacles in the transformed image
        find_obstacles(args.output, args.obstacle_output)
