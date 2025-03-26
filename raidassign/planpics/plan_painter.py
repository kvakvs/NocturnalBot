import io
from PIL import Image, ImageFont, ImageDraw


class PlanPainter:
    """
    Loads a raid room image, overlays the positions and assigns on it, outputs the image
    ready to be published on discord.
    """
    COLOR_RAGE = (100, 0, 0, 255)
    COLOR_MANA = (0, 0, 128, 255)
    COLOR_PLAYER = (0, 64, 0, 255)
    COLOR_PLAYER_ORANGE = (192, 128, 0, 255)

    def __init__(self, image_path: str):
        # Load with alpha channel
        self.image: Image.Image = Image.open(image_path).convert('RGBA')
        self.font = ImageFont.truetype("fonts/friz-quadrata-regular-os.ttf", 16)
        self.draw = ImageDraw.Draw(self.image)

    def output(self, out_file: str) -> io.BytesIO:
        """Saves image to a BytesIO object, it can be used to construct a discord.File object"""
        arr = io.BytesIO()

        if out_file.endswith('.jpg'):
            # JPEG requires that there is no alpha channel
            self.image.convert('RGB').save(arr, format='JPEG', quality=100)
        elif out_file.endswith('.png'):
            self.image.save(arr, format='PNG')
        else:
            raise ValueError(f"Unsupported file extension: {out_file}")

        arr.seek(0)
        return arr

    def text_size(self, text: str) -> tuple[int, int]:
        """Returns the width and height of the text"""
        l, t, r, b = self.font.getbbox(text)
        return int(r - l), int(b - t)

    def add_icon(self, icon_path: str,
                 xy_relative: tuple[float, float],
                 icon_size: int,
                 text: str | None = None,
                 background_color: tuple[int, int, int, int] = (0, 0, 0, 255)):
        """
        Place an icon at a relative position, with an optional text label under (or over) it.
        """
        icon = Image.open(icon_path)
        icon = icon.resize((icon_size, icon_size))
        xpos = int(xy_relative[0] * self.image.width)
        ypos = int(xy_relative[1] * self.image.height)

        # Center the icon on the position
        center_on_xpos = xpos - icon.width // 2
        center_on_ypos = ypos - icon.height // 2
        self.draw.circle((xpos, ypos), icon_size // 2, fill=background_color)
        self.image.paste(icon, (center_on_xpos, center_on_ypos), icon)

        if text:
            # Draw text in the bottom part of the icon
            text_w, text_h = self.text_size(text)
            self.draw.text((xpos - text_w // 2, ypos + icon_size // 2),
                           text,
                           font=self.font,
                           stroke_fill=(255, 255, 255, 255),
                           align="center")
