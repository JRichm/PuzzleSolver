import pygame
import solver

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False

solver = solver.Solver()

while not done:
    
    # poll for events
    for event in pygame.event.get():

        # quit if window is closed
        if event.type == pygame.QUIT:
            done = True
        
    # add window rendering / update
    solver.show(screen)

    # flip display 
    pygame.display.flip()

    # limit FPS to 60
    clock.tick(60)


# quit when reach end of file
pygame.quit()