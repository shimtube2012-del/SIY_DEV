import pygame
import random
import math

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("공 튀기기 추첨 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 80, 80)
ORANGE = (255, 165, 0)
YELLOW = (255, 230, 100)
GREEN = (100, 255, 100)
BLUE = (100, 150, 255)
PURPLE = (200, 100, 255)
PINK = (255, 150, 200)
CYAN = (100, 255, 255)
GOLD = (255, 215, 0)
BROWN = (139, 90, 43)
DARK_BROWN = (100, 60, 30)

BALL_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, CYAN]

# 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_large = pygame.font.Font(font_path, 52)
font_medium = pygame.font.Font(font_path, 32)
font_small = pygame.font.Font(font_path, 24)
font_tiny = pygame.font.Font(font_path, 18)
font_countdown = pygame.font.Font(font_path, 100)

# 게임 영역 설정
GAME_LEFT = 50
GAME_RIGHT = SCREEN_WIDTH - 50
GAME_TOP = 100
GAME_BOTTOM = 620

# 깔때기 설정
FUNNEL_TOP_WIDTH = 180
FUNNEL_BOTTOM_WIDTH = 45
FUNNEL_HEIGHT = 120
FUNNEL_X = SCREEN_WIDTH // 2
FUNNEL_TOP_Y = GAME_BOTTOM
FUNNEL_BOTTOM_Y = FUNNEL_TOP_Y + FUNNEL_HEIGHT

# 속도 제한
MAX_SPEED = 15

# 장애물(못) 클래스
class Peg:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.hit = False
        self.hit_timer = 0

    def draw(self, surface):
        color = ORANGE if self.hit else BROWN
        pygame.draw.circle(surface, DARK_BROWN, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x - 3), int(self.y - 3)), 3)

        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hit = False

# 기울어진 장애물 클래스
class Platform:
    def __init__(self, x1, y1, x2, y2, thickness=10):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.thickness = thickness

    def collide(self, ball):
        px = ball.x - self.x1
        py = ball.y - self.y1
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        length_sq = dx**2 + dy**2
        if length_sq == 0:
            return False

        t = max(0, min(1, (px * dx + py * dy) / length_sq))
        closest_x = self.x1 + t * dx
        closest_y = self.y1 + t * dy

        dist_x = ball.x - closest_x
        dist_y = ball.y - closest_y
        dist = math.sqrt(dist_x**2 + dist_y**2)

        if dist < ball.radius + self.thickness / 2 and dist > 0:
            nx = dist_x / dist
            ny = dist_y / dist
            dot = ball.dx * nx + ball.dy * ny
            if dot < 0:
                ball.dx -= 2 * dot * nx * ball.bounce
                ball.dy -= 2 * dot * ny * ball.bounce
                overlap = ball.radius + self.thickness / 2 - dist
                ball.x += nx * overlap
                ball.y += ny * overlap
                ball.dx += random.uniform(-0.3, 0.3)
            return True
        return False

    def draw(self, surface):
        pygame.draw.line(surface, DARK_BROWN, (self.x1, self.y1), (self.x2, self.y2), self.thickness + 4)
        pygame.draw.line(surface, BROWN, (self.x1, self.y1), (self.x2, self.y2), self.thickness)

