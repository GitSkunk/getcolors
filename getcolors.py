__author__ = 'Trent'

from PIL import Image
import argparse
import heapq

# Now with heapq magics.

def getcolors(image, count):
    """
    Get the most used COUNT colors used in an image. IMAGE may be either a PIL Image object or a string containing a
    path to the image to examine. Returns a tuple containing true/false whether the image was palettized or not, and a
    list of tuples containing the colors and how many pixels in the image were of that color.

    :param image: Image object or string containing a path to the image file.
    :param count: How many of the most used colors to return.
    :return: A tuple containing T/F whether the image was palettized or not, and a list containing tuples of the colors
             and how many pixels in the image were of that color.
    """
    if isinstance(image, str):
        image = Image.open(image)
    width, height = image.size
    palette = image.getpalette()
    palette_indexed = []
    palettized = False
    colors = []
    if palette:
        palettized = True
    if palettized:
        while len(palette) > 1:
            # Eat up the palette and convert it to a list of RGB entries
            palette_indexed.append((palette.pop(0), palette.pop(0), palette.pop(0)))
        colors_used = image.getcolors()
        # Convert the palette indexes into actual colors using the color table we just made
        for color in colors_used:
            colors.append((color[0], palette_indexed[color[1]]))
    else:
        colors = image.getcolors(width * height)
    pal = heapq.nlargest(count, colors, key=lambda s: s[0])
    output = []
    for a in pal:
        if palettized:
            output.append((a[0], a[1]))
        else:
            output.append((a[0], a[1][:-1]))
    return (palettized, output)


def main():
    parser = argparse.ArgumentParser(description="Extract the palette of an image in text format.")
    parser.add_argument("target")
    parser.add_argument("-c", "--count", type=int, default=20, help="Return the $count most used colors.")
    parser.add_argument("-x", "--inhex", action='store_true',  help="Output colors in #RRGGBB format.")
    parser.add_argument("outfile", nargs="?", default=None)
    args = parser.parse_args()

    image = Image.open(args.target)
    pal = getcolors(image, args.count)
    pal = pal[1]  # Discard the bit about whether image was palettized since we don't care for this purpose
    if args.outfile:
        fh = open(args.outfile, "wt", encoding='utf-8')
    for color in pal:
        rgb = color[1]
        if args.inhex:
            rgb = ''.join('{:02X}'.format(a) for a in rgb)
            rgb = "#" + rgb
        if (args.outfile):
            fh.write("{}:{}\n".format(color[0], rgb))
        else:
            print("{}:{}".format(color[0], rgb))
    if args.outfile:
        fh.close()

if __name__ == '__main__':
    main()
