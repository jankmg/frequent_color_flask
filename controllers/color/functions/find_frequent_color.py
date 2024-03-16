from PIL import Image
import requests
from io import BytesIO
from collections import Counter

from controllers.color.functions.helpers.convert_rgb_to_hsl import convert_rgb_to_hsl

def get_pixels_from_image(url):
    #get and open image from url
    img = requests.get(url) 
    image = Image.open(BytesIO(img.content))

    #get the pixels from the image
    pixels = image.getdata()
    return pixels


#get the most common (frequent) values in a list
def get_frequent_values(list, length):
    count = Counter(list)
    frequent_colors = count.most_common(length)
    return frequent_colors


def filter_frequent_color(most_frequent_colors, offset):
    #to avoid black, white, and gray:
    #if the most frequent color is darker set value or lighter than set value save it as frequent color
    most_frequent = (0,0,0)
    for freq in most_frequent_colors:
        frequent = tuple(sorted(freq[0], reverse=True))
        if frequent[0] - frequent[1] < offset and frequent[1] - frequent[2] < offset:
            continue
        else:
            most_frequent = freq[0]
    print(most_frequent_colors)
    return most_frequent


def find_most_frequent_color(url: str, offset: int):
    #get pixels
    pixels = get_pixels_from_image(url)
    #reorder pixels from most to least common
    top_frequent_colors = get_frequent_values(pixels, 100)
    #filter the most frequent color to avoid grayscale colors
    frequent_color = filter_frequent_color(top_frequent_colors, offset)
    return frequent_color


def organize_colors(color, num_bins, color_cluster):
    hue = color[0]

    if len(color_cluster) != num_bins:
        color_cluster = [[] for _ in range(num_bins)]

    for x in range(num_bins):
       if hue > 360 / num_bins * (x + 1):
        color_cluster[x].append(color)
    
    return color_cluster



def find_most_dominant_color(url: str):
    pixels = get_pixels_from_image(url)
    top_frequent_colors = get_frequent_values(pixels, len(pixels))
    
    colors = []
    colors_names = ["red", "orange", "yellow", "green", "blue", "violet"]
    for color in top_frequent_colors:
        hsl_color = convert_rgb_to_hsl(color[0])
        hue,saturation,luminance = hsl_color

        if saturation < 20 or luminance < 10 or luminance > 80:
            continue

        colors = organize_colors(hsl_color, len(colors_names), colors)

    for color in colors:
        print(len(color))
    
    return (max(colors)[0])

    

