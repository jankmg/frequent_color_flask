# Jank's Colors API

Jank's Colors API allows users to retrieve the most common color in an image.

**Link to project:**
You can checkout Jank's Colors API at: https://api.jankmg.com  
You can checkout Jank's Colors web app at: https://www.jankmg.com

## How it's used:

(I need to explain how I use it and how people can use it)

## How It's Made:

**Tech used:** Python, Flask, Pillow, and more. Checkout <a href="./requirements.txt">requirements.txt</a> for more information


Here's the main cycle:

- Request is received
- Input validation.
- Retrive colors from each pixel.
- Convert colors into hsl.
- Organazie colors into categories based on hue.
- Find the category with most colors and the most common color within that category.
- Return the most frequent color as response.


I will try to explain in detail how the code actually works. I will explain what each part of the code does in order to have the final result. The project is written using modular programming in order to implement separation of cencerns standards. Meaning that each function only does one specific task. It currently has an awful error handling, but keep in mind that the app is still in development, so I will change that in the near future.

### Input validation
When the user visits https://api.jankmg.com/get_dominant_color, the `get_dominant_color` function is executed. It catches different errors, such as an image not existing, etc. (You can check the full code here: <a href="./controllers/color/get_dominant_color.py">get_dominant_color.py</a>). If everything is okay and an image exists. It executes the `find_most_dominant_color()` function and passes the image url as an argument. I will break down the code, but for now, here's the entire function:

```python

def find_most_dominant_color(url: str):
    #get pixels from image
    pixels = get_pixels_from_image(url)
    colors = list(pixels)
    
    # red, orange, yellow, green, cyan, light blue, blue, violet, magenta, red
    colors_threshold = [(0,15), (15,35), (35, 66), (66,168), (168,187), (187,225), (225,260), (260,272), (272,345), (345, 360)]

    #create categories for colors
    organized_colors = [[] for _ in range(len(colors_threshold) - 1)]

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
        organized_colors = categorize_colors(hsl_color, organized_colors, colors_threshold)

    #if colors is empty return default value    
    if all(not color for color in organized_colors):
        organized_colors[0].append((0,0,10))

    #slect the category with more colors
    frequent_color_list = max(organized_colors, key=len)
    sorted_frequent_color = get_frequent_values(frequent_color_list, len(frequent_color_list))
    frequent_color = sorted_frequent_color[0][0]

    return frequent_color

```
### Retriving color from each pixel
Function in use: `get_pixels_from_image(url)`.  
Whole function:
```python

from PIL import Image
import requests
from io import BytesIO

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

```

#### Breakdown:
The colors are stored as a list in the variable `colors`. We get those colors by executing the function `get_pixels_from_image(url)`. The `get_pixels_from_image(url)` function gets the data from the url using the `get` method from the `requests` library. Then it opens it as an image using Pillow and io.

```python
from PIL import Image
import requests
from io import BytesIO

    img = requests.get(url) 
    image = Image.open(BytesIO(img.content))
```

Then the app checks if the image is too big. If it is too big, it resize it in order to be easier to calculate. Then using the `getdata` method from Pillow, it retrieves the color of each pixel. And it returns the pixels.

```python
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
```
### Organizing colors
__Note:__ The app currently has the color from each pixel. Now it needs to find the most common color. In order to do that, it sorts the colors, placing each color on a category based on its hue. That requires a for loop. But in order to make the calculations simpler, it converts the rgb colors into hsl. Which also requires a for loop. So the app only runs a single for loop. In each iteration, the app converts the color to hsl and places it inside a category.

```python
    #get pixels from image
    pixels = get_pixels_from_image(url)
    colors = list(pixels)
    
    # red, orange, yellow, green, cyan, light blue, blue, violet, magenta, red
    colors_threshold = [(0,15), (15,35), (35, 66), (66,168), (168,187), (187,225), (225,260), (260,272), (272,345), (345, 360)]

    #create categories for colors
    organized_colors = [[] for _ in range(len(colors_threshold) - 1)]
```

In the code above, we can see the colors stored in the variable `colors` and two new variables; `colors_threshold`, `organized_colors`. The variable `colors_threshold` is a list containing the tuples that represent threshold ranges for different colors  on a scale from 0 to 360. For example, green starts at 66 and ends at 168. The variable `organized_colors` is dynamically defined based on the length of `color_threshold`. This variable containes the "categories" in which each color value inside the `colors` list will be placed in depending on its hue.

After that, a for loop based on the list `colors` is executed.
```python
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
        organized_colors = categorize_colors(hsl_color, organized_colors, colors_threshold)
```

For every value inside colors, it checks if the value has a lenght of 3. If it does, then it converts the rgb color into hsl. The purpose of this convertion is to make the next step (sorting colors based on hue) more managable. Managing colors in rgb can be quite hard. So in order to make the organization process easier the app converts the rgb values into HSL. It follows the formula explained in: https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/. 

