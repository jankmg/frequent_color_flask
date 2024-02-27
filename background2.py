from PIL import Image
import requests
from io import BytesIO
from collections import Counter



url = "https://lh3.googleusercontent.com/hwau7OVWx96XaME5KpRuJ0I_MscrerK6SbRH1UwYHYaxIDQQtn7RZK02LDSfBzCreidFgDsJeXyqDct6EZiH6vsV=w640-h400-e365-rj-sc0x00ffffff"
def get_pixels_from_image(url):
    #get and open image from url
    img = requests.get(url) 
    image = Image.open(BytesIO(img.content))

    #get the pixels from the image
    pixels = image.getdata()
    return pixels


def get_top_frequent_colors(pixels, length):
    count = Counter(pixels)
    frequent_colors = count.most_common(length)
    return frequent_colors


def get_frequent_color(most_frequent_colors):
    #if the most frequent color is darker set value or lighter than set value save it as frequent color
    most_frequent = (0,0,0)
    for frequent in most_frequent_colors:
        freq = frequent[0]
        if freq > (50,50,50) and freq < (200,200,200):
            most_frequent = freq
            break
    return most_frequent


def print_most_frequent_color(url):
    pixels = get_pixels_from_image(url)
    top_frequent_colors = get_top_frequent_colors(pixels, len(pixels))
    frequent_color = get_frequent_color(top_frequent_colors)
    print(frequent_color)

print_most_frequent_color(url)