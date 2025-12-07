import pygame
import sys
import os
import random


pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


# --- Window settings ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CrabHacks 2025")
clock = pygame.time.Clock()


# --- Player settings ---
crab_size = 75
crab_speed = 3
crab_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, crab_size, crab_size)
facing_right = True


# --- Health ---
max_health = 5
crab_health = max_health


# --- Font ---
font = pygame.font.SysFont(None, 36)
font = pygame.font.Font(None, 48)


# --- Paths ---
BASE_PATH = os.path.dirname(__file__)
CRAB_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/CrabWithBottleCap")
HAZARD_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/Hazards")
OBJECT_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/Plastic")
MUSIC_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/background_music.wav")
START_BG_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/Water")


#shell
SHELL_PATH = os.path.join(BASE_PATH, "shell.png")
shell_img = pygame.image.load(SHELL_PATH).convert_alpha()
shell_img = pygame.transform.scale(shell_img, (50, 50))
shell_rect = shell_img.get_rect()
shell_active = False  # Only active in level 4


# --- Level Backgrounds ---
LEVEL_BG_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/Levels")


level_backgrounds = []
for i in range(1, 5):   # Loads background_1.png to background_4.png
   bg_path = os.path.join(LEVEL_BG_PATH, f"background_{i}.png")
   bg = pygame.image.load(bg_path).convert()
   bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
   level_backgrounds.append(bg)


current_level = 0   # start at level 0 (background_1)


# --- Load music ---
if os.path.exists(MUSIC_PATH):
   pygame.mixer.music.load(MUSIC_PATH)
   pygame.mixer.music.play(-1)


# --- Load crab frames ---
crab_frames = []
for i in range(4):
   path = os.path.join(CRAB_PATH, f"sprite_{i}.png")
   frame = pygame.image.load(path).convert_alpha()
   frame = pygame.transform.scale(frame, (crab_size, crab_size))
   crab_frames.append(frame)


current_frame = 0
frame_timer = 0
animation_speed = 0.15


# --- Load start screen frames ---
start_frames = []
for i in range(3):   # 3 frames: start_0.png, start_1.png, start_2.png
   path = os.path.join(START_BG_PATH, f"sprite_{i}.png")
   frame = pygame.image.load(path).convert()
   frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
   start_frames.append(frame)


# --- Hazards with variable frame counts ---
hazard_frame_counts = [4, 2]  # Example: first hazard 4 frames, second 2 frames, third 3 frames
num_hazards = len(hazard_frame_counts)
hazard_frames = []
hazard_rects = []
hazard_current_frames = []
hazard_timers = []
hazard_animation_speeds = [0.1, 0.1]  # optional: different speed per hazard


for h in range(num_hazards):
   frames = []
   for f in range(hazard_frame_counts[h]):
       path = os.path.join(HAZARD_PATH, f"sprite_{h}_{f}.png")
       img = pygame.image.load(path).convert_alpha()
       img = pygame.transform.scale(img, (50, 50))
       frames.append(img)
   hazard_frames.append(frames)
   rect = frames[0].get_rect()
   rect.topleft = (random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50))
   hazard_rects.append(rect)
   hazard_current_frames.append(0)
   hazard_timers.append(0)


# --- Collectible objects and facts ---
object_files = ["sprite_0.png","sprite_1.png","sprite_2.png","sprite_3.png"]
facts = [
   "Creates microplastics in the water",
   "Often mistaken for jellyfish and eaten",
   "Turtles get their heads stuck",
   "Crabs get entangled in twine or injured by hooks"
]


objects = []
for i, img_file in enumerate(object_files):
   img_path = os.path.join(OBJECT_PATH, img_file)
   img = pygame.image.load(img_path).convert_alpha()
   img = pygame.transform.scale(img, (40, 40))
   rect = img.get_rect()
   rect.topleft = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-150))
   objects.append({"image": img, "rect": rect, "fact": facts[i]})


def start_screen():
   title_font = pygame.font.SysFont(None, 72)


   small_font = pygame.font.SysFont(None, 36)


   current_frame = 0
   frame_timer = 0
   animation_speed = 0.01  # adjust for faster/slower animation


   while True:
       # --- Animate the background ---
       frame_timer += animation_speed
       if frame_timer >= 1:
           frame_timer = 0
           current_frame = (current_frame + 1) % len(start_frames)


       # Draw animated background
       screen.blit(start_frames[current_frame], (0, 0))


       # Title text
       title = title_font.render(" CrabHacks 2025 ", True, (255, 255, 255), 'black')
       screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))


       # Instructions
       subtitle = small_font.render(" Click to Start ", True, (255, 255, 0), 'black')
       screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2))


       pygame.display.flip()


       # --- Handle events ---
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               return


