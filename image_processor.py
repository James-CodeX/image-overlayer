from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap


class ImageOverlay:
    def __init__(self, background_image):
        """Initialize with a background image (PIL Image or bytes)"""
        if isinstance(background_image, bytes):
            self.image = Image.open(BytesIO(background_image)).convert('RGBA')
        else:
            self.image = background_image.convert('RGBA')

        self.width, self.height = self.image.size
        self.overlay = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.overlay)

    def add_text(self, text, position='center', font_size=40, color=(0, 0, 0, 255),
                 font_path=None, max_width=None, line_spacing=10):
        """Add text to the image with word wrapping"""
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Try common system fonts
                system_fonts = [
                    'arial.ttf', 'Arial.ttf',
                    'C:/Windows/Fonts/arial.ttf',
                    'C:/Windows/Fonts/calibri.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    '/System/Library/Fonts/Helvetica.ttc'
                ]
                font = None
                for font_file in system_fonts:
                    try:
                        font = ImageFont.truetype(font_file, font_size)
                        break
                    except:
                        continue
                if font is None:
                    font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Word wrap if max_width specified
        if max_width:
            lines = []
            for line in text.split('\n'):
                wrapped = textwrap.fill(line, width=max_width)
                lines.extend(wrapped.split('\n'))
            text = '\n'.join(lines)

        # Calculate text position
        bbox = self.draw.multiline_textbbox(
            (0, 0), text, font=font, spacing=line_spacing)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if position == 'center':
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
        elif isinstance(position, tuple):
            x, y = position
        else:
            x, y = 50, 50

        self.draw.multiline_text((x, y), text, fill=color, font=font,
                                 spacing=line_spacing, align='center')

    def add_logo(self, logo_image, position='bottom-right', size=None, opacity=255):
        """Add a logo to the image"""
        if isinstance(logo_image, bytes):
            logo = Image.open(BytesIO(logo_image)).convert('RGBA')
        else:
            logo = logo_image.convert('RGBA')

        # Resize logo if size specified
        if size:
            logo = logo.resize(size, Image.Resampling.LANCZOS)

        # Adjust opacity
        if opacity < 255:
            alpha = logo.split()[3]
            alpha = alpha.point(lambda p: int(p * opacity / 255))
            logo.putalpha(alpha)

        logo_width, logo_height = logo.size
        margin = 30

        # Calculate position
        if position == 'bottom-right':
            x = self.width - logo_width - margin
            y = self.height - logo_height - margin
        elif position == 'bottom-left':
            x = margin
            y = self.height - logo_height - margin
        elif position == 'top-right':
            x = self.width - logo_width - margin
            y = margin
        elif position == 'top-left':
            x = margin
            y = margin
        elif isinstance(position, tuple):
            x, y = position
        else:
            x, y = margin, margin

        self.overlay.paste(logo, (x, y), logo)

    def get_result(self, format='PNG'):
        """Combine layers and return the final image"""
        result = Image.alpha_composite(self.image, self.overlay)
        result = result.convert('RGB')

        output = BytesIO()
        result.save(output, format=format)
        output.seek(0)
        return output
