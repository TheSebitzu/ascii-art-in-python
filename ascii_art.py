from PIL import Image

ascii_characters = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def open_image(path):

    # Returns the image or None if it cant be loaded
    try:
        image = Image.open(path)
        print("Image loaded successfully")
        return image
    except FileNotFoundError:
        print("Unable to load image")
        return None


def get_pixel_matrix(image):
    # Get the pixel list
    pixels = list(image.getdata())

    # Turn the list into a matrix
    return [pixels[i : i + image.width] for i in range(0, len(pixels), image.width)]


def get_brightness_matrix(image):
    pixel_matrix = get_pixel_matrix(image)

    # Initialize a matrix the same size as the pixel matrix
    brightness_matrix = [
        [0 for _ in range(len(pixel_matrix[0]))] for _ in range(len(pixel_matrix))
    ]

    # Calculate each pixel's brightness
    for i in range(len(pixel_matrix)):
        for j in range(len(pixel_matrix[i])):
            pixel = pixel_matrix[i][j]
            brightness_matrix[i][j] = (pixel[0] + pixel[1] + pixel[2]) / 3

    return brightness_matrix


def get_ascii_matrix(image):
    brightness_matrix = get_brightness_matrix(image)

    # Initialize a matrix the same size as the brightness matrix
    ascii_matrix = [
        [0 for _ in range(len(brightness_matrix[0]))]
        for _ in range(len(brightness_matrix))
    ]

    # Calculate the coresponding ascii chars
    for i in range(len(brightness_matrix)):
        for j in range(len(brightness_matrix[i])):
            # Calculate the position in the ascii chars string
            ascii_matrix[i][j] = ascii_characters[
                int(brightness_matrix[i][j] / 255 * (len(ascii_characters) - 1))
            ]

    return ascii_matrix


def get_color_matrix(image):
    pixel_matrix = get_pixel_matrix(image)
    ascii_matrix = get_ascii_matrix(image)

    for i in range(len(ascii_matrix)):
        for j in range(len(ascii_matrix[i])):
            # Get red, green, blue
            r, g, b = pixel_matrix[i][j]

            # Give the coresponding color
            ascii_matrix[i][j] = f"\033[38;2;{r};{g};{b}m{ascii_matrix[i][j]}\033[0m"

    return ascii_matrix


def write_to_file(image, path, terminal=False, color=False):
    # Choose to print in terminal or not and in color or black and white
    
    ascii_matrix = get_ascii_matrix(image)

    if terminal == True:
        # Resize so it fits the terminal
        image = image.resize((100, int(image.height * 100 / image.width)))
        
        # Update black and white matrix with the resized image
        ascii_matrix = get_ascii_matrix(image)

        if color == True:
            # Print in terminal with color
            color_matrix = get_color_matrix(image)
            for row in color_matrix:
                # Print 3 chars for size
                print("".join([ch + ch + ch for ch in row]))

        else:
            # Print in terminal black and white
            for row in ascii_matrix:
                print("".join([ch + ch + ch for ch in row]))

    else:
        # Write in a file

        # Clear file
        with open(path, "w") as f:
            f.write("")

        # Write
        for row in ascii_matrix:
            with open(path, "a") as f:
                f.write("".join([ch + ch + ch for ch in row]) + "\n")

        # Terminal message for confirmation
        print("\nASCII art created!\n")


def main():

    # If there is an image
    if image := open_image(path=""): # Add file here

        # Color doesnt work outside terminal
        write_to_file(image, path="output.txt", terminal=True, color=True)


if __name__ == "__main__":
    main()
