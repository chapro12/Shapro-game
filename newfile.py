import pygame
import sys
import random
import os

# Ініціалізація
pygame.init()

# Налаштування екрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("ШАПРО")

# --- КОЛЬОРИ ---
BLACK, WHITE = (5, 5, 10), (255, 255, 255)
RED, BLUE = (220, 20, 60), (0, 191, 255)      
YELLOW, GRAY, GREEN = (255, 215, 0), (50, 50, 60), (46, 204, 113)
ORANGE, PURPLE = (255, 140, 0), (150, 0, 255)
DARK_GRAY = (80, 80, 90) 
DARK_OVERLAY = (0, 0, 0, 160)

# --- СТВОРЕННЯ КОСМІЧНОГО ФОНУ ---
def create_nebula():
    nebula = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    nebula.fill((0, 0, 0, 0)) 
    for r in range(WIDTH // 2, 0, -2):
        alpha = int(30 * (1 - r / (WIDTH // 2)))
        pygame.draw.circle(nebula, (0, 100, 255, alpha), (0, HEIGHT), r)
    for r in range(WIDTH // 2, 0, -2):
        alpha = int(35 * (1 - r / (WIDTH // 2)))
        pygame.draw.circle(nebula, (120, 0, 255, alpha), (WIDTH, 0), r)
    return nebula

nebula_bg = create_nebula()
background_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
background_surface.fill(BLACK)
background_surface.blit(nebula_bg, (0, 0))
game_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
# === ГОТОВИЙ ФОН ДЛЯ СПОВІЛЬНЕННЯ ===
slow_background_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
slow_background_surface.fill((10, 10, 30))
slow_background_surface.blit(nebula_bg, (0, 0))

# Шрифти
font_main = pygame.font.SysFont("Arial", 100, bold=True)
font_small = pygame.font.SysFont("Arial", 35)

# --- СИСТЕМА ЗБЕРЕЖЕННЯ ---
HS_FILE, PROGRESS_FILE = "highscore.txt", "progress.txt"
BLUE_CR_FILE, PURPLE_CR_FILE = "blue_crystals.txt", "purple_crystals.txt"
LVL_SLOW_FILE, LVL_AMMO_FILE, LVL_SHIELD_FILE = "lvl_slow.txt", "lvl_ammo.txt", "lvl_shield.txt"
SKIN_CURRENT_FILE, SKIN_OWNED_FILE = "skin_current.txt", "skin_owned.txt"

def get_data(filename, default=0):
    if not os.path.exists(filename): return default
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if filename in [SKIN_CURRENT_FILE, SKIN_OWNED_FILE]: return content
            return int(content)
    except: return default
    
def save_data(filename, val):
    try:
        with open(filename, "w") as f: f.write(str(val))
    except: pass

lvl_slow = get_data(LVL_SLOW_FILE, 1)
lvl_ammo = get_data(LVL_AMMO_FILE, 1)
lvl_shield = get_data(LVL_SHIELD_FILE, 1)
def draw_sci_fi_panel(surface, rect, base_color, text, is_active=False):
    x, y, w, h = rect
    r = 20

    # 1. Легка підкладка-тінь (замість важкого циклу)
    bg_col_shadow = tuple(max(0, c - 40) for c in base_color)
    pygame.draw.rect(surface, bg_col_shadow, (x+3, y+3, w, h), border_radius=r)

    # 2. Основна плашка кнопки
    pygame.draw.rect(surface, base_color, (x, y, w, h), border_radius=r)

    # 3. Обводка кнопок
    if not is_active:
        light_col = tuple(min(255, c + 100) for c in base_color)
        pygame.draw.rect(surface, light_col, rect, 2, border_radius=r)
    else:
        pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=r)

    # 4. Текст із тінню
    txt_obj = font_small.render(text, True, (255, 255, 255))
    txt_obj_s = font_small.render(text, True, (0, 0, 0))
    surface.blit(txt_obj_s, (rect.centerx - txt_obj.get_width()//2 + 2, rect.centery - txt_obj.get_height()//2 + 2))
    surface.blit(txt_obj, (rect.centerx - txt_obj.get_width()//2, rect.centery - txt_obj.get_height()//2))
def draw_skin_button(surface, rect, title, status_text, skin_color, is_active=False):
    x, y, w, h = rect
    r = 15
    bg_col = (50, 50, 65) if not is_active else (35, 140, 75)
    pygame.draw.rect(surface, (20, 20, 25), (x+4, y+4, w, h), border_radius=r)
    pygame.draw.rect(surface, bg_col, rect, border_radius=r)
    border_col = (255, 255, 255) if is_active else (90, 90, 110)
    pygame.draw.rect(surface, border_col, rect, 2, border_radius=r)
    
    preview_rect = pygame.Rect(x + 25, y + h//2 - 25, 50, 50)
    pygame.draw.rect(surface, skin_color, preview_rect, border_radius=8)
    pygame.draw.rect(surface, (255, 255, 255), preview_rect, 1, border_radius=8)
    
    txt_title = font_small.render(title, True, (255, 255, 255))
    surface.blit(txt_title, (x + 100, y + 25))
    status_color = (255, 215, 0) if "АКТИВНО" in status_text else (185, 90, 235)
    txt_status = font_small.render(status_text, True, status_color)
    surface.blit(txt_status, (x + 100, y + h - 55))

def draw_sci_fi_icon(surface, rect, base_color, icon_type):
    x, y = rect.centerx + 130, rect.centery
    glow_col = tuple(min(255, c + 120) for c in base_color)
    
    for i in range(1, 4):
        icon_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        if icon_type == "const":
            # КОМПАНІЯ
            pts = [(10, 10), (25, 5), (35, 20), (20, 30)]
            pygame.draw.lines(icon_surface, (*glow_col, 150), True, pts, 2)
            for p in pts: pygame.draw.circle(icon_surface, (255, 255, 255), p, 3)
        elif icon_type == "garage":
            # ГАРАЖ
            for j in range(3): pygame.draw.rect(icon_surface, (*glow_col, 150), (10+j*8, 10, 5, 20))
        elif icon_type == "barn":
            # АНГАР
            pygame.draw.polygon(icon_surface, (*glow_col, 150), [(10, 25), (20, 10), (30, 25)])
        elif icon_type == "exit":
            # ВИХІД
            pygame.draw.circle(icon_surface, (*glow_col, 150), (20, 20), 10, 3)
            pygame.draw.rect(icon_surface, (255, 255, 255), (18, 10, 4, 10))
        
        surface.blit(icon_surface, (x - 20, y - 20))

# Складові системи скінів
current_skin = get_data(SKIN_CURRENT_FILE, "classic")
if type(current_skin) == int or current_skin == "1": current_skin = "classic"
owned_skins_data = get_data(SKIN_OWNED_FILE, "classic")
if type(owned_skins_data) == int: owned_skins_data = "classic"
owned_skins = str(owned_skins_data).split(",")

# --- СИСТЕМА ЗІРОК ---
stars_near, stars_far = [], []
for _ in range(40): stars_near.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(150, 250)])
for _ in range(60): stars_far.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(30, 80)])

def draw_stars(surface, dt):
    for s in stars_far:
        s[1] += s[2] * dt
        if s[1] > HEIGHT: s[1] = 0; s[0] = random.randint(0, WIDTH)
        pygame.draw.circle(surface, (100, 100, 120), (int(s[0]), int(s[1])), 1)
    for s in stars_near:
        s[1] += s[2] * dt
        if s[1] > HEIGHT: s[1] = 0; s[0] = random.randint(0, WIDTH)
        pygame.draw.circle(surface, (180, 180, 200), (int(s[0]), int(s[1])), 2)

# --- ТРЯСІННЯ ---
shake_intensity, shake_timer = 0, 0
def trigger_shake(intensity, duration):
    global shake_intensity, shake_timer
    shake_intensity, shake_timer = intensity, duration

# Стан гри
game_state, game_mode = "menu", "endless"
is_paused, score = False, 0
current_level = get_data(PROGRESS_FILE, 1)
blue_crystals, purple_crystals = get_data(BLUE_CR_FILE, 0), get_data(PURPLE_CR_FILE, 0)

# --- МЕХАНІКА СПОВІЛЬНЕННЯ ---
slow_motion_timer, wave_radius, wave_active = 0, 0, False
max_slow_duration = 2.0 + (lvl_slow - 1) * 1.0
current_s_mult = 1.0

# Гравець
p_size, p_speed = 60, 900
p_x, p_y = WIDTH // 2, HEIGHT // 3
current_shield_hp, ammo_count = 0, 0
MAX_AMMO = 30 + (lvl_ammo - 1) * 15
bullets, bullet_speed = [], 1300
shoot_delay, shoot_timer = 0.15, 0

# Об'єкти
enemies, powerups, particles, collect_sparks = [], [], [], []
e_speed_base, spawn_timer = 400, 0

# --- КЛАСИ БОСІВ ---
class RedBoss:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 100, -250, 200, 200)
        self.hp = 60; self.max_hp = 60; self.speed = 300; self.move_dir = 1
        self.projectiles = []
    def update(self, p_rect, dt, speed_mult):
        if self.rect.y < 120: self.rect.y += 120 * dt * speed_mult
        else:
            self.rect.x += self.speed * self.move_dir * dt * speed_mult
            if self.rect.right > WIDTH - 50 or self.rect.left < 50: self.move_dir *= -1
        if random.random() < 0.05 * speed_mult:
            self.projectiles.append(pygame.Rect(self.rect.centerx-20, self.rect.bottom, 40, 40))
        for p in self.projectiles[:]:
            p.y += 500 * dt * speed_mult
            if p.y > HEIGHT: self.projectiles.remove(p)

class YellowBoss:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 100, -250, 200, 200)
        self.hp = 90; self.max_hp = 90; self.speed = 350; self.move_dir = 1
        self.state = "IDLE"; self.dash_timer = 4.0; self.prep_timer = 1.2
        self.shake_off = 0; self.projectiles = []
    def update(self, p_rect, dt, speed_mult):
        for p in self.projectiles[:]:
            p.y += 700 * dt * speed_mult
            if p.y > HEIGHT: self.projectiles.remove(p)
        if self.state == "IDLE":
            if self.rect.y < 120: self.rect.y += 150 * dt * speed_mult
            else:
                self.rect.y = 120
                self.rect.x += self.speed * self.move_dir * dt * speed_mult
                if self.rect.right > WIDTH - 50 or self.rect.left < 50: self.move_dir *= -1
                if random.random() < 0.04 * speed_mult:
                    self.projectiles.append(pygame.Rect(self.rect.centerx-20, self.rect.bottom, 40, 40))
                self.dash_timer -= dt * speed_mult
                if self.dash_timer <= 0:
                    self.state = "PREPARING"; self.prep_timer = 1.2; trigger_shake(10, 1.2)
        elif self.state == "PREPARING":
            self.shake_off = random.randint(-10, 10)
            self.prep_timer -= dt * speed_mult
            if self.prep_timer <= 0: self.state = "DASHING"; self.shake_off = 0
        elif self.state == "DASHING":
            self.rect.y += 800 * dt * speed_mult
            if self.rect.y >= HEIGHT - 400: self.state = "RETREAT"
        elif self.state == "RETREAT":
            self.rect.y -= 150 * dt * speed_mult
            if self.rect.y <= 120: self.rect.y = 120; self.state = "IDLE"; self.dash_timer = 4.0

boss = None

# Керування
cx, base_y, btn_s = WIDTH // 2, HEIGHT - 350, 160
btn_up = pygame.Rect(cx - btn_s//2, base_y - btn_s - 30, btn_s, btn_s)
btn_down = pygame.Rect(cx - btn_s//2, base_y + 30, btn_s, btn_s)
btn_left = pygame.Rect(cx - btn_s*1.5 - 50, base_y, btn_s, btn_s)
btn_right = pygame.Rect(cx + btn_s//2 + 50, base_y, btn_s, btn_s)

def reset_game(mode, level=None):
    global p_x, p_y, enemies, powerups, particles, collect_sparks, score, current_shield_hp, ammo_count, MAX_AMMO, is_paused, boss, bullets, game_mode, current_level, slow_motion_timer, wave_active, max_slow_duration, lvl_ammo, lvl_slow, lvl_shield, current_s_mult
    game_mode = mode; p_x, p_y = WIDTH//2 - 30, HEIGHT//3
    enemies, powerups, particles, bullets, collect_sparks = [], [], [], [], []
    score = 0; is_paused = False; ammo_count = 0; current_shield_hp = 0
    slow_motion_timer = 0; wave_active = False; current_s_mult = 1.0
    
    MAX_AMMO = 30 + (lvl_ammo - 1) * 15
    max_slow_duration = 2.0 + (lvl_slow - 1) * 1.0
    if level is not None: current_level = level
    else: current_level = get_data(PROGRESS_FILE, 1)
    if game_mode == "campaign":
        if current_level == 5: boss = RedBoss()
        elif current_level >= 10: boss = YellowBoss()
        else: boss = None
    else: boss = None

def create_explosion(x, y, color):
    for _ in range(8): particles.append({"x": x, "y": y, "vx": random.uniform(-300, 300), "vy": random.uniform(-300, 300), "life": 0.5, "color": color})

def create_collect_sparks(x, y, color):
    for _ in range(6): collect_sparks.append({"pos": [x, y], "color": color, "speed": random.uniform(10, 20)})

# КНОПКИ ГОЛОВНОГО МЕНЮ
btn_w, btn_h = 400, 90
btn_endless_rect = pygame.Rect(WIDTH//2-btn_w//2, HEIGHT//2 - 210, btn_w, btn_h)
btn_campaign_rect = pygame.Rect(WIDTH//2-btn_w//2, HEIGHT//2 - 100, btn_w, btn_h)
btn_garage_rect = pygame.Rect(WIDTH//2-btn_w//2, HEIGHT//2 + 10, btn_w, btn_h)
btn_barn_rect = pygame.Rect(WIDTH//2-btn_w//2, HEIGHT//2 + 120, btn_w, btn_h)
btn_exit_rect = pygame.Rect(WIDTH//2-btn_w//2, HEIGHT//2 + 230, btn_w, btn_h)

btn_back_rect = pygame.Rect(40, 40, 200, 80)
btn_pause_rect = pygame.Rect(40, 40, 80, 80)
btn_resume_rect = pygame.Rect(WIDTH//2-200, HEIGHT//2-60, 400, 80)
btn_menu_rect = pygame.Rect(WIDTH//2-200, HEIGHT//2+60, 400, 80)

# КНОПКИ АНГАРА СКІНІВ
btn_skin_classic = pygame.Rect(WIDTH//2 - 250, 250, 500, 140)
btn_skin_triangle = pygame.Rect(WIDTH//2 - 250, 430, 500, 140)
btn_skin_comet = pygame.Rect(WIDTH//2 - 250, 610, 500, 140)

level_buttons = []
for i in range(10):
    row, col = i // 5, i % 5
    rect = pygame.Rect(WIDTH//2 - 350 + col*150, HEIGHT//2 - 100 + row*150, 120, 120)
    level_buttons.append((rect, i + 1))

shop_w, shop_h, shop_x = 600, 120, WIDTH // 2 - 300
btn_buy_ammo = pygame.Rect(shop_x, 250, shop_w, shop_h)
btn_buy_slow = pygame.Rect(shop_x, 400, shop_w, shop_h)
btn_buy_shield = pygame.Rect(shop_x, 550, shop_w, shop_h)

clock = pygame.time.Clock()
running = True
MAX_DT = 0.1 

# --- ГОЛОВНИЙ ЦИКЛ ГРИ ---
while running:
    raw_dt = clock.tick(60) / 1000.0 
    dt = min(raw_dt, MAX_DT)
    m_pos = pygame.mouse.get_pos()
    is_pressing = pygame.mouse.get_pressed()[0]
    
    # --- ЛОГІКА ПЛАВНОГО СПОВІЛЬНЕННЯ ---
    target_s_mult = 0.6 if slow_motion_timer > 0 else 1.0
    current_s_mult += (target_s_mult - current_s_mult) * 3.0 * dt
    s_mult = current_s_mult

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if game_state == "menu":
                if btn_endless_rect.collidepoint(mx, my): reset_game("endless"); game_state = "game"
                elif btn_campaign_rect.collidepoint(mx, my): game_state = "levels_menu"
                elif btn_garage_rect.collidepoint(mx, my): game_state = "garage"
                elif btn_barn_rect.collidepoint(mx, my): game_state = "barn"
                elif btn_exit_rect.collidepoint(mx, my): running = False
            elif game_state == "levels_menu":
                if btn_back_rect.collidepoint(mx, my): game_state = "menu"
                for rect, lvl_num in level_buttons:
                    if rect.collidepoint(mx, my) and lvl_num <= get_data(PROGRESS_FILE, 1):
                        reset_game("campaign", lvl_num); game_state = "game"
            elif game_state == "garage":
                if btn_back_rect.collidepoint(mx, my): game_state = "menu"
                if btn_buy_ammo.collidepoint(mx, my) and lvl_ammo < 5:
                    price = lvl_ammo * 50
                    if blue_crystals >= price:
                        blue_crystals -= price; lvl_ammo += 1; MAX_AMMO = 30 + (lvl_ammo - 1) * 15
                        save_data(BLUE_CR_FILE, blue_crystals); save_data(LVL_AMMO_FILE, lvl_ammo)
                elif btn_buy_slow.collidepoint(mx, my) and lvl_slow < 5:
                    price = lvl_slow * 30
                    if purple_crystals >= price:
                        purple_crystals -= price; lvl_slow += 1; max_slow_duration = 2.0 + (lvl_slow - 1) * 1.0
                        save_data(PURPLE_CR_FILE, purple_crystals); save_data(LVL_SLOW_FILE, lvl_slow)
                elif btn_buy_shield.collidepoint(mx, my) and lvl_shield < 2:
                    price = 150
                    if purple_crystals >= price:
                        purple_crystals -= price; lvl_shield += 1; save_data(PURPLE_CR_FILE, purple_crystals); save_data(LVL_SHIELD_FILE, lvl_shield)
            elif game_state == "barn":
                if btn_back_rect.collidepoint(mx, my): 
                    game_state = "menu"
                elif btn_skin_classic.collidepoint(mx, my):
                    current_skin = "classic"
                    with open(SKIN_CURRENT_FILE, "w") as f: f.write(current_skin)
                elif btn_skin_triangle.collidepoint(mx, my):
                    if "triangle" in owned_skins:
                        current_skin = "triangle"
                        with open(SKIN_CURRENT_FILE, "w") as f: f.write(current_skin)
                    elif blue_crystals >= 50:
                        blue_crystals -= 50
                        owned_skins.append("triangle")
                        current_skin = "triangle"
                        save_data(BLUE_CR_FILE, blue_crystals)
                        with open(SKIN_OWNED_FILE, "w") as f: f.write(",".join(owned_skins))
                        with open(SKIN_CURRENT_FILE, "w") as f: f.write(current_skin)
                elif btn_skin_comet.collidepoint(mx, my):
                    if "comet" in owned_skins:
                        current_skin = "comet"
                        with open(SKIN_CURRENT_FILE, "w") as f: f.write(current_skin)
                    elif purple_crystals >= 100:
                        purple_crystals -= 100
                        owned_skins.append("comet")
                        current_skin = "comet"
                        save_data(PURPLE_CR_FILE, purple_crystals)
                        with open(SKIN_OWNED_FILE, "w") as f: f.write(",".join(owned_skins))
                        with open(SKIN_CURRENT_FILE, "w") as f: f.write(current_skin)
            elif game_state == "game":
                if is_paused:
                    if btn_resume_rect.collidepoint(mx, my): is_paused = False
                    elif btn_menu_rect.collidepoint(mx, my): 
                        save_data(HS_FILE, max(int(score), get_data(HS_FILE))); game_state = "menu"
                elif btn_pause_rect.collidepoint(mx, my): is_paused = True
            elif game_state in ["game_over", "win"]: game_state = "menu"

    if shake_timer > 0:
        shake_timer -= dt
        if shake_timer <= 0: shake_intensity = 0

    if game_state == "game" and not is_paused:
        if slow_motion_timer > 0: slow_motion_timer -= dt
        if wave_active:
            wave_radius += 2000 * dt
            if wave_radius > WIDTH: wave_active = False

        p_rect = pygame.Rect(p_x, p_y, p_size, p_size)
        if is_pressing:
            moved = False
            if btn_left.collidepoint(m_pos) and p_x > 0: p_x -= p_speed * dt; moved = True
            if btn_right.collidepoint(m_pos) and p_x < WIDTH - p_size: p_x += p_speed * dt; moved = True
            if btn_up.collidepoint(m_pos) and p_y > 0: p_y -= p_speed * dt; moved = True
            if btn_down.collidepoint(m_pos) and p_y < HEIGHT - 550: p_y += p_speed * dt; moved = True
            if moved and ammo_count > 0:
                shoot_timer += dt
                if shoot_timer >= shoot_delay:
                    bullets.append(pygame.Rect(p_x + p_size//2 - 5, p_y, 10, 30))
                    ammo_count -= 1; shoot_timer = 0
        
        if game_mode == "endless": score += 8 * dt * s_mult
        
        for b in bullets[:]:
            b.y -= bullet_speed * dt
            hit = False
            if boss and b.colliderect(boss.rect):
                boss.hp -= 1; create_explosion(b.centerx, b.top, YELLOW); hit = True
                if boss.hp <= 0:
                    reward = 5 if isinstance(boss, RedBoss) else 10
                    purple_crystals += reward; save_data(PURPLE_CR_FILE, purple_crystals)
                    create_collect_sparks(boss.rect.centerx, boss.rect.centery, PURPLE)
                    if current_level >= get_data(PROGRESS_FILE, 1): save_data(PROGRESS_FILE, current_level + 1)
                    save_data(HS_FILE, max(int(score), get_data(HS_FILE))); boss = None
                    if current_level >= 10: game_state = "win"
                    else: game_state = "levels_menu"
            if not hit and boss and hasattr(boss, 'projectiles'):
                for bp in boss.projectiles[:]:
                    if b.colliderect(bp): create_explosion(bp.centerx, bp.centery, PURPLE); boss.projectiles.remove(bp); hit = True; break
            if not hit:
                for e in enemies[:]:
                    if b.colliderect(e["rect"]):
                        e["hp"] -= 1
                        if e["hp"] <= 0:
                            chance = random.random()
                            if e["col"] == RED and chance < 0.20: blue_crystals += 1; save_data(BLUE_CR_FILE, blue_crystals); create_collect_sparks(e["rect"].centerx, e["rect"].centery, BLUE)
                            elif e["col"] == YELLOW and chance < 0.35: blue_crystals += 1; save_data(BLUE_CR_FILE, blue_crystals); create_collect_sparks(e["rect"].centerx, e["rect"].centery, BLUE)
                            elif e["col"] == DARK_GRAY and chance < 0.15: purple_crystals += 1; save_data(PURPLE_CR_FILE, purple_crystals); create_collect_sparks(e["rect"].centerx, e["rect"].centery, PURPLE)
                            elif e["col"] == GREEN and chance < 0.80: purple_crystals += 1; save_data(PURPLE_CR_FILE, purple_crystals); create_collect_sparks(e["rect"].centerx, e["rect"].centery, GREEN)
                            create_explosion(e["rect"].centerx, e["rect"].centery, e["col"])
                            trigger_shake(8 if e["col"]==DARK_GRAY else 4, 0.15); enemies.remove(e)
                        else: create_explosion(b.centerx, b.top, YELLOW)
                        hit = True; break
            if hit or b.y < -50: 
                if b in bullets: bullets.remove(b)

        if boss:
            boss.update(p_rect, dt, s_mult)
            can_collide = not (isinstance(boss, YellowBoss) and boss.state == "RETREAT")
            if can_collide and boss.rect.colliderect(p_rect): 
                if current_shield_hp > 0: current_shield_hp -= 1; trigger_shake(10, 0.2); boss.rect.y -= 50
                else: game_state = "game_over"; save_data(HS_FILE, max(int(score), get_data(HS_FILE))); trigger_shake(20, 0.5)
            if hasattr(boss, 'projectiles'):
                for bp in boss.projectiles[:]:
                    if bp.colliderect(p_rect):
                        if current_shield_hp > 0: current_shield_hp -= 1; boss.projectiles.remove(bp)
                        else: game_state = "game_over"; save_data(HS_FILE, max(int(score), get_data(HS_FILE))); trigger_shake(20, 0.5)

        spawn_timer += dt
        if not boss and spawn_timer > 0.4:
            if game_mode == "endless":
                types = [1]
                if score >= 100: types.append(2)
                if score >= 150: types.append(3)
                if score >= 200: types.append(4) 
            else:
                types = [1] if current_level < 3 else ([1, 2] if current_level < 6 else [1, 2, 3])
            chosen = random.choice(types)
            if chosen == 1: enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH-70), -70, 70, 70), "col": RED, "f": False, "hp": 1, "type": "v"})
            elif chosen == 2: enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH-70), -70, 70, 70), "col": YELLOW, "f": True, "hp": 1, "type": "v"})
            elif chosen == 3: enemies.append({"rect": pygame.Rect(random.randint(0, WIDTH-100), -100, 100, 100), "col": DARK_GRAY, "f": False, "hp": 3, "type": "v"})
            elif chosen == 4: 
                side = random.choice([-70, WIDTH + 70])
                enemies.append({"rect": pygame.Rect(side, random.randint(100, 400), 70, 70), "col": GREEN, "f": False, "hp": 2, "type": "h", "dir": 1 if side < 0 else -1})
            spawn_timer = 0

        if random.random() < (0.002 if current_level <= 5 else 0.006):
            rand_val = random.random()
            p_type = "gun" if rand_val < 0.4 else ("shield" if rand_val < 0.7 else "slow")
            powerups.append({"rect": pygame.Rect(random.randint(0, WIDTH-40), -40, 40, 40), "type": p_type})
            
        for p in powerups[:]:
            p["rect"].y += 350 * dt * s_mult
            if p["rect"].colliderect(p_rect):
                if p["type"] == "shield": current_shield_hp = lvl_shield
                elif p["type"] == "gun": ammo_count = MAX_AMMO 
                elif p["type"] == "slow": slow_motion_timer = max_slow_duration; wave_active = True; wave_radius = 0
                powerups.remove(p)

        for e in enemies[:]:
            progression = current_level if game_mode=="campaign" else (int(score) // 300)
            spd = (e_speed_base + progression * 10) * (1.4 if e["f"] else 1.0)
            if e["col"] == DARK_GRAY: spd *= 0.6
            if e.get("type") == "h":
                e["rect"].x += spd * 1.2 * e["dir"] * dt * s_mult
                if (e["dir"] == 1 and e["rect"].left > WIDTH) or (e["dir"] == -1 and e["rect"].right < 0): enemies.remove(e); continue
            else:
                e["rect"].y += spd * dt * s_mult
                if e["rect"].top > HEIGHT: enemies.remove(e); continue
            if e["rect"].colliderect(p_rect):
                if current_shield_hp > 0: current_shield_hp -= 1; enemies.remove(e)
                else: game_state = "game_over"; save_data(HS_FILE, max(int(score), get_data(HS_FILE))); trigger_shake(20, 0.5)

        for part in particles[:]:
            part["x"] += part["vx"] * dt * s_mult; part["y"] += part["vy"] * dt * s_mult; part["life"] -= dt
            if part["life"] <= 0: particles.remove(part)

        for s in collect_sparks[:]:
            target_x, target_y = p_x + p_size // 2, p_y + p_size // 2
            dx, dy = target_x - s["pos"][0], target_y - s["pos"][1]; dist = (dx**2 + dy**2)**0.5
            if dist < 15: collect_sparks.remove(s)
            else: s["pos"][0] += (dx / dist) * s["speed"] * dt * 60 * s_mult; s["pos"][1] += (dy / dist) * s["speed"] * dt * 60 * s_mult

    # --- СЕКЦІЯ МАЛЮВАННЯ (РЕНДЕРИНГ) ---
    screen.fill(BLACK)
    off_x = random.uniform(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    off_y = random.uniform(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    
    if slow_motion_timer > 0:
        game_surface.blit(slow_background_surface, (0, 0))
    else:
        game_surface.blit(background_surface, (0, 0))
    
    if game_state == "menu":
        draw_stars(game_surface, dt)
        t = font_main.render("ШАПРО", True, WHITE); game_surface.blit(t, (WIDTH//2-t.get_width()//2, HEIGHT//8))
        hs_text = font_small.render(f"РЕКОРД: {get_data(HS_FILE, 0)}", True, YELLOW); game_surface.blit(hs_text, (WIDTH//2-hs_text.get_width()//2, HEIGHT//8 + 120))
        # === ОСЬ ЦІ ЧОТИРИ РЯДКИ ПРОСТО ВСТАВ СЮДИ ===
        txt_blue = font_small.render(f"СИНІ: {blue_crystals}", True, BLUE)
        txt_purple = font_small.render(f"ФІОЛ.: {purple_crystals}", True, PURPLE)
        game_surface.blit(txt_blue, (WIDTH - txt_blue.get_width() - 40, 40))
        game_surface.blit(txt_purple, (WIDTH - txt_purple.get_width() - 40, 90))
        game_surface.blit(txt_blue, (WIDTH - txt_blue.get_width() - 40, 40))
        game_surface.blit(txt_purple, (WIDTH - txt_purple.get_width() - 40, 90))
        # --- МАЛЮВАННЯ НОВИХ КНОПОК МЕНЮ ---
        m_pos = pygame.mouse.get_pos()

        # 1. НЕСКІНЧЕННО (Синій)
        is_end = btn_endless_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_endless_rect, BLUE, "НЕСКІНЧЕННО", is_end)

        # 2. КОМПАНІЯ (Зелений)
        is_comp = btn_campaign_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_campaign_rect, GREEN, "КОМПАНІЯ", is_comp)
        draw_sci_fi_icon(game_surface, btn_campaign_rect, GREEN, "const")

        # 3. ГАРАЖ (Сірий)
        is_gar = btn_garage_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_garage_rect, GRAY, "ГАРАЖ", is_gar)
        draw_sci_fi_icon(game_surface, btn_garage_rect, GRAY, "garage")

        # 4. АНГАР СКІНІВ (Пурпурний)
        is_bar = btn_barn_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_barn_rect, PURPLE, "АНГАР СКІНІВ", is_bar)
        draw_sci_fi_icon(game_surface, btn_barn_rect, PURPLE, "barn")

        # 5. ВИХІД (Червоний)
        is_exit = btn_exit_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_exit_rect, RED, "ВИХІД", is_exit)
        draw_sci_fi_icon(game_surface, btn_exit_rect, RED, "exit")
    
    elif game_state == "levels_menu":
        draw_stars(game_surface, dt)
        t = font_main.render("РІВНІ", True, WHITE); game_surface.blit(t, (WIDTH//2-t.get_width()//2, 50))
        unlocked = get_data(PROGRESS_FILE, 1)
        for rect, lvl_num in level_buttons:
            col = GREEN if lvl_num <= unlocked else GRAY
            pygame.draw.rect(game_surface, col, rect, border_radius=15); pygame.draw.rect(game_surface, WHITE, rect, 2, border_radius=15)
            num_t = font_small.render(str(lvl_num), True, WHITE); game_surface.blit(num_t, (rect.centerx - num_t.get_width()//2, rect.centery - num_t.get_height()//2))
        pygame.draw.rect(game_surface, RED, btn_back_rect, border_radius=20); bt = font_small.render("НАЗАД", True, WHITE); game_surface.blit(bt, (btn_back_rect.centerx-bt.get_width()//2, btn_back_rect.centery-15))

    elif game_state == "garage":
        draw_stars(game_surface, dt)
        
        # 1. Заголовок
        t = font_main.render("ГАРАЖ", True, WHITE)
        game_surface.blit(t, (250, 45))
        
        # 2. Кнопка НАЗАД
        m_pos = pygame.mouse.get_pos()
        is_back_hover = btn_back_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_back_rect, RED, "НАЗАД", is_back_hover)
        
        # 3. Список товарів
        items = [
            (btn_buy_ammo, "ЗАПАС ПАТРОНІВ", lvl_ammo, 5, lvl_ammo*50, BLUE),
            (btn_buy_slow, "СПОВІЛЬНЕННЯ", lvl_slow, 5, lvl_slow*30, PURPLE),
            (btn_buy_shield, "ПОТУЖНІСТЬ ЩИТА", lvl_shield, 2, 150, PURPLE)
        ]
        
        # 4. Один єдиний правильний цикл малювання
        for rect, name, lvl, m_lvl, price, c_col in items:
            is_max = lvl >= m_lvl
            is_hover = rect.collidepoint(m_pos)
            
            # Визначаємо колір основи
            base_button_color = (40, 40, 45) if is_max else (55, 55, 70)
            
            # Малюємо об'ємну кнопку через функцію (текст передаємо порожній "")
            draw_sci_fi_panel(game_surface, rect, base_button_color, "", is_hover)
            
            # Накладаємо текст двома рядками поверх плашки
            txt_n = font_small.render(f"{name} (Рівень {lvl})", True, WHITE)
            game_surface.blit(txt_n, (rect.centerx - txt_n.get_width()//2, rect.y + 20))
            
            status_str = "MAX" if is_max else f"КУПИТИ ЗА {price}"
            status_color = (255, 215, 0) if is_max else c_col
            txt_p = font_small.render(status_str, True, status_color)
            game_surface.blit(txt_p, (rect.centerx - txt_p.get_width()//2, rect.y + rect.height - 45))
            
        # 5. Кристали в самому низу екрана
        txt_blue = font_small.render(f"СИНІ: {blue_crystals}", True, BLUE)
        txt_purple = font_small.render(f"ФІОЛ.: {purple_crystals}", True, PURPLE)
        game_surface.blit(txt_blue, (WIDTH//2 - txt_blue.get_width()//2, HEIGHT - 110))
        game_surface.blit(txt_purple, (WIDTH//2 - txt_purple.get_width()//2, HEIGHT - 65))

    # Прямо після кристалів має йти Ангар, без жодних зайвих ліній!
    
    elif game_state == "barn":
        draw_stars(game_surface, dt)
        
        # 1. Заголовок (підняли в самий верх і зробили коротшим)
        t = font_main.render("АНГАР", True, WHITE)
        game_surface.blit(t, (WIDTH//2 - t.get_width()//250, 45))
        
        # 2. Кнопка НАЗАД (малюється на своєму місці)
        m_pos = pygame.mouse.get_pos()
        is_back_hover = btn_back_rect.collidepoint(m_pos)
        draw_sci_fi_panel(game_surface, btn_back_rect, RED, "НАЗАД", is_back_hover)
        
        # 3. Лічильники кристалів переносимо в САМИЙ НИЗ (HEIGHT - 100 та HEIGHT - 60)
        txt_blue = font_small.render(f"СИНІ: {blue_crystals}", True, BLUE)
        txt_purple = font_small.render(f"ФІОЛ.: {purple_crystals}", True, PURPLE)
        game_surface.blit(txt_blue, (WIDTH//2 - txt_blue.get_width()//2, HEIGHT - 110))
        game_surface.blit(txt_purple, (WIDTH//2 - txt_purple.get_width()//2, HEIGHT - 65))
        
        # 4. МАЛЮВАННЯ КНОПОК СКІНІВ (Тільки через нову функцію!)
        # Скін 1: КВАДРАТ
        is_classic_active = (current_skin == "classic")
        classic_status = "АКТИВНО" if is_classic_active else "ВИБРАТИ"
        draw_skin_button(game_surface, btn_skin_classic, "КВАДРАТ (СТАНДАРТ)", classic_status, WHITE, is_classic_active)
        
        # Скін 2: ТРИКУТНИК
        is_triangle_active = (current_skin == "triangle")
        triangle_status = "АКТИВНО" if is_triangle_active else "ВИБРАТИ"
        draw_skin_button(game_surface, btn_skin_triangle, "ТРИКУТНИК", triangle_status, BLUE, is_triangle_active)
        
        # Скін 3: КОМЕТА
        btn_skin_comet = pygame.Rect(btn_skin_triangle.x, btn_skin_triangle.y + 170, btn_skin_triangle.width, btn_skin_triangle.height)
        is_comet_active = (current_skin == "comet")
        
        # Перевірка, чи відкрита комета
        try:
            comet_owned = comet_owned  # використовуємо твою змінну, якщо вона створена вище
        except:
            comet_owned = False
            
        comet_status = "АКТИВНО" if is_comet_active else ("ВИБРАТИ" if comet_owned else "КУПИТИ ЗА 100 ФІОЛ.")
        draw_skin_button(game_surface, btn_skin_comet, "КОМЕТА (ЖОВТИЙ КУБ)", comet_status, YELLOW, is_comet_active)

    elif game_state == "game":
        draw_stars(game_surface, dt * s_mult)
        if wave_active: pygame.draw.circle(game_surface, ORANGE, (int(p_x + p_size//2), int(p_y + p_size//2)), int(wave_radius), 5)
        for b in bullets: pygame.draw.rect(game_surface, YELLOW, b, border_radius=5)
        
        # --- МАЛЮВАННЯ ГРАВЦЯ ЗАЛЕЖНО ВІД СКІНУ ---
        if current_skin == "classic":
            pygame.draw.rect(game_surface, WHITE, (p_x, p_y, p_size, p_size), border_radius=12)
        elif current_skin == "triangle":
            pygame.draw.polygon(game_surface, BLUE, [(p_x + p_size//2, p_y), (p_x, p_y + p_size), (p_x + p_size, p_y + p_size)])
        elif current_skin == "comet":
            if random.random() < 0.4:
                particles.append({"x": p_x + p_size//2, "y": p_y + p_size, "vx": random.uniform(-40, 40), "vy": random.uniform(100, 200), "life": 0.3, "color": ORANGE})
            pygame.draw.rect(game_surface, YELLOW, (p_x, p_y, p_size, p_size), border_radius=6)

        if ammo_count > 0: pygame.draw.rect(game_surface, ORANGE, (p_x, p_y + p_size + 10, p_size * (ammo_count / MAX_AMMO), 8))
        if current_shield_hp > 0: pygame.draw.rect(game_surface, BLUE if current_shield_hp == 1 else (0, 255, 255), (p_x-8, p_y-8, p_size+16, p_size+16), 4, 15)
        if boss:
            if isinstance(boss, YellowBoss):
                bc = YELLOW if boss.state == "IDLE" else (WHITE if boss.state in ["PREPARING", "DASHING"] else GRAY)
                dr = boss.rect.copy()
                if boss.state == "PREPARING": dr.x += boss.shake_off
                pygame.draw.rect(game_surface, bc, dr, border_radius=20); pygame.draw.rect(game_surface, GREEN, (dr.x, dr.y-30, 200*(boss.hp/boss.max_hp), 15))
            else:
                pygame.draw.rect(game_surface, RED, boss.rect, border_radius=20); pygame.draw.rect(game_surface, GREEN, (boss.rect.x, boss.rect.y-30, 200*(boss.hp/boss.max_hp), 15))
            for bp in boss.projectiles: pygame.draw.rect(game_surface, PURPLE, bp, border_radius=5)
        for e in enemies: pygame.draw.rect(game_surface, e["col"], e["rect"], border_radius=8)
        for p in powerups: pygame.draw.rect(game_surface, BLUE if p["type"]=="shield" else (ORANGE if p["type"]=="slow" else YELLOW), p["rect"], border_radius=10)
        for part in particles: pygame.draw.circle(game_surface, part["color"], (int(part["x"]), int(part["y"])), 4)
        for s in collect_sparks: pygame.draw.circle(game_surface, s["color"], (int(s["pos"][0]), int(s["pos"][1])), 5)
        screen.blit(game_surface, (off_x, off_y)) 
        for b, s in [(btn_up, "^"), (btn_down, "v"), (btn_left, "<"), (btn_right, ">")]:
            pygame.draw.rect(screen, GRAY, b, border_radius=40); pygame.draw.rect(screen, WHITE, b, 2, border_radius=40)
            st = font_small.render(s, True, WHITE); screen.blit(st, (b.centerx-st.get_width()//2, b.centery-st.get_height()//2))
        pygame.draw.circle(screen, GRAY, btn_pause_rect.center, 40); pygame.draw.circle(screen, WHITE, btn_pause_rect.center, 40, 2)
        pygame.draw.rect(screen, WHITE, (btn_pause_rect.centerx-12, btn_pause_rect.centery-15, 8, 30)); pygame.draw.rect(screen, WHITE, (btn_pause_rect.centerx+4, btn_pause_rect.centery-15, 8, 30))
        header = f"РІВЕНЬ {current_level}" if game_mode=="campaign" else f"РАХУНОК: {int(score)}"
        screen.blit(font_small.render(header, True, WHITE), (WIDTH//2-50, 30))
        if slow_motion_timer > 0: pygame.draw.rect(screen, ORANGE, (0, 0, WIDTH * (slow_motion_timer / max_slow_duration), 15))
        if is_paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill(DARK_OVERLAY); screen.blit(overlay, (0,0))
            pygame.draw.rect(screen, BLUE, btn_resume_rect, border_radius=20); pygame.draw.rect(screen, RED, btn_menu_rect, border_radius=20)
            screen.blit(font_small.render("ПРОДОВЖИТИ", True, WHITE), (btn_resume_rect.centerx-100, btn_resume_rect.centery-15)); screen.blit(font_small.render("В МЕНЮ", True, WHITE), (btn_menu_rect.centerx-55, btn_menu_rect.centery-15))
    
    elif game_state in ["game_over", "win"]:
        screen.blit(game_surface, (off_x, off_y))
        msg = "ГРА ЗАКІНЧЕНА" if game_state == "game_over" else "ПЕРЕМОГА!"
        t = font_main.render(msg, True, RED if game_state=="game_over" else GREEN); screen.blit(t, (WIDTH//2-t.get_width()//2, HEIGHT//2-50))
        
    if game_state in ["menu", "garage", "levels_menu", "barn"]: screen.blit(game_surface, (off_x, off_y))
    pygame.display.flip()

pygame.quit()