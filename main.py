from asc import AsciiConverter
import sys


def main():
    # default values
    scale = 0.5
    font = "fonts/UbuntuMono.ttf"
    font_size = 15
    colour = False
    contrast = None
    brightness = None
    force = False

    # get arguments
    if len(sys.argv) < 2:
        filename = input("Please enter the path to the image file.")
    else:
        filename = sys.argv[len(sys.argv) - 1]

    for i, arg in enumerate(sys.argv):
        match arg:
            case "-s":
                scale = int(sys.argv[i + 1])
            case "-f":
                font = sys.argv[i + 1]
            case "-fs":
                font_size = int(sys.argv[i + 1])
            case "-col":
                colour = True
            case "-c":
                contrast = float(sys.argv[i + 1])
            case "-b":
                brightness = float(sys.argv[i + 1])
            case "-F":
                force = True

    # run program
    converter = AsciiConverter(filename, scale, font, font_size)

    if brightness != None:
        converter.apply_brightness(brightness)
    if contrast != None:
        converter.apply_contrast(contrast)

    if colour:
        converter.generate_colour_ascii()
    else:
        converter.generate_grey_ascii(force)


if __name__ == "__main__":
    main()
