import RPi.GPIO as GPIO
import time
import pygame

GPIO.setmode(GPIO.BOARD)

pygame.mixer.pre_init(44100, -16, 4, 512)
pygame.init()

class HC_SR04:

    def __init__(self, echo, trig):
        self.echo = echo
        self.trig = trig

        GPIO.setup(trig, GPIO.OUT)
        GPIO.output(trig, 0)

        GPIO.setup(echo, GPIO.IN)

        time.sleep(0.1)

        self.dist = None

    def get_dist(self):
        GPIO.output(self.trig, 1)
        time.sleep(0.00001)
        GPIO.output(self.trig, 0)
        
        begin = time.time()

        while GPIO.input(self.echo) == 0 and time.time() - begin < 1:
            pass
        start = time.time()
        while GPIO.input(self.echo) == 1 and time.time() - begin < 2: 
            pass
        end = time.time()
    
        dist = round((end - start) * 17150, 2)

        self.dist = dist

        time.sleep(0.01)  #prevents catching signals of other sensors

        return dist

    def conv_to_sound(self, max_dist):
        if self.dist == None:
            self.get_dist()

        if self.dist < max_dist:
            sound = round(1 -  self.dist / max_dist, 2)
        else:
            sound = 0.0
        
        self.sound = sound

        return sound

# noteFd = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/Piano_F#.wav")  #notes initialisation
# noteG = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/Piano_G.wav")
# noteGd = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/Piano_G#.wav")
# noteA = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/Piano_A.wav")

noteFd = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/NoteF#.wav")  #notes initialisation
noteG = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/NoteG.wav")
noteGd = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/NoteG#.wav")
noteA = pygame.mixer.Sound("/home/pi/Yura/Projects/Tones/AudioFiles/NoteA.wav")

s1 = HC_SR04(11, 13)  #sensors initialisation
s2 = HC_SR04(15, 16)
s3 = HC_SR04(18, 22)
s4 = HC_SR04(29, 31)
print('__init__ success')

while True:
    print('distance: ', s1.get_dist(), ' ', s2.get_dist(), ' ', s3.get_dist(), ' ', s4.get_dist())
    print('volume:   ', s1.conv_to_sound(20), ' ', s2.conv_to_sound(20), ' ', s3.conv_to_sound(20), ' ', s4.conv_to_sound(20))

    noteFd.set_volume(s1.conv_to_sound(40))
    noteG.set_volume(s2.conv_to_sound(40))
    noteGd.set_volume(s3.conv_to_sound(40))
    noteA.set_volume(s4.conv_to_sound(40))
    
    noteFd.play()
    noteG.play()
    noteGd.play()
    noteA.play()

    time.sleep(1)