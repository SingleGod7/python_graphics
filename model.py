from PIL import Image

class Materals:
    def __init__(self, filepath):
        self.materials = {}
        self.materials_in_use = None
        self.a_texture = None
        self.d_texture = None
        self.s_texture = None

        current_material = None
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith('#') or len(line) == 0:
                    #忽略空行和注释
                    continue

                values = line.split()
                if values[0] == 'newmtl':
                    current_material = {'name': values[1]}
                    self.materials[current_material['name']] = current_material
                elif current_material == None:
                    continue
                
                elif values[0] == 'Ka':
                    current_material['ambient_color'] = tuple(map(float, values[1:]))
                elif values[0] == 'Kd':
                    current_material['diffuse_color'] = tuple(map(float, values[1:]))
                elif values[0] == 'Ks':
                    current_material['specular_color'] = tuple(map(float, values[1:]))
                elif values[0] == 'Ns':
                    current_material['shininess'] = float(values[1])
                elif values[0] == 'd':
                    current_material['opacity'] = float(values[1])
                elif values[0] == 'map_Ka':
                    current_material['ambient_texture'] = values[1]
                elif values[0] == 'map_Kd':
                    current_material['diffuse_texture'] = values[1]
                elif values[0] == 'map_Ks':
                    current_material['specular_texture'] = values[1]
                elif values[0] == 'map_Ns':
                    current_material['shininess_texture'] = values[1]
                elif values[0] == 'map_d':
                    current_material['opacity_texture'] = values[1]
                else:
                # 忽略其他不支持的属性
                    pass 
    
    def use_materal(self, name):
        if(name in self.materials.keys):
            self.materials_in_use = self.materials[name]
            if("ambient_texture" in self.materials_in_use.keys):
                self.a_texture = Image.open(self.materials_in_use["ambient_texture"])
            if("diffuse_texture" in self.materials_in_use.keys):
                self.d_texture = Image.open(self.materials_in_use["diffuse_texture"])
            if("specular_texture" in self.materials_in_use.keys):
                self.s_texture = Image.open(self.materials_in_use["specular_texture"])
        else:
            raise NameError("Can't find the material!")
        
    def get_ambient_color(self, texcoord=None):
        color = self.materials_in_use['ambient_color']
        if(texcoord != None and self.s_texture != None):
            x,y = texcoord
            color *= self.a_texture.getpixel((round(x), round(y)))
        return color
    
    def get_diffuse_color(self, texcoord=None):
        color = self.materials_in_use['diffuse_color']
        if(texcoord != None and self.s_texture != None):
            x,y = texcoord
            color *= self.d_texture.getpixel((round(x), round(y)))
        return color
    
    def get_specular_color(self, texcoord=None):
        color = self.materials_in_use['specular_color']
        if(texcoord != None and self.s_texture != None):
            x,y = texcoord
            color *= self.s_texture.getpixel((round(x), round(y)))
        return color
    
class Model:
    def __init__(self, filepath):
        self.vertex = []
        self.normal = []
        self.texcoord = []
        self.face = []
        self.material = None

        with open(filepath, "r") as f:
            for line in f:
                line = line.split()
                if(len(line) == 0):
                    continue
                elif(line[0] == "v"):
                    x, y, z = [float(x) for x in line[1:]]
                    self.vertex.append((x, y, z))
                elif(line[0]  == "vt"):
                    x, y = [float(x) for x in line[1:]]
                    self.texcoord.append((x, y))
                elif(line[0] == "vn"):
                    self.normal.append((x, y, z))
                elif(line[0] == "f"):
                    f = []
                    for i in line[1:]:
                        v, n, t = [int(x) for x in i.split("/")]
                        #obj是1开始索引的
                        f.append((v - 1, n - 1, t - 1))
                    self.face.append(f)
                elif(line[0] == "mtllib"):
                    a = filepath.split("/")
                    a[-1] = line[1]
                    a = "/".join(a)
                    self.material = Materals(a)

    def get_vertex(self, f):
        x, y, z = [f[i][0] for i in range(3)]
        return (self.vertex[x], self.vertex[y], self.vertex[z])
    
    def get_texcoord(self, f):
        x, y, z = [f[i][1] for i in range(3)]
        return (self.texcoord[x], self.texcoord[y], self.texcoord[z])
    
    def get_normal(self, f):
        x, y, z = [f[i][2] for i in range(3)]
        return (self.texcoord[x], self.texcoord[y], self.texcoord[z])
        
