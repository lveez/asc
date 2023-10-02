import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


class AsciiConverter:
    def __init__(
        self,
        path,
        image_scale=1,
        font="fonts/UbuntuMono.ttf",
        font_size=12,
        custom_chars=None,
    ):
        self.path = path  # path to file
        self.image_scale = image_scale  # image scaling before ascii conversion is done

        # load image
        self.image_data = Image.open(path)
        self.width = self.image_data.width
        self.height = self.image_data.height
        self.resize_image()
        self.pixels = self.__image_to_pixels()

        # init fonts
        if font_size % 2:
            font_size += 1
        self.__font_size = font_size
        self.__font_name = font
        self.__font = ImageFont.truetype(font, size=font_size)

        # ascii char database
        self.__chars = np.array(list(' .",:;!~+-xmo*#W&8@'))
        self.__colour_chars = np.array(list(" ixzao*#MW&8%B@$"))
        self.__custom_chars = None  # custom chars for the ascii conversion
        if custom_chars != None:
            self.__custom_chars == custom_chars

    # generates a greyscale ascii art version of the current image
    def generate_grey_ascii(self, force_all_characters=False):
        if self.__custom_chars != None:
            chars = self.__custom_chars
        else:
            chars = self.__chars

        luminance = self.__convert_pixels_to_luminance(self.pixels)
        if force_all_characters == True:
            luminance = luminance / max(luminance)
        indexes = np.around(luminance * (len(self.__chars) - 1)).astype(np.int32)
        indexes = np.split(indexes, len(indexes) / self.image_data.width)

        # create new image
        target = Image.new(
            "RGB",
            (
                int(self.image_data.width * self.__font_size / 2),
                int(self.image_data.height * self.__font_size),
            ),
            color=0,
        )
        draw = ImageDraw.Draw(target)
        draw.font = self.__font

        offset = 0

        for line in indexes:
            s = "".join(chars[line])
            draw.text((0, offset), s, align="center")
            offset += self.__font_size

        target.save(self.path[:-4] + "_ascii.png")
        target.show()

    # generates a colour ascii art version of the current image
    def generate_colour_ascii(self):
        if self.__custom_chars != None:
            chars = self.__custom_chars
        else:
            chars = self.__colour_chars

        luminance = self.__convert_pixels_to_luminance(self.pixels)
        indexes = np.around(luminance * (len(self.__colour_chars) - 1)).astype(np.int32)
        indexes = np.split(indexes, len(indexes) / self.image_data.width)

        # create new image
        target = Image.new(
            "RGB",
            (
                int(self.image_data.width * self.__font_size / 2),
                int(self.image_data.height * self.__font_size),
            ),
            color=0,
        )
        draw = ImageDraw.Draw(target)
        draw.font = self.__font

        y_offset = 0
        pixel = 0
        for line in indexes:
            x_offset = 0
            for index in line:
                draw.text(
                    (x_offset, y_offset),
                    str(chars[index]),
                    align="center",
                    fill=tuple(self.pixels[pixel]),
                )
                x_offset += self.__font_size / 2
                pixel += 1
            y_offset += self.__font_size

        target.save(self.path[:-4] + "_ascii.png")
        target.show()

    # changes the current image
    def change_image(self, path):
        self.path = path
        self.image_data = Image.open(path)
        self.width = self.image_data.width
        self.height = self.image_data.height
        self.resize_image()
        self.pixels = self.__image_to_pixels()

    # changes font size of ascii art (only even values allowed)
    def change_font_size(self, font_size):
        if font_size % 2:
            font_size += 1
        self.__font_size = font_size
        self.__font = ImageFont.truetype(self.__font_name, size=font_size)

    # changes current font (use monospace)
    def change_font(self, font):
        self.__font_name = font
        self.__font = ImageFont.truetype(font, self.__font_size)

    # set a custom ascii character database
    def custom_chars(self, custom_chars=None):
        self.__custom_chars = custom_chars

    # apply brightness effect (0 => darker, 1 => no effect, > 1 => brighter)
    def apply_brightness(self, brightness):
        enhancer = ImageEnhance.Brightness(self.image_data)
        self.image_data = enhancer.enhance(brightness)
        self.resize_image()
        self.pixels = self.__image_to_pixels()

    # apply contrast effect (0 => less, 1 => no effect, > 1 => more)
    def apply_contrast(self, contrast):
        enhancer = ImageEnhance.Contrast(self.image_data)
        self.image_data = enhancer.enhance(contrast)
        self.resize_image()
        self.pixels = self.__image_to_pixels()

    # scale image to be bigger or smaller (final ascii is often large amount of pixels)
    def resize_image(self, scale=None):
        if scale != None:
            self.image_scale = scale

        sz = (self.width, self.height * 0.5)
        new_sz = tuple(int(self.image_scale * x) for x in sz)
        self.image_data = self.image_data.resize(
            new_sz, resample=Image.Resampling.LANCZOS
        )

    def __convert_pixels_to_luminance(self, pixels):
        scale = np.array([0.3, 0.5, 0.11])
        luminance = pixels * scale / 255
        return np.sum(luminance, axis=1)

    def __image_to_pixels(self):
        return np.array(self.image_data.getdata())
