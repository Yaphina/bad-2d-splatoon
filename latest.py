import pygame
from sys import exit

pygame.init()

class classMovement:

	def __init__(self):

		self.strDirectionFacing = "left"

		self.intStunTimer = 0

		self.intInkStored = 1000

		self.ultimateRectVertical = pygame.Rect((0, 0), (100, intScreenHeight))
		self.ultimateRectHorizontal = pygame.Rect((0, 0), (intScreenWidth, 100))

	def funcPosChange(self, intXChange, intYChange):

		if self.intInkStored > 1:

			self.intInkStored -= 1

		self.playerSpriteRect.x += intXChange
		self.playerSpriteRect.y += intYChange

		for wall in arrWalls:
			
			if self.playerSpriteRect.colliderect(wall.rect):

				if intXChange > 0:

					self.playerSpriteRect.right = wall.rect.left

				if intXChange < 0:

					self.playerSpriteRect.left = wall.rect.right

				if intYChange > 0:

					self.playerSpriteRect.bottom = wall.rect.top

				if intYChange < 0:

					self.playerSpriteRect.top = wall.rect.bottom

	def funcBoundryCheck(self):

		intScreenSize = pygame.display.get_window_size()

		if (self.playerSpriteRect.x < 0):

			self.playerSpriteRect.x = 0

		if (self.playerSpriteRect.y < 101):

			self.playerSpriteRect.y = 101

		if ((self.playerSpriteRect.right) > intScreenSize[0]):

			self.playerSpriteRect.x = intScreenSize[0] - self.playerSpriteRect.height

		if ((self.playerSpriteRect.bottom) > intScreenSize[1]):

			self.playerSpriteRect.y = intScreenSize[1] - self.playerSpriteRect.width

	def funcUltimateCountDown(self):

		if self.intUltCD > 0:

			self.intUltCD -= 1 

	def funcUltCollision(self,ultRect):

		if self == player1:

			if ultRect.colliderect(player2.playerSpriteRect):

				player2.intStunTimer = 300
		
		else:

			if ultRect.colliderect(player1.playerSpriteRect):

				player1.intStunTimer = 300

	def funcUltimate(self):

		if self.strDirectionFacing == "left":

			self.ultimateRectHorizontal.right = self.playerSpriteRect.left
			self.ultimateRectHorizontal.centery = self.playerSpriteRect.centery
			pygame.draw.rect(surfInkMap, self.inkColour, self.ultimateRectHorizontal)
			self.funcUltCollision(self.ultimateRectHorizontal)
			
		elif self.strDirectionFacing == "right":

			self.ultimateRectHorizontal.left = self.playerSpriteRect.right
			self.ultimateRectHorizontal.centery = self.playerSpriteRect.centery
			pygame.draw.rect(surfInkMap, self.inkColour, self.ultimateRectHorizontal)
			self.funcUltCollision(self.ultimateRectHorizontal)

		elif self.strDirectionFacing == "up":

			self.ultimateRectVertical.bottom = self.playerSpriteRect.top
			self.ultimateRectVertical.centerx= self.playerSpriteRect.centerx
			pygame.draw.rect(surfInkMap, self.inkColour, self.ultimateRectVertical)
			self.funcUltCollision(self.ultimateRectVertical)

		else:

			self.ultimateRectVertical.top = self.playerSpriteRect.bottom
			self.ultimateRectVertical.centerx= self.playerSpriteRect.centerx
			pygame.draw.rect(surfInkMap, self.inkColour, self.ultimateRectVertical)
			self.funcUltCollision(self.ultimateRectVertical)

		self.intInkStored -= 500
		self.intUltCD = 1500 #ult cd (fps * seconds), currently 60(fps) * 10 seconds

	def funcMove(self): # movement leads to diagnol movement to move more than 1 direction (need to consider)

		arrUserInput = pygame.key.get_pressed()

		intYChange = intXChange = 0	

		if self.intStunTimer > 0:

			self.intStunTimer -= 1
		
		else:

			if arrUserInput[pygame.K_q] and self.intInkStored < 1000 and surfInkMap.get_at(self.playerSpriteRect.center) == self.inkColour:

				self.intInkStored += 5

			else:

				arrUserInput = pygame.key.get_pressed()

				intYChange = intXChange = 2	

				if arrUserInput[pygame.K_w]:

					self.funcPosChange(0, -intYChange)
					self.strDirectionFacing = "up"

				if arrUserInput[pygame.K_s]:

					self.funcPosChange(0, intYChange)
					self.strDirectionFacing = "down"
				
				if arrUserInput[pygame.K_a]:

					self.funcPosChange(-intXChange, 0)
					self.strDirectionFacing = "left"

				if arrUserInput[pygame.K_d]:

					self.funcPosChange(intXChange, 0)
					self.strDirectionFacing = "right"

				if arrUserInput[pygame.K_e] and self.intInkStored > 500 and self.intUltCD == 0:

					self.funcUltimate()

				self.funcBoundryCheck()

				self.inkingRect.x = self.playerSpriteRect.x 
				self.inkingRect.y = self.playerSpriteRect.y

