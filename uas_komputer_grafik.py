import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# === DATA KUBUS 3D ===
cube_vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]
cube_edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

# === DATA PERSEGI 2D ===
square_vertices = [
    [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]
]

# === STATE VARIABEL ===
c_trans = [-2, 0, -10] # Posisi awal agak ke kiri
c_rot = [0, 0, 0]
c_scale = 1.0

s_trans = [0, 0]
s_rot = 0
s_scale = 1.0
s_shear = 0.0 
s_reflect = 1.0 # 1.0 normal, -1.0 refleksi sumbu Y

def draw_cube():
    glPushMatrix()
    glTranslatef(c_trans[0], c_trans[1], c_trans[2])
    glRotatef(c_rot[0], 1, 0, 0)
    glRotatef(c_rot[1], 0, 1, 0)
    glScalef(c_scale, c_scale, c_scale)
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 1.0) # Biru Muda 
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glPopMatrix()

def draw_square():
    glPushMatrix()
    # Pindah ke posisi translasi
    glTranslatef(s_trans[0], s_trans[1], 0)
    # Rotasi sumbu Z
    glRotatef(s_rot, 0, 0, 1)
    # Skala & Refleksi (s_reflect membalik sumbu X untuk flip horizontal)
    glScalef(s_scale * s_reflect, s_scale, 1)
    
    # Matriks Shearing (Horizontal)
    shear_matrix = [
        1.0, 0.0, 0.0, 0.0,
        s_shear, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]
    glMultMatrixf(shear_matrix)

    glBegin(GL_QUADS)
    glColor3f(1.0, 0.5, 0.0) #Warna Orange
    for vertex in square_vertices:
        glVertex3fv(vertex)
    glEnd()
    glPopMatrix()

def main():
    global c_trans, c_rot, c_scale, s_trans, s_rot, s_scale, s_shear, s_reflect
    
    pygame.init()
    display = (1000, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("UAS Grafika Komputer - Qhaza Al Qhifary")

    glEnable(GL_DEPTH_TEST)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_w: c_trans[1] += 0.2 # Translasi Atas
                if event.key == K_s: c_trans[1] -= 0.2 # Translasi Bawah
                if event.key == K_a: c_trans[0] -= 0.2 # Translasi Kiri
                if event.key == K_d: c_trans[0] += 0.2 # Translasi Kanan
                if event.key == K_q: c_rot[0] += 10    # Rotasi (Sumbu X)
                if event.key == K_e: c_rot[1] += 10    # Rotasi (Sumbu Y)
                if event.key == K_r: c_scale += 0.1    # Skala Besar
                if event.key == K_f: c_scale = max(0.1, c_scale - 0.1) # Skala Kecil
                if event.key == K_UP:    s_trans[1] += 0.2 # Translasi Atas
                if event.key == K_DOWN:  s_trans[1] -= 0.2 # Translasi Bawah
                if event.key == K_LEFT:  s_trans[0] -= 0.2 # Translasi Kiri
                if event.key == K_RIGHT: s_trans[0] += 0.2 # Translasi Kanan
                if event.key == K_k:     s_rot += 10       # Rotasi Z
                if event.key == K_l:     s_scale += 0.1    # Skala Besar
                if event.key == K_m:     s_scale = max(0.1, s_scale - 0.1) # Skala Kecil
                if event.key == K_o:     s_shear += 0.1    # Shearing
                if event.key == K_p:     s_reflect *= -1   # Refleksi (Toggle Flip)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Viewport Kiri (3D)
        glViewport(0, 0, 500, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (500/600), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        draw_cube()

        # Viewport Kanan (2D)
        glViewport(500, 0, 500, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-5, 5, -5, 5) 
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        draw_square()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
