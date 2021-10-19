import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import glm


class Camera:
    def __init__(self) -> None:
        '''               
                  y
                 /|\      
                  |       .
                  |     .
                  |   .
           - - - - - - - - - -> x
                . |
              .   |
            |_    |
            z
        
        order: xyz
        (1,0,0) -> (0,0,-1): yaw(0 -> 90)
        (0,0,-1) -> (0,1,0): pitch(0 -> 90)
        '''
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.yaw = -90.0
        self.pitch = -0.0
        self.roll = 90.0
        self.front = None
        self.right = None
        self.up = None
        self.UpdateCameraVectors()
    
    def UpdateCameraVectors(self) -> None:
        front = glm.vec3(
            math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
            math.sin(glm.radians(self.pitch)),
            math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)))
        camera_world_up = glm.vec3(
            math.cos(glm.radians(self.roll)),
            math.sin(glm.radians(self.roll)),
            0.0)
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, camera_world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
    
    def SetPosition(self, xyz) -> None: 
        if isinstance(xyz, glm.vec3):
            self.position = xyz
        else:
            self.position = glm.vec3(xyz[0], xyz[1], xyz[2])
    
    def SetYaw(self, yaw: float) -> None: 
        self.yaw = yaw
        self.UpdateCameraVectors()

    def SetPitch(self, pitch: float) -> None: 
        self.pitch = pitch
        self.UpdateCameraVectors()

    def SetRoll(self, roll: float) -> None: 
        self.roll = roll
        self.UpdateCameraVectors()
    
    def SetYP(self, yaw: float, pitch: float) -> None:
        self.yaw = yaw
        self.pitch = pitch
        self.UpdateCameraVectors()
    
    def SetYPR(self, yaw: float, pitch: float, roll: float) -> None:
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.UpdateCameraVectors()
    
    def LookAt(self, target) -> None:
        eps = 1e-10
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dz = target[2] - self.position[2]
        dze = dz + eps
        dxe = dx + eps
        if dz <= 0: pitch = glm.degrees(math.atan(-dy / dze))
        elif dy >= 0: pitch = 180.0 - glm.degrees(math.atan(dy / dze))
        else: pitch = glm.degrees(math.atan(-dy / dze)) - 180.0
        if dx >= 0: yaw = glm.degrees(math.atan(-dz / dxe))
        elif dz >= 0: yaw = glm.degrees(math.atan(-dz / dxe)) - 180.0
        else: yaw = 180.0 - glm.degrees(math.atan(dz / dxe))
        self.SetYP(yaw, pitch)

    def GetView(self) -> glm.mat4:
        return glm.lookAt(self.position, self.position + self.front, self.up)


class ViewCamera(Camera):
    def __init__(self) -> None:
        super().__init__()
        self.zoom = 45.0
    
    def SetZoom(self, zoom: float) -> None: 
        self.zoom = zoom
    
    def GetProjection(self, win_height: float, win_width: float) -> glm.mat4:
        return glm.perspective(glm.radians(self.zoom), \
            win_width / win_height, 0.1, 100.0)
    
    def RenderGL(self, shader, win_height: float, win_width: float) -> None:
        glUseProgram(shader)
        uniform = { u : glGetUniformLocation(shader, u) for u in \
            ['view',  'projection', 'camera_position'] }
        view = self.GetView()
        projection = self.GetProjection(win_height, win_width)
        glUniformMatrix4fv(uniform['view'], 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(uniform['projection'], 1, GL_FALSE, glm.value_ptr(projection))
        glUniform3fv(uniform['camera_position'], 1, glm.value_ptr(self.position))
