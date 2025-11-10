import pygame
import random
import os

# --- INICIALIZACIÓN Y CONFIGURACIÓN ---
pygame.init()

# Colores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50) 
PINK = (255, 240, 245) # Fondo suave para el mensaje
GREEN = (0, 150, 0) # Para el botón SÍ
YELLOW_BG = (250, 250, 200) # Fondo de la pantalla de pregunta

# Pantalla (Resolución estándar vertical para Android)
SIZE = (720, 1280)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("9 Meses Juntos - Para Mi Amor")

# Clock y FPS
clock = pygame.time.Clock()
FPS = 60

# --- FUENTES ---
try:
    FONT_TITLE = pygame.font.Font(None, 85)
    FONT_BUTTON = pygame.font.Font(None, 95)
    FONT_MSG = pygame.font.Font(None, 50)
except:
    FONT_TITLE = pygame.font.SysFont("Arial", 85)
    FONT_BUTTON = pygame.font.SysFont("Arial", 95)
    FONT_MSG = pygame.font.SysFont("Arial", 50)


# --- CLASE DE PARTICULAS (Para la animación de pétalos/brillos) ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.original_image = image 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = random.randint(1, 3) 
        self.speed_x = random.uniform(-0.5, 0.5) 
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        self.rotation += self.rotation_speed
        try:
            self.image = pygame.transform.rotate(self.original_image, self.rotation)
            self.rect = self.image.get_rect(center=self.rect.center)
        except:
            pass
        
        if self.rect.top > SIZE[1]:
            self.kill()

# --- CARGA DE RECURSOS (Imágenes) ---
def load_image(name, scale_factor=1.0):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
        w, h = image.get_size()
        image = pygame.transform.scale(image, (int(w * scale_factor), int(h * scale_factor)))
        return image
    except pygame.error as message:
        print(f"ERROR: No se pudo cargar la imagen: {fullname}. {message}")
        return None

# Cargar imágenes (AJUSTA LOS NOMBRES DE ARCHIVO AQUÍ si son diferentes)
FLOWER_IMAGE = load_image('ramo_flores.png', scale_factor=0.6) 
PETAL_IMAGE = load_image('petal.png', scale_factor=0.1) 

# --- GESTIÓN DE FALLOS EN CARGA DE IMAGEN ---
if not FLOWER_IMAGE:
    print("USANDO IMAGEN DE RELLENO para FLOWER_IMAGE.")
    FLOWER_IMAGE = pygame.Surface((300, 500), pygame.SRCALPHA) 
    FLOWER_IMAGE.fill(RED)
if not PETAL_IMAGE:
    print("USANDO IMAGEN DE RELLENO para PETAL_IMAGE.")
    PETAL_IMAGE = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(PETAL_IMAGE, (255, 255, 0), (10, 10), 10) 

Particle.original_image = PETAL_IMAGE 

# Grupos de sprites (para manejar las animaciones)
particles = pygame.sprite.Group()

# --- VARIABLES GLOBALES DE INTERFAZ Y LÓGICA ---
# 1: Principal, 2: Pregunta, 3: Regalo
current_screen = 1 

# Rectángulos de los botones de SÍ y NO (Necesarios para la lógica de toque)
yes_rect = pygame.Rect(0, 0, 0, 0)
no_rect = pygame.Rect(0, 0, 0, 0)

