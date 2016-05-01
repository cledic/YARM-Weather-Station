#!/usr/bin/python

# -*- coding: utf-8 -*-
from threading import Timer
from time import sleep
import datetime
from subprocess import call
import pygame, sys, os, time, glob
import json

_filepath="/tmp/images/"

# ####################################################
def curr_weather():
    infile = open(_filepath+"curr_weather.txt","rb")
    weather_string = infile.readline()
    infile.close()
    parsed_weather = json.loads(weather_string)
    # 
    myimage = pygame.image.load( parsed_weather['icona'])
    myimage = pygame.transform.scale( myimage, (96, 96))
    imagerect = myimage.get_rect()
    imagerect.x = 10
    imagerect.y = 24
    DISPLAYSURF.blit(myimage, imagerect)
    # render text
    medfont = pygame.font.SysFont("monospace", 24, bold=True)
    label = medfont.render("Tempo In Atto", 1, (0,0,255))
    DISPLAYSURF.blit(label, (10, 0))
    # temperatura
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Temperatura: "+parsed_weather['temperatura'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 24))
    # umidita
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Umidita: "+parsed_weather['umidita'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 24*2))
    # pressione
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Pressione: "+parsed_weather['pressione'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 24*3))
    # pioggia
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Pioggia: "+parsed_weather['pioggia'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 24*4))
    
    pygame.display.flip()

def tomorrow_weather():
    infile = open(_filepath+"tomorrow_weather.txt","rb")
    weather_string = infile.readline()
    infile.close()
    parsed_weather = json.loads(weather_string)
    # 
    myimage = pygame.image.load( parsed_weather['icona'])
    myimage = pygame.transform.scale( myimage, (96, 96))
    imagerect = myimage.get_rect()
    imagerect.x = 10
    imagerect.y = 154
    DISPLAYSURF.blit(myimage, imagerect)
    # render text
    medfont = pygame.font.SysFont("monospace", 24, bold=True)
    label = medfont.render("Tempo per Domani", 1, (0,0,255))
    DISPLAYSURF.blit(label, (10, 130))    
    # tempo
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Tempo: "+parsed_weather['tempo'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 154))
    # tMax
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Temp. Max: "+parsed_weather['tMax'], 1, (255,0,0))
    DISPLAYSURF.blit(label, (10+96+10, 154+24))
    # tMin
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Temp. Min: "+parsed_weather['tMin'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 154+(24*2)))
    # pioggia
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Pioggia: "+parsed_weather['pioggia'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 154+(24*3)))
    
    pygame.display.flip()

def twodayslater_weather():
    infile = open(_filepath+"twodayslater_weather.txt","rb")
    weather_string = infile.readline()
    infile.close()
    parsed_weather = json.loads(weather_string)
    # 
    myimage = pygame.image.load( parsed_weather['icona'])
    myimage = pygame.transform.scale( myimage, (96, 96))
    imagerect = myimage.get_rect()
    imagerect.x = 10
    imagerect.y = 284
    DISPLAYSURF.blit(myimage, imagerect)
    # render text
    medfont = pygame.font.SysFont("monospace", 24, bold=True)
    label = medfont.render("Tempo per Dopodomani", 1, (0,0,255))
    DISPLAYSURF.blit(label, (10, 260))   
    # tempo
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Tempo:"+parsed_weather['tempo'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 284))
    # tMax
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Temp. Max:"+parsed_weather['tMax'], 1, (255,0,0))
    DISPLAYSURF.blit(label, (10+96+10, 284+24))
    # tMin
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Temp. Min:"+parsed_weather['tMin'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 284+(24*2)))
    # pioggia
    medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
    label = medfont.render("Pioggia:"+parsed_weather['pioggia'], 1, (0,0,255))
    DISPLAYSURF.blit(label, (10+96+10, 284+(24*3)))
    
    pygame.display.flip()

def Sensor_AtHome():
    #
    infile = open(_filepath+"sensor_1.txt","rb")
    weather_string = infile.readline()
    infile.close()
    #print(weather_string)
    parsed_weather = json.loads(weather_string)
    if parsed_weather['RxError'] == 0:
        pygame.draw.rect(DISPLAYSURF, LBLUE, (410,0,800,130), 0)
        # render text
        medfont = pygame.font.SysFont("monospace", 24, bold=True)
        label = medfont.render("Sensore 1", 1, (0,0,255))
        DISPLAYSURF.blit(label, (410, 0))
        # temperature
        medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
        label = medfont.render("Temperatura: "+str(parsed_weather['temperature'])+" C", 1, (0,0,255))
        DISPLAYSURF.blit(label, (400+10, 24))
        # humidity
        medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
        label = medfont.render("Umidita    : "+str(parsed_weather['humidity'])+" %", 1, (0,0,255))
        DISPLAYSURF.blit(label, (400+10, 24*2))
        # pressure
        medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
        label = medfont.render("Pressione  : "+str(parsed_weather['pressure'])+" hP", 1, (0,0,255))
        DISPLAYSURF.blit(label, (400+10, 24*3))
        # pioggia
        #medfont = pygame.font.SysFont("monospace", 24, bold=False, italic=True)
        #label = medfont.render("Pioggia:"+parsed_weather['pioggia'], 1, (0,0,255))
        #DISPLAYSURF.blit(label, (400+10, 24*4))
        
        pygame.display.flip()

def ANSA_News( idx=1):
    #
    pygame.draw.rect(DISPLAYSURF, LBLUE, (0,395,800,85), 0)
    infile = open(_filepath+"ansa_news-"+str(idx)+".txt","rb")
    ansa_string = infile.readline()
    infile.close()
    parsed_ansa = json.loads(ansa_string)
    # render text
    medfont = pygame.font.SysFont("monospace", 24, bold=True)
    label = medfont.render("ANSA News:", 1, (0,0,0))
    DISPLAYSURF.blit(label, (10, 390))
    # titolo
    medfont = pygame.font.SysFont("monospace", 22, bold=False, italic=True)
    label = medfont.render(parsed_ansa['titolo'], 1, (0,0,0))
    DISPLAYSURF.blit(label, (10, 390+24))
    # testo
    medfont = pygame.font.SysFont("monospace", 22, bold=False, italic=False)
    label = medfont.render(parsed_ansa['testo'], 1, (0,0,0))
    DISPLAYSURF.blit(label, (10, 390+(24*2)))
    
    pygame.display.flip()


# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
LBLUE  = (  0,   255, 255)

os.environ["SDL_FBDEV"] = "/dev/fb0"
os.environ["SDL_MOUSEDEV"] = "/dev/input/event0"
time.sleep(0.5)
pygame.init()

DISPLAYSURF = pygame.display.set_mode((800, 480), 0, 32)

surf = pygame.Surface((480, 800)).convert()

pygame.mouse.set_visible(0)

# draw on the surface object
DISPLAYSURF.fill(LBLUE)
idx=1

curr_weather()
tomorrow_weather()
twodayslater_weather()
pygame.display.update()

while True:

    #curr_weather()
    #tomorrow_weather()
    #twodayslater_weather()
    #
    pygame.draw.line( DISPLAYSURF, (0,0,255),(10,130),(790,130))
    pygame.draw.line( DISPLAYSURF, (0,0,255),(10,260),(790,260))
    pygame.draw.line( DISPLAYSURF, (0,0,255),(0,390),(800,390))
    pygame.draw.line( DISPLAYSURF, (0,0,255),(400,5),(400,125))
    #
    Sensor_AtHome()
    ANSA_News( idx)
    idx=idx+1
    if idx>10:
      idx=1

    pygame.display.update()
    time.sleep(3)

