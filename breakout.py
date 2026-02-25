import pygame
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블록깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
BLUE = (100, 150, 255)
PURPLE = (200, 100, 255)
GRAY = (150, 150, 150)

BLOCK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

# 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕
font_large = pygame.font.Font(font_path, 48)
font_medium = pygame.font.Font(font_path, 32)
font_small = pygame.font.Font(font_path, 24)

# 게임 설정
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_SPEED = 10

BALL_SIZE = 12
BALL_SPEED = 6

BLOCK_ROWS = 6
BLOCK_COLS = 10
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 25
BLOCK_PADDING = 5
BLOCK_TOP_OFFSET = 80

# 패들 클래스
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, GRAY, self.rect, 2)

# 공 클래스
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.dx = random.choice([-1, 1]) * BALL_SPEED * 0.7
        self.dy = -BALL_SPEED
        self.rect = pygame.Rect(self.x - BALL_SIZE//2, self.y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # 벽 충돌
        if self.x <= BALL_SIZE//2:
            self.x = BALL_SIZE//2
            self.dx = abs(self.dx)
        elif self.x >= SCREEN_WIDTH - BALL_SIZE//2:
            self.x = SCREEN_WIDTH - BALL_SIZE//2
            self.dx = -abs(self.dx)

        if self.y <= BALL_SIZE//2:
            self.y = BALL_SIZE//2
            self.dy = abs(self.dy)

        self.rect.x = self.x - BALL_SIZE//2
        self.rect.y = self.y - BALL_SIZE//2

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), BALL_SIZE//2)

# 블록 클래스
class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.color = color
        self.alive = True

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 1)

# 블록 생성
def create_blocks():
    blocks = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = col * (BLOCK_WIDTH + BLOCK_PADDING) + 35
            y = row * (BLOCK_HEIGHT + BLOCK_PADDING) + BLOCK_TOP_OFFSET
            color = BLOCK_COLORS[row % len(BLOCK_COLORS)]
            blocks.append(Block(x, y, color))
    return blocks

# 게임 상태
def draw_text_center(surface, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y))
    surface.blit(text_surface, text_rect)

def game_start_screen():
    screen.fill(BLACK)
    draw_text_center(screen, "블록깨기 게임", font_large, WHITE, 200)
    draw_text_center(screen, "← → 방향키로 패들 이동", font_small, GRAY, 300)
    draw_text_center(screen, "Space: 시작 / P: 일시정지 / R: 재시작", font_small, GRAY, 340)
    draw_text_center(screen, "SPACE를 눌러 시작", font_medium, YELLOW, 450)
    draw_text_center(screen, "Made by IYShim", font_small, GRAY, 550)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    return False
    return True

def game_over_screen(score, won):
    screen.fill(BLACK)
    if won:
        draw_text_center(screen, "축하합니다!", font_large, GREEN, 200)
        draw_text_center(screen, "모든 블록을 깼습니다!", font_medium, WHITE, 280)
    else:
        draw_text_center(screen, "게임 오버", font_large, RED, 200)

    draw_text_center(screen, f"점수: {score}", font_medium, WHITE, 350)
    draw_text_center(screen, "R: 재시작 / ESC: 종료", font_small, GRAY, 450)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
    return False

def main():
    clock = pygame.time.Clock()

    if not game_start_screen():
        pygame.quit()
        return

    while True:
        # 게임 초기화
        paddle = Paddle()
        ball = Ball()
        blocks = create_blocks()
        score = 0
        lives = 3
        paused = False
        running = True

        # 게임 루프
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            if paused:
                draw_text_center(screen, "일시정지", font_large, YELLOW, SCREEN_HEIGHT//2)
                pygame.display.flip()
                clock.tick(60)
                continue

            # 키 입력 처리
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")

            # 공 이동
            ball.move()

            # 패들 충돌
            if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
                ball.dy = -abs(ball.dy)
                # 패들 위치에 따라 반사 각도 조절
                hit_pos = (ball.x - paddle.x) / paddle.width
                ball.dx = (hit_pos - 0.5) * BALL_SPEED * 2

            # 블록 충돌
            for block in blocks:
                if block.alive and ball.rect.colliderect(block.rect):
                    block.alive = False
                    score += 10

                    # 충돌 방향 계산
                    if abs(ball.rect.bottom - block.rect.top) < 10 or abs(ball.rect.top - block.rect.bottom) < 10:
                        ball.dy = -ball.dy
                    else:
                        ball.dx = -ball.dx
                    break

            # 공이 아래로 떨어짐
            if ball.y > SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.reset()
                else:
                    if not game_over_screen(score, False):
                        pygame.quit()
                        return
                    running = False

            # 모든 블록 파괴
            if all(not block.alive for block in blocks):
                if not game_over_screen(score, True):
                    pygame.quit()
                    return
                running = False

            # 화면 그리기
            screen.fill(BLACK)

            # UI 그리기
            score_text = font_small.render(f"점수: {score}", True, WHITE)
            lives_text = font_small.render(f"목숨: {'♥' * lives}", True, RED)
            screen.blit(score_text, (20, 20))
            screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))

            # 게임 오브젝트 그리기
            paddle.draw(screen)
            ball.draw(screen)
            for block in blocks:
                block.draw(screen)

            # 하단 크레딧
            credit_text = font_small.render("Made by IYShim", True, GRAY)
            screen.blit(credit_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 30))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
