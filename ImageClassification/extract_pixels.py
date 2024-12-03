from PIL import Image
import csv

def extract_pixels(filename):
    # Open the image
    img = Image.open(filename)  # Replace with your image path

    # Resize the image to 5x5 pixels (if the image isn't already 5x5)
    img_resized = img.resize((28, 28))

    # Convert the image to grayscale
    img_gray = img_resized.convert('L')  # 'L' mode means grayscale (8-bit pixels, black and white)

    # Get the pixel values as a flattened list
    pixels = list(img_gray.getdata())  # This will give a flattened list of pixel
    return pixels

def save_pixels_to_csv(pixels_list, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write each flattened array as a row in the CSV file
        for i, flattened_pixels in enumerate(pixels_list):
            writer.writerow(flattened_pixels)
    
    # print(f"Pixel data has been saved to {output_filename}")

# enable this while compiling else code wont run
filename = input()
pixels_list = [extract_pixels(filename)]
save_pixels_to_csv(pixels_list, './lib/cache/input_image_cache.csv')


# Save the multiple pixel grids to a CSV file
# save_pixels_to_csv(pixels_list, 'multiple_images_pixels.csv')


# If you want the pixels in a 2D array format (rows and columns):
# width, height = img.size
# pixel_values_2d = [pixels[i * width:(i + 1) * width] for i in range(height)]

# Print the pixel values
# print("Flattened pixel values:", pixels)
# print("2D pixel values (first 5 rows):", pixel_values_2d[:5])

# pixels_list = [
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_0.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_1.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_2.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_3.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_4.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_5.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_6.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_7.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_8.png'),
#     extract_pixels('BallTrees/ImageClassification/number_images/digit_9.png')
# ]

# save_pixels_to_csv(pixels_list, 'BallTrees/ImageClassification/csv/numberData.csv')