"""Draw a deterministic, original five-story news briefing with Pillow."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
INK = '#172A36'
PAPER = '#F5F2E9'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')


def font(size, bold=False):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(FONT_DIR / name), size)


def pictogram(draw, kind, x, y, color):
    """Original pictograms, composed entirely from explicit Pillow shapes."""
    def line(points, width=4, fill=INK):
        draw.line([(x + a, y + b) for a, b in points], fill=fill, width=width,
                  joint='curve')

    def ellipse(box, fill=None, outline=INK, width=4):
        draw.ellipse(tuple(v + (x if i % 2 == 0 else y)
                           for i, v in enumerate(box)),
                     fill=fill, outline=outline, width=width)

    def polygon(points, fill=color):
        draw.polygon([(x + a, y + b) for a, b in points], fill=fill)

    if kind == 'poland':
        # A schematic aircraft and a small Polish flag.
        polygon([(45, 4), (52, 35), (81, 58), (80, 66), (51, 54),
                 (50, 77), (62, 88), (29, 88), (40, 77), (39, 54),
                 (10, 66), (9, 58), (38, 35)])
        line([(4, 92), (87, 92)], width=3)
        draw.rectangle((x + 4, y + 106, x + 85, y + 117), fill='white')
        draw.rectangle((x + 4, y + 118, x + 85, y + 129), fill='#D94B50')
    elif kind == 'climate':
        ellipse((3, 13, 88, 98), fill='#DBE8DD', outline=color)
        ellipse((27, 13, 64, 98), outline=color, width=3)
        line([(5, 55), (86, 55)], fill=color, width=3)
        line([(13, 31), (77, 31)], fill=color, width=3)
        line([(13, 78), (77, 78)], fill=color, width=3)
        line([(23, 111), (70, 111)], fill=color)
        line([(46, 100), (46, 111)], fill=color)
    elif kind == 'deal':
        # Two interlocking hands with differently colored cuffs.
        polygon([(1, 40), (20, 35), (35, 67), (16, 77)])
        polygon([(90, 40), (72, 35), (56, 67), (75, 77)], fill='#D6AC47')
        polygon([(21, 43), (37, 35), (52, 40), (68, 49), (61, 73),
                 (46, 84), (28, 69)], fill='#E8D7BE')
        line([(21, 43), (37, 35), (52, 40), (68, 49), (61, 73),
              (46, 84), (28, 69)], width=3)
        line([(62, 41), (48, 35), (34, 50), (41, 56), (51, 49),
              (67, 61)], width=3)
        line([(41, 65), (53, 76)], width=3)
        line([(49, 60), (61, 71)], width=3)
        line([(17, 102), (74, 102)], fill=color, width=3)
        ellipse((40, 95, 52, 108), fill=color, outline=color, width=1)
    elif kind == 'quake':
        line([(0, 63), (17, 63), (26, 44), (37, 91), (48, 16),
              (60, 77), (69, 53), (79, 63), (92, 63)], fill=color, width=5)
        line([(6, 108), (37, 108), (46, 98), (54, 119), (63, 108),
              (87, 108)], width=3)
    elif kind == 'storm':
        ellipse((10, 30, 51, 69), fill=color, outline=color)
        ellipse((29, 12, 74, 64), fill=color, outline=color)
        ellipse((54, 32, 90, 70), fill=color, outline=color)
        draw.rectangle((x + 27, y + 45, x + 74, y + 69), fill=color)
        polygon([(45, 73), (31, 102), (47, 101), (40, 127),
                 (68, 89), (51, 90)], fill='#D6AC47')
        line([(4, 84), (25, 84)], fill=color, width=3)
        line([(68, 79), (91, 79)], fill=color, width=3)
        line([(71, 100), (86, 100)], fill=color, width=3)


def render(destination):
    image = Image.new('RGB', (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1023, 94), fill=INK)
    title = 'SATURDAY 21 NOVEMBER 2026'
    draw.text((36, 25), title, font=font(41, True), fill=PAPER)

    stories = [
        ('POLAND', 'poland', '#B84646', 'Russian missiles land in Poland',
         ['Two Kh-101 missiles + drone land in south-east Poland.',
          'NATO jets scrambled; no injuries reported.']),
        ('CLIMATE', 'climate', '#39705C', 'COP31 runs into overtime',
         ['Antalya summit misses deadline; talks continue.',
          'Draft text drops all mention of fossil fuels.']),
        ('UK–EU', 'deal', '#3C658F', 'UK and EU seal reset deal',
         ['Most food/farm checks end Mar 2028; carbon link Jan 2028.',
          'Youth mobility: up to 100,000 per side, ages 18–31.']),
        ('PERU', 'quake', '#B56835', 'Magnitude 6.7 quake hits Peru',
         ['Central Peru near Junin; tremors felt in Lima.',
          'No deaths or serious damage reported.']),
        ('BRAZIL', 'storm', '#6A5A85', 'Deadly storm batters Brazil',
         ['Tupanciretan: winds up to 114 km/h kill three.',
          'About 5,000 homes wrecked by the powerful storm.']),
    ]

    for index, (label, kind, color, headline, summary) in enumerate(stories):
        top = 111 + index * 179
        draw.rounded_rectangle((22, top, 1001, top + 164), radius=13,
                               fill='#FFFEFA')
        draw.rounded_rectangle((22, top, 30, top + 164), radius=4, fill=color)
        pictogram(draw, kind, 57, top + 17, color)
        draw.text((177, top + 9), label, font=font(18, True), fill=color)
        draw.text((175, top + 35), headline, font=font(36, True), fill=INK)
        for line_index, text in enumerate(summary):
            if draw.textlength(text, font=font(25)) > 803:
                raise ValueError(f'Summary exceeds block width: {text}')
            draw.text((177, top + 88 + 32 * line_index), text,
                      font=font(25), fill=INK)

    # No metadata, time fields, random values, or external input affect the PNG.
    image.save(destination, format='PNG', optimize=True, compress_level=9)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).resolve().with_name('entry.png'))
    render(parser.parse_args().output)
