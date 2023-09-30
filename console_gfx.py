# Border images


# Color list
BLACK, RED, DARK_GREEN, GOLD, BLUE, GARNETT, ORANGE, LIGHT_GRAY = (0, 1, 2, 3, 4, 5, 6, 7)
GRAY, PEACH, GREEN, BRIGHT_GOLD, CYAN, MAGENTA, BRIGHT_ORANGE, WHITE = (8, 9, 10, 11, 12, 13, 14, 15)

# Add special color variants
CLEAR = MAGENTA
TRANS_DISPLAY = BLACK

TEST_RAINBOW = [16, 2,
               0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
               0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

TEST_IMAGE = [14, 6,
             CLEAR, CLEAR, GREEN, GREEN, GREEN, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, GREEN, GREEN, CLEAR,
             CLEAR, GREEN, WHITE, BLACK, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, DARK_GREEN, GREEN, GREEN,
             GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, CLEAR,
             GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, BLACK, BLACK, BLACK, GREEN, CLEAR,
             GREEN, GREEN, GREEN, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, GREEN, GREEN, GREEN, CLEAR, CLEAR,
             CLEAR, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR]

# Initialize palettes / escape codes
fg_palette = []
bg_palette = []
em_palette = []
ul_palette = []

# Build dark color palettes
for color in range(0, 8):
    fg_palette.append("\033[0;3%dm" % color)
    em_palette.append("\033[1;3%dm" % color)
    ul_palette.append("\033[4;3%dm" % color)
    bg_palette.append("\033[4%dm" % color)

# Build bright color palettes
for color in range(0, 8):
    fg_palette.append("\033[0;9%dm" % color)
    em_palette.append("\033[1;9%dm" % color)
    ul_palette.append("\033[4;9%dm" % color)
    bg_palette.append("\033[10%dm" % color)

# Set up the color reset code
COLOR_RESET = "\033[0m"


def display_image(image_data, horizontal='═', up_left='╔', up_right='╗', vertical='║', low_left='╚', low_right='╝'):
    width = image_data[0]
    height = image_data[1]
    data_index = 2

    # Print first line of border box
    print(up_left + horizontal * width + up_right)

    # Print image in box
    for y_index in range(0, height, 2):
        out_string = vertical
        for x_index in range (0, width):
            out_color = image_data[data_index]
            out_string += fg_palette[TRANS_DISPLAY if out_color == CLEAR else out_color]
            out_color = image_data[data_index + width] if y_index + 1 < height else CLEAR
            out_string += bg_palette[TRANS_DISPLAY if out_color == CLEAR else out_color]
            out_string += "▀"
            data_index += 1
        data_index += width
        print(out_string + COLOR_RESET + vertical)

    # Print last line of border box
    print(low_left + horizontal * width + low_right)


def load_file(filename):
    with open(filename, "rb") as infile:
        return infile.read()

    return None
