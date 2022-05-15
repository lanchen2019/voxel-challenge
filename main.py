from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (1.0, 1.0, 1.0))
scene.set_background_color((1, 0.8, 0.8))
scene.set_directional_light((1, 1, -1), 0.3, (1, 0.8, 0.8))

@ti.func
def create_sea(pos, size, color, color_noise):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_base(pos, radius, color):
    for I in ti.grouped(ti.ndrange((-radius, radius), (-radius, radius), (-radius, radius))):
        if I.norm() < radius: 
            if I[1] > 1 *radius / 3:
                scene.set_voxel(pos + I, 2, color) 
            else:
                scene.set_voxel(pos + I, 1, color) 

@ti.func
def create_halfball(pos, radius, color):
    for I in ti.grouped(ti.ndrange((-radius, radius), (0, radius), (-radius, radius))):
        if I.norm() < radius: 
            if I[1] > 1 *radius / 3:
                scene.set_voxel(pos + I, 2, color) 
            else:
                scene.set_voxel(pos + I, 1, color) 

@ti.func
def create_halfball2(pos, radius, color):
    for I in ti.grouped(ti.ndrange((-radius, radius), (-radius, 0), (-radius, radius))):
        if I.norm() < radius:  
            scene.set_voxel(pos + I, 1, color) 

@ti.func
def create_human(pos, radius, color, mat_in = 2, mat_out = 1, feet_mat=1):
    for I in ti.grouped(ti.ndrange((0, radius), (0, radius), (0, radius))): 
        if (I[0] == I[1] or I[0]+I[1] == (radius-1) )and I[2] == (radius-1):
            scene.set_voxel(pos + I, mat_in, color)  
        else:
            scene.set_voxel(pos + I, mat_out, color)  
    scene.set_voxel(pos + (0, -1, radius//2), feet_mat, color)
    scene.set_voxel(pos + (radius-1, -1, radius//2), feet_mat, color)   

@ti.func
def create_human_circle(pos, radius, color):
    for I in ti.grouped(ti.ndrange((-radius, radius), (0, 1), (-radius, radius))): 
        if I.norm() > radius-1 and I.norm() < radius and (I[0] % 4) == 0 :# and I[0] != 3 and  I[0] != -3:
            create_human(pos + I, 3, color) 
        elif I [0] == 0:
            create_human(pos + I, 3, color)
            
@ti.func
def create_elevator(pos, radius, color):
    radius2 = 1 
    for I in ti.grouped(ti.ndrange((-radius2,radius2+1), (-radius, radius), (-radius2,radius2+1))):
        if ((I[1]+1) // radius2 ) % 2 == 0:
            scene.set_voxel(pos + I, 2, color) 
        else:
            scene.set_voxel(pos + I, 1, color)  

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    create_halfball(ivec3(0, -50, 0), 45, vec3(252.0/255.0, 159.0/255.0, 193.0/255.0))
    create_halfball2(ivec3(0, 50, 0), 45, vec3(252.0/255.0, 159.0/255.0, 193.0/255.0))
    create_elevator(ivec3(1, 0, 0), 64, vec3(252.0/255.0, 159.0/255.0, 193.0/255.0))
    for i in range(16, 33):
        if i % 8 == 0:  
            create_human_circle(ivec3(0, 51, 0), i, vec3(252.0/255.0, 159.0/255.0, 193.0/255.0)) 

initialize_voxels()

scene.finish()
