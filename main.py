import pygame
import math

pygame.init()

FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ARROW_LENGTH = 100
ARROW_HIGHT = 30

size = (1500, 800)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

font = pygame.font.Font('./font/NotoSansKR-Medium.otf', 50)

arrow = pygame.image.load('./img/arrow.png')
arrow = pygame.transform.scale(arrow, (ARROW_LENGTH, ARROW_HIGHT))
bullet_img = pygame.image.load('./img/bullet.png')
hit_img = pygame.image.load('./img/hit.png')


# https://volfeed.blogspot.com/2020/10/pygame.html
def blitRotate(image, pos, originPos, angle): 
    w, h       = image.get_size() 
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]] 
    box_rotate = [p.rotate(angle) for p in box] 
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1]) 
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1]) 
 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1]) 
    pivot_rotate = pivot.rotate(angle) 
    pivot_move   = pivot_rotate - pivot 
 
    origin = ((pos[0] - originPos[0] + min_box[0] - pivot_move[0]), (pos[1] - originPos[1] - max_box[1] + pivot_move[1])) 
 
    rotated_image = pygame.transform.rotate(image, angle) 
    return (rotated_image, origin)


def getRotate(cri_pos, pos):
    deltaX = pos[0] - cri_pos[0]
    deltaY = pos[1] - cri_pos[1]
    value = math.degrees(math.atan2(deltaX, deltaY)) -90
    if value < 0:
        value += 360
    return value


def get_length(r, arrow_center, enemy_pos):
    enemy_rotation = [0, 0, 0, 0]
    enemy_rotation[0] = getRotate(arrow_center, enemy_pos) # 좌상
    enemy_rotation[1] = getRotate(arrow_center, (enemy_pos[0], enemy_pos[1]+100)) # 좌하
    enemy_rotation[2] = getRotate(arrow_center, (enemy_pos[0]+100, enemy_pos[1]+100)) # 우하
    enemy_rotation[3] = getRotate(arrow_center, (enemy_pos[0]+100, enemy_pos[1])) # 우상
        
    # 사각형 위쪽 변
    if r >= enemy_rotation[0] and r <= enemy_rotation[3]: 
        delta_y = arrow_center[1] - enemy_pos[1]
        delta_x = (math.tan(math.radians(r))**-1)*delta_y
        length = math.dist(arrow_center, (arrow_center[0] + delta_x, enemy_pos[1]))-ARROW_LENGTH
        return length, True
        
    # 사각형 아래쪽 변
    if r <= enemy_rotation[1] and r >= enemy_rotation[2]:
        delta_y = arrow_center[1] - (enemy_pos[1] + 100)
        delta_x = (math.tan(math.radians(r))**-1)*delta_y
        length = math.dist(arrow_center, (arrow_center[0] + delta_x, enemy_pos[1] + 100))-ARROW_LENGTH
        return length, True

    if r >= 270 or r <= 90:
    # 사각형이 0°와 360°의 경계에 위치
        if enemy_rotation[0] < 90 and enemy_rotation[0] < enemy_rotation[1]:
            if r <= enemy_rotation[0] or r >= enemy_rotation[1]:
                delta_x = enemy_pos[0] - arrow_center[0]
                delta_y = math.tan(math.radians(r)) * delta_x
                length = math.dist(arrow_center, (enemy_pos[0], arrow_center[1]-delta_y))-ARROW_LENGTH
                return length, True

    # 사각형 왼쪽 변
        if r <= enemy_rotation[0] and r >= enemy_rotation[1]:
            delta_x = enemy_pos[0] - arrow_center[0]
            delta_y = math.tan(math.radians(r)) * delta_x
            length = math.dist(arrow_center, (enemy_pos[0], arrow_center[1]-delta_y))-ARROW_LENGTH
            return length, True

    # 사각형 오른쪽 변
    if r > 90 and r < 270:
        if r <= enemy_rotation[2] and r >= enemy_rotation[3]:
            delta_x = enemy_pos[0]+100 - arrow_center[0]
            delta_y = math.tan(math.radians(r)) * delta_x
            length = math.dist(arrow_center, (enemy_pos[0]+100, arrow_center[1]-delta_y))-ARROW_LENGTH
            return length, True

    return 1700, False
    

def runGame():
    global done
    r = 0
    length = 750
    arrow_center = [750, 400]
    bullet = []
    bullet_shape = [[], []]
    hit = []
    mouse_pos = (0, 0)
    enemy_pos = [1300, 600]
    shot = False

    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        r = getRotate(arrow_center, mouse_pos)
        if r >= 270 or r <= 90:
            sight = "right"
        elif r > 90 and r < 270:
            sight = "left"
        
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                length, shot = get_length(r, arrow_center, enemy_pos)
                if length < 0:
                    length = 0
                    shot = False

                bullet_shape[0].append(20)
                bullet_shape[1].append(r)
                bullet.append(0)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if enemy_pos[0] < 1400:
                enemy_pos[0] += 2
        elif keys[pygame.K_LEFT]:
            if enemy_pos[0] > 0:
                enemy_pos[0] -= 2
        elif keys[pygame.K_DOWN]:
            if enemy_pos[1] < 700:
                enemy_pos[1] += 2
        elif keys[pygame.K_UP]:
            if enemy_pos[1] > 0:
                enemy_pos[1] -= 2
        elif keys[pygame.K_d]:
            if arrow_center[0] < 1450:
                arrow_center[0] += 2
        elif keys[pygame.K_a]:
            if arrow_center[0] > 50:
                arrow_center[0] -= 2
        elif keys[pygame.K_s]:
            if arrow_center[1] < 750:
                arrow_center[1] += 2
        elif keys[pygame.K_w]:
            if arrow_center[1] > 50:
                arrow_center[1] -= 2

        for i in range(len(bullet_shape[0])):
            bullet_shape[0][i] -= 2

        for i in range(len(bullet_shape[0])):
            try:
                if bullet_shape[0][i] <= 0:
                    del bullet_shape[0][i]
                    del bullet_shape[1][i]
                    del bullet[i]
                    del hit[i]
            except: pass

        pygame.draw.rect(screen, (255, 0, 0), (enemy_pos[0], enemy_pos[1], 100, 100))

        for i in range(len(bullet_shape[0])):
            bullet[i] = (pygame.transform.scale(bullet_img, (length, bullet_shape[0][i])))
            bullet[i] = blitRotate(bullet[i], arrow_center, (-ARROW_LENGTH, bullet_shape[0][i]/2), bullet_shape[1][i])
        for i in range(len(bullet)):
            screen.blit(bullet[i][0], bullet[i][1])

        if shot:
            tmp_hit = (pygame.transform.scale(hit_img, (20, 20)))
            hit.append(blitRotate(tmp_hit, arrow_center, (-ARROW_LENGTH-length+10, 10), r))
            shot = False
        for i in range(len(hit)):
            screen.blit(hit[i][0], hit[i][1])

        rotate_arrow = blitRotate(arrow, arrow_center, (0, ARROW_HIGHT / 2), r)
        screen.blit(rotate_arrow[0], rotate_arrow[1])

        sight_txt = font.render(sight, True, WHITE)
        screen.blit(sight_txt, (0, 0))

        pygame.display.update()

runGame()
pygame.quit