# 회전 장애물 클래스
class Spinner:
    def __init__(self, x, y, length, speed):
        self.x = x
        self.y = y
        self.length = length
        self.angle = random.uniform(0, math.pi * 2)
        self.speed = speed
        self.thickness = 8

    def update(self):
        self.angle += self.speed

    def collide(self, ball):
        # 회전 막대의 양 끝점 계산
        x1 = self.x + math.cos(self.angle) * self.length
        y1 = self.y + math.sin(self.angle) * self.length
        x2 = self.x - math.cos(self.angle) * self.length
        y2 = self.y - math.sin(self.angle) * self.length

        # 선분과 공의 충돌 검사
        px = ball.x - x1
        py = ball.y - y1
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx**2 + dy**2
        if length_sq == 0:
            return

        t = max(0, min(1, (px * dx + py * dy) / length_sq))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        dist_x = ball.x - closest_x
        dist_y = ball.y - closest_y
        dist = math.sqrt(dist_x**2 + dist_y**2)

        if dist < ball.radius + self.thickness / 2 and dist > 0:
            nx = dist_x / dist
            ny = dist_y / dist
            # 회전 방향으로 힘 추가
            ball.dx += nx * 3 + self.speed * 20
            ball.dy += ny * 2
            overlap = ball.radius + self.thickness / 2 - dist
            ball.x += nx * overlap
            ball.y += ny * overlap

    def draw(self, surface):
        x1 = self.x + math.cos(self.angle) * self.length
        y1 = self.y + math.sin(self.angle) * self.length
        x2 = self.x - math.cos(self.angle) * self.length
        y2 = self.y - math.sin(self.angle) * self.length
        pygame.draw.line(surface, DARK_GRAY, (x1, y1), (x2, y2), self.thickness + 4)
        pygame.draw.line(surface, PURPLE, (x1, y1), (x2, y2), self.thickness)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 6)

# 바운스 패드 클래스
class BouncePad:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 12
        self.active = False
        self.active_timer = 0

    def collide(self, ball):
        if (self.x - self.width/2 < ball.x < self.x + self.width/2 and
            self.y - self.height < ball.y + ball.radius < self.y + self.height):
            if ball.dy > 0:
                ball.dy = -abs(ball.dy) * 1.5 - 5
                ball.dx += random.uniform(-3, 3)
                self.active = True
                self.active_timer = 10
                return True
        return False

    def update(self):
        if self.active:
            self.active_timer -= 1
            if self.active_timer <= 0:
                self.active = False

    def draw(self, surface):
        color = YELLOW if self.active else GREEN
        rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        pygame.draw.rect(surface, DARK_GRAY, rect, border_radius=5)
        pygame.draw.rect(surface, color, (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4), border_radius=4)

# 파티클 클래스 (당첨 연출용)
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-8, -1)
        self.gravity = 0.15
        self.max_lifetime = random.randint(40, 80)
        self.lifetime = self.max_lifetime
        self.radius = random.randint(3, 7)

    def update(self):
        self.dy += self.gravity
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface):
        factor = max(0, self.lifetime / self.max_lifetime)
        r, g, b = self.color
        color = (int(r * factor), int(g * factor), int(b * factor))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.radius * factor)))

