# Script to generate bulk of my Another's Dreams (Full) palette
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

class GimpPalColor(object):
    '''
    represents - and prints to - a gimp palette color
    '''
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.name = "Untitled"
        
    def __repr__(self):
        ret = ""
        
        ret = ret + str(self.r).rjust(3, " ")
        ret = ret + " "
        ret = ret + str(self.g).rjust(3, " ")
        ret = ret + " "
        ret = ret + str(self.b).rjust(3, " ")
        ret = ret + " "
        ret = ret + self.name
        
        return ret

def labToRGB(l, a, b):
    '''
    converts CIEL*ab color to RGB tuple, values 0-255,
    includes rounding
    '''
    lab = LabColor(l, a, b)
    out = convert_color(lab, sRGBColor)
    
    r = int(round(out.clamped_rgb_r * 255))
    g = int(round(out.clamped_rgb_g * 255))
    b = int(round(out.clamped_rgb_b * 255))
    
    return (r, g, b)

def main():
    '''
    Just a typical main block incase someone tries to import this as
    a library
    '''
    
    # turns out a is first, 16 steps
    for a in range(-90, 91, 12):
        # ten brightness steps
        for i in range(10):
            # need that as a multiple of 11.11 to cover most the gamut
            l = 11.11 * i
            
            # last is b
            for b in range(-90, 91, 12):
                # do the thing!
                c = GimpPalColor()
                c.r, c.g, c.b = labToRGB(l, a, b)
                print(c)
                
        # after every grouping, place a row of black cells.
        for i in range(16):
            c = GimpPalColor()
            print(c)
            
if __name__ == "__main__":
    main()