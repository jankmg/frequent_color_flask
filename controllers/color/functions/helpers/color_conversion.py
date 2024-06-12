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

def convert_hsl_to_rgb(hsl):
    #separate hue, saturation, luminance. 
    #convert saturation and luminance into percentages
    hue,saturation,luminance = hsl
    saturation = saturation / 100
    luminance = luminance / 100

    c = (1 - abs(2 * luminance - 1)) * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = luminance - c/2

    #based on the hue, choose an order in which the variables above fall into the rgb channels
    cases = [(c,x,0), (x,c,0), (0,c,x), (0,x,c), (x,0,c), (c,0,x)]
    for i in range(int(360/60)):
        if i*60 < hue < (i + 1)*60:
            r,g,b = cases[i]
    
    rgb = (round((r+m)*255), round((g+m)*255), round((b+m)*255))
    return rgb