# Coordenadas variables del botón NO (para que se escape)
no_button_pos = [SIZE[0] // 2 + 150, 800] 

# Secuencia de mensajes al presionar NO
NO_MESSAGES = [
    "¿Me amas?",               
    "como que no :(",          
    "oye porque le sigues dando que no :(", 
    "enserio no me amas?",     
    "amooooooooooor",          
    "ya dententeeeeee",        
    "te voy a hackear el celular como le sigas dando que no", 
    "..."                      
]
message_index = 0 # Inicia en el primer mensaje

# Botón de "9 Meses" (en la Pantalla 1)
button_text = FONT_BUTTON.render("9 MESES", True, WHITE)
button_rect = button_text.get_rect(center=(SIZE[0] // 2, 700))

# --- FUNCIONES DE DIBUJO ---
def draw_screen1():
    """Dibuja la pantalla de bienvenida con el mensaje de felicitación."""
    screen.fill(WHITE) 
    
    # Títulos (Texto "felices 9 meses mi blanquita preciosa")
    title_line1 = FONT_TITLE.render("Felices 9 meses", True, BLACK)
    title_line2 = FONT_TITLE.render("mi blanquita preciosa", True, BLACK) 
    
    screen.blit(title_line1, title_line1.get_rect(center=(SIZE[0] // 2, 200)))
    screen.blit(title_line2, title_line2.get_rect(center=(SIZE[0] // 2, 300)))
    
    # Dibuja el botón
    pygame.draw.rect(screen, RED, button_rect.inflate(80, 50), border_radius=25)
    screen.blit(button_text, button_rect)

def draw_screen2():
    """Dibuja la pantalla de la pregunta interactiva: ¿Me amas?"""
    global yes_rect, no_rect, no_button_pos
    
    screen.fill(YELLOW_BG) 
    
    # Pregunta (Usa el mensaje actual de la lista)
    current_message = NO_MESSAGES[message_index]
    question_text = FONT_TITLE.render(current_message, True, BLACK)
    screen.blit(question_text, question_text.get_rect(center=(SIZE[0] // 2, 300)))
    
    # --- Botón SÍ (Fijo) ---
    yes_label = FONT_BUTTON.render("SÍ", True, WHITE)
    # Definimos la posición del botón SÍ
    yes_rect = yes_label.get_rect(center=(SIZE[0] // 2 - 150, 800))
    pygame.draw.rect(screen, GREEN, yes_rect.inflate(80, 50), border_radius=25)
    screen.blit(yes_label, yes_rect)

    # --- Botón NO (Móvil) ---
    no_label = FONT_BUTTON.render("NO", True, WHITE)
    # Usamos la posición actual de no_button_pos
    no_rect = no_label.get_rect(center=(no_button_pos[0], no_button_pos[1]))
    pygame.draw.rect(screen, RED, no_rect.inflate(80, 50), border_radius=25) 
    screen.blit(no_label, no_rect)

def draw_screen3():
    """Dibuja la pantalla de regalo con flores y animación."""
    screen.fill(PINK) 
    
    # 1. Animación de Partículas (pétalos cayendo)
    particles.update()
    particles.draw(screen)
    
    # 2. Ramo de Flores
    flower_rect = FLOWER_IMAGE.get_rect(center=(SIZE[0] // 2, SIZE[1] * 0.55))
    screen.blit(FLOWER_IMAGE, flower_rect)
        
    # 3. Mensaje Final
    msg_line1 = FONT_MSG.render("¡Felices 9 meses, mi vida!", True, BLACK) 
    msg_line2 = FONT_MSG.render("Gracias por hacer mi mundo florecer.", True, BLACK) 
    
    screen.blit(msg_line1, msg_line1.get_rect(center=(SIZE[0] // 2, 100)))
    screen.blit(msg_line2, msg_line2.get_rect(center=(SIZE[0] // 2, 150)))
    
# --- BUCLE PRINCIPAL ---
running = True
particle_timer = 0
PARTICLE_RATE = 10 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detección de toque (MOUSEBUTTONDOWN funciona como un toque en Android)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == 1:
                # Si toca el botón "9 MESES"
                if button_rect.collidepoint(event.pos):
                    current_screen = 2 # Va a la pantalla de la pregunta
            
            elif current_screen == 2:
                # Lógica en la pantalla de pregunta
                if yes_rect.collidepoint(event.pos):
                    # Presionó SÍ: Va al regalo
                    current_screen = 3 
                    message_index = 0 # Reiniciamos el contador 
                elif no_rect.collidepoint(event.pos):
                    # Presionó NO: Mueve el botón de forma aleatoria Y cambia el mensaje
                    
                    # 1. Incrementa el índice del mensaje y lo resetea si es necesario
                    message_index += 1
                    if message_index >= len(NO_MESSAGES):
                        message_index = 0 
                    
                    # 2. Mueve el botón a una nueva posición aleatoria
                    no_button_pos[0] = random.randint(50, SIZE[0] - 100)
                    no_button_pos[1] = random.randint(300, SIZE[1] - 100)
            
            elif current_screen == 3:
                # Si está en el regalo, ignoramos el toque para que lo siga viendo
                pass

    # --- LÓGICA DE ANIMACIÓN ---
    if current_screen == 3:
        particle_timer += 1
        if particle_timer >= PARTICLE_RATE:
            x_pos = random.randint(50, SIZE[0] - 50)
            new_particle = Particle(x_pos, -20, PETAL_IMAGE)
            particles.add(new_particle)
            particle_timer = 0

    # --- DIBUJO ---
    if current_screen == 1:
        draw_screen1()
    elif current_screen == 2:
        draw_screen2()
    elif current_screen == 3:
        draw_screen3()
        
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar la velocidad
    clock.tick(FPS)

pygame.quit()