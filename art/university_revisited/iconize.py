# tested against:
# - python 3.11.0
# - pillow 10.2.0
from PIL import Image

class Color:
    """Very stupid, simple color class
    """
    def __init__(self, red:int, green:int, blue:int):
        self.red:int   = red
        self.green:int = green
        self.blue:int  = blue

    def asTuple(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def linearizeChannel(self, val:float) -> float:
        ret:float = 0.0

        if (val <= 0.04045):
            ret = val / 12.92
        else:
            ret = val + 0.055
            ret = ret / 1.055
            ret = pow(ret, 2.4)
        
        return ret

    def getLstar(self) -> float:
        ret:float = 0

        # range numbers 0.0 to 1.0
        vR:float = float(self.red)   / 255.0
        vG:float = float(self.green) / 255.0
        vB:float = float(self.blue)  / 255.0

        # Linearize channels
        lR:float = self.linearizeChannel(vR)
        lG:float = self.linearizeChannel(vG)
        lB:float = self.linearizeChannel(vB)

        # luminance (y) portion via standard coefficients for primaries
        yR:float = lR * 0.2126
        yG:float = lG * 0.7152
        yB:float = lB * 0.0722

        # luminance is just their sum
        y:float = yR + yG + yB

        # l* - perceived lightness - is just a quick bit of math away
        if (y <= (216.0/24389.0)):
            ret = (y * (24389.0/27.0))
        else:
            ret = pow(y, (1.0/3.0))
            ret = ret * 116
            ret = ret - 16
        
        # done
        return ret

def iconize(src:Image.Image, thresholds:list[float], colors:list[Color]) -> Image.Image:
    # work definitely, without a doubt, on a three channel copy
    ret:Image.Image = src.copy().convert("RGB")

    # most basic error check
    if (len(thresholds) != (len(colors) - 1)):
        raise ValueError("Must have one more color than thresholds")

    # alright kids
    for x in range(ret.width):
        for y in range(ret.height):
            px:tuple[int, int, int] = ret.getpixel((x, y))
            col:Color = Color(px[0], px[1], px[2])

            recolored:bool = False

            for i in range(len(thresholds)):
                if (not recolored):
                    if (col.getLstar() <= thresholds[i]):
                        ret.putpixel((x, y), colors[i].asTuple())
                        recolored = True
            
            if (not recolored):
                ret.putpixel((x, y), colors[len(thresholds)].asTuple())
                recolored = True
    
    # done
    return ret

def obinicon(src:Image.Image) -> Image.Image:
    colors:list[Color] = [
        Color(  0,   0,   0),
        Color(255, 255, 255)
    ]

    thresholds:list[float] = [
        50.0
    ]

    return iconize(src, thresholds, colors)

def obamicon(src:Image.Image) -> Image.Image:
    # I've gone ahead and found perceptual brightnesses and sorted these
    # darkest to lightest with perceptual brightness
    #
    # probably not the intended way, but it looks nice enough IMHO given good
    # full spectrum white balance
    colors:list[Color] = [
        Color(0,    51,  76),
        Color(218,  31,  33),
        Color(112, 150, 158),
        Color(252, 226, 165)
    ]

    thresholds:list[float] = [
        19.60,
        46.97,
        59.64
    ]

    return iconize(src, thresholds, colors)

def wrap(function, path):
    # just wraps a function to apply to the path so I can test these
    im = Image.open(path)
    out = function(im)
    out.show()