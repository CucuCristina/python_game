#sprite

import pygame
from setting import *
#initializeaza modul de fonturi din cadrul Pygame
pygame.font.init()
#CREEARE OBIECTE GRAFICE
#class Tile mosteneste de la clasa pygame.sprite.Sprite 
#obiectele create in aceasta clasa vor avea caracteristicile unei sprite-uri pygame si pot fi adaugate la grupuri de sprite-uri 
class Tile(pygame.sprite.Sprite):
    #x,y - coordonate, sprite-ului de pe ecran; game-obiectul jocului; text- text afisat de sprite
    def __init__ (self, game, x, y, text):
        self.groups = game.all_sprites
        #se apeleaza constructorul clasei de baza cu grupul de sprite-uri pt a adauga obiectul curent la acest grup
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #se creaza o suprafata pt imaginea sprite-ului, de dim. tilesize*tilesize
        self.image=pygame.Surface((TILESIZE,TILESIZE))
        #stocam coordonatele x si y in variabilele de instanta
        self.x=x
        self.y=y
        self.text=text
        #creaza un obiect de tip dreptunghi pt sprite bazat pe dimensiunile imaginii
        self.rect=self.image.get_rect()
        if self.text!= "empty":
            #crearea unui obiect de tip font 
            self.font=pygame.font.SysFont("Calibri",50)
            #crearea unei suprafate de text , utilizand fontul si textul 
            font_surface= self.font.render(self.text, True, BLACK)
            #se umple suprafata sprite-ului
            self.image.fill(WHITE)
            #se obtine dimensiunea textului pt a pozitiona corect textul in cadrul sprite-ului
            self.font_size=self.font.size(self.text)
            #se adauga suprafata de text la suprafata sprite-ului la poz specificata de coordonate
            self.image.blit(font_surface,(self.x,self.y))
            #acesta este un mod de a crea si afisa spriteuri de text intr-un joc pygame

    
#POZITIA
#metoda actualizeaza pozitia dreptunghiului in functie de coordonatele x si y ale obiectului tile
    def update(self):
        #determina exact coordonata 
        self.rect.x=self.x * TILESIZE
        self.rect.y=self.y * TILESIZE
#metoda verifica daca un punct dat de coordonate (mouse_x, mouse_y) se afla in interiorul dreptunghiului
    def click(self, mouse_x, mouse_y):
        #pozitia mouseului in interiorul patratului 
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    #verifica daca sprite-ul se poate deplasa in dreapta 
    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE
    #verifica daca sprite-ul se poate deplasa in stanga 
    def left(self):
        return self.rect.x - TILESIZE >=0
    #verifica daca sprite-ul se poate deplasa in sus 
    def up(self):
        return self.rect.y -TILESIZE >=0
    #verifica daca sprite-ul se poate deplasa in jos
    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE
    #metode utile pentru a verifica si gestiona intercatiuniile jucatorului cu sprite-urile
    #verificarea clickurilor de mouse si a posibilitatilor de deplasare in diferite directii        

#INTERFATA
class UIElement:
    def __init__(self, x, y, text):
        self.x=x
        self.y=y
        self.text=text
    #deseneaza elementul de interfata pe ecran; primeste un obiect de tip ecran ca parametru
    def draw(self, screen):
        #se creaza un obiect de tip font si este initializat
        font=pygame.font.SysFont("Calibri", 30)
        #se creaza o suprafata de text utilizand fontul creat
        text= font.render(self.text, True, WHITE)
        #se plaseaza suprafata de text in pozitia specificata de coord. pe ecran
        screen.blit(text, (self.x, self.y))

#CREARE BUTON
class Button:
    #x,y-coordonatele butonului; width,height-latime si inaltime; text-textul afisat pe buton; colour-culoarea butonului; textcol-culoarea textului
    def __init__(self, x, y, width, height, text, colour, textcol):
        self.colour, self.textcol =colour, textcol
        self.width, self.height=width, height
        self.x, self.y= x,y
        self.text=text
    #responsabila pentru desenarea butonului
    def draw(self, screen):
        #definim butoanele ca un dreptunghi
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font=pygame.font.SysFont("Calibri", 30)
        text=font.render(self.text, True, self.textcol)
        self.font_size=font.size(self.text)
        #asezarea in mijloc a textului butoanelor
        draw_x=self.x+(self.width/2)-self.font_size[0]/2
        draw_y=self.y+(self.height/2)-self.font_size[1]/2
        screen.blit(text, (draw_x, draw_y))
#metoda verifica daca un punct dat de coordonate (mouse_x, mouse_y) se afla in interiorul butonului
    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x+self.width and self.y <= mouse_y <= self.y+self.height
    
                         
            
        
        
        
         
     
