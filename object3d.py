import struct
import ctypes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import glm


class Object3DContainer:
    def __init__(self):
        self.map_identity2buffer_ = {}
        self.map_name2object_ = {}
    
    def AddBufferBySTLFile(self, stl_file_path, scale=1.0):
        identity = None
        with open(stl_file_path, 'rb') as f:
            f.read(80)
            num_tris = struct.unpack('i', f.read(4))[0]
            data = []
            cx, cy, cz = 0, 0, 0
            for i in range(num_tris):
                norm = struct.unpack('f'*3, f.read(4*3))
                tri = struct.unpack('f'*9, f.read(4*9))
                for j in range(0, 3): data.append(tri[j]*scale)
                for j in range(0, 3): data.append(norm[j]*scale)
                for j in range(3, 6): data.append(tri[j]*scale)
                for j in range(0, 3): data.append(norm[j]*scale)
                for j in range(6, 9): data.append(tri[j]*scale)
                for j in range(0, 3): data.append(norm[j]*scale)
                f.read(2)
                cx += (data[0] + data[6] + data[12])/3.0
                cy += (data[1] + data[7] + data[13])/3.0
                cz += (data[2] + data[8] + data[14])/3.0
            cx /= num_tris
            cy /= num_tris
            cz /= num_tris
            vao = glGenVertexArrays(1)
            identity = str(stl_file_path)
            info = {
                'len':num_tris*18,
                'data':data,
                'vao':vao,
                'identity':identity,
                'center':[cx, cy, cz]
            }
            self.map_identity2buffer_[identity] = info
        return identity
    
    def GetCenter(self, identity):
        return self.map_identity2buffer_[identity]['center']

    def AddObject(self, name, identity):
        info = {
            'buffer': self.map_identity2buffer_[identity],
            'model': glm.mat4(1),
            'color': glm.vec3(0.2, 0.8, 0.1),
            'f0': glm.vec3(1.0, 0.71, 0.29),
            'ao': 0.4,
            'roughness': 0.4,
            'metallic': 0.4
        }
        self.map_name2object_[name] = info
        if self.map_identity2buffer_[identity].get('count', None) is None:
            self.map_identity2buffer_[identity]['count'] = 0
        else:
            self.map_identity2buffer_[identity]['count'] += 1
    
    def RotateTo(self, name, degree, axis):
        if isinstance(axis, list): axis = glm.vec3(axis[0], axis[1], axis[2])
        obj_info = self.map_name2object_[name]
        model = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(degree), axis)
        obj_info['model'] = model
    
    def TranslateTo(self, name, position):
        if isinstance(position, list): position = glm.vec3(position[0], position[1], position[2])
        obj_info = self.map_name2object_[name]
        model = glm.mat4(1.0)
        model = glm.translate(model, position)
        obj_info['model'] = model
    
    def RenderGL(self, shader):
        glUseProgram(shader)
        uniform = { u : glGetUniformLocation(shader, u) for u in \
            ['model',  'object_color', 'object_f0', 'ao', 'roughness', 'metallic'] }
        for name in self.map_name2object_.keys():
            obj_info = self.map_name2object_[name]
            buffer_info = obj_info['buffer']
            glBindVertexArray(buffer_info['vao'])
            if not buffer_info.get('is_glbuffer', False):
                vbo = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vbo)
                glBufferData(GL_ARRAY_BUFFER, (GLfloat * buffer_info['len'])(*buffer_info['data']), GL_STATIC_DRAW)
                glVertexAttribPointer(0, 3, GL_FLOAT, False, 6*ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
                glEnableVertexAttribArray(0)
                glVertexAttribPointer(1, 3, GL_FLOAT, False, 6*ctypes.sizeof(GLfloat), ctypes.c_void_p(3*ctypes.sizeof(GLfloat)))
                glEnableVertexAttribArray(1)
                buffer_info['is_glbuffer'] = True
            glUniformMatrix4fv(uniform['model'], 1, GL_FALSE, glm.value_ptr(obj_info['model']))
            glUniform3fv(uniform['object_color'], 1, glm.value_ptr(obj_info['color']))
            glUniform3fv(uniform['object_f0'], 1, glm.value_ptr(obj_info['f0']))
            glUniform1f(uniform['ao'], obj_info['ao'])
            glUniform1f(uniform['roughness'], obj_info['roughness'])
            glUniform1f(uniform['metallic'], obj_info['metallic'])
            glDrawArrays(GL_TRIANGLES, 0, buffer_info['len']//6)
        glBindVertexArray(0)


if __name__ == '__main__':
    objc = Object3DContainer
    objc.AddBufferBySTLFile('model3d/SHL_2pcs.stl')