from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
from collections import Counter

from controllers.color.functions.helpers.color_conversion import convert_rgb_to_hsl
from controllers.color.functions.helpers.color_conversion import convert_hsl_to_rgb

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

def categorize_colors(color, colors, thresholds):
    hue = color[0]
    new_colors = colors
    
    #get the index
    for index, threshold in enumerate(thresholds):
        #if the hue of the color is higher than the first starting point in the threshold and lower than the threshold append it into a color category
        if hue > threshold[0] and hue <= threshold[1]:
            #if it's the last threshold append it to the first category (red) since red is both the first and last threshold
            if index == len(thresholds) - 1:
                new_colors[0].append(tuple(color))
                break
            else:
                #if it's not the last threshold then append it to the current color category
                new_colors[index].append(tuple(color))
                break

    return new_colors


def find_most_dominant_color(url: str):
    #get pixels from image
    try:
        if not url.startswith(("http://", "https://")):
            raise requests.exceptions.InvalidURL("Invalid URL. Must start with 'https://' or 'http://'")

        pixels = get_pixels_from_image(url)
        colors = list(pixels)
    except requests.exceptions.InvalidURL as e:
        print("Error: ", e)
        return [422, False, "Invalid URL. Please try again with another one. URL must start with 'https://' or 'http://'", ""]
    except requests.exceptions.Timeout as e:
        print("Error: ", e)
        return [408, False, "Timeout error. Try again with another URL"]
    except UnidentifiedImageError as e:
        print("Error: ", e)
        return [422, False, "Not an image", ""]
    except Exception as e:
        print("Error: ", e )
        return [500, False, "Something went wrong", ""]
    
    # red, orange, yellow, green, cyan, light blue, blue, violet, magenta, red
    colors_threshold = [(0,15), (15,35), (35, 66), (66,168), (168,187), (187,225), (225,260), (260,272), (272,345), (345, 360)]

    #create categories for colors
    organized_colors = [[] for _ in range(len(colors_threshold) - 1)]

    for color in colors:
        #convert rgb to hsl
        if len(color) < 3:
            continue
        hsl_color = convert_rgb_to_hsl((color[0], color[1], color[2]))
        hue,saturation,luminance = hsl_color

        #filter colors close or in the grayscale
        if saturation < 20 or luminance < 10 or luminance > 80:
            continue
        
        #organize colors by placing them in categories depending on its hue
        organized_colors = categorize_colors(hsl_color, organized_colors, colors_threshold)

    #if colors is empty return default value
    if all(not color for color in organized_colors):
        organized_colors[0].append((0,0,10))


    #slect the category with more colors
    frequent_color_list = max(organized_colors, key=len)
    sorted_frequent_color = get_frequent_values(frequent_color_list, len(frequent_color_list))
    frequent_color_hsl = sorted_frequent_color[0][0]
    # print("color: ", convert_hsl_to_rgb(frequent_color_hsl))
    frequent_color_rgb = convert_hsl_to_rgb(frequent_color_hsl)
    data = [frequent_color_hsl, frequent_color_rgb]
    frequent_color_data = [200, True, "Most common color sucessfully found", data]

    return frequent_color_data