__Converting RGB to HSL:__
Function in use: `convert_rgb_to_hsl`
Whole function:
```python
def convert_rgb_to_hsl(rgb):
    #convert rgb values to percentages
    red, green, blue = rgb
    r = red / 255
    g = green / 255
    b = blue / 255

    #find max and min values of rgb
    max_rgb = max(r,g,b)
    min_rgb = min(r, g, b)


    #calculate raw luminance (raw = decimals)
    #calculate luminance by converting it into a percentage
    raw_luminance =  (min_rgb + max_rgb) / 2
    luminance = round(raw_luminance * 100)

    #if min and max rgb are the same, it means there's no saturation. If there's no saturation, you don't need to calculate hue; we only set it to 0
    if min_rgb == max_rgb:
        saturation = 0
        hue = 0
        hsl = [hue, saturation, luminance]
        return hsl

    #if min and max are not the same. Calculate saturation
    if raw_luminance <= 0.5:
        raw_saturation = (max_rgb - min_rgb)/(max_rgb + min_rgb)
    else:
        raw_saturation = (max_rgb - min_rgb)/(2.0-max_rgb-min_rgb)
    saturation = round(raw_saturation * 100)

    #and calculate hue
    if max_rgb == r:
        raw_hue = (g - b) / (max_rgb - min_rgb)
    elif max_rgb == g:
        raw_hue = 2.0 + (b - r) / (max_rgb - min_rgb)
    elif max_rgb == b:
        raw_hue = 4.0 + (r-g) / (max_rgb - min_rgb)


    hue = round(raw_hue * 60)
    if hue < 0:
        hue = hue + 360

    hsl = [hue, saturation, luminance]
    return hsl
```
The algorithm starts by separating red, green, and blue from the rgb value and then converting it into a percentage as decimals by dividing it by 255.
```python
    #convert rgb values to percentages
    red, green, blue = rgb
    r = red / 255
    g = green / 255
    b = blue / 255
```

Once it finds the percentages as decimals, it gets the highest and lowest values between the 3 values.
```python
    #find max and min values of rgb
    max_rgb = max(r,g,b)
    min_rgb = min(r, g, b)
```

Then it calculates the luminance and converts it into a percentage. This is the "L" value in "HSL".
```python
    #calculate raw luminance (raw = decimals)
    #calculate luminance by converting it into a percentage
    raw_luminance =  (min_rgb + max_rgb) / 2
    luminance = round(raw_luminance * 100)
```

It moves to the next step where it calculates the saturation. This step has a condition. If the highest and lowest rgb value is are the same, saturation and hue is equal to 0.
```python
    #if min and max rgb are the same, it means there's no saturation. If there's no saturation, you don't need to calculate hue; we only set it to 0
    if min_rgb == max_rgb:
        saturation = 0
        hue = 0
        hsl = [hue, saturation, luminance]
        return hsl
```

But if then are not the same. It calculates the saturation based on if the luminance is lower or equal to 0.5. If it is, it finds the saturation using the code in the if statement. If it is not lower than 0.5 then it uses the code in the else statement. Then the saturation is converted into a percentage.
```python
    #if min and max are not the same. Calculate saturation
    if raw_luminance <= 0.5:
        raw_saturation = (max_rgb - min_rgb)/(max_rgb + min_rgb)
    else:
        raw_saturation = (max_rgb - min_rgb)/(2.0-max_rgb-min_rgb)
    saturation = round(raw_saturation * 100)
```

So far we have the luminance and saturation. Now we need to find the hue. There are 3 different formulas to find the hue based on which rgb value is the highest.
```python
    #and calculate hue
    if max_rgb == r:
        raw_hue = (g - b) / (max_rgb - min_rgb)
    elif max_rgb == g:
        raw_hue = 2.0 + (b - r) / (max_rgb - min_rgb)
    elif max_rgb == b:
        raw_hue = 4.0 + (r-g) / (max_rgb - min_rgb)


    hue = round(raw_hue * 60)
    if hue < 0:
        hue = hue + 360
```

Once we have all three we combine them and return the hsl value.
```python
    hsl = [hue, saturation, luminance]
    return hsl
```

Once it has the hue, saturation, and luminance. It checks if the color falls within the grayscale (or close to it) by comparing if the saturaton and luminance fall within the ranges of grayscale colors. If it does fall within that range, the color is skiped and the loop jumps into the next iteration. If it doesn't fall within the grayscale, it then runs the `categorize_colors` function. Which as its name sugguests, it places the color within a sublist inside the `organized_colors` list based on the color hue.

__Categorizing colors__
Function in use: `categorize_colors`
Whole function:
```python
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
```

__Breakdown:__ This function needs 3 parameters. The color it's going to categorize, the list of colors already categorized, and the thresholds in order to know where to categorize each color. Then it grabs the hue of the current color. It runs a loop through the thresholds and checks if the color fits within a threshold.

If the hue falls within the threshold and it's the last threshold it appends the color into the first category. Which is red.
```python
        if hue > threshold[0] and hue <= threshold[1]:
            #if it's the last threshold append it to the first category (red) since red is both the first and last threshold
            if index == len(thresholds) - 1:
                new_colors[0].append(tuple(color))
```

And if not it appends it to the color based on the current threshold.
```python
#if it's not the last threshold then append it to the current color category
    new_colors[index].append(tuple(color))
```

