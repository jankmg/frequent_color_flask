from PIL import Image
import requests
from io import BytesIO
from collections import Counter

from controllers.color.functions.helpers.color_conversion import convert_rgb_to_hsl

def get_pixels_from_image(url):
    #get and open image from url
    img = requests.get(url) 
    image = Image.open(BytesIO(img.content))

    if image.size > (1000, 1000):
        width, height = image.size

        # Calculate the new width and height.
        new_width = int(1000 * width / height)
        new_height = int(1000 * height / width)

        # Resize the image.
        image = image.resize((new_width, new_height))


    #get the pixels from the image
    pixels = image.getdata()
    return pixels


#get the most common (frequent) values in a list
def get_frequent_values(list, length):
    count = Counter(list)
    frequent_colors = count.most_common(length)
    return frequent_colors

def organize_colors(color, colors):
    #place a color in a list depending on its hue.
    hue = color[0]
    new_colors = colors

    if hue > 0 and hue <= 15:
        new_colors[0].append(tuple(color))
    elif hue > 345:
        new_colors[0].append(tuple(color))
    elif hue > 15 and hue <= 35:
        new_colors[1].append(tuple(color))
    elif hue > 35 and hue <= 66:
        new_colors[2].append(tuple(color))
    elif hue > 66 and hue <= 158:
        new_colors[3].append(tuple(color))
    elif hue > 158 and hue <= 187:
        new_colors[4].append(tuple(color))
    elif hue > 187 and hue <= 225:
        new_colors[5].append(tuple(color))
    elif hue > 225 and hue <= 260:
        new_colors[6].append(tuple(color))
    elif hue > 260 and hue <= 272:
        new_colors[7].append(tuple(color))
    elif hue > 272 and hue <= 345:
        new_colors[8].append(tuple(color))
    
    return new_colors



def find_most_dominant_color(url: str):
    #get pixels from image
    pixels = get_pixels_from_image(url)
    colors = list(pixels)
    
    #create categories for colors
    organized_colors = [[] for _ in range(9)]

    for color in colors:
        #convert rgb to hsl
        if len(color) != 3:
            continue
        hsl_color = convert_rgb_to_hsl(color)
        hue,saturation,luminance = hsl_color

        #filter colors close or in the grayscale
        if saturation < 20 or luminance < 10 or luminance > 80:
            continue
        
        #organize colors by placing them in categories depending on its hue
        organized_colors = organize_colors(hsl_color, organized_colors)

    #for debugging: show each color category's length

    #if colors is empty return default value    
    if all(not color for color in organized_colors):
        organized_colors[0].append((0,0,10))

    #slect the category with more colors
    frequent_color_list = max(organized_colors, key=len)
    sorted_frequent_color = get_frequent_values(frequent_color_list, len(frequent_color_list))
    frequent_color = sorted_frequent_color[0][0]

    return frequent_color