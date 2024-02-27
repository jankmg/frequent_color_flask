from  PIL import Image
import requests
from io import BytesIO


url = "https://images.genius.com/8b9d3e6ed3781672e83f8b11d35078a5.1000x1000x1.png"
image = requests.get(url) 

img = Image.open(BytesIO(image.content))
pixel_data = img.getdata()
num_pixels = len(pixel_data)
result = tuple(sum(x) for x in zip(*pixel_data))
average = tuple(x // num_pixels for x in result)
print(average)
