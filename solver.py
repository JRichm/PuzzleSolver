import pygame
import easygui

class Solver:
    def __init__(self):
        self.menu_surface = pygame.Surface((1280, 720))
        self.menu_surface.fill('white')    
        self.new_image_button = Button(self, (100, 100), 'new puzzle', open_new_puzzle)
        self.buttons = [self.new_image_button]

    def show_puzzle(self, image_url):
        puzzleIMG = pygame.image.load(image_url)
        img_w = puzzleIMG.get_width()
        img_h = puzzleIMG.get_height()

        if img_w > img_h:
            self.puzzleIMG = pygame.transform.scale(puzzleIMG, (400, img_h * (400 / img_w)))
        else:
            self.puzzleIMG = pygame.transform.scale(puzzleIMG, (img_w * (400 / img_h), 400))


        self.new_completed_image_button = Button(self, (600, 100), 'open solved reference', open_solved_pic)
        self.buttons.append(self.new_completed_image_button)
        self.menu_surface.blit(self.puzzleIMG, (100, 200))

    def show_double_view(self, solved_image_url):
        solved_puzzleIMG = pygame.image.load(solved_image_url)
        img_w = solved_puzzleIMG.get_width()
        img_h = solved_puzzleIMG.get_height()
        
        if img_w > img_h:
            self.solved_puzzleIMG = pygame.transform.scale(solved_puzzleIMG, (400, img_h * (400 / img_w)))
        else:
            self.solved_puzzleIMG = pygame.transform.scale(solved_puzzleIMG, (img_w * (400 / img_h), 400))

        self.menu_surface.blit(self.puzzleIMG, (100, 200))
        self.menu_surface.blit(self.solved_puzzleIMG, (600, 200))

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
        self.visible = True
        self.text = text
        self.button_square = pygame.Surface((400, 35))
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
        if not self.visible:
            return

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
    solver.new_image_button.visible = False
    solver.menu_surface.fill('white')
    solver.show_puzzle(file)

def open_solved_pic(solver):
    print('opening pic to solve for')
    file = easygui.fileopenbox()
    solver.new_completed_image_button.visible = False
    solver.menu_surface.fill('white')
    solver.show_double_view(file)