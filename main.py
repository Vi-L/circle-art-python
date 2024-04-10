# ! creates new image file at Vicle\Documents\programming\Circle Art
from multiprocessing.sharedctypes import Value
from PIL import Image, ImageDraw

# ? source: https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
def get_dominant_color(pil_img, palette_size=16):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return dominant_color

def check_inputs():
    if min_depth <= 0 or max_depth <= 0:
        raise ValueError("depths must be greater than 0!")
    if min_depth > max_depth:
        raise ValueError("max depth must be greater than or equal to min_depth!")

    if initial_opacity < 0 or initial_opacity > 1:
        raise ValueError("initial opacity must be between 0 and 1!")
    if decay < 0 or decay > 1:
        raise ValueError("decay must be between 0 and 1!")

    if outline_width < 0:
        raise ValueError("width must be greater than or equal to 0!")

print("---------- CIRCLE ART GENERATOR ----------")
# get inputs
path = input("Name of image in folder (include the file type, e.g. image.png): ")
min_depth = int(input("Min depth (lowest resolution, e.g. 2 -> 2x2 circles): "))
max_depth = int(input("Max depth (highest resolution, e.g. 20 -> 20x20 circles): ")) 
initial_opacity = float(input("Initial opacity (opacity of lowest resolution circles from 0 to 1, e.g. 0.3): ")) 
decay = float(input("Decay (factor by which opacity decreases by on each layer from 0 to 1, e.g. 0.95): "))
use_outlines = True if input("Use outlines? (Y/N): ") == "Y" else False
outline_width = int(input("Outline width (e.g. 1): "))

print("opening your image...") 
try:
    im = Image.open(path) 
except:
    raise ValueError("error while opening image! try checking the name or making sure the image is in this folder!")

check_inputs()

width, height = im.size
print("initializing new image...")
res_im = Image.new("RGB", im.size, (255, 255, 255))
draw = ImageDraw.Draw(res_im, "RGBA")

for i in range(min_depth, max_depth + 1): # range is inclusive/exclusive, so +1
    print('Computing {i} by {i}...'.format(i=i))
    for x in range(i):
        for y in range(i):
            x_space = width / i
            y_space = height / i
            box = x_space*x, y_space*y, x_space*(x+1), y_space*(y+1)
            subsection = im.crop(box) # top left to bottom right coords
            dominant_color = get_dominant_color(subsection)
            # convert dominant color to tuple and add opacity as value from 0 to 255
            fill_color = tuple(dominant_color) + (int(255 * initial_opacity * (decay ** i)),)
            outline_color = tuple(dominant_color) + (255,)
            draw.ellipse(box, fill=fill_color, outline=outline_color if use_outlines else None, width=outline_width)
            
res_im.save("result.png", "PNG")
print("done! saved as \"result.png\"! ")
print("------------------------------------------")