class classPlayer(classMovement):

	def __init__(self, intPosX, intPosY, inkColour):

		super().__init__()#when using super don't need to enter self into the brackets

		self.intUltCD = 600 #initial CD(fps * seconds)

		self.inkColour = inkColour

		self.intUltTimerTextPosX = 220
		self.intUltTimerTextPosY = 50

		self.intInkStoredTextPosX = 312
		self.intInkStoredTextPosY = 50

		self.surfPlayerSprite = pygame.image.load("assets/image/squid.png").convert_alpha()# specific in naming for sprite to work such image and rect
		self.surfPlayerSprite = pygame.transform.scale(self.surfPlayerSprite, (50, 50))

		self.arrSquidImageRotation = [self.surfPlayerSprite]

		for i in range(3):

			self.surfPlayerSprite = pygame.transform.rotate(self.surfPlayerSprite, -90)
			self.arrSquidImageRotation.append(self.surfPlayerSprite)

		self.surfPlayerSprite = pygame.transform.rotate(self.surfPlayerSprite, -90)#to keep image upright

		self.playerSpriteRect = self.surfPlayerSprite.get_rect(topleft = (intPosX, intPosY))

		self.inkingRect = self.playerSpriteRect.copy()

	def funcDisplayUltCDTimer(self):

		font = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)
		orange = (244, 122, 35)

		if self.intUltCD == 0:

			strUltTimerText = "Ready"

		else:

			strUltTimerText = str(int(self.intUltCD/60))

		surfText = font.render(strUltTimerText, True, orange)
		textRect = surfText.get_rect(topleft = (self.intUltTimerTextPosX, self.intUltTimerTextPosY))

		surfScreen.blit(surfText, textRect)

	def funcDisplayInkAmount(self):

		font = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)
		orange = (244, 122, 35)

		strText = str(int(self.intInkStored / 10)) + "%"

		surfText = font.render(strText, True, orange)
		textRect = surfText.get_rect(topleft = (self.intInkStoredTextPosX, self.intInkStoredTextPosY))

		surfScreen.blit(surfText, textRect)

	def funcPlayerUpdate(self):

		self.funcUltimateCountDown()

		self.funcMove()

		if self == player1:

			if self.strDirectionFacing == "up":

				self.surfPlayerSprite = self.arrSquidImageRotation[0]

			elif self.strDirectionFacing == "right":

				self.surfPlayerSprite = self.arrSquidImageRotation[1]
			
			elif self.strDirectionFacing == "down":

				self.surfPlayerSprite = self.arrSquidImageRotation[2]
			
			else:

				self.surfPlayerSprite = self.arrSquidImageRotation[3]

		if self.intInkStored > 1:

			pygame.draw.rect(surfInkMap, self.inkColour, self.inkingRect) # draw ink on the inkmap surface

		surfScreen.blit(surfInkMap, (0, 0))

		funcDrawWalls()

class classPlayer2(classPlayer):

	def __init__(self, intPosX, intPosY, inkColour):

		classMovement.__init__(self)

		self.intUltCD = 600 #initial CD(fps * seconds)

		self.inkColour = inkColour

		self.intUltTimerTextPosX = 720
		self.intUltTimerTextPosY = 50

		self.intInkStoredTextPosX = 543
		self.intInkStoredTextPosY = 50

		self.font = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)

		self.surfStunnedText = self.font.render("Stunned", True, "yellow")

		hedgehogStill = funcLoadImage(self, "assets/image/hedgehog_still.png")
		hedgehogWalk1 = funcLoadImage(self, "assets/image/hedgehog_walk_1.png")
		hedgehogWalk2 = funcLoadImage(self, "assets/image/hedgehog_walk_2.png")

		self.surfPlayerSprite = hedgehogStill
		self.playerSpriteRect = hedgehogStill.get_rect(topleft = (intPosX, intPosY))

		self.arrHedgehogWalkAnimation = [hedgehogStill, hedgehogWalk1, hedgehogStill, hedgehogWalk2]

		self.fltPlayerAnimationIndex = 0

		self.inkingRect = self.playerSpriteRect.copy()
		
	def funcMove(self): # movement leads to diagnol movement to move more than 1 direction (need to consider)
		arrUserInput = pygame.key.get_pressed()

		intYChange = intXChange = 2	

		if self.intStunTimer > 0: 

			self.intStunTimer -= 1
				
		else:

			if arrUserInput[pygame.K_l] and self.intInkStored < 1000 and surfInkMap.get_at(self.playerSpriteRect.center) == self.inkColour:

				self.intInkStored += 5

			else:

				if arrUserInput[pygame.K_UP]:

					self.funcPosChange(0, -intYChange)
					self.strDirectionFacing = "up"

				if arrUserInput[pygame.K_DOWN]:

					self.funcPosChange(0, intYChange)
					self.strDirectionFacing = "down"
				
				if arrUserInput[pygame.K_LEFT]:

					self.funcPosChange(-intXChange, 0)
					self.strDirectionFacing = "left"

				if arrUserInput[pygame.K_RIGHT]:

					self.funcPosChange(intXChange, 0)
					self.strDirectionFacing = "right"

				if arrUserInput[pygame.K_RSHIFT] and self.intInkStored > 500 and self.intUltCD == 0:

					self.funcUltimate()
					
				self.funcBoundryCheck()

				self.inkingRect.x = self.playerSpriteRect.x 
				self.inkingRect.y = self.playerSpriteRect.y
				
	def funcPlayerWalkAnimation(self):

		self.fltPlayerAnimationIndex += 0.1

		if self.fltPlayerAnimationIndex >= 4:

			self.fltPlayerAnimationIndex = 0

		self.surfPlayerSprite = self.arrHedgehogWalkAnimation[int(self.fltPlayerAnimationIndex)]

	def funcPlayerUpdate(self):

		self.funcPlayerWalkAnimation()# even function leave out self in a class

		super().funcPlayerUpdate()

