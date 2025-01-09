import os
import csv
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("rename_files.log"),
        logging.StreamHandler()
    ]
)

def setup_argparse():
    """
    Sets up and parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Rename files based on a CSV list of old and new names.")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing the files to rename.")
    parser.add_argument("-l", "--list", required=True, help="CSV file with 'Old_name' and 'New_name' columns.")
    return parser.parse_args()

def read_csv(csv_file):
    """
    Reads a CSV file and extracts old and new file names.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        list of tuple: A list of tuples, where each tuple contains (old_name, new_name).

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing from the CSV.
    """
    logging.info(f"Reading CSV file: {csv_file}")
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if "Old_name" not in reader.fieldnames or "New_name" not in reader.fieldnames:
            raise ValueError("CSV file must contain 'Old_name' and 'New_name' columns.")
        
        rename_list = [(row["Old_name"], row["New_name"]) for row in reader]
        logging.info(f"Found {len(rename_list)} entries in the CSV file.")
    return rename_list

def rename_files(directory, rename_list):
    """
    Renames files in the specified directory based on the given rename list.

    Args:
        directory (str): Path to the directory containing the files to rename.
        rename_list (list of tuple): List of tuples containing old and new file names.

    Returns:
        None
    """
    logging.info(f"Changing working directory to: {directory}")
    os.chdir(directory)

    for old_name, new_name in rename_list:
        try:
            os.rename(old_name, new_name)
            logging.info(f"Renamed: {old_name} -> {new_name}")
        except FileNotFoundError:
            logging.error(f"File not found: {old_name}")
        except FileExistsError:
            logging.error(f"Target file already exists: {new_name}")
        except OSError as e:
            logging.error(f"Error renaming {old_name} -> {new_name}: {e}")

def main():
    """
    Main function to execute the file renaming process.

    Returns:
        None
    """
    args = setup_argparse()

    # Validate directory
    if not os.path.isdir(args.directory):
        logging.error(f"Directory does not exist: {args.directory}")
        return

    try:
        # Read CSV file and rename files
        rename_list = read_csv(args.list)
        rename_files(args.directory, rename_list)
    except (FileNotFoundError, ValueError) as e:
        logging.error(e)

if __name__ == "__main__":
    main()
