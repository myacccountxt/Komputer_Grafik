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
c_trans = [0, 0, -5]
c_rot = [0, 0, 0]
c_scale = 1.0

s_trans = [0, 0]
s_rot = 0
s_scale = 1.0
s_shear = [0, 0] 
s_reflect = [1, 1] 

def draw_cube():
    glPushMatrix()
    glTranslatef(c_trans[0], c_trans[1], c_trans[2])
    glRotatef(c_rot[0], 1, 0, 0)
    glRotatef(c_rot[1], 0, 1, 0)
    glScalef(c_scale, c_scale, c_scale)
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 1.0) # Cyan
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glPopMatrix()

def draw_square():
    glPushMatrix()
    glTranslatef(s_trans[0], s_trans[1], 0)
    glRotatef(s_rot, 0, 0, 1)
    glScalef(s_scale * s_reflect[0], s_scale * s_reflect[1], 1)
    
    # Matriks Shearing
    shear_matrix = [
        1.0, s_shear[1], 0.0, 0.0,
        s_shear[0], 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ]
    glMultMatrixf(shear_matrix)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 1.0) # Cyan (Sama dengan Kubus)
    for vertex in square_vertices:
        glVertex3fv(vertex)
    glEnd()
    glPopMatrix()

def main():
    global c_trans, c_rot, c_scale, s_trans, s_rot, s_scale, s_shear, s_reflect
    
    pygame.init()
    display = (1000, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("UAS Grafika Komputer - 3D & 2D Transformation")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                # --- KONTROL KUBUS 3D ---
                if event.key == K_w: c_trans[1] += 0.2  # Translasi Atas
                if event.key == K_s: c_trans[1] -= 0.2  # Translasi Bawah
                if event.key == K_a: c_rot[1] -= 10     # Rotasi Kiri
                if event.key == K_d: c_rot[1] += 10     # Rotasi Kanan
                if event.key == K_q: c_scale += 0.1     # Skala Besar
                if event.key == K_e: c_scale = max(0.1, c_scale - 0.1) # Skala Kecil

                # --- KONTROL PERSEGI 2D ---
                # Translasi
                if event.key == K_UP:    s_trans[1] += 0.2
                if event.key == K_DOWN:  s_trans[1] -= 0.2
                if event.key == K_LEFT:  s_trans[0] -= 0.2
                if event.key == K_RIGHT: s_trans[0] += 0.2
                
                # Rotasi
                if event.key == K_r: s_rot += 15
                
                # Skala (Menggunakan Tombol +/- biasa, bukan Numpad agar lebih stabil)
                if event.key == K_EQUALS or event.key == K_KP_PLUS: s_scale += 0.1
                if event.key == K_MINUS or event.key == K_KP_MINUS: s_scale = max(0.1, s_scale - 0.1)
                
                # Shearing
                if event.key == K_h: s_shear[0] += 0.2  # Tambah Shear
                if event.key == K_j: s_shear[0] = 0     # Reset Shear
                
                # Refleksi
                if event.key == K_x: s_reflect[1] *= -1 # Refleksi Sumbu X (Flip Y)
                if event.key == K_y: s_reflect[0] *= -1 # Refleksi Sumbu Y (Flip X)

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
