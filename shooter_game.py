#Импортируем PyGame и randint
#Importing PyGame and randint
from pygame import * #PyGame
from random import randint #randint

#Текст
#Text
font.init() #"Конструктор" текста #The "constructor" of the text
font2 = font.SysFont('Arial',25) #Счетчики и прочий текст в окне программы #Counters and other text in the program window
font1 = font.SysFont('Arial',80) #Победа/Проигрыш #Victory/Loss
winner = font1.render('ПОБЕДА!', True, (168,228,160)) #Текст "ПОБЕДА!" #The text "VICTORY!"
lose = font1.render('ПРОИГРЫШ!', True, (227,38,54)) #Текст "ПРОИГРАЛ!" #The text "LOST!"

height = 500 #Значение высоты. Используется в некоторых классах #Height value. Used in some classes

#Создаем супер-класс GameSprite для создания персонажей
#Creating a super GameSprite class to create characters
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__() #Супер-класс #Super class
        self.image = transform.scale(image.load(sprite_image),(size_x,size_y)) #Изображение и размер #Image and size
        self.speed = sprite_speed #Скорость #Speed
        self.rect = self.image.get_rect() #Изображение #Image
        self.rect.x = sprite_x #Координаты x #X coordinates
        self.rect.y = sprite_y #Координаты y #Y coordinates

    #Отображение созданных нами объектов
    #Display of objects created by us
    def visibility(self):
        okno.blit(self.image,(self.rect.x, self.rect.y)) #Отображение объектов в окне

#Создаем дочерний класс супер-класса GameSprite для управления персонажем
#Creating a child class of the GameSprite super class to control the character
class Rocet(GameSprite):
    #Управление по нажатию на кнопки
    #Control by pressing the buttons
    def move(self):
        keys = key.get_pressed()
        #Условия
        #Conditions
        if keys[K_a] and self.rect.x >5: 
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 615:
            self.rect.x += self.speed
    #Система стрельбы по нажатию кнопки "SPACE"
    #Firing system by pressing the "SPACE" button
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 12,20,-15) #Пуля #Bullet
        bullets.add(bullet)

#Дочерний класс супер-класса GameSprite для счетчика пропущенных врагов
#Child class of the GameSprite super class for the missed enemies counter
class Enemy(GameSprite):
    #Счетчик пропущенных врагов
    #Counter of missed enemies
    def update(self):
        self.rect.y += self.speed
        global lost #Глобальная переменная lost #Global variable lost
        #Условия работы счетчика
        #Counter working conditions
        if self.rect.y > height: 
            self.rect.x = randint(100,600)
            self.rect.y = 0
            lost = lost + 1

#Создаем дочерний класс супер-класса GameSprite для пуль
#Creating a child class of the GameSprite super class for bullets
class Bullet(GameSprite):
    #Передвижение пуль
    #Movement of bullets
    def update(self): 
        self.rect.y += self.speed
        #Условия убийства
        #Murder conditions
        if self.rect.y < 0:
            self.kill()

#Создание окна и фон
#Create window and background
okno = display.set_mode((700,500)) #Размеры окна #Window dimensions
display.set_caption('Shooter') #Название приложения #Application Name
fon = transform.scale(image.load('galaxy.jpg'),(700,500)) #Фон #Background
pablo = Rocet('rocket.png',5, 400,80,100,20) #Создание самой управляемой ракеты #Creating the most guided missile

#Фоновая музыка
#Background music
mixer.init() #"Конструктор" музыки #"Constructor" of music
mixer.music.load('space.ogg') #Загрузка музыки "space.ogg" #Download music "space.ogg"
mixer.music.play() #Воспроизведение музыки #Play music
fire_mus = mixer.Sound('fire.ogg') 

#Создание групп пуль и спрайтов
#Creating groups of bullets and sprites
enemyes = sprite.Group() #Группа врагов #Group of enemies
bullets = sprite.Group() #Группа пуль #Group of bullets

#Рандомный спавн врагов
#Random spawn of enemies
for i in range(1,6):
    bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
    enemyes.add(bot)

#FPS и значения (переменные) счетчиков
#FPS and counter values (variables)
FPS = 45 #FPS
game = True #Статус игры (При game = False игра закроется) #Game status (If game = False, the game will close)
win = False #Статус победы (При win = True выведет надпись "ПОБЕДА!") #Victory status (If win = True, it will display the inscription "VICTORY!")
score = 0 #Счетчик "Счет:" #Counter "Account:"
lost = 0 #Счетчик "Пропущено:" #Counter "Skipped:"

#Игровой цикл
#Game cycle
while game:
    #Выход из игры при закрытии окна
    #Exit the game when the window is closed
    for e in event.get():
        if e.type == QUIT:
            game = False
        #Система стрельбы по нажатию кнопки "SPACE"
        #Firing system by pressing the "SPACE" button
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pablo.fire()
    
    if not win:
        okno.blit(fon,(0,0))
        pablo.visibility()
        pablo.move()
        enemyes.update()
        bullets.update()
        enemyes.draw(okno)
        bullets.draw(okno)
        
        #Столкновения спрайтов с пулями
        #Sprite collisions with bullets
        collides = sprite.groupcollide(enemyes, bullets, True, True)
        for col in collides:
            score += 1
            bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
            enemyes.add(bot)
        
        #Условия победы и (или) проигрыша
        #Winning and (or) losing conditions
        if sprite.spritecollide(pablo, enemyes, False) or lost >= 3:
            win = True
            okno.blit(lose, (180,210))
        
        if score >= 10:
            win = True
            okno.blit(winner, (180,210))
        
        #Cчетчики "Счет:" и "Пропущено:"
        #Counters "Account:" and "Missed:"
        text = font2.render('Счёт:'+str(score),1 ,(200,200,200)) #Счетчик "Счет:" #Counter "Account:"
        okno.blit(text,(10,20))
        text_p = font2.render('Пропущено:'+str(lost),1 ,(200,200,200)) #Счетчик "Пропущено:" #Counter "Skipped:"
        okno.blit(text_p,(10,40))
    
    #Перезапуск игры в случае проигрыша или победы
    #Restarting the game in case of loss or victory
    else:
        win = False #Статус победы (проиграл) #Victory Status (lost)
        #Сбрасываются значения счетчиков
        #Counter values are reset
        score = 0 #Счетчик "Счет:" #Counter "Account:"
        lost = 0 #Счетчик "Пропущено:" #Counter "Skipped:"
        
        #Перезапуск циклов for
        #Restarting for loops
        for b in bullets:
            b.kill()
        
        for en in enemyes:
            en.kill()
        time.delay(300)
        
        for i in range(1,6):
            bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
            enemyes.add(bot)

    #Отображение интерфейса программного обеспечения
    #Software interface display
    display.update()
    time.delay(FPS)