class classWall():

	def __init__(self, intPosX, intPosY, intWidth, intHeight):

		arrWalls.append(self)

		self.rect = pygame.Rect(intPosX, intPosY, intWidth, intHeight)

def funcLoadImage(player, strImageAddress):

	image = pygame.image.load(strImageAddress).convert_alpha()
	image = pygame.transform.scale(image, (50, 50))

	return image

def funcPercentMapCoverage(colour):

	intTotalWallPixels = (50 * 100 * 2) + (50 * 200)

	intSurfaceSize = intScreenWidth * (intScreenHeight - 100)

	intNumberOfMatchingPixels = 0

	for intPosX in range(0, intScreenWidth):

		for intPosY in range(0, intScreenHeight - 100):

			if surfInkMap.get_at((intPosX, intPosY)) == colour:

				intNumberOfMatchingPixels += 1

	fltPercentMapCoverage = (intNumberOfMatchingPixels / (intSurfaceSize - intTotalWallPixels)) * 100

	return fltPercentMapCoverage

def funcGameTimer(intStartFrame):

	intTimeLapsed = int((pygame.time.get_ticks() - intStartFrame) / 1000)

	intCountDownTime = 120 - intTimeLapsed

	#arrUserInput = pygame.key.get_pressed()

	if intCountDownTime == 0:

		running = False

	else:

		running = True

	surfTime = fontInkFree50.render(str(intCountDownTime), False, (255, 255, 255))
	timeRect = surfTime.get_rect(center = (intScreenWidth/2, 50))

	surfScreen.blit(surfTime, timeRect)

	return running

def funcDrawWalls():

	for wall in arrWalls:

		pygame.draw.rect(surfInkMap, "grey", wall.rect)

def funcMenu():

	surfHowToPlay = pygame.image.load("assets/image/How to play.png").convert_alpha()
	surfScreen.blit(surfHowToPlay, (0, 0))

	running = True

	while running:

		clock.tick(60)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				pygame.quit()
				exit()

		arrUserInput = pygame.key.get_pressed()

		if arrUserInput[pygame.K_RETURN]:

			running = False

		elif arrUserInput[pygame.K_RIGHT]:

			surfHowToPlay = pygame.image.load("assets/image/How to play page 2.png").convert_alpha()

		elif arrUserInput[pygame.K_LEFT]:

			surfHowToPlay = pygame.image.load("assets/image/How to play.png").convert_alpha()

		surfScreen.blit(surfHowToPlay, (0, 0))

		pygame.display.flip()

def funcMainGame():

	intStartFrame = pygame.time.get_ticks()

	surfInkMap.fill("black")

	running = True

	while running:

		clock.tick(60)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				pygame.quit()
				exit()

		surfScreen.fill("black")

		player1.funcPlayerUpdate()

		player2.funcPlayerUpdate()

		surfScreen.blit(surfPlayerHUD, (0, 0))

		player1.funcDisplayUltCDTimer()
		player2.funcDisplayUltCDTimer()

		player1.funcDisplayInkAmount()
		player2.funcDisplayInkAmount()

		surfScreen.blit(player1.surfPlayerSprite, player1.playerSpriteRect)
		surfScreen.blit(player2.surfPlayerSprite, player2.playerSpriteRect)

		if player2.intStunTimer > 0:

			inkFreeFont = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)

			surfStunnedText = inkFreeFont.render("Stunned", True, "yellow")

			stunnedTextRect = surfStunnedText.get_rect(center = player2.playerSpriteRect.center)
			surfScreen.blit(surfStunnedText,stunnedTextRect)

		if player1.intStunTimer > 0:

			inkFreeFont = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)

			surfStunnedText = inkFreeFont.render("Stunned", True, "yellow")

			stunnedTextRect = surfStunnedText.get_rect(center = player1.playerSpriteRect.center)
			surfScreen.blit(surfStunnedText,stunnedTextRect)


		running = funcGameTimer(intStartFrame)

		pygame.display.flip()

