import logging
import math
from random import randint, uniform, choice

import pygame

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bin/firework.log', encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

logger = logging.getLogger(__name__)

vector = pygame.math.Vector2
options = {
    "screen_width": 800,
    "screen_height": 800,
    "dynamic_offset": 1,
    "static_offset": 5,
    "gravity": pygame.math.Vector2(0, 0.3),
    "trail_colours": [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)],
    "glyph": 100,
    "greetings": "新年快乐",
    "bold": True
}

class InitFirework:

    def __init__(self, pos=None, vec=None):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = (
            (randint(0, 255), randint(0, 255), randint(0, 255)
             ), (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)))
        if not pos:
            self.yan_hua = CreateFirework(randint(0, options["screen_width"]),
                                          options["screen_height"], True, self.colour)
            # 创建烟花
        else:
            self.yan_hua = CreateFirework(pos, options["screen_height"], True, self.colour, vec)
        self.exploded = False
        self.particles = []
        self.min_max_particles = vector(100, 225)

    def update(self, screen):  # 加载烟花
        if not self.exploded:
            self.yan_hua.apply_force(options["gravity"])
            self.yan_hua.move()
            for tf in self.yan_hua.trails:
                tf.show(screen)

            self.show(screen)

            if self.yan_hua.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.apply_force(
                    vector(options["gravity"].x + uniform(-1, 1) / 20, options["gravity"].y / 2 + (randint(1, 8) / 100))
                )
                particle.move()
                for t in particle.trails:
                    t.show(screen)
                particle.show(screen)

    def explode(self):
        amount = randint(int(self.min_max_particles.x), int(self.min_max_particles.y))
        for _ in range(amount):
            self.particles.append(
                CreateFirework(self.yan_hua.pos.x, self.yan_hua.pos.y, False, self.colours))

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.yan_hua.pos.x), int(
            self.yan_hua.pos.y)), self.yan_hua.size)

    def remove(self):
        if self.exploded:
            # 使用列表推导式安全地移除元素
            self.particles = [p for p in self.particles if not p.remove]

            if len(self.particles) == 0:
                return True
            else:
                return False
        return None


class CreateFirework:

    def __init__(self, x, y, yan_hua, colour, vec=None):
        self.yan_hua = yan_hua
        self.pos = vector(x, y)
        self.origin = vector(x, y)
        self.radius = 20
        self.remove = False
        self.explosion_radius = randint(5, 18)
        self.life = 0
        self.acc = vector(0, 0)
        self.trails = []  # 存储粒子跟踪对象
        self.prev_pos_x = [-10] * 10  # 存储最后 10 个位置
        self.prev_pos_y = [-10] * 10  # 存储最后 10 个位置

        if self.yan_hua:
            self.vel = vector(0, -randint(17, 20))
            self.size = 5
            self.colour = colour
            for n in range(5):
                self.trails.append(DrawFirework(n, self.size, True))
        else:
            if not vec:
                self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            else:
                self.vel = vector(vec, vec)

            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(2, 4)
            self.colour = choice(colour)
            for n in range(5):
                self.trails.append(DrawFirework(n, self.size, False))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.yan_hua:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.yan_hua:  # 检查颗粒是否在爆炸半径之外
            distance = math.sqrt((self.pos.x - self.origin.x)
                                 ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.trail_update()

        self.life += 1

    def show(self, screen):
        pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2], 0),
                           (int(self.pos.x), int(self.pos.y)), self.size)

    def decay(self):
        if 10 < self.life < 50:
            ran = randint(0, 30)
            if ran == 0:
                self.remove = True
        elif self.life > 50:
            ran = randint(0, 5)
            if ran == 0:
                self.remove = True

    def trail_update(self):
        self.prev_pos_x.pop()
        self.prev_pos_x.insert(0, int(self.pos.x))
        self.prev_pos_y.pop()
        self.prev_pos_y.insert(0, int(self.pos.y))

        for n, t in enumerate(self.trails):
            # 检查索引是否超出范围
            dynamic_offset = n + options["dynamic_offset"]
            static_offset = n + options["static_offset"]

            if self.yan_hua and dynamic_offset < len(self.prev_pos_x):
                t.get_pos(self.prev_pos_x[dynamic_offset],
                          self.prev_pos_y[dynamic_offset])
            elif not self.yan_hua and static_offset < len(self.prev_pos_x):
                t.get_pos(self.prev_pos_x[static_offset],
                          self.prev_pos_y[static_offset])


class DrawFirework:

    def __init__(self, n, size, dynamic):
        self.pos_in_line = n
        self.pos = vector(-10, -10)
        self.dynamic = dynamic

        if self.dynamic:
            self.colour = options["trail_colours"][n]
            self.size = int(size - n / 2)
        else:
            self.colour = (255, 255, 200)
            self.size = size - 2
            if self.size < 0:
                self.size = 0

    def get_pos(self, x, y):
        self.pos = vector(x, y)

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(
            self.pos.x), int(self.pos.y)), self.size)


def update(screen, yan_hua_list):
    # 使用反向迭代避免在迭代时修改列表
    for i in range(len(yan_hua_list) - 1, -1, -1):
        yan_hua = yan_hua_list[i]
        yan_hua.update(screen)
        if yan_hua.remove():
            yan_hua_list.pop(i)

    pygame.display.update()



def main():
    pygame.init()

    # 检查pygame是否成功初始化
    if not pygame.get_init():
        logger.error("Pygame initialization failed!")
        return

    # 安全加载资源
    try:
        icon = pygame.image.load("bin/image/Logo_Mr.X.ico")
        pygame.display.set_caption("烟花盛宴")
        pygame.display.set_icon(icon)
    except pygame.error:
        logger.warning("Could not load icon file, using default icon")

    try:
        pygame.mixer.music.load("bin/music/bgm.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error:
        logger.warning("Could not load music file, running without sound")

    try:
        font = pygame.font.Font("bin/font/WeiRuanYaHei.ttc", options["glyph"])
    except pygame.error:
        logger.warning("Could not load font file, using default font")
        font = pygame.font.Font(None, options["glyph"])

    screen = pygame.display.set_mode((options["screen_width"], options["screen_height"]))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    yan_hua_list = [InitFirework() for _ in range(2)]  # 创建第一个烟花
    running = True

    logger.info("开始运行烟花程序")

    while running:
        clock.tick(60)

        for event in pygame.event.get():  # 侦测事件
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        # 在循环中安全加载字体（如果之前加载失败）
        try:
            current_font = pygame.font.Font("bin/font/WeiRuanYaHei.ttc", options["glyph"])
        except pygame.error:
            current_font = pygame.font.Font(None, options["glyph"])

        text = f"{options['greetings']}"
        image = current_font.render(text, True, "red")
        rect = image.get_rect()
        rect.center = screen_rect.center

        screen.fill((20, 20, 30))  # 绘制背景
        if randint(0, 20) == 1:  # 有几率(5%)创建新烟花，使程序不单调
            yan_hua_list.append(InitFirework())

        screen.blit(image, (rect.x, rect.y))
        update(screen, yan_hua_list)

    logger.info("烟花程序结束运行")

    pygame.quit()


# 执行程序
if __name__ == '__main__':
    main()
