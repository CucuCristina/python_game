#main

import pygame
import random
import time
#din cele doua proiecte vom importa tot continutul
from sprite import *
from setting import *

class Game:
    #Inițializarea Pygame și setarea variabilelor de stare ale jocului
    def __init__(self):
        pygame.init()
        #seteaza marimile ferestrei de joc
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        #seteaza titlul joc
        pygame.display.set_caption(title)
        self.clock=pygame.time.Clock()
        self.shuffle_time=0
        self.start_shuffle=False
        #variabila de instata ce salveaza ultima pozitie a directiei 
        #se utilizeaza in metoda shuffle
        self.previous_choice=""
        self.start_game= False
        self.start_timer=False
        #tine evidenta timpului scurs in joc
        self.elapsed_time=0
        #scorul este pastrat intr o variabila de instanta a clasei
        self.high_score=float(self.get_high_score()[0])

    def get_high_score(self):
        with open("high_score.txt", "r") as file:
            #citeste continutul din fisierul text si trateaza elementele sub forma unei liste
            scores= file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            #scrie in fisierul text scorul cu 3 zecimale
            file.write(str("%.3f\n" % self.high_score))

    # Metodă pentru a crea configurația inițială a puzzle-ului
    def create_game(self):
        #construim o lista bidimensionala avand "GAME_SIZE" linii si coloane
        #for x in range(1, GAME_SIZE + 1) itereaza elementele fiecarui rand pornind de la primul pana la marimea lui "GAME_SIZE"
        #for y in range(GAME_SIZE) itereaza prin randurile listei bidimensionale
        grid=[[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        #seteaza ultimul element al ultimului rand al matricei cu 0
        #valoarea 0 este folosita pentru a reprezenta spatiul gol
        grid[-1][-1]=0
        return grid
    
    #Metoda pentru a amesteca piesele in joc
    def shuffle(self):
        #creaza o lista goala care va contine directiile valide in care piesele vor fi mutate
        possible_moves=[]
        #bucla externa care parcurge fiecare rand
        for row, tiles in enumerate(self.tiles):
            #bucla interna care parcurge fiecare piesa din randul curent
            for col, tile in enumerate(tiles):
                #verifica daca piesa curenta este piesa goala
                if tile.text == "empty":
                    #se verifica posibilitatea de a muta in fiecare directie
                    #daca o directie este posibila, aceasta se adauga in lista
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            #daca s-au gasit directii valide de mutare, se iese din buclele de iterare
            if len(possible_moves) > 0:
                break
            #pentru fiecare directie anterioara gasita, se va sterge directia opusa pentru a se evita amestecarea pieselor din acelasi loc de unde au plecat 
        if self.previous_choice=="right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice=="left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice=="up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice=="down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves
        #se alege aleatoriu o directie din lista
        choice= random.choice(possible_moves)
        self.previous_choice=choice
        #se efectueaza schimbul de pozitii intre piesa goala si piesa adiacentă in directia aleasă
        if choice =="right":
            self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1],self.tiles_grid[row][col]
        elif choice =="left":
            self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1],self.tiles_grid[row][col]
        elif choice =="up":
            self.tiles_grid[row][col], self.tiles_grid[row-1][col] = self.tiles_grid[row-1][col],self.tiles_grid[row][col]
        elif choice =="down":
            self.tiles_grid[row][col], self.tiles_grid[row+1][col] = self.tiles_grid[row+1][col],self.tiles_grid[row][col]


    #metoda pentru a desena piesele in fereasta de joc
    def draw_tiles(self):
        #lista ce va contine piesele jocului
        self.tiles = []
        #bucla externa care itereaza prin fiecare rand al matricei
        for row, x in enumerate(self.tiles_grid):
            #se adauga un nou rand in lista tiles pentru fiecare rand al matricei tiles_grid
            self.tiles.append([])
            #bucla interna care itereaza prin fiecare piesa din randul curent al matricei tiles_grid
            for col, tile in enumerate(x):
                #se verifica daca valoarea piesei nu este 0
                if tile != 0:
                    #se creaza un obiect Tile si se adauga la randul corespunzator din lista tiles
                    #se paseaza instanta curenta a clasei, coordonatele coloanei si randului si textul care va fi afisat pe piesa
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    #se creaza un obiect Tile cu textul empty si se adauga la lista tiles
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    #metoda pentru a initializa un joc nou 
    def new(self):
        #se creeaza un obiect de tipul group din modulul pygame.sprite (este folosita pt a organiza si manipula obiecte grafice) 
        self.all_sprites = pygame.sprite.Group()
        #se intializeaza tiles_grid o noua configuratie de piese generata prin apelul metodei create_game
        self.tiles_grid= self.create_game()
        self.tiles_grid_completed= self.create_game()
        #tine evidenta timpului scurs in joc, acesta se intializeaza cu valoarea 0
        self.elapsed_time=0
        #indica daca cronometrul jocului a inceput sau nu
        self.start_timer=False
        #indica daca jocul a inceput sau nu
        self.start_game=False
        #se creaza o lista de butoane si se adauga un obiect de tip Button pentru a forma butoanele de shuffle si reset
        self.buttons_list=[]
        self.buttons_list.append(Button(775,100,200,50, "Shuffle",WHITE, BLACK))
        self.buttons_list.append(Button(775,170,200,50, "Reset",WHITE, BLACK))
        self.draw_tiles()

    
    def run(self):
        #atribut folosit pentru a controla daca jocul este in desfasurare sau nu
        self.playing =True
        while self.playing:
            #asigura ca bucla de joc ruleaza cu o viteza constanta
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
            

    def update(self):
        #verifica daca jocul a inceput
        if self.start_game:
            #verifica daca configuratia actuala a pieselor este identica cu configuratia pieselor initiala
            if self.tiles_grid==self.tiles_grid_completed:
                #daca jocul a fost rezolvat, se dezactiveaza starea de joc
                self.start_game = False
                #daca scorul are o valoare anterioara se actualizeaza cu valoarea minima dintre timpul curent si scorul anterior
                if self.high_score>0:
                    self.high_score=self.elapsed_time if self.elapsed_time <self.high_score else self.high_score
                else:
                     ##daca scorul acumulat este mai mare decat 0 acesta se modifica doar in cazul in care scorul acumulat este mai mare decat cel inregstrat
                     self.high_score=self.elapsed_time
                self.save_score()
            #verifica daca cronometrul  jocului trebuie pornit
            if self.start_timer:
                self.timer=time.time()
                #dezactiveaza starea de pornire a cronometrului
                self.start_timer=False
                #calculeaza timpul scurs de la ultima pornire a cronometrului
            self.elapsed_time=time.time() - self.timer
        #verifica daca procesul de amestecare a pieselor este in curs de realizare 
        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            #incrementeaza un contor de timp pentru amestecare
            self.shuffle_time +=1
            #daca amestecarea a durat 120 de cadre la o rata de 60 FPS
            if self.shuffle_time>120:
                #dezactiveaza starea de amestecare
                self.start_shuffle =False
                #activeaza starea de joc
                self.start_game=True
                #activeaza cronometrul
                self.start_timer=True
        #apeleaza metoda update pe toate obiectele sprite
        self.all_sprites.update()
        

    #metoda ce creeaza o retea de linii verticale si orizontale pentru a forma o grila pe ecran
    def draw_grid(self):
        #asigura ca linia de inceput si sfarsit a grilei este corespunzatoare
        for row in range(-1,GAME_SIZE * TILESIZE, TILESIZE):
            #deseneaza linii pe ecran conform parametrilor specificati
            #row,0 - coordonatele de inceput ale liniei pe axa x si y
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0),(row, GAME_SIZE * TILESIZE))
        for col in range(-1,GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE,col))
    
    def draw(self):
        #setarea culoriii de fundal
        self.screen.fill(BGCOLOUR)
        #desenarea obiectelor grafice pe ecran
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        #desenarea butoanelor pe ecran
        for button in self.buttons_list:
            button.draw(self.screen)
        #scrierea timpului pe ecran
        UIElement(825, 35,"%.3f" % self.elapsed_time).draw(self.screen)
        #scrierea scorului pe ecran (daca acesta este 0, adica nu s a inregistrat niciun castig, se va scrie 0 pe ecran)
        UIElement(710, 380,"High Score - %.3f " % (self.high_score if self.high_score>0 else 0) ).draw(self.screen)
        #metoda pentru a actualiza continutul ecranului afisat 
        pygame.display.flip()

    
    def events(self):
        #bucla care itereaza prin toate evenimentele inregistrate de pygame
        for event in pygame.event.get():
            #inchiderea ferestrei jocului
            if event.type==pygame.QUIT:
                pygame.quit()
                quit(0)
            #verifica daca evenimentul implica apasarea unui buton al mouse-ului
            if  event.type == pygame.MOUSEBUTTONDOWN:
                #obtine coordonatele actuale ale mouse-ului
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        #verifica daca coordonatele mouse-ului se afla in interiorul zonei ocupate de piesa
                        if tile.click(mouse_x, mouse_y):
                            #mutam piesele in dreapta
                            if tile.right()and self.tiles_grid[row][col+1]==0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col+1] = self.tiles_grid[row][col+1],self.tiles_grid[row][col]
                            #mutam piesele in stanga
                            if tile.left()and self.tiles_grid[row][col-1]==0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col-1] = self.tiles_grid[row][col-1],self.tiles_grid[row][col]
                            #mutam piesele in sus
                            if tile.up()and self.tiles_grid[row-1][col]==0:
                                self.tiles_grid[row][col], self.tiles_grid[row-1][col] = self.tiles_grid[row-1][col],self.tiles_grid[row][col]
                            #mutam piesele in jos
                            if tile.down()and self.tiles_grid[row+1][col]==0:
                                self.tiles_grid[row][col], self.tiles_grid[row+1][col] = self.tiles_grid[row+1][col],self.tiles_grid[row][col] 
                            self.draw_tiles()
                #itereaza prin lista de butoane a jocului
                for button in self.buttons_list:
                    ##verifica daca coordonatele mouse-ului se afla in interiorul zonei ocupate de buton
                    if button.click(mouse_x, mouse_y):
                        #realizeaza comenzile speciale pentru fiecare tip de buton
                        if button.text=="Shuffle":
                            self.shuffle_time=0
                            self.start_shuffle= True
                        if button.text=="Reset":
                            self.new()
                           
#construim un obiect de tip game
game = Game()

while True:
    game.new()
    game.run()
    
