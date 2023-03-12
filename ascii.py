from PIL import Image

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', '$', 'S', 'H', 'M', 'W']


def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_pixels = ''.join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return ascii_pixels


def image_to_ascii(image_path, output_path):

    image = Image.open(image_path)
    image = resize_image(image)

    image = image.convert('L')


    ascii_pixels = pixels_to_ascii(image)
    lines = [ascii_pixels[index:index+image.width] for index in range(0, len(ascii_pixels), image.width)]

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

image_to_ascii('data/1.jpeg', 'data/output.txt')