# 공 클래스
class Ball:
    def __init__(self, name, color, start_x, start_y=None):
        self.name = name
        self.color = color
        self.radius = 16
        self.start_x = start_x
        self.start_y = start_y if start_y is not None else GAME_TOP + 25
        self.reset_position()

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.dx = 0
        self.dy = 0
        self.gravity = 0.4
        self.friction = 0.995
        self.bounce = 0.7
        self.finished = False
        self.winner = False
        self.pulse = 0
        self.stuck_count = 0
        self.last_x = self.x
        self.last_y = self.y
        self.stuck_timer = 0

    def move(self, pegs, platforms, spinners, bounce_pads, balls, game_started, maze_broken):
        if self.finished:
            return

        if not game_started:
            return

        self.dy += self.gravity
        self.dx *= self.friction

        # 속도 제한 (관통 방지)
        self.dx = max(-MAX_SPEED, min(MAX_SPEED, self.dx))
        self.dy = max(-MAX_SPEED, min(MAX_SPEED, self.dy))

        self.x += self.dx
        self.y += self.dy

        # 벽 충돌
        if self.x <= GAME_LEFT + self.radius:
            self.x = GAME_LEFT + self.radius
            self.dx = abs(self.dx) * self.bounce
        elif self.x >= GAME_RIGHT - self.radius:
            self.x = GAME_RIGHT - self.radius
            self.dx = -abs(self.dx) * self.bounce

        if self.y <= GAME_TOP + self.radius:
            self.y = GAME_TOP + self.radius
            self.dy = abs(self.dy) * self.bounce

        # 미로가 깨지지 않았을 때만 장애물 충돌 처리
        if not maze_broken:
            # 못 충돌
            for peg in pegs:
                dx = self.x - peg.x
                dy = self.y - peg.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < self.radius + peg.radius and dist > 0:
                    nx = dx / dist
                    ny = dy / dist
                    dot = self.dx * nx + self.dy * ny
                    self.dx = (self.dx - 2 * dot * nx) * self.bounce
                    self.dy = (self.dy - 2 * dot * ny) * self.bounce
                    self.dx += random.uniform(-1.5, 1.5)
                    overlap = self.radius + peg.radius - dist
                    self.x += nx * overlap
                    self.y += ny * overlap
                    peg.hit = True
                    peg.hit_timer = 15

            # 플랫폼 충돌
            for platform in platforms:
                platform.collide(self)

            # 회전 장애물 충돌
            for spinner in spinners:
                spinner.collide(self)

            # 바운스 패드 충돌
            for pad in bounce_pads:
                pad.collide(self)

            # 갇힘 감지: X+Y 총 이동거리로 판단
            total_movement = abs(self.x - self.last_x) + abs(self.y - self.last_y)
            if total_movement < 3:
                self.stuck_timer += 1
                if self.stuck_timer >= 30:
                    self.stuck_count += 1
                    self.stuck_timer = 0
            else:
                self.stuck_timer = 0

            self.last_x = self.x
            self.last_y = self.y

        # 깔때기 영역
        if self.y + self.radius > FUNNEL_TOP_Y:
            progress = (self.y - FUNNEL_TOP_Y) / FUNNEL_HEIGHT
            progress = max(0, min(1, progress))
            current_width = FUNNEL_TOP_WIDTH - (FUNNEL_TOP_WIDTH - FUNNEL_BOTTOM_WIDTH) * progress
            left_edge = FUNNEL_X - current_width / 2
            right_edge = FUNNEL_X + current_width / 2

            if self.x < left_edge - 10 or self.x > right_edge + 10:
                if self.y + self.radius > FUNNEL_TOP_Y:
                    self.y = FUNNEL_TOP_Y - self.radius
                    self.dy = -abs(self.dy) * self.bounce * 0.5
                    if self.x < FUNNEL_X:
                        self.dx += 3
                    else:
                        self.dx -= 3
            else:
                if self.x - self.radius < left_edge:
                    self.x = left_edge + self.radius
                    self.dx = abs(self.dx) * 0.3 + 2
                elif self.x + self.radius > right_edge:
                    self.x = right_edge - self.radius
                    self.dx = -abs(self.dx) * 0.3 - 2

        if self.y > FUNNEL_BOTTOM_Y + 30:
            self.finished = True

        # 다른 공과 충돌
        for other in balls:
            if other is not self and not other.finished:
                self.collide_with(other)

    def collide_with(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.radius + other.radius and dist > 0:
            nx = dx / dist
            ny = dy / dist
            dvx = self.dx - other.dx
            dvy = self.dy - other.dy
            dvn = dvx * nx + dvy * ny

            if dvn > 0:
                self.dx -= dvn * nx * 0.5
                self.dy -= dvn * ny * 0.5
                other.dx += dvn * nx * 0.5
                other.dy += dvn * ny * 0.5

            overlap = (self.radius + other.radius - dist) / 2
            self.x -= nx * overlap
            self.y -= ny * overlap
            other.x += nx * overlap
            other.y += ny * overlap

    def draw(self, surface):
        if self.winner:
            self.pulse += 0.2
            glow_radius = int(self.radius + 8 + math.sin(self.pulse) * 4)
            pygame.draw.circle(surface, GOLD, (int(self.x), int(self.y)), glow_radius + 5)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), glow_radius)

        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        highlight_x = int(self.x - self.radius * 0.3)
        highlight_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(surface, WHITE, (highlight_x, highlight_y), self.radius // 4)

        name_surface = font_tiny.render(self.name, True, BLACK)
        name_rect = name_surface.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(name_surface, name_rect)

# 텍스트 입력 박스
class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.composing = ""

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if not self.active:
            return None

        if event.type == pygame.TEXTEDITING:
            self.composing = event.text
            return None

        if event.type == pygame.TEXTINPUT:
            if len(self.text) < 5:
                self.text += event.text
            self.composing = ""
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                name = self.text.strip()
                self.text = ""
                self.composing = ""
                return name
            elif event.key == pygame.K_BACKSPACE:
                if self.composing:
                    self.composing = ""
                elif self.text:
                    self.text = self.text[:-1]
        return None

    def get_display_text(self):
        return self.text + self.composing

    def draw(self, surface):
        color = WHITE if self.active else LIGHT_GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        display_text = self.get_display_text()
        text_surface = font_small.render(display_text, True, BLACK)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))

