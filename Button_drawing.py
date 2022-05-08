from turtle import Screen
import pygame
import ChessMain
import button
class ButtonDraw():
    #load button images
    new_img = pygame.image.load('Form\\nutnew1.png').convert_alpha()
    back_img= pygame.image.load('Form\\nutback1.png').convert_alpha()
    exit_img = pygame.image.load('Form\\nutexit1.png').convert_alpha()
    next_img = pygame.image.load('Form\\nutnext1.png').convert_alpha()

    def resize(self, image, scale):
        '''resize sacle of image'''
        x = image.get_width()
        y = image.get_height()
        image = pygame.transform.scale(image, (x*scale, y*scale))
        return image

    def label(self, x, y, infomation):
        text = self.font.render(infomation, True, pygame.Color("blue"), None)
        textRect = text.get_rect()
        textRect.center = (x,y)
        return text, textRect

    #create button instances
    new_button = button.Button(100,600, new_img, 0.8)
    back_button = button.Button(200, 600, back_img, 0.8)
    exit_button = button.Button(300, 600, exit_img, 0.8)
    next_button = button.Button(400, 600, next_img, 0.8)

    #create labels
    new_x, new_y = label(130, 670, 'New')
    back_x, back_y = label(230, 670, 'Back')
    exit_x, exit_y = label(330, 670, 'Exit')
    next_x, next_y = label(430, 670, 'Next')

    def draw(self, screen, button_panel_location_x :int, button_panel_location_y :int, button_panel_width :int, button_panel_height :int, gs):
        button_rect = pygame.Rect(button_panel_location_x, button_panel_location_y, button_panel_width, button_panel_height)
        pygame.draw.rect(screen, pygame.Color("pink"), button_rect)

        new_img = self.resize(new_img, 0.3)
        back_img = self.resize(back_img, 0.3)
        exit_img = self.resize(exit_img, 0.3)
        next_img = self.resize(next_img, 0.3)

        screen.blit(self.new_x, self.new_y)
        screen.blit(self.back_x, self.back_y)
        screen.blit(self.exit_x, self.exit_y)
        screen.blit(self.next_x, self.next_y)
                
        if self.new_button.draw(screen):
            ChessMain.Reset_game()
        if self.back_button.draw(screen):
            print('Back')
        if self.exit_button.draw(screen):
            run = False
        if self.next_button.draw(screen):
            print('next')




