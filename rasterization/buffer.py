from PIL import Image
from IPython.display import display
import io, time

class Buffer:
    def __init__(self, width, height, clear_color = (0, 0, 0)):
        self.width = width
        self.height = height
        self.buffer = Image.new('RGB', (width, height), color= clear_color)

    def __getitem__(self, index):
        x, y = index
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Index out of range")
        return self.buffer.getpixel((x, y))

    def __setitem__(self, index, value):
        x, y = index
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Index out of range")
        self.buffer.putpixel((x, y), value)
    
    def display(self):
        try:
        # 如果get_ipython函数存在，并且返回值不为None，那么就说明是在Jupyter Notebook环境下运行
            if(get_ipython()):
                display(self.buffer) 
        except NameError:
        # 如果get_ipython函数未定义，那么就说明不是在Jupyter Notebook环境下运行
            self.buffer.show()

    @classmethod
    def from_file(cls, filename):
        with Image.open(filename) as img:
            width, height = img.size
            buffer = cls(width, height)
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    buffer[x, y] = r, g, b
            return buffer

class FrameBuffer(Buffer):
    def __init__(self, width, height, clear_color=(0, 0, 0)):
        super().__init__(width, height, clear_color)
    
    ################################################
    ###               Operations                 ###
    ################################################

    #填充缓冲区为纯色
    def fill(self, value):
        if type(value) != tuple:
            raise TypeError("Value should be tuple")
        self.buffer = Image.new('RGB', (self.width, self.height), color=value)
    
    def clear(self):
        self.fill((0, 0, 0))

    def draw_point(self, position, color=(255, 255, 255)):
        x, y = position
        x = round(x)
        y = round(y)
        self.buffer.putpixel((x, y), color)

    def save(self, filepath = "./framebuffer"):
        if(filepath == "./framebuffer"):
            t = time.localtime()
            filepath += '@{}-{}-{}-{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
            filepath += '.ppm'
        self.buffer.save(filepath)

    def draw_line(self, start, end, color = (0, 0, 0), reverse=False):
        x0, y0 = start
        x1, y1 = end
        if(x0 > x1):
            return self.draw_line(end, start, color, reverse)
        if(x1 == x0):
            self.draw_point(start)
            return
        if abs(x1 - x0) < abs(y1 - y0):
            return self.draw_line((y0, x0), (y1, x1), color, True)
        dt = (y1 - y0) / (x1 - x0)
        if reverse:
            for i in range(round(x0), round(x1) + 1):
                y0 += dt
                self.draw_point((y0, i), color)
        else:
            for i in range(round(x0), round(x1) + 1):
                y0 += dt
                self.draw_point((i, y0), color)        
