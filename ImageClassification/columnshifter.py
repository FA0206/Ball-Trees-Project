import csv

def move_first_column_to_last(input_file, output_file):
    """
    Moves the first column of a CSV file to the last column.
    
    Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file with the modified column order.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Process each row: move the first column to the end
        for row in reader:
            if row:  # Skip empty rows
                modified_row = row[1:] + [row[0]]  # Move first column to the last position
                writer.writerow(modified_row)
    
    print(f"Modified CSV saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_csv = ""  # Input CSV file
    output_csv = ""  # Output CSV file
    move_first_column_to_last(input_csv, output_csv)
