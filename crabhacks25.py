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

# --- Paths ---
BASE_PATH = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_PATH, "Image")
# Prefer using the workspace `Image/` folder. Keep old program paths as fallback.
CRAB_PATH = os.path.join(IMAGE_DIR, "CrabWithBottleCapRight")
CRAB_PATH_LEFT = os.path.join(IMAGE_DIR, "CrabWithBottleCapLeft")
HAZARD_CANDIDATES = ["CatFishLeft", "CatFishRight", "Shell", "GreenCrab", "CheeringCrab"]
OBJECT_PATH = os.path.join(IMAGE_DIR, "Plastic")
MUSIC_PATH = os.path.join(BASE_PATH, "programs/crabhacks 2025/background_music.wav")
START_BG_PATH = os.path.join(IMAGE_DIR, "Water")

# --- Load music ---
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)

# --- Load crab frames ---
def load_frames_from_dir(dir_path, size=None, convert_alpha=True):
    frames = []
    if not os.path.isdir(dir_path):
        return frames
    files = sorted([f for f in os.listdir(dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    for fname in files:
        path = os.path.join(dir_path, fname)
        try:
            img = pygame.image.load(path)
            img = img.convert_alpha() if convert_alpha else img.convert()
            if size is not None:
                img = pygame.transform.scale(img, size)
            frames.append(img)
        except Exception as e:
            print("Failed to load image:", path, e)
    return frames

# Attempt to load crab frames from Image directory first, fallback if empty
crab_frames = load_frames_from_dir(CRAB_PATH, size=(crab_size, crab_size))
if not crab_frames:
    # try left folder and flip as needed
    left_frames = load_frames_from_dir(CRAB_PATH_LEFT, size=(crab_size, crab_size))
    if left_frames:
        crab_frames = [pygame.transform.flip(f, True, False) for f in left_frames]
    else:
        # fallback to old location if present (older project layout)
        old_crab = os.path.join(BASE_PATH, "programs/crabhacks 2025/CrabWithBottleCap")
        crab_frames = load_frames_from_dir(old_crab, size=(crab_size, crab_size))

if not crab_frames:
    raise SystemExit("No crab frames found. Make sure your images are in Image/CrabWithBottleCapRight or Image/CrabWithBottleCapLeft")

current_frame = 0
frame_timer = 0
animation_speed = 0.15

# --- Load start screen frames ---
# --- Load start screen frames ---
start_frames = load_frames_from_dir(START_BG_PATH, size=(WIDTH, HEIGHT), convert_alpha=False)
if not start_frames:
    # fallback: try old path
    old_start = os.path.join(BASE_PATH, "programs/crabhacks 2025/Water")
    start_frames = load_frames_from_dir(old_start, size=(WIDTH, HEIGHT), convert_alpha=False)
if not start_frames:
    # create a single blank background to avoid crash
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((173, 216, 230))
    start_frames = [surf]

# --- Hazards with variable frame counts ---
# --- Hazards: load from subfolders in Image/ when available ---
hazard_frames = []
hazard_rects = []
hazard_current_frames = []
hazard_timers = []
hazard_animation_speeds = []

for candidate in HAZARD_CANDIDATES:
    folder = os.path.join(IMAGE_DIR, candidate)
    frames = load_frames_from_dir(folder, size=(50, 50))
    if frames:
        hazard_frames.append(frames)
        rect = frames[0].get_rect()
        rect.topleft = (random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50))
        hazard_rects.append(rect)
        hazard_current_frames.append(0)
        hazard_timers.append(0)
        hazard_animation_speeds.append(0.1)

if not hazard_frames:
    # fallback: try old Hazards folder layout
    old_hazard = os.path.join(BASE_PATH, "programs/crabhacks 2025/Hazards")
    if os.path.isdir(old_hazard):
        files = sorted([f for f in os.listdir(old_hazard) if f.lower().endswith('.png')])
        if files:
            # crude single-hazard fallback: load any matching files
            frames = []
            for f in files:
                path = os.path.join(old_hazard, f)
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.scale(img, (50, 50))
                    frames.append(img)
                except Exception:
                    pass
            if frames:
                hazard_frames.append(frames)
                rect = frames[0].get_rect()
                rect.topleft = (random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50))
                hazard_rects.append(rect)
                hazard_current_frames.append(0)
                hazard_timers.append(0)
                hazard_animation_speeds.append(0.1)

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
    animation_speed = 0.15  # adjust for faster/slower animation

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


# def win_screen():
#     # Load win background frames (WinLose folder)
#     win_bg = load_frames_from_dir(os.path.join(IMAGE_DIR, "WinLose"), size=(WIDTH, HEIGHT), convert_alpha=False)
#     if not win_bg:
#         # fallback to a simple filled screen
#         surf = pygame.Surface((WIDTH, HEIGHT))
#         surf.fill((255, 223, 186))
#         win_bg = [surf]

#     # Load cheering crab animation (if present)
#     cheer_frames = load_frames_from_dir(os.path.join(IMAGE_DIR, "CheeringCrab"), size=(crab_size, crab_size))
#     # Load a shell image to display on win screen (optional)
#     shell_frames = load_frames_from_dir(os.path.join(IMAGE_DIR, "Shell"), size=(80, 80))

#     bg_idx = 0
#     bg_timer = 0
#     bg_speed = 0.12

#     cheer_idx = 0
#     cheer_timer = 0
#     cheer_speed = 0.15

#     shell_y = HEIGHT
#     shell_target_y = HEIGHT//2 + 60

#     while True:
#         bg_timer += bg_speed
#         if bg_timer >= 1:
#             bg_timer = 0
#             bg_idx = (bg_idx + 1) % len(win_bg)

#         cheer_timer += cheer_speed
#         if cheer_timer >= 1 and cheer_frames:
#             cheer_timer = 0
#             cheer_idx = (cheer_idx + 1) % len(cheer_frames)

#         # simple shell float-in animation
#         if shell_frames and shell_y > shell_target_y:
#             shell_y -= 4

#         screen.blit(win_bg[bg_idx], (0, 0))

#         # draw shell (centered)
#         if shell_frames:
#             s_img = shell_frames[0]
#             s_rect = s_img.get_rect(center=(WIDTH//2 - 80, shell_y))
#             screen.blit(s_img, s_rect)

#         # draw cheering crab (center)
#         if cheer_frames:
#             c_img = cheer_frames[cheer_idx]
#             c_rect = c_img.get_rect(center=(WIDTH//2 + 80, HEIGHT//2))
#             screen.blit(c_img, c_rect)

#         # win text
#         win_font = pygame.font.SysFont(None, 72)
#         text = win_font.render("You Win!", True, (0, 100, 0))
#         screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)):
#                 # Exit game after clicking or pressing return/space on win screen
#                 pygame.quit()
#                 sys.exit()

start_screen()

# --- Main game loop ---
show_fact = ""
fact_timer = 0  # timer to show fact temporarily

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
    for i in range(len(hazard_frames)):
        hazard_timers[i] += hazard_animation_speeds[i]
        if hazard_timers[i] >= 1:
            hazard_timers[i] = 0
            hazard_current_frames[i] = (hazard_current_frames[i] + 1) % len(hazard_frames[i])

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
            # remove collected object; when all collected, trigger win
            try:
                objects.remove(obj)
            except ValueError:
                pass
            if not objects:
                win_screen()

    if fact_timer > 0:
        fact_timer -= 1
    else:
        show_fact = ""

    # --- Check game over ---
    if crab_health <= 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # --- Drawing ---
    screen.fill((173, 216, 230))  # background

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

    # Draw health bar
    for i in range(crab_health):
        pygame.draw.rect(screen, (255, 0, 0), (10 + i*35, 10, 30, 30))

    # Draw health text
    health_text = font.render(f"Health: {crab_health}/{max_health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 50))

    # Draw fact text
    if show_fact:
        fact_render = font.render(" "+show_fact+" ", True, (0, 0, 128), 'black')
        screen.blit(fact_render, (WIDTH//2 - fact_render.get_width()//2, HEIGHT - 50))

    pygame.display.flip()
    clock.tick(60)
