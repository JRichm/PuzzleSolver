import pygame
import easygui

class Solver:
    def __init__(self):
        self.menu_surface = pygame.Surface((1280, 720))
        self.menu_surface.fill('white')    
        new_image_button = Button(self, (100, 100), 'new', open_new_puzzle)
        self.buttons = [new_image_button]

    def show_puzzle(self, image_url):
        print(image_url)

    def show(self, window):
        window.blit(self.menu_surface, (0, 0))
        for button in self.buttons:
            button.check_hover(pygame.mouse.get_pos())


class Button:
    def __init__(self, solver, position, text, function):
        self.function = function
        self.menu_surface = solver.menu_surface
        self.solver = solver
        self.position = position
        self.hovering = False
        self.text = text
        self.button_square = pygame.Surface((100, 35))
        self.button_square.fill('black')
        self.button_square.fill('white', ((1, 1), (98, 33)))
        self.clicked = False

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.render_text = self.font.render(self.text, True, (0,0,0), (255,255,255))

        self.menu_surface.blit(self.button_square, position)
        self.menu_surface.blit(self.render_text, (position[0] + 1, position[1] + 1))

        self.cords = position
        self.max_cords = (position[0] + self.button_square.get_width(), position[1] + self.button_square.get_height())

    def check_hover(self, mouse_cords):
        if (mouse_cords[0] > self.cords[0] and mouse_cords[0] < self.max_cords[0] and mouse_cords[1] > self.cords[1] and mouse_cords[1] < self.max_cords[1]):
            if pygame.mouse.get_pressed()[0] and not self.hovering:
                return

            if not self.hovering:
                print('start hovering')
                self.hovering = True
                self.render_text = self.font.render(self.text, True, (0,0,0), (222,222,222))
                self.button_square.fill((222,222,222), ((1, 1), (98, 33)))
                self.menu_surface.blit(self.button_square, self.position)
                self.menu_surface.blit(self.render_text, (self.position[0] + 1, self.position[1] + 1))

            elif pygame.mouse.get_pressed()[0]:
                if not self.clicked:
                    self.function(self.solver)
                self.clicked = True

            else:
                self.clicked = False


        else:
            if self.hovering:
                self.hovering = False
                self.render_text = self.font.render(self.text, True, (0,0,0), (255,255,255))
                self.button_square.fill((255,255,255), ((1, 1), (98, 33)))
                self.menu_surface.blit(self.button_square, self.position)
                self.menu_surface.blit(self.render_text, (self.position[0] + 1, self.position[1] + 1))


                
def open_new_puzzle(solver):
    print('opening new puzzle')
    file = easygui.fileopenbox()
    solver.show_puzzle(file)