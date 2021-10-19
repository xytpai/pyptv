import os, sys; sys.path.append(os.getcwd())
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import ctypes
import glm
from engine import *


def main_loop():
    win_width = 1920
    win_height = 1080
    pygame.init()
    window = pygame.display.set_mode((win_width, win_height), \
        pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    clock = pygame.time.Clock()
    with open('./shader/vertex_base.glsl', 'r') as f: glsl_vert = f.read()
    with open('./shader/fragment_base.glsl', 'r') as f: glsl_frag = f.read()
    program = compileProgram( 
        compileShader(glsl_vert, GL_VERTEX_SHADER),
        compileShader(glsl_frag, GL_FRAGMENT_SHADER))
    attrib = { a : glGetAttribLocation(program, a) for a in ['in_position', 'in_normal'] }
    # print(attrib)
    uniform = { u : glGetUniformLocation(program, u) for u in \
        ['model', 'view', 'projection', 'light_direction', 'camera_position', 
        'object_f0', 'object_color', 'light_color', 'metallic', 'roughness', 'ao'] }
    # print(uniform)
    glUseProgram(program)
    container = Object3DContainer()
    camera = ViewCamera()
    str1 = container.AddObjectBySTLFile('model3d/SHL_2pcs.stl', 0.1)
    camera.SetPosition([0, 0, -40])    
    # camera.SetPitch(180)
    container.AddInstance('haha', str1)
    container.TranslateInstanceTo('haha', container.GetObjectCenter(str1))
    container.SetInstanceColor('haha', [255,0,0])
    # camera.UpdateCameraVectors()
    camera.LookAt(container.GetObjectCenter(str1))

    container.SetInstanceRoughness('haha', 0.9)
    container.SetInstanceMetallic('haha', 0.3)
    container.SetInstanceAO('haha', 0.5)

    degree = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                win_height = event.h
                win_width = event.w
        
        # camera.SetPitch(degree)
        
        # model = glm.rotate(model, glm.radians(angle_y), glm.vec3(0, 1, 0))
        # glUniformMatrix4fv(uniform['u_proj'], 1, GL_FALSE, glm.value_ptr(proj))
        glClearColor(0.5, 0.5, 0.5, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        container.RotateInstanceTo('haha', degree, [0,1,1])
        glUniform3fv(uniform['light_color'], 1, glm.value_ptr(glm.vec3(1.0, 1.0, 1.0)))
        glUniform3fv(uniform['light_direction'], 1, glm.value_ptr(glm.vec3(0,0,-1)))
        camera.RenderGL(program, win_height, win_width)
        container.RenderGL(program)
        
        degree += 1
        if degree>=180: degree = -180
        # print(degree)
        
        pygame.display.flip()
    pygame.quit()



if __name__ == '__main__':
    main_loop()