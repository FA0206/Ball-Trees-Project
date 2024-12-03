import struct
import numpy as np
import csv

def read_idx(filename):
    """Read MNIST IDX file format and return as a NumPy array."""
    with open(filename, 'rb') as f:
        zero, data_type, dims = struct.unpack('>HBB', f.read(4))
        shape = tuple(struct.unpack('>I', f.read(4))[0] for _ in range(dims))
        data = np.frombuffer(f.read(), dtype=np.uint8).reshape(shape)
    return data

def save_to_csv_with_labels_last(images, labels, output_file):
    """Save MNIST data to CSV with labels as the last column."""
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header (optional)
        writer.writerow([f"pixel_{i}" for i in range(784)] + ["label"])
        
        # Write each image's data with its label
        for img, label in zip(images, labels):
            row = img.flatten().tolist() + [label]  # Pixels first, then the label
            writer.writerow(row)

def main():
    # File paths (update with your actual paths)
    # train_images_path = ""
    # train_labels_path = ""

    train_images_path = ""
    train_labels_path = ""
    output_csv = ""
    
    # Read the data
    print("Reading MNIST data...")
    images = read_idx(train_images_path)
    labels = read_idx(train_labels_path)
    
    # Save to CSV
    print("Saving to CSV...")
    save_to_csv_with_labels_last(images, labels, output_csv)
    print(f"Data saved to {output_csv}")

if __name__ == "__main__":
    main()
