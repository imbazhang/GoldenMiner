import pygame
from pygame.locals import *  # 调包
import time
import math
from sys import exit
import random

pygame.init()  # 初始化
screen = pygame.display.set_mode((551, 401), 0, 32)  # 创建图形化窗口
pygame.display.set_caption("Start Coding Now! 黄金矿工")  # 窗口标题

background_start = 'all_start.png'  # 加载背景

backGround = pygame.image.load(background_start).convert_alpha()  # 初始背景为启动背景
backGround_judge = 'start'

pointer = '钻石.png'  # 添加指针
poInter = pygame.image.load(pointer).convert_alpha()

gold_small = pygame.image.load(
    '金矿.png').convert_alpha()  # 小金矿，尺寸 46 * 42
gold_mid = pygame.transform.smoothscale(gold_small, (66, 61))  # 中金矿，尺寸100 * 84
gold_big = pygame.transform.smoothscale(gold_small, (121, 104))  # 大金矿，尺寸121 * 104
background_play_1 = pygame.image.load('background1.png').convert()
background_play_2 = pygame.image.load('background2.png').convert()
background_success_end = pygame.image.load('success_end.png').convert()
background_end_all = pygame.image.load('end_all.png').convert()
hook = pygame.image.load('hook.png').convert_alpha()  # 图片尺寸 44 * 25
stone_1 = pygame.image.load('stone1.png').convert_alpha()  # 68 * 60
stone_2 = pygame.image.load('stone2.png').convert_alpha()  # 65 * 54
background_start_1 = pygame.image.load('start_1.png').convert_alpha()
background_start_2 = pygame.image.load('start_2.png').convert_alpha()
background_start = [background_start_1, background_start_2]
screen.blit(backGround, (0, 0))

hook_pos_x = 476
hook_pos_y = 76

levels = 1
score_levels = [650, 1150]

pygame.time.Clock().tick(180)
time_countdown = 60
TIME_DOWN = pygame.USEREVENT + 1
pygame.time.set_timer(TIME_DOWN, 1000)

DIRECRTION_FLAG = -1

ROTATE_DEGREE = pygame.USEREVENT + 3
pygame.time.set_timer(ROTATE_DEGREE, 20)
degree = 75

pygame.mouse.set_visible(True)
pygame.event.set_grab(True)

speed = {'x': 0, 'y': 0}
gold_levels = [[[150, 210, 'small', 46, 42], [680, 180, 'small', 46, 42], [240, 320, 'mid', 66, 61],
                [0, 320, 'big', 121, 104], [900, 280, 'small', 46, 42], [250, 440, 'mid', 66, 61],
                [550, 210, 'small', 46, 42], [580, 600, 'mid', 66, 61], [680, 400, 'big', 121, 104],
                [260, 230, 'small', 46, 42]]]

stone_levels = [[120, 260, 1, 68, 60], [550, 300, 2, 65, 54], [420, 160, 1, 68, 60]
                ]

score = 0  # 对变量进行初始化::分数
hook_state = 'spare'  # 初始化钩子状态：空闲

carry = []


def init_start():  # 初始化启动
    global hook_state
    global degree
    global backGround
    global backGround_judge
    global DIRECRTION_FLAG
    global time_countdown
    hook_state = 'spare'
    degree = 75
    DIRECRTION_FLAG = -1
    backGround = background_start[levels - 1]
    screen = pygame.display.set_mode((891, 647), 0, 32)
    screen.blit(backGround, (0, 0))
    pygame.display.update()
    time.sleep(2.0)
    L = [background_play_2, background_play_1]
    x = random.choice(L)
    backGround_judge = 'play'
    backGround = x
    screen = pygame.display.set_mode((995, 712), 0, 32)
    screen.blit(backGround, (0, 0))
    time_countdown = 30
    pygame.display.update()


def end_level():
    global backGround
    global backGround_judge
    global levels
    if score >= score_levels[levels - 1]:
        backGround_judge = 'success'
        backGround = background_success_end
        screen = pygame.display.set_mode((550, 400), 0, 32)
        screen.blit(backGround, (0, 0))
        pygame.display.update()
        levels += 1
    else:
        backGround = background_end_all
        backGround_judge = 'end'
        screen = pygame.display.set_mode((544, 400), 0, 32)
        screen.blit(backGround, (0, 0))
        pygame.display.update()


