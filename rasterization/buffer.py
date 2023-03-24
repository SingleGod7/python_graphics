from PIL import Image
from IPython.display import display
import io, time
import geometry

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
    
    #清空缓存区
    def clear(self):
        self.fill((0, 0, 0))

    #画一个点
    def draw_point(self, position, color=(255, 255, 255)):
        x, y = position
        x = round(x)
        y = round(y)
        self.buffer.putpixel((x, y), color)

    #保存文件
    def save(self, filepath = "./framebuffer"):
        if(filepath == "./framebuffer"):
            t = time.localtime()
            filepath += '@{}-{}-{}-{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
            filepath += '.ppm'
        self.buffer.save(filepath)

    #画一条线
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

    #求重心坐标
    def barycentric_coord(self, v0, v1, v2, point):
        vec0 = geometry.Vec2(v1) - geometry.Vec2(v0)
        vec1 = geometry.Vec2(v2) - geometry.Vec2(v1)
        vec2 = geometry.Vec2(v0) - geometry.Vec2(v2)

        S = abs(vec0.cross(vec1))
        if(S == 0):
            return (-1, 1, 1)
        alpha = (geometry.Vec2(point) - geometry.Vec2(v0)).cross(vec0) / S
        beta = (geometry.Vec2(point) - geometry.Vec2(v1)).cross(vec1) / S
        gamma = (geometry.Vec2(point) - geometry.Vec2(v2)).cross(vec2) / S

        if(alpha + beta + gamma + 1 < 1e-5):
            alpha = -alpha
            beta = -beta
            gamma = -gamma
        return (alpha, beta, gamma)
    
    #填充三角形
    def fill_triangle(self, v0, v1, v2, color = (255, 255, 255)):
        max_x = max(v0[0], max(v1[0], v2[0]))
        max_y = max(v0[1], max(v1[1], v2[1]))

        min_x = min(v0[0], min(v1[0], v2[0]))
        min_y = min(v0[1], min(v1[1], v2[1]))
        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                coord = self.barycentric_coord(v0, v1, v2, (i, j))
                if(coord[0] >= 0 and coord[1] >= 0 and coord[2] >= 0):
                    self.draw_point((i, j), color)