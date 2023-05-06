#Импортируем PyGame и randint
from pygame import * #PyGame
from random import randint #Рандомайзер

#Текст
font.init() #"Конструктор" текста
font2 = font.SysFont('Arial',25) #Счетчики и прочий текст в окне программы
font1 = font.SysFont('Arial',80) #Победа/Проигрыш
winner = font1.render('ПОБЕДА!', True, (168,228,160)) #Текст "ПОБЕДА!"
lose = font1.render('ПРОИГРЫШ!', True, (227,38,54)) #Текст "ПРОИГРАЛ!"

height = 500 #Значение высоты. Используется в некоторых классах

#Создаем супер-класс GameSprite для создания персонажей
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__() #Супер-класс
        self.image = transform.scale(image.load(sprite_image),(size_x,size_y)) #Изображение и размер
        self.speed = sprite_speed #Скорость
        self.rect = self.image.get_rect() #Изображение
        self.rect.x = sprite_x #Координаты x
        self.rect.y = sprite_y #Координаты y

    #Отображение созданных нами объектов
    def visibility(self):
        okno.blit(self.image,(self.rect.x, self.rect.y)) #Отображение объектов в окне

#Создаем дочерний класс супер-класса GameSprite для управления персонажем
class Rocet(GameSprite):
    #Управление по нажатию на кнопки
    def move(self):
        keys = key.get_pressed()
        #Условия
        if keys[K_a] and self.rect.x >5: 
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 615:
            self.rect.x += self.speed
    #Система стрельбы по нажатию кнопки "SPACE"
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 12,20,-15) #Пуля
        bullets.add(bullet)

#Дочерний класс супер-класса GameSprite для счетчика пропущенных врагов
class Enemy(GameSprite):
    #Счетчик пропущенных врагов
    def update(self):
        self.rect.y += self.speed
        global lost #Глобальная переменная lost
        #Условия работы счетчика
        if self.rect.y > height: 
            self.rect.x = randint(100,600)
            self.rect.y = 0
            lost = lost + 1

#Создаем дочерний класс супер-класса GameSprite для пуль 
class Bullet(GameSprite):
    #Передвижение пуль
    def update(self): 
        self.rect.y += self.speed
        #Условия убийства
        if self.rect.y < 0:
            self.kill()

#Создание окна и фон
okno = display.set_mode((700,500)) #Размеры окна
display.set_caption('Shooter') #Название приложения
fon = transform.scale(image.load('galaxy.jpg'),(700,500)) #Фон
pablo = Rocet('rocket.png',5, 400,80,100,20) #Создание самой управляемой ракеты

#Фоновая музыка
mixer.init() #"Конструктор" музыки
mixer.music.load('space.ogg') #Загрузка музыки "space.ogg"
mixer.music.play() #Воспроизведение музыки
fire_mus = mixer.Sound('fire.ogg') 

#Создание групп пуль и спрайтов
enemyes = sprite.Group() #Группа врагов
bullets = sprite.Group() #Группа пуль

#Рандомный спавн врагов
for i in range(1,6):
    bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
    enemyes.add(bot)

#FPS и значения (переменные) счетчиков
FPS = 45 #FPS
game = True #Статус игры (При game = False игра закроется)
win = False #Статус победы (При win = True выведет надпись "ПОБЕДА!")
score = 0 #Счетчик "Счет:"
lost = 0 #Счетчик "Пропущено:"

#Игровой цикл
while game:
    #Выход из игры при закрытии окна
    for e in event.get():
        if e.type == QUIT:
            game = False
        #Система стрельбы по нажатию кнопки "SPACE"
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pablo.fire()
    
    #Отображается до победы
    if not win:
        okno.blit(fon,(0,0))
        pablo.visibility()
        pablo.move()
        enemyes.update()
        bullets.update()
        enemyes.draw(okno)
        bullets.draw(okno)
        
        #Столкновения спрайтов с пулями
        collides = sprite.groupcollide(enemyes, bullets, True, True)
        for col in collides:
            score += 1
            bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
            enemyes.add(bot)
        
        #Условия победы и (или) проигрыша
        if sprite.spritecollide(pablo, enemyes, False) or lost >= 3:
            win = True
            okno.blit(lose, (180,210))
        
        if score >= 10:
            win = True
            okno.blit(winner, (180,210))
        
        #Cчетчики "Счет:" и "Пропущено:"
        text = font2.render('Счёт:'+str(score),1 ,(200,200,200)) #Счетчик "Счет:"
        okno.blit(text,(10,20))
        text_p = font2.render('Пропущено:'+str(lost),1 ,(200,200,200)) #Счетчик "Пропущено:"
        okno.blit(text_p,(10,40))
    
    #Перезапуск игры в случае проигрыша
    else:
        win = False #Статус победы (проиграл)
        #Сбрасываются значения счетчиков
        score = 0 #Счетчик "Счет:"
        lost = 0 #Счетчик "Пропущено:"
        
        #Перезапуск циклов for
        for b in bullets:
            b.kill()
        
        for en in enemyes:
            en.kill()
        time.delay(300)
        
        for i in range(1,6):
            bot = Enemy('ufo.png',randint(100,600),5,80,50,randint(5,10))
            enemyes.add(bot)

    #Отображение интерфейса программного обеспечения
    display.update()
    time.delay(FPS)