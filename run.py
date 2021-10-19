import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import ctypes
import glm
from config import cfg
from object3d import *
from camera import *


def main_loop():
    pygame.init()
    window = pygame.display.set_mode((cfg.win_width, cfg.win_height), \
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
    str1 = container.AddBufferBySTLFile('model3d/SHL_2pcs.stl', 0.1)
    camera.SetPosition([0, 0, -40])    
    camera.SetPitch(180)
    container.AddObject('haha', str1)
    container.TranslateTo('haha', container.GetCenter(str1))
    # camera.UpdateCameraVectors()

    degree = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.VIDEORESIZE:
                pass
                # glViewport(0, 0, event.w, event.h)
                # proj = set_projection(event.w, event.h)
        
        # camera.SetPitch(degree)
        
        # model = glm.rotate(model, glm.radians(angle_y), glm.vec3(0, 1, 0))
        # glUniformMatrix4fv(uniform['u_proj'], 1, GL_FALSE, glm.value_ptr(proj))
        glClearColor(0.5, 0.5, 0.5, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        container.RotateTo('haha', degree, [0,0,122])
        glUniform3fv(uniform['light_color'], 1, glm.value_ptr(glm.vec3(1.0, 1.0, 1.0)))
        glUniform3fv(uniform['light_direction'], 1, glm.value_ptr(-camera.front))
        camera.RenderGL(program, cfg.win_height, cfg.win_width)
        container.RenderGL(program)
        
        degree += 1
        if degree>=180: degree = -180
        # print(degree)
        
        pygame.display.flip()
    pygame.quit()



if __name__ == '__main__':
    main_loop()