def funcDisplayText(strText, intPosX, intPosY, font):

	surfText = font.render(strText, True, "white")
	textRect = surfText.get_rect(center = (intPosX, intPosY))

	surfScreen.blit(surfText, textRect)

def funcEndOfGame(surfInkMap):

	running = True
	surfEndScreen = pygame.image.load("assets/image/end screen.png").convert_alpha()

	surfScreen.blit(surfEndScreen, (0, 0))

	#fontInkFree20 = pygame.font.Font("assets/fonts/INKFREE.TTF", 20)

	fltPlayerPercentCoverage = round(funcPercentMapCoverage(player1.inkColour), 2)
	fltPlayer2PercentCoverage = round(funcPercentMapCoverage(player2.inkColour), 2)

	#strPlayerPercentCoverageText = "Pink player map coverage is {0}%".format(str(fltPlayerPercentCoverage))
	#strPlayer2PercentCoverageText = "Light blue player map coverage is {0}%".format(str(fltPlayer2PercentCoverage))

	#funcDisplayText(strPlayerPercentCoverageText, 200, 50, fontInkFree20)
	#funcDisplayText(strPlayer2PercentCoverageText, 700, 50, fontInkFree20)
	player1.surfPlayerSprite = player1.arrSquidImageRotation[0]

	player2.surfPlayerSprite = player2.arrHedgehogWalkAnimation[0]
	player2SpriteRect = player2.surfPlayerSprite.get_rect()

	if fltPlayerPercentCoverage > fltPlayer2PercentCoverage:

		#strWinnerText = "pink player wins!!!"
		player1.playerSpriteRect.bottom = 460
		player1.playerSpriteRect.centerx = 480

		surfScreen.blit(player1.surfPlayerSprite, player1.playerSpriteRect)

		player2SpriteRect.bottom = 510
		player2SpriteRect.centerx = 390

		surfScreen.blit(player2.surfPlayerSprite, player2SpriteRect)

	elif fltPlayerPercentCoverage < fltPlayer2PercentCoverage:

		player1.playerSpriteRect.bottom = 510
		player1.playerSpriteRect.centerx = 390

		surfScreen.blit(player1.surfPlayerSprite, player1.playerSpriteRect)

		player2SpriteRect.bottom = 460
		player2SpriteRect.centerx = 480

		surfScreen.blit(player2.surfPlayerSprite, player2SpriteRect)

		#strWinnerText = "light blue player wins!!!"

	surfHUD = pygame.image.load("assets/image/HUD.png").convert_alpha()

	surfInkMap.blit(surfHUD, (0, 0))

	surfInkMap = pygame.transform.scale(surfInkMap, (300, 200))
	
	surfScreen.blit(surfInkMap, (333, 87))
	#funcDisplayText(strWinnerText, intScreenWidth/2, intScreenHeight/2, pygame.font.Font("assets/fonts/INKFREE.TTF", 80))

	while running:

		clock.tick(60)

		#for loop to prevent crashing and for quiting
		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				pygame.quit()
				exit()

		pygame.display.flip()

fontInkFree50 = pygame.font.Font("assets/fonts/INKFREE.TTF", 50)

pygame.display.set_caption("splatoon 2d")

intScreenWidth = 900
intScreenHeight = 600

surfScreen = pygame.display.set_mode((intScreenWidth, intScreenHeight))

lightBlue = (66, 230, 245)

pink = (252, 89, 255)

surfInkMap = pygame.Surface((intScreenWidth, intScreenHeight))

surfPlayerHUD = pygame.image.load("assets/image/PlayerHUD.png").convert_alpha()
rectPlayerHUD = surfPlayerHUD.get_rect()

intPlayer1StartPosX = 20
intPlayer1StartPosY = 120

intPlayer2StartPosX = 830
intPlayer2StartPosY = 530

player1 = classPlayer(intPlayer1StartPosX, intPlayer1StartPosY, pink)
player2 = classPlayer2(intPlayer2StartPosX, intPlayer2StartPosY, lightBlue)

arrWalls = []

classWall(200, 100, 50, 100)
classWall(700, 500, 50, 100)
classWall(425, 250, 50, 200)

clock = pygame.time.Clock()

funcMenu()

funcMainGame()

funcEndOfGame(surfInkMap)