After all colors are organized. The last steps are to check if the most frequent color doesn't exists (maybe because the image was all grayscale colors) and 
```python
    #if colors is empty return default value    
    if all(not color for color in organized_colors):
        organized_colors[0].append((0,0,10))
```

Then grab the most frequent color. To do this we grab the category of colors with most elements (`frequent_color_list`). Get the most frequent value in that list using `get_frequent_values` function. 
```python
    #slect the category with more colors
    frequent_color_list = max(organized_colors, key=len)
    sorted_frequent_color = get_frequent_values(frequent_color_list, len(frequent_color_list))
```
The `get_frequent_values` function finds the most repeated value in a list using teh counter library and returns it.
```python
#get the most common (frequent) values in a list
def get_frequent_values(list, length):
    count = Counter(list)
    frequent_colors = count.most_common(length)
    return frequent_colors
```

Then we return that value to the response handler.
```python
    frequent_color = sorted_frequent_color[0][0]

    return frequent_color
```

(I need to expand more on how I used each technology)

## Optimizations


I felt overwhelmed by this small project. I started to think why I felt that way. I realized the code was not organized properly. The concept of the project only existed in my mind. So I thought I would need a visualization. I started making a diagram to show the lifecycle of my app. I realized that was something I should've done before even starting to write code. I talk more about this in <a href="#lessons-learned"></a>.

I made this diagram when the app didn't have a proper handling of errors. I noticed that problem thanks to the diagram itself. It made me realize that I had only worked to get the final expected result, but did not communicate problems and errors clearly, both to the user and to the developer when coding.

![Diagram of early app lifecycle](./readme%20resources/diagram-lack-error-handling.png)

My current structure only checks for one error. Then it basically returns to the user whatever each library returns. It is not very user friendly, since those libraries throw errors meant for developers, not users. 

(I need to explain how my approach changed throughout the development)
How I changed the way the algorithm organizes colors.
I changed how the most frequent color is found
I will change the error handling.

## Lessons Learned:

The most important lesson I've learned with this project is planning. I struggle a lot in previous projects, I felt overwhelmed and sometimes that made me not want to continue a project. I think the problem was how little I planned before starting to write code. I did the same on this project, I got to write code from the moment I got the idea; later when judging if the project was ready to be presented as a final project, I realized that while the project did what it was meant to be doing, it was not up to production standards. I've learned that it's better to spend a lot of time cleaning, planning, documenting in the early stages to slowly build a robust program that allows scalability thanks to the constant, clean, and carefully thought structure rather than getting to the final result quickly, but in a clumsy way. Which you will have to modify in the future in order to make changes more manageable.

Before this project, I had no experience in Python. My only experience was in JavaScript, building small projects in React and NodeJS. However, I kept hearing a lot about Python, and I wanted to get into Python. During my journey as a hobbist coder I've learn that the best way to get into something new, is to pair it with something you already know.

Python doens't work for frontend web projects in the same way JavaScript does, so I had to make something related to servers. That's when I got the idea of building a small project, where one can give an image as an input and receive the most frequent color in that image. It could work great as an introduction to Python, since a project of this magnitude would be easy to do for me in NodeJS, I only had to "translate" my knowledge into a new language.

I started by investigating what technologies are available for backend development in Python. I came across two frequently use frameworks: Django and Flask. The next step was to investigate each framework. In multiple sources and forums across the internet, Django was described as robust framework, widely used because of its way of managing databases. Flask was described as a micro-framework, perfect for simple projects because it doesn't add any "unnecessary overhead". Since my "frequent color app" was just a simple project to get used to learn the basics of Python where I would not need a database, it would be the best option.

First I wrote some simple code to get my Flask app running to show the classic "Hello world" following the guide of the official flask documentation and then started reading Python documentation to get the basics of how the syntax works and how everything should be organized. I started experimenting with simple variable and function declarations to get familiar with the syntax before moving to the next step.

Once I had an application running and after playing around. I decided it was time to investigate image manipulation in Python. I searched on Google how to get colors from pixels of an image. That's when I found out about Pillow. I manage to loop through all the pixels and get each of their colors. And by doing so, I learned about tuples, which is a new type of data type for me, which got me curious about other data types in Python. So I research that for a while, Googling and asking Chat-GPT certain questions which were too specific to find on Google. 

My first atempt was to just get the most repeated RGB color in the list of colors using Counter. But it didn't take into account small variations from color to color. `rgb(231,152,184)` was considered a different color from `rgb(231,152,185)`, which to the human eye it's practically the same. So I knew I had to find another way. By reading information about color from different sources and Chat-GPT as well, I figured that in order to make everything more manageable I should convert RGB to HSL. So I wrote an algorithm that does exactly that following this: https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/. I will go through this further. Then I needed a way to take into account small variation in color. So I came up with an idea. Create a list containing an item for each color, have each color have a threshold and then compare each pixel color to that threshold and put it into the list in order from most common to least common. Then check the length of each list and get the first value from that list. It's not perfect but it does a good job at getting the most common color.

## Things I could've done better:
Better planning. I should've started by documenting what my goal was. How I was planning to implement things. 