start_screen()


def ending_screen():
   title_font = pygame.font.SysFont(None, 72)
   small_font = pygame.font.SysFont(None, 36)
   while True:
       screen.fill((0, 100, 200))  # background color
       title = title_font.render("Congratulations!", True, (255, 255, 255))
       screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
       subtitle = small_font.render("You helped Hermit find a new shell!", True, (255, 255, 0))
       screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2))
       pygame.display.flip()


       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               return


# --- Main game loop ---
show_fact = ""
fact_timer = 0  # timer to
#show fact temporarily


while True:
   # --- Event handling ---
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()


   # --- Player movement ---
   keys = pygame.key.get_pressed()
   moving = False
   if keys[pygame.K_LEFT]:
       crab_rect.x -= crab_speed
       moving = True
       facing_right = False
   if keys[pygame.K_RIGHT]:
       crab_rect.x += crab_speed
       moving = True
       facing_right = True
   if keys[pygame.K_UP]:
       crab_rect.y -= crab_speed
       moving = True
   if keys[pygame.K_DOWN]:
       crab_rect.y += crab_speed
       moving = True


   # Keep crab inside screen
   crab_rect.x = max(0, min(crab_rect.x, WIDTH - crab_size))
   crab_rect.y = max(0, min(crab_rect.y, HEIGHT - crab_size))


   # --- Animate crab ---
   if moving:
       frame_timer += animation_speed
       if frame_timer >= 1:
           frame_timer = 0
           current_frame = (current_frame + 1) % len(crab_frames)
   else:
       current_frame = 0


   # --- Animate hazards ---
   for i in range(num_hazards):
       hazard_timers[i] += hazard_animation_speeds[i]
       if hazard_timers[i] >= 1:
           hazard_timers[i] = 0
           hazard_current_frames[i] = (hazard_current_frames[i] + 1) % hazard_frame_counts[i]


   # --- Check collisions with hazards ---
   for i, rect in enumerate(hazard_rects):
       if crab_rect.colliderect(rect):
           crab_health -= 1
           crab_health = max(0, crab_health)
           rect.topleft = (random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50))


   # --- Check collisions with objects ---
   for obj in objects[:]:
       if crab_rect.colliderect(obj["rect"]):
           show_fact = obj["fact"]
           fact_timer = 180  # show for 3 seconds
           obj["rect"].topleft = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-150))
       if current_level == 3 and shell_active:
           if crab_rect.colliderect(shell_rect):
               ending_screen()
               pygame.quit()
               sys.exit()


   if fact_timer > 0:
       fact_timer -= 1
   else:
       show_fact = ""
  
   # --- Level progression ---
   if crab_rect.top <= 0:  # crab reaches top of screen
       if current_level < 3:    # if not already on final level
           current_level += 1
           crab_rect.centery = HEIGHT - 50  # move crab to bottom for new level


   if current_level == 3:  # Level 4 (0-indexed)
       if not shell_active:
           shell_rect.topleft = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-150))
           shell_active = True


   # --- Check game over ---
   if crab_health <= 0:
       print("Game Over!")
       pygame.quit()
       sys.exit()


   # --- Drawing ---
   screen.blit(level_backgrounds[current_level], (0, 0))


   level_text = font.render(f"Level {current_level + 1}", True, (0, 0, 0))
   screen.blit(level_text, (20, 100))


   # Draw hazards
   for i, rect in enumerate(hazard_rects):
       current_img = hazard_frames[i][hazard_current_frames[i]]
       screen.blit(current_img, rect)


   # Draw objects
   for obj in objects:
       screen.blit(obj["image"], obj["rect"])


   # Draw crab
   frame = crab_frames[current_frame]
   if not facing_right:
       frame = pygame.transform.flip(frame, True, False)
   screen.blit(frame, crab_rect)


   # Draw shell
   if current_level == 3 and shell_active:
       screen.blit(shell_img, shell_rect)


   # Draw health bar
   for i in range(crab_health):
       pygame.draw.rect(screen, (255, 0, 0), (10 + i*35, 10, 30, 30))


   # Draw health text
   health_text = font.render(f"Health: {crab_health}/{max_health}", True, (0, 0, 0))
   screen.blit(health_text, (10, 50))


   # Draw fact text
   if show_fact:
       fact_render = font.render(" "+show_fact+" ", True, (255, 255, 255), 'black')
       screen.blit(fact_render, (WIDTH//2 - fact_render.get_width()//2, HEIGHT - 50))


   pygame.display.flip()
   clock.tick(60)
