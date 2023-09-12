import pygame
import easygui
import cv2
import numpy as np

class Solver:
    def __init__(self):
        self.menu_surface = pygame.Surface((1650, 720))
        self.menu_surface.fill('white')    
        self.new_image_button = Button(self, (50, 100), 'open incomplete puzzle', open_new_puzzle)
        self.buttons = [self.new_image_button]

    def show_puzzle(self, image_url):
        puzzleIMG = pygame.image.load(image_url)
        self.pre_process_puzzle(image_url)
        puzzleIMG = pygame.image.load('puzzle_pieces_with_contours.jpg')
        img_w = puzzleIMG.get_width()
        img_h = puzzleIMG.get_height()

        if img_w > img_h:
            self.puzzleIMG = pygame.transform.scale(puzzleIMG, (400, img_h * (400 / img_w)))
        else:
            self.puzzleIMG = pygame.transform.scale(puzzleIMG, (img_w * (400 / img_h), 400))


        self.new_completed_image_button = Button(self, (450, 100), 'open reference', open_solved_pic)
        self.buttons.append(self.new_completed_image_button)
        self.menu_surface.blit(self.puzzleIMG, (50, 200))

    def pre_process_puzzle(self, image_url):
        puzzle_image = cv2.imread(image_url)

        gray_image = cv2.cvtColor(puzzle_image, cv2.COLOR_BGR2GRAY)

        _, thresholded_image = cv2.threshold(gray_image, 75, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.int8)
        morphed_image = cv2.erode(thresholded_image, kernel, iterations=1)
        morphed_image = cv2.dilate(morphed_image, kernel, iterations=1)

        contours, _ = cv2.findContours(morphed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_contour_area = 1000
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

        mask = np.zeros_like(thresholded_image)
        cv2.drawContours(mask, filtered_contours, -1, 255, thickness=cv2.FILLED)

        puzzle_pieces = cv2.bitwise_and(puzzle_image, puzzle_image, mask=mask)

        cv2.imwrite('puzzle_pieces_noBG.jpg', puzzle_pieces)

        puzzle_image = cv2.imread('puzzle_pieces_noBG.jpg', cv2.IMREAD_GRAYSCALE)

        contours, _ = cv2.findContours(puzzle_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_image = cv2.cvtColor(puzzle_image, cv2.COLOR_GRAY2BGR)

        piece_index = 0

        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)

            piece = puzzle_image[y:y+h, x:x+w]

            piece_filename = f'/pieces/piece_{piece_index}.jpg'
            
            cv2.imwrite(piece_filename, piece)

            cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 255, 0))

            piece_index += 1
            
        cv2.imwrite('puzzle_pieces_with_contours.jpg', contour_image)

    def show_double_view(self, solved_image_url):
        solved_puzzleIMG = pygame.image.load(solved_image_url)
        img_w = solved_puzzleIMG.get_width()
        img_h = solved_puzzleIMG.get_height()
        
        if img_w > img_h:
            self.solved_puzzleIMG = pygame.transform.scale(solved_puzzleIMG, (300, img_h * (300 / img_w)))
        else:
            self.solved_puzzleIMG = pygame.transform.scale(solved_puzzleIMG, (img_w * (300 / img_h), 300))

        self.menu_surface.blit(self.puzzleIMG, (50, 200))
        self.menu_surface.blit(self.solved_puzzleIMG, (450, 200))

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