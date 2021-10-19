import glm
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *


class Camera:
    def __init__(self):
        self.position = glm.vec3(-50.0, 50.0, 50.0)
        self.yaw = -90.0
        self.pitch = -0.0
        self.roll = 90.0
        self.UpdateCameraVectors()
    
    def SetPosition(self, xyz): 
        self.position = glm.vec3(xyz[0], xyz[1], xyz[2])
    
    def SetYaw(self, yaw): 
        self.yaw = yaw
        self.UpdateCameraVectors()

    def SetPitch(self, pitch): 
        self.pitch = pitch
        self.UpdateCameraVectors()

    def SetRoll(self, roll): 
        self.roll = roll
        self.UpdateCameraVectors()
    
    def SetYPR(self, yaw, pitch, roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.UpdateCameraVectors()
    
    def UpdateCameraVectors(self):
        front = glm.vec3(
            math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
            math.sin(glm.radians(self.pitch)),
            math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)))
        self.front = glm.normalize(front)
        camera_world_up = glm.vec3(
            math.cos(glm.radians(self.roll)),
            math.sin(glm.radians(self.roll)),
            0.0)
        self.right = glm.normalize(glm.cross(self.front, camera_world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
    
    def GetViewMatrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)
    
    # def GetViewMatrixLookAt(self, target, up):
    #     if isinstance(up, list): up = glm.vec3(up[0], up[1], up[2])
    #     up = glm.normalize(up)
    #     return glm.lookAt(self.position, target, up)


class ViewCamera(Camera):
    def __init__(self):
        super().__init__()
        self.zoom = 45.0
    
    def SetZoom(self, zoom): self.zoom = zoom
    
    def GetProjectionMatrix(self, win_height, win_width):
        return glm.perspective(glm.radians(self.zoom), \
            win_width / win_height, 0.1, 100.0)
    
    def RenderGL(self, shader, win_height, win_width):
        glUseProgram(shader)
        uniform = { u : glGetUniformLocation(shader, u) for u in \
            ['view',  'projection', 'camera_position'] }
        view = self.GetViewMatrix()
        projection = self.GetProjectionMatrix(win_height, win_width)
        glUniformMatrix4fv(uniform['view'], 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(uniform['projection'], 1, GL_FALSE, glm.value_ptr(projection))
        glUniform3fv(uniform['camera_position'], 1, glm.value_ptr(self.position))