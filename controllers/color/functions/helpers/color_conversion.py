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