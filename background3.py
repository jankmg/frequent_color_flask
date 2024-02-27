from PIL import Image
import requests
from io import BytesIO
from collections import Counter



url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Cillian_Murphy_at_Berlinale_2024%2C_Ausschnitt.jpg/1024px-Cillian_Murphy_at_Berlinale_2024%2C_Ausschnitt.jpg"
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


def get_frequent_color(most_frequent_colors, offset):
    #if the most frequent color is darker set value or lighter than set value save it as frequent color
    most_frequent = (0,0,0)
    for freq in most_frequent_colors:
        frequent = tuple(sorted(freq[0], reverse=True))
        if frequent[0] - frequent[1] > offset and frequent[1] - frequent[2] > offset:
            most_frequent = freq[0]

    return most_frequent


def print_most_frequent_color(url, offset):
    pixels = get_pixels_from_image(url)
    top_frequent_colors = get_top_frequent_colors(pixels, len(pixels))
    frequent_color = get_frequent_color(top_frequent_colors, offset)
    print(frequent_color)

print_most_frequent_color(url, 20)