def throw_hook():  # 扔钩子
    global hook_state
    hook_state = 'down'  # 重置钩子状态：向下
    speed['x'] = math.sin(abs(math.radians(degree)))
    speed['y'] = abs(math.cos(abs(math.radians(degree))))
    if degree > 0:
        speed['x'] = abs(speed['x'])
    else:
        speed['x'] = -abs(speed['x'])


def clasp_hook():  # 收钩子
    speed['x'] = -speed['x']
    speed['y'] = -speed['y']


def hit_gold(element):  # 判定
    global hook_state
    print(speed['x'], speed['y'], sep=' ')
    hook_state = 'carry'
    if element == 'big':
        hook_state = 'carry_big'
        k = 0.3
    elif element == 'mid':
        hook_state = 'carry_mid'
        k = 0.55
    elif element == 'small':
        hook_state = 'carry_small'
        k = 0.75
    else:
        k = 1
    speed['x'] = -speed['x'] * k
    speed['y'] = -speed['y'] * k
    print(speed['x'], speed['y'], sep=' ')


def hit_stone():
    global hook_state
    hook_state = 'carry_stone'
    print(speed['x'], speed['y'], sep=' ')
    speed['x'] = -speed['x'] * 0.2
    speed['y'] = -speed['y'] * 0.2
    print(speed['x'], speed['y'], sep=' ')


