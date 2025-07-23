import csv
from PIL import Image
import numpy as np
import os

def array_to_image(flattened_array, image_size=(28, 28), output_file=None):
    """
    Converts a flattened array into an image.
    
    Parameters:
        flattened_array (list or np.array): The flattened pixel values (e.g., 784 for MNIST).
        image_size (tuple): The dimensions of the image (default is (28, 28) for MNIST).
        output_file (str): Path to save the image file. If None, the image is just displayed.
    
    Returns:
        None
    """
    # Ensure the input array is a NumPy array
    array = np.array(flattened_array, dtype=np.uint8)
    
    # Reshape the array into the specified image dimensions
    reshaped_array = array.reshape(image_size)
    
    # Create an image from the array
    img = Image.fromarray(reshaped_array, mode='L')  # 'L' for grayscale
    
    # Save or display the image
    if output_file:
        img.save(output_file)
        print(f"Image saved to {output_file}")
    else:
        img.show()

def process_csv_file(file_path, image_size=(28, 28), num_images=10, output_dir="output_images"):
    """
    Reads pixel arrays from a CSV file and converts the first N arrays to images.
    
    Parameters:
        file_path (str): Path to the CSV file containing flattened arrays (each row is an array).
        image_size (tuple): The dimensions of the image (default is (28, 28)).
        num_images (int): Number of arrays to process.
        output_dir (str): Directory to save the output images.
    
    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read pixel arrays from CSV
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row
        rows = list(reader)  # Read the remaining rows

    # Process the first `num_images` arrays
    for i, row in enumerate(rows[:num_images]):
        # Ignore the last column (label) and convert the row of strings to integers
        pixel_array = list(map(int, row[:-1]))  # Exclude the last column (label)
        
        # Generate output file name
        output_file = os.path.join(output_dir, f"image_{i+1}.png")
        
        # Convert array to image
        array_to_image(pixel_array, image_size=image_size, output_file=output_file)

    print(f"Processed and saved {num_images} images to {output_dir}")

# Example usage
if __name__ == "__main__":
    # Replace this with the path to your CSV file containing pixel arrays and labels
    csv_file = "Datasets/csv/EMNIST_BAL_test.csv"  # Each row represents one flattened array and label
    process_csv_file(csv_file, image_size=(28, 28), num_images=15, output_dir="test_images/test_EMNIST_BAL")
