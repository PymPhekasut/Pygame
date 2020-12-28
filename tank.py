#tank.py
import pygame
import os
import random

#geometry
WIDTH = 500
HEIGHT = 600
FPS = 30 #30 frame rate/s

#color picker
BLACK =(0, 0, 0)
WHITE =(255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (51, 242, 99)
CREAM = (247, 173, 54)

#Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #setting screen
background = pygame.image.load('battle2.jpg')
pygame.display.set_caption('Army Tank')
clock = pygame.time.Clock()









######Create tank######
game_folder = os.path.dirname(__file__)
#C:\Users\neera\Desktop\Python_Project\Pygame
img_folder = os.path.join(game_folder,'img')
#C:\Users\neera\Desktop\Python_Project\Pygame\img


print(game_folder)

class Tank(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image = pygame.Surface((50,40)) #initial setting
		sub_img = os.path.join(img_folder,'tankNavy.png')
		self.image = pygame.image.load(sub_img).convert()
		self.image.set_colorkey(BLACK) #cut off background colory of image
		#self.image.fill(BLUE) #initial setting
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2 
		self.rect.bottom = HEIGHT - 10

		self.speedx = 0
		self.speedy = 0

	def update(self):
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -5

		if keystate[pygame.K_RIGHT]:
			self.speedx = 5

		if keystate[pygame.K_UP]:
			self.speedy = -5

		if keystate[pygame.K_DOWN]:
			self.speedy = 5


		self.rect.x += self.speedx
		self.rect.y += self.speedy

		 #set moving within frame

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH

		if self.rect.left < 0:
			self.rect.left = 0

		print(self.rect.centerx)

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		sub_img = os.path.join(img_folder,'tank.png')
		self.image = pygame.image.load(sub_img).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width) #random
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,5)

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 6:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(2,5)


class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		sub_img = os.path.join(img_folder,'bullet.png')
		self.image = pygame.image.load(sub_img).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y 
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()
		

#sprite is a player
all_sprites = pygame.sprite.Group()
tank = Tank() # Add tank
all_sprites.add(tank)

enemys = pygame.sprite.Group()

bullets = pygame.sprite.Group() 

for i in range(10): #amount of enemy
	em = Enemy()
	all_sprites.add(em)
	enemys.add(em)



running = True 

while running:
	clock.tick(FPS)

	for event in pygame.event.get():
		#check for closing
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				tank.shoot()

	all_sprites.update()

	#check hits enemy
	hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
	if hits:
		em = Enemy()
		all_sprites.add(em)
		enemys.add(em)


	hits = pygame.sprite.spritecollide(tank, enemys, False)
	if hits:
		running = False


	screen.fill((0,0,0))
	screen.blit(background, (0,0))
	all_sprites.draw(screen)
	pygame.display.flip()


	

pygame.quit()