while True:  # 实现指针移动//游戏主循环
    # print(backGround_judge, hook_state, degree, sep=' ')
    screen.blit(backGround, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()  # 设置键盘退出ESC
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()  # 设置退出
            if backGround_judge == 'start':
                if event.key == K_SPACE or event.key == K_KP_ENTER or event.key == K_0:
                    init_start()
            if backGround_judge == 'play':
                if event.key == K_SPACE or event.key == K_KP_ENTER:
                    if hook_state == 'spare':
                        throw_hook()
            if backGround_judge == 'success':
                if event.key == K_SPACE or event.key == K_KP_ENTER:
                    init_start()
        if event.type == pygame.MOUSEBUTTONDOWN:  #
            if backGround_judge == 'start':
                if 47 <= event.pos[0] <= 195 and 46 <= event.pos[1] <= 188:
                    init_start()
            if backGround_judge == 'play':
                if 720 <= event.pos[0] <= 820 and 20 <= event.pos[1] <= 80:
                    exit()
            if backGround_judge == 'success':
                if 170 <= event.pos[0] <= 400 and 270 <= event.pos[1] <= 321:
                    init_start()
            if backGround_judge == 'end':
                if 42 <= event.pos[0] <= 320 and 515 <= event.pos[1] <= 370:
                    exit()
        if event.type == TIME_DOWN:
            time_countdown -= 1
        if event.type == ROTATE_DEGREE and hook_state == 'spare':
            if DIRECRTION_FLAG == -1:
                degree = degree - 1
            else:
                degree = degree + 1
            if degree == 75:
                DIRECRTION_FLAG = -1
            if degree == -75:
                DIRECRTION_FLAG = 1

    if backGround_judge == 'play':
        font_object = pygame.font.SysFont(None, 40)
        time_text_screen = font_object.render(str(time_countdown), True, (23, 168, 61))
        time_text_rect = time_text_screen.get_rect()
        time_text_rect.center = (951, 32)
        screen.blit(time_text_screen, time_text_rect)

        levels_text_screen = font_object.render(str(levels), True, (23, 168, 61))
        levels_text_rect = levels_text_screen.get_rect()
        levels_text_rect.center = (902, 75)
        screen.blit(levels_text_screen, levels_text_rect)

        score_levels_screen = font_object.render(str(score_levels[levels - 1]), True, (23, 168, 61))
        score_levels_rect = score_levels_screen.get_rect()
        score_levels_rect.center = (204, 79)
        screen.blit(score_levels_screen, score_levels_rect)

        score_screen = font_object.render(str(score), True, (23, 168, 61))
        score_rect = score_screen.get_rect()
        score_rect.center = (171, 34)
        screen.blit(score_screen, score_rect)

        i = 0
        while i < (len(gold_levels[levels - 1])):
            if gold_levels[levels - 1][i][2] == 'small':
                screen.blit(gold_small, (gold_levels[levels - 1][i][0], gold_levels[levels - 1][i][1]))
            elif gold_levels[levels - 1][i][2] == 'mid':
                screen.blit(gold_mid, (gold_levels[levels - 1][i][0], gold_levels[levels - 1][i][1]))
            else:
                screen.blit(gold_big, (gold_levels[levels - 1][i][0], gold_levels[levels - 1][i][1]))

            if int(hook_pos_x + 20) in range(gold_levels[levels - 1][i][0],
                                             gold_levels[levels - 1][i][0] + gold_levels[levels - 1][i][3]) \
                    and int(hook_pos_y + 25) in range(gold_levels[levels - 1][i][1],
                                                      gold_levels[levels - 1][i][1] + gold_levels[levels - 1][i][4]):
                hit_gold(gold_levels[levels - 1][i][2])
                carry.append(gold_levels[levels - 1][i])
                print(gold_levels[levels - 1][i])
                del gold_levels[levels - 1][i]
            else:
                i += 1

        i = 0
        while i < len(stone_levels):
            if stone_levels[i][2] == 1:
                screen.blit(stone_2, (stone_levels[i][0], stone_levels[i][1]))
            else:
                screen.blit(stone_1, (stone_levels[i][0], stone_levels[i][1]))

            if int(hook_pos_x + 20) in range(stone_levels[i][0], stone_levels[i][0] + stone_levels[i][3]) \
                    and int(hook_pos_y + 25) in range(stone_levels[i][1], stone_levels[i][1] + stone_levels[i][4]):
                hit_stone()
                carry.append(stone_levels[i])
                print(stone_levels[i])
                del stone_levels[i]
            else:
                i += 1

        if hook_state == 'spare':
            hook_rotate = pygame.transform.rotate(hook, degree)
            screen.blit(hook_rotate, (hook_pos_x, hook_pos_y))

        if hook_state == 'down' or hook_state == 'carry_small' or \
                hook_state == "carry_mid" or hook_state == 'carry_big' or hook_state == 'carry_stone':
            hook_rotate = pygame.transform.rotate(hook, degree)
            hook_pos_x = hook_pos_x + speed['x']
            hook_pos_y = hook_pos_y + speed['y']
            if hook_pos_x <= 0 or hook_pos_x >= 910 or hook_pos_y <= 0 or hook_pos_y >= 660:
                clasp_hook()
            if 475 <= hook_pos_x <= 476 or 75 <= hook_pos_y <= 76:
                hook_pos_x = 476
                hook_pos_y = 76
                if hook_state == 'carry_big':
                    score += 500
                elif hook_state == 'carry_mid':
                    score += 200
                elif hook_state == 'carry_small':
                    score += 50
                elif hook_state == 'carry_stone':
                    score += 50

                hook_state = 'spare'
                carry = []
                speed['x'] = 0
                speed['y'] = 0

            if carry != []:
                if carry[0][2] == 'small':
                    screen.blit(gold_small, (hook_pos_x + 30, hook_pos_y + 20))
                elif carry[0][2] == 'mid':
                    screen.blit(gold_mid,  (hook_pos_x + 40, hook_pos_y + 44))
                elif carry[0][2] == 'big':
                    screen.blit(gold_big,  (hook_pos_x - 20, hook_pos_y + 60))
                elif carry[0][2] == 1:
                    screen.blit(stone_1, (hook_pos_x, hook_pos_y + 30))
                else:
                    screen.blit(stone_2,  (hook_pos_x, hook_pos_y + 30))

            screen.blit(hook_rotate, (hook_pos_x, hook_pos_y))

    if time_countdown == 0:
        end_level()

    pygame.display.update()  # 界面刷新