# 버튼 클래스
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.enabled = True

    def draw(self, surface):
        color = self.color if self.enabled else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        text_surface = font_small.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

# 공 시작 위치 계산 (균등 분할, 여러 줄)
def calculate_start_position(index):
    cols = 5
    row = index // cols
    col = index % cols
    area_width = GAME_RIGHT - GAME_LEFT - 100
    col_width = area_width / cols
    x = GAME_LEFT + 50 + col * col_width + col_width / 2 + random.randint(-15, 15)
    y = GAME_TOP + 25 + row * 40
    return x, y

# 미로 생성
def create_maze():
    pegs = []
    platforms = []
    spinners = []
    bounce_pads = []

    # 못 배치 - 더 촘촘하게
    rows = 9
    for row in range(rows):
        y = GAME_TOP + 60 + row * 55
        cols = 10 if row % 2 == 0 else 9
        offset = 0 if row % 2 == 0 else 40
        for col in range(cols):
            x = GAME_LEFT + 45 + offset + col * 80
            if GAME_LEFT + 20 < x < GAME_RIGHT - 20:
                # 중앙 부분은 못을 조금 비움
                if not (FUNNEL_X - 60 < x < FUNNEL_X + 60 and row > 6):
                    pegs.append(Peg(x, y))

    # 기울어진 플랫폼 - V자 형태로 중앙으로 모이게
    platform_rows = [
        (GAME_TOP + 100, 35),
        (GAME_TOP + 200, 45),
        (GAME_TOP + 300, 55),
        (GAME_TOP + 400, 65),
        (GAME_TOP + 500, 75),
    ]

    for y, slope in platform_rows:
        # 왼쪽 플랫폼 (오른쪽 아래로)
        platforms.append(Platform(GAME_LEFT, y, GAME_LEFT + 180, y + slope))
        # 오른쪽 플랫폼 (왼쪽 아래로)
        platforms.append(Platform(GAME_RIGHT, y, GAME_RIGHT - 180, y + slope))

    # 회전 장애물 추가
    spinners.append(Spinner(SCREEN_WIDTH // 2 - 150, GAME_TOP + 180, 60, 0.03))
    spinners.append(Spinner(SCREEN_WIDTH // 2 + 150, GAME_TOP + 180, 60, -0.03))
    spinners.append(Spinner(SCREEN_WIDTH // 2, GAME_TOP + 350, 70, 0.025))
    spinners.append(Spinner(SCREEN_WIDTH // 2 - 120, GAME_TOP + 450, 50, -0.035))
    spinners.append(Spinner(SCREEN_WIDTH // 2 + 120, GAME_TOP + 450, 50, 0.035))

    # 바운스 패드 추가
    bounce_pads.append(BouncePad(SCREEN_WIDTH // 2, GAME_TOP + 250, 80))
    bounce_pads.append(BouncePad(GAME_LEFT + 100, GAME_TOP + 380, 60))
    bounce_pads.append(BouncePad(GAME_RIGHT - 100, GAME_TOP + 380, 60))

    return pegs, platforms, spinners, bounce_pads

# 깔때기 그리기
def draw_funnel(surface):
    left_top = (FUNNEL_X - FUNNEL_TOP_WIDTH // 2, FUNNEL_TOP_Y)
    right_top = (FUNNEL_X + FUNNEL_TOP_WIDTH // 2, FUNNEL_TOP_Y)
    left_bottom = (FUNNEL_X - FUNNEL_BOTTOM_WIDTH // 2, FUNNEL_BOTTOM_Y)
    right_bottom = (FUNNEL_X + FUNNEL_BOTTOM_WIDTH // 2, FUNNEL_BOTTOM_Y)

    points = [left_top, right_top, right_bottom, left_bottom]
    pygame.draw.polygon(surface, BROWN, points)
    pygame.draw.polygon(surface, BLACK, points, 3)

    pipe_rect = pygame.Rect(FUNNEL_X - FUNNEL_BOTTOM_WIDTH // 2, FUNNEL_BOTTOM_Y,
                            FUNNEL_BOTTOM_WIDTH, 50)
    pygame.draw.rect(surface, BROWN, pipe_rect)
    pygame.draw.rect(surface, BLACK, pipe_rect, 3)

    pygame.draw.rect(surface, GOLD, (FUNNEL_X - 40, FUNNEL_BOTTOM_Y + 50, 80, 30), border_radius=8)
    win_text = font_small.render("당첨!", True, BLACK)
    win_rect = win_text.get_rect(center=(FUNNEL_X, FUNNEL_BOTTOM_Y + 65))
    surface.blit(win_text, win_rect)

    # 깔때기 양옆 바닥
    pygame.draw.rect(surface, DARK_BROWN, (GAME_LEFT, FUNNEL_TOP_Y, FUNNEL_X - FUNNEL_TOP_WIDTH//2 - GAME_LEFT, 12))
    pygame.draw.rect(surface, DARK_BROWN, (FUNNEL_X + FUNNEL_TOP_WIDTH//2, FUNNEL_TOP_Y, GAME_RIGHT - FUNNEL_X - FUNNEL_TOP_WIDTH//2, 12))

def main():
    clock = pygame.time.Clock()

    # UI 요소
    input_box = InputBox(50, 25, 120, 40)
    add_button = Button(180, 25, 65, 40, "추가", GREEN)
    start_button = Button(255, 25, 80, 40, "시작!", RED)
    retry_button = Button(345, 25, 80, 40, "재시작", BLUE)
    reset_button = Button(435, 25, 80, 40, "초기화", GRAY)

    # 배속 버튼
    speed_buttons = [
        Button(700, 25, 50, 40, "x1", LIGHT_GRAY),
        Button(755, 25, 50, 40, "x2", LIGHT_GRAY),
        Button(810, 25, 50, 40, "x3", LIGHT_GRAY),
    ]

    balls = []
    names_colors = []  # (이름, 색상) 저장
    color_index = 0
    winner = None
    game_started = False
    maze_broken = False
    max_hits = 100
    countdown = 0
    speed_multiplier = 1
    particles = []

    # 미로 생성
    pegs, platforms, spinners, bounce_pads = create_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 배속 버튼 (항상 처리)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, btn in enumerate(speed_buttons):
                    if btn.is_clicked(event.pos):
                        speed_multiplier = i + 1

            if not game_started and countdown == 0:
                name = input_box.handle_event(event)
                if name and len(balls) < 15:
                    # 중복 이름 방지
                    if not any(nc[0] == name for nc in names_colors):
                        color = BALL_COLORS[color_index % len(BALL_COLORS)]
                        start_x, start_y = calculate_start_position(len(balls))
                        balls.append(Ball(name, color, start_x, start_y))
                        names_colors.append((name, color))
                        color_index += 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.is_clicked(event.pos):
                        name = input_box.text.strip()
                        if name and len(balls) < 15 and not any(nc[0] == name for nc in names_colors):
                            color = BALL_COLORS[color_index % len(BALL_COLORS)]
                            start_x, start_y = calculate_start_position(len(balls))
                            balls.append(Ball(name, color, start_x, start_y))
                            names_colors.append((name, color))
                            color_index += 1
                        input_box.text = ""
                        input_box.composing = ""

                    elif start_button.is_clicked(event.pos) and len(balls) >= 2:
                        countdown = 180  # 3초 카운트다운

                    elif retry_button.is_clicked(event.pos) and len(names_colors) >= 2:
                        # 같은 참가자로 재시작
                        balls = []
                        for i, (n, c) in enumerate(names_colors):
                            sx, sy = calculate_start_position(i)
                            balls.append(Ball(n, c, sx, sy))
                        winner = None
                        game_started = False
                        maze_broken = False
                        countdown = 0
                        particles = []
                        pegs, platforms, spinners, bounce_pads = create_maze()

                    elif reset_button.is_clicked(event.pos):
                        balls = []
                        names_colors = []
                        winner = None
                        game_started = False
                        maze_broken = False
                        color_index = 0
                        countdown = 0
                        particles = []
                        pegs, platforms, spinners, bounce_pads = create_maze()

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.is_clicked(event.pos) and len(names_colors) >= 2:
                        balls = []
                        for i, (n, c) in enumerate(names_colors):
                            sx, sy = calculate_start_position(i)
                            balls.append(Ball(n, c, sx, sy))
                        winner = None
                        game_started = False
                        maze_broken = False
                        countdown = 0
                        particles = []
                        pegs, platforms, spinners, bounce_pads = create_maze()

                    elif reset_button.is_clicked(event.pos):
                        balls = []
                        names_colors = []
                        winner = None
                        game_started = False
                        maze_broken = False
                        color_index = 0
                        countdown = 0
                        particles = []
                        pegs, platforms, spinners, bounce_pads = create_maze()

        # 카운트다운 처리
        if countdown > 0:
            countdown -= 1
            if countdown == 0:
                game_started = True
                for ball in balls:
                    ball.dx = random.uniform(-2, 2)
                    ball.dy = random.uniform(3, 6)

        # 회전 장애물/바운스 패드 업데이트 + 공 이동 (배속 적용)
        for _ in range(speed_multiplier):
            if not maze_broken:
                for spinner in spinners:
                    spinner.update()

            for pad in bounce_pads:
                pad.update()

            for ball in balls:
                ball.move(pegs, platforms, spinners, bounce_pads, balls, game_started, maze_broken)

        # 미로 파괴 체크
        if game_started and not maze_broken:
            total_stuck = sum(ball.stuck_count for ball in balls)
            if total_stuck >= max_hits:
                maze_broken = True

        # 당첨자 확인 (동시 도착 시 y 좌표가 가장 큰 공 선택)
        if game_started and not winner:
            finished_balls = [ball for ball in balls if ball.finished]
            if finished_balls:
                winner = max(finished_balls, key=lambda b: b.y)
                winner.winner = True
                winner.x = FUNNEL_X
                winner.y = FUNNEL_BOTTOM_Y + 65
                # 당첨 파티클 생성
                for _ in range(30):
                    particles.append(Particle(winner.x, winner.y,
                        random.choice([GOLD, RED, YELLOW, GREEN, BLUE, PURPLE, PINK, CYAN])))

        # 파티클 업데이트
        particles = [p for p in particles if p.update()]
        # 당첨자가 있으면 지속적으로 파티클 생성
        if winner and random.random() < 0.3:
            particles.append(Particle(winner.x, winner.y,
                random.choice([GOLD, RED, YELLOW, GREEN, BLUE, PURPLE, PINK, CYAN])))

        # 화면 그리기
        screen.fill((25, 25, 45))

        # 게임 영역 배경
        pygame.draw.rect(screen, (35, 35, 55), (GAME_LEFT, GAME_TOP, GAME_RIGHT - GAME_LEFT, GAME_BOTTOM - GAME_TOP))
        pygame.draw.rect(screen, WHITE, (GAME_LEFT, GAME_TOP, GAME_RIGHT - GAME_LEFT, GAME_BOTTOM - GAME_TOP), 3)

        # 미로 그리기 (파괴되면 반투명하게)
        if not maze_broken:
            for platform in platforms:
                platform.draw(screen)
            for spinner in spinners:
                spinner.draw(screen)
            for pad in bounce_pads:
                pad.draw(screen)
            for peg in pegs:
                peg.draw(screen)

        # 깔때기 그리기
        draw_funnel(screen)

        # UI 그리기
        input_box.draw(screen)
        add_button.enabled = not game_started and countdown == 0 and len(balls) < 15
        start_button.enabled = not game_started and countdown == 0 and len(balls) >= 2
        retry_button.enabled = len(names_colors) >= 2
        add_button.draw(screen)
        start_button.draw(screen)
        retry_button.draw(screen)
        reset_button.draw(screen)

        # 배속 버튼 그리기
        for i, btn in enumerate(speed_buttons):
            if i + 1 == speed_multiplier:
                # 선택된 배속 버튼 강조
                pygame.draw.rect(screen, GOLD, btn.rect, border_radius=8)
                pygame.draw.rect(screen, BLACK, btn.rect, 2, border_radius=8)
                text_surface = font_small.render(btn.text, True, BLACK)
                text_rect = text_surface.get_rect(center=btn.rect.center)
                screen.blit(text_surface, text_rect)
            else:
                btn.draw(screen)

        # 참가자 수 표시
        count_text = font_tiny.render(f"참가자: {len(balls)}/15명", True, WHITE)
        screen.blit(count_text, (530, 35))

        # 갇힘 횟수 표시 (게임 중일 때)
        if game_started and not maze_broken:
            total_stuck = sum(ball.stuck_count for ball in balls)
            if total_stuck > 0:
                stuck_text = font_small.render(f"갇힘: {total_stuck}/{max_hits}", True, ORANGE)
                screen.blit(stuck_text, (GAME_LEFT + 10, GAME_TOP + 10))
        elif maze_broken:
            broken_text = font_small.render("*** 미로 파괴! ***", True, RED)
            screen.blit(broken_text, (GAME_LEFT + 10, GAME_TOP + 10))

        # 참가자 목록 표시 (하단 영역)
        if names_colors:
            items_per_row = min(len(names_colors), 8)
            for i, (name, color) in enumerate(names_colors):
                row = i // items_per_row
                col = i % items_per_row
                item_width = (GAME_RIGHT - GAME_LEFT) / items_per_row
                x = GAME_LEFT + col * item_width + 15
                y = 780 + row * 25
                pygame.draw.circle(screen, color, (int(x), int(y + 10)), 8)
                pygame.draw.circle(screen, WHITE, (int(x), int(y + 10)), 8, 1)
                name_text = font_tiny.render(name, True, WHITE)
                screen.blit(name_text, (int(x + 14), int(y)))

        # 안내 문구
        if len(balls) < 2 and not game_started:
            hint_text = font_small.render("이름을 입력하고 추가하세요 (최소 2명)", True, YELLOW)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, GAME_TOP + 280))
            screen.blit(hint_text, hint_rect)

        # 공 그리기
        for ball in balls:
            if not ball.finished or ball.winner:
                ball.draw(screen)

        # 파티클 그리기
        for p in particles:
            p.draw(screen)

        # 카운트다운 표시
        if countdown > 0:
            count_num = math.ceil(countdown / 60)
            count_surface = font_countdown.render(str(count_num), True, GOLD)
            count_rect = count_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            overlay = pygame.Surface((200, 150))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            screen.blit(overlay, (count_rect.centerx - 100, count_rect.centery - 75))
            screen.blit(count_surface, count_rect)

        # 당첨자 표시
        if winner:
            overlay = pygame.Surface((SCREEN_WIDTH, 80))
            overlay.fill(BLACK)
            overlay.set_alpha(220)
            screen.blit(overlay, (0, SCREEN_HEIGHT - 100))

            winner_text = font_large.render(f"★ {winner.name} 당첨! ★", True, GOLD)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            screen.blit(winner_text, winner_rect)

        # 크레딧
        credit_text = font_tiny.render("Made by IYShim", True, GRAY)
        screen.blit(credit_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
