import io
import math
from PIL import Image, ImageFont, ImageDraw


class PlanPainter:
    """
    Loads a raid room image, overlays the positions and assigns on it, outputs the image
    ready to be published on discord.
    """
    COLOR_RAGE = (100, 0, 0, 255)
    COLOR_MANA = (0, 0, 128, 255)
    COLOR_ENERGY = (255, 245, 105, 255)

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

    def add_circle(self, xy_relative: tuple[float, float], radius: int, color: tuple[int, int, int, int], text: str | None = None, width: int = 1):
        xpos = int(xy_relative[0] * self.image.width)
        ypos = int(xy_relative[1] * self.image.height)

        self.draw.circle((xpos, ypos), radius, outline=color, width=width)

        if text:
            shadow_offset = 1
            text_w, text_h = self.text_size(text)
            text_xpos = xpos - text_w // 2
            text_ypos = ypos + radius
            self.draw.text((text_xpos-shadow_offset, text_ypos-shadow_offset),
                           text, font=self.font, fill=(0, 0, 0, 128))
            self.draw.text((text_xpos+shadow_offset, text_ypos+shadow_offset),
                           text, font=self.font, fill=(0, 0, 0, 128))
            self.draw.text((text_xpos, text_ypos), text, font=self.font, fill=color)

    def draw_arrow(self, xy_relative: tuple[float, float], length: float, angle_deg: float,
                   color: tuple = (255, 255, 255), width: int = 2, head_length: int = 10):
        """
        Draw an arrow on the image starting from (x,y) with given length and angle

        Args:
            draw: ImageDraw object
            xy_relative: Starting position in fraction of image width and height
            length: Length of the arrow
            angle_deg: Angle in degrees (0 = right, 90 = up, 180 = left, 270 = down)
            color: RGB or RGBA color tuple
            width: Line width in pixels
            head_length: Length of the arrow head lines
        """
        x = xy_relative[0] * self.image.width
        y = xy_relative[1] * self.image.height

        # Convert angle to radians
        angle_rad = math.radians(angle_deg)

        # Calculate end point
        end_x = x + length * math.cos(angle_rad)
        end_y = y - length * math.sin(angle_rad)  # Subtract because y increases downwards

        # Draw main line
        self.draw.line([(x, y), (end_x, end_y)], fill=color, width=width)

        # Calculate arrow head
        arrow_angle1 = angle_rad + math.radians(135)  # Left side of arrowhead
        arrow_angle2 = angle_rad - math.radians(135)  # Right side of arrowhead

        # Arrow head points
        head1_x = end_x + head_length * math.cos(arrow_angle1)
        head1_y = end_y - head_length * math.sin(arrow_angle1)

        head2_x = end_x + head_length * math.cos(arrow_angle2)
        head2_y = end_y - head_length * math.sin(arrow_angle2)

        # Draw arrow head
        self.draw.line([(end_x, end_y), (head1_x, head1_y)], fill=color, width=width)
        self.draw.line([(end_x, end_y), (head2_x, head2_y)], fill=color, width=width)

    def draw_text(self, xy_relative: tuple[float, float], text: str, color: tuple[int, int, int, int] = (255, 255, 255, 255)):
        xpos = int(xy_relative[0] * self.image.width)
        ypos = int(xy_relative[1] * self.image.height)
        self.draw.text((xpos, ypos), text, font=self.font, fill=color)
