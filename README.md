# getcolors
Simple little bit of python to extract the most used colors in an image.

Get the most used COUNT colors used in an image. IMAGE may be either a PIL Image object or a string containing a
path to the image to examine. Returns a tuple containing true/false whether the image was palettized or not, and a
list of tuples containing the colors and how many pixels in the image were of that color.

from getcolors import getcolors
colors = getcolors(image, count)
print(colors)

image: Image object or string containing a path to the image file.
count: How many of the most used colors to return.

A tuple containing T/F whether the image was palettized or not, and a list containing tuples of the colors
and how many pixels in the image were of that color.
