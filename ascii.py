"""
File:   ascii.py
Author: Marco Plaitano
Date:   16 Feb 2022

IMAGE TO ASCII CONVERTER
Create a text document containing the ASCII representation of any given image.
"""

from sys import argv
from PIL import Image, UnidentifiedImageError


DEFAULT_IMAGE = "data/fish.jpeg"

# Output text file.
ASCII_FILE_PATH = "ascii_image.txt"

# Width (row size) of the output text.
# The higher this value is, the more details the ASCII text will show.
# Set this to 0 to keep the original size.
OUTPUT_WIDTH = 120

# ASCII characters to replace the image pixels with. Sorted to match from lowest
# to highest level of brightness.
SEQUENCE = " .:-=+*#%@"

# When True, map "higher value" characters of SEQUENCE to the shadowy part of
# the image.
# To be used when displaying black text on white background.
PRODUCE_NEGATIVE = False



def resize_image(image, new_width):
    """Resize the given image to have the specified new width and a new height
    that mantains the original aspect ratio.

    If new_width param is 0 the image will NOT be modified."""
    if new_width == 0:
        return image
    old_width, old_height = image.size
    new_height = int( old_height * new_width / old_width * 0.55 )
    return image.resize((new_width, new_height), Image.ANTIALIAS)


def negative(ascii_string):
    """Replace the characters of the ASCII string to generate a negative
    representation of the image."""
    new_string = ""
    for c in ascii_string:
        if c == "\n":
            new_string += "\n"
        else:
            index = len(SEQUENCE) - SEQUENCE.index(c) - 1
            new_string += SEQUENCE[index]
    return new_string


def create_ascii_string(image):
    """Find, for each pixel of the image, the corresponding character of the
    ASCII sequence to form a string."""
    string = ""
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            # Get index of character in SEQUENCE corresponding to current
            # pixel's brightness.
            index = int( pixel / 255 * (len(SEQUENCE) - 1) )
            # Add character to the string.
            string += SEQUENCE[index]
        # New line for every new row of pixels.
        string += "\n"
    return string



if __name__ == "__main__":
    if len(argv) > 1:
        image_path = argv[1]
    else:
        if DEFAULT_IMAGE:
            image_path = DEFAULT_IMAGE
        else:
            print("No image given.")
            exit(1)

    # Open the image file.
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Image file '{image_path}' not found.")
        exit(1)
    except UnidentifiedImageError:
        print(f"File '{image_path}' is not an image.")
        exit(1)

    # Resize image to have a width of 80 characters while keeping the original
    # aspect ratio
    image = resize_image(image, OUTPUT_WIDTH)

    # Turn image to greyscale to get, for each pixel its brightness value.
    image = image.convert("L")

    # Map pixels to characters.
    ascii_text = create_ascii_string(image)
    if PRODUCE_NEGATIVE:
        ascii_text = negative(ascii_text)

    # Write string to output file.
    with open(ASCII_FILE_PATH, "w", encoding="UTF-8") as file:
        file.write(ascii_text)
