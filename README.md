# Jank's Colors API

Jank's Colors API allows you to get different data related to colors in an image. Currently it can get the most common color in an image. This API is used in the Jank's Colors web app.

**Link to project:**
You can checkout Jank's Colors API at: https://api.jankmg.com
You can checkout Jank's Colors web app at: https://www.jankmg.com

## How it's used:

(I need to explain how I use it and how people can use it)

## How It's Made:

**Tech used:** Python, Flask, Pillow, and more. Checkout <a href="./requirements.txt">requirements.txt</a> for more information

(I need to expand more on how I used each technology)

## Optimizations

(I need to explain how my approach changed throughout the development)

## Lessons Learned:

Before this project, I had no experience in Python. My only experience was in JavaScript, building small projects in React and NodeJS. However, I kept hearing a lot about Python, and I wanted to get into Python. During my journey as a hobbist coder I've learn that the best way to get into something new, is to pair it with something you already know.

Python doens't work for frontend web projects in the same way JavaScript does, so I had to make something related to servers. That's when I got the idea of building a small project, where one can give an image as an input and receive the most frequent color in that image. It could work great as an introduction to Python, since a project of this magnitude would be easy to do for me in NodeJS, I only had to "translate" my knowledge into a new language.

I started by investigating what technologies are available for backend development in Python. I came across two frequently use frameworks: Django and Flask. The next step was to investigate each framework. In multiple sources and forums across the internet, Django was described as robust framework, widely used because of its way of managing databases. Flask was described as a micro-framework, perfect for simple projects because it doesn't add any "unnecessary overhead". Since my "frequent color app" was just a simple project to get used to learn the basics of Python where I would not need a database, it would be the best option.

First I wrote some simple code to get my Flask app running to show the classic "Hello world" following the guide of the official flask documentation and then started reading Python documentation to get the basics of how the syntax works and how everything should be organized. I started experimenting with simple variable and function declarations to get familiar with the syntax before moving to the next step.

Once I had an application running and after playing around. I decided it was time to investigate image manipulation in Python. I searched on Google how to get colors from pixels of an image. That's when I found out about Pillow. I manage to loop through all the pixels and get each of their colors. And by doing so, I learned about tuples, which is a new type of data type for me, which got me curious about other data types in Python. So I research that for a while, Googlign and asking Chat-GPT certain questions which were too specific to find on Google. 

My first atempt was to just get the most repeated RGB color in the list of colors using Counter. But it didn't take into account small variations from color to color. </code>rgb(231,152,184)</code> was considered a different color from <code>rgb(231,152,185)</code>, which to the human eye it's practically the same. So I knew I had to find another way. By reading information about color from different sources and Chat-GPT as well, I figured that in order to make everything more manageable I should convert RGB to HSL. So I wrote an algorithm that does exactly that following this: https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/. I will go through this further. Then I needed a way to take into account small variation in color. So I came up with an idea. Create a list containing an item for each color, have each color have a treshold and then compare each pixel color to that threshold and put it into the list in order from most common to least common. Then check the length of each list and get the first value from that list. It's not perfect but it does a good job at getting the most common color.