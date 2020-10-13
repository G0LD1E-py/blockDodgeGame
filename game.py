import pygame
import sys
import random

pygame.init()

width = 800
height = 600

red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)

playerSize = 50
playerPos = [width/2, height-2*playerSize]

enemySize = 50
enemyPos = [random.randint(0, width-enemySize), 0]
enemySpeed = 5
enemyList = [enemyPos]

backgroundColor = black
screen = pygame.display.set_mode((width, height))

gameOver = False

clock = pygame.time.Clock()

score = 0

myFont = pygame.font.SysFont("monospace", 35)
gameOverMsg = '\nThanks for playing!\n\nScore: '

def setLevel(score, enemySpeed):
	enemySpeed = score/10 + 5
	return enemySpeed

def dropEnemies(enemyList):
	delay = random.random()
	if len(enemyList) < 10 and delay < 0.15:
		x_pos = random.randint(0,width-enemySize)
		y_pos = 0
		enemyList.append([x_pos, y_pos])

def drawEnemies(enemyList):
	for enemyPos in enemyList:
		pygame.draw.rect(screen, blue, (enemyPos[0], enemyPos[1], enemySize, enemySize))

def updateEnemyPositions(enemyList, score):
	for idx, enemyPos in enumerate(enemyList):
		if (enemyPos[1] >= 0) and (enemyPos[1] < height):
			enemyPos[1] += enemySpeed
		else:
			enemyList.pop(idx)
			score += 1
	return score

def collisionCheck(enemyList, playerPos):
	for enemyPos in enemyList:
		if detectCollision(enemyPos, playerPos):
			return True
	else:
		return False

def detectCollision(playerPos, enemyPos):
	#player Coordinates
	p_x = playerPos[0]
	p_y = playerPos[1]
	#enemy Coordinates
	e_x = enemyPos[0]
	e_y = enemyPos[1]
	#Collision clause
	if (e_x >= p_x and e_x < (p_x + playerSize)) or (p_x >= e_x and p_x < (e_x + enemySize)):
		if (e_y >= p_y and e_y < (p_y + playerSize)) or (p_y >= e_y and p_y < (e_y + enemySize)):
			return True
	return False

while not gameOver:
	for event in pygame.event.get():
		#Quit Event
		if event.type == pygame.QUIT:
			sys.exit()
		#Player Movement
		if event.type == pygame.KEYDOWN:
			x = playerPos[0]
			y = playerPos[1]
			if event.key == pygame.K_LEFT:
				x -= playerSize
			elif event.key == pygame.K_RIGHT:
				x += playerSize
			playerPos = [x,y]

	screen.fill(black)
	dropEnemies(enemyList)
	score = updateEnemyPositions(enemyList, score)
	enemySpeed = setLevel(score, enemySpeed)
	text = "Score" + str(score)
	label = myFont.render(text, 1, white)
	screen.blit(label, (width-200, height-40))

	if collisionCheck(enemyList, playerPos):
		gameOver = True
		print(gameOverMsg + str(score))
		break

	drawEnemies(enemyList)
	pygame.draw.rect(screen, red, (playerPos[0], playerPos[1], playerSize, playerSize))

	clock.tick(60)

	pygame.display.update()