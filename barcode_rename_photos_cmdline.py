import os
import argparse
from PIL import Image
from pyzbar.pyzbar import decode

################################################################################
# Works through a folder of images (.jpg/.cr2/.tif)
# Opens each image and reads in the text contained by the barcode/s in the image
# Chooses the NBGW barcode to rename the image if multiple options present
# If multiple images with the same barcode are encountered will append _B _C etc
# Will skip if it can't find a barcode in the image

# python3 barcode_rename_photos_cmdline.py folder_name

# Author  : Laura Jones
################################################################################

def decode_my_photo(file_name):
    result = decode(Image.open(file_name))
    decoded_items = []
    for x in result:
        decoded_items.append(str(x.data).replace("'", "").replace("b", ""))
    return decoded_items

def process_folder(folder_path):
    filename_count = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".cr2") or filename.lower().endswith(".tif"):
            file_path = os.path.join(folder_path, filename)
            decoded_data = decode_my_photo(file_path)
            if decoded_data:
                nbgw_item = next((item for item in decoded_data if item.startswith("NBGW")), None)
                selected_item = nbgw_item if nbgw_item else decoded_data[0]
                # Create a base new filename based on the selected item
                new_base_filename = f"{selected_item}{os.path.splitext(filename)[1]}"
                # Check if the filename has been encountered before
                if new_base_filename in filename_count:
                    count = filename_count[new_base_filename]
                    count += 1
                    filename_count[new_base_filename] = count
                    new_filename = f"{os.path.splitext(new_base_filename)[0]}_{chr(65 + count)}{os.path.splitext(new_base_filename)[1]}"
                else:
                    filename_count[new_base_filename] = 0
                    new_filename = new_base_filename
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")
            else:
                print(f"Skipping {filename} as barcode data is empty")

def main():
    parser = argparse.ArgumentParser(description='Read barcode in image and use it to rename the files in a folder.')
    parser.add_argument('folder_path', help='Path to the folder containing image files.')

    args = parser.parse_args()
    folder_path = args.folder_path

    process_folder(folder_path)

if __name__ == "__main__":
    main()