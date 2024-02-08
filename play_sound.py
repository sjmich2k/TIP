
import pygame

from sheet_maker import SheetMaker

pygame.init()
pygame.mixer.init()

right = pygame.mixer.Sound('sounds/right.mp3')
left = pygame.mixer.Sound('sounds/left.mp3')
up = pygame.mixer.Sound('sounds/up.mp3')
down = pygame.mixer.Sound('sounds/down.mp3')
scroll_up = pygame.mixer.Sound('sounds/scroll_up.mp3')
scroll_down = pygame.mixer.Sound('sounds/scroll_down.mp3')
zoom_in = pygame.mixer.Sound('sounds/zoom_in.mp3')
zoom_out = pygame.mixer.Sound('sounds/zoom_out.mp3')
type_right = pygame.mixer.Sound('sounds/type_right.mp3')
type_left = pygame.mixer.Sound('sounds/type_left.mp3')
type_both = pygame.mixer.Sound('sounds/type_both.mp3')
screenshot = pygame.mixer.Sound('sounds/screenshot.mp3')

sheet = SheetMaker(pygame, 100, 100)


def play_sound(action):
    if action == "R":
        sheet.add_sr()
        right.play()
    if action == "L":
        sheet.add_sl()
        left.play()
    if action == "U":
        sheet.add_su()
        up.play()
    if action == "D":
        sheet.add_sd()
        down.play()
    if action == "W":
        sheet.add_scru()
        scroll_up.play()
    if action == "S":
        sheet.add_scrd()
        scroll_down.play()
    if action == "+":
        sheet.add_zi()
        zoom_in.play()
    if action == "-":
        sheet.add_zo()
        zoom_out.play()
    if action == "N":
        sheet.add_tr()
        type_right.play()
    if action == "M":
        sheet.add_tl()
        type_left.play()
    if action == "B":
        sheet.add_tb()
        type_both.play()
    if action == "SCREENSHOT":
        sheet.add_ss()
        screenshot.play()
    return True


def no_sound():
    sheet.add_n()


def end():
    sheet.save()

