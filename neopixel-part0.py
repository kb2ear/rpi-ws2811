### Sample python code for NeoPixels on Raspberry Pi
### this code is random suggestion from my family, friends, and other examples on the web
### orginal code: https://github.com/DanStach/rpi-ws2811
import time
import board
import neopixel
import random
import math
import serial
import ctypes



# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


### colorAll2Color(c1, c2) allows two alternating colors to be shown
def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()

# colorAllColorGroup(colorObject) allows colors to be 
# - colorObject: list of color objects. example ((255, 0, 0), (0, 255, 0))  
def colorAllColorGroup(colorObject):
    colorCount = len(colorObject)

    for i in range(num_pixels):
            colorIndex = i % colorCount]
            pixels[i] = colorObject[colorIndex]

    pixels.show()

### wheel(pos) will convert value 0 to 255 to get a color value.
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def brightnessRGB(red, green, blue, bright):
    r = (bright/256.0)*red
    g = (bright/256.0)*green
    b = (bright/256.0)*blue
    return (int(r), int(g), int(b))

def FadeInOut(red, green, blue, delay):
    r = 0
    g = 0
    b = 0
      
    for k in range(256):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
     
    for k in range(256, -1, -1):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
        
#   
#   steps: (1-...) number of intermediate steps to transition to new color  
def TransitionColorStripExisting(stripFinal, steps, delay):

    # gather existing colors in strip of pixel
    stripStarting = []
    for i in range(num_pixels):
        stripStarting.append(pixels[i])
    

    # fixme: may need to pre-calculate the color values to improve timing preformance

    for step in range(steps):
        TransRatio =  step/steps

        for i in range(num_pixels):
            # gather old and final color
            oldColor = stripStarting[i]
            finalColor = stripFinal[i]

            # calculate diffence in color range for color values
            # fixme: rather than calc by R, G, B. maybe by object
            deltaR = (finalColor[0] - oldColor[0])
            deltaG = (finalColor[1] - oldColor[1])
            deltaB = (finalColor[2] - oldColor[2])

            # calculate new color values 
            newR = (TransRatio * deltaR) + oldColor[0]
            newG = (TransRatio * deltaG) + oldColor[1]
            newB = (TransRatio * deltaB) + oldColor[2]

            # assign new color to pixel
            pixels[i] = (int(newR), int(newG), int(newB))

        # show new color, and wait if needed
        pixels.show()
        time.sleep(delay)
     
    for k in range(256, -1, -1):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
        
def fadeToBlack(ledNo, fadeValue):
    oldColor = pixels[ledNo]
    r = oldColor[0]
    g = oldColor[1]
    b = oldColor[2]

    if (r<=10):
        r = 0
    else:
        r = r - ( r * fadeValue / 256 )

    if (g<=10):
        g = 0
    else:
        g = g - ( g * fadeValue / 256 )

    if (b<=10):
        b = 0
    else:
        b = b - ( b * fadeValue / 256 )

    pixels[ledNo] = ( int(r), int(g), int(b) )




### makes the strand of pixels show Fire
# Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
#CoolingRangeStart = 0-255
#CoolingRangeEnd = 0-255
#Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
#SparkingRangeStart = 0-255 
#SparkingRangeEnd = 0-255
#FireColor = 0-2 (0=red, 1=blue , 2=green)
#FireEffect = 0-2 (these are differnet ways of adding sparks to the strip)
def FireCustom(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, LoopCount):
    heat = []
    for i in range(num_pixels):
    heat.append(0)

    for l in range(LoopCount):
        cooldown = 0
        
        # Step 1.  Cool down every cell a little
        for i in range(num_pixels):
            # for 50 leds and cooling 50
            # cooldown = random.randint(0, 12)
            # cooldown = random.randint(0, ((Cooling * 10) / num_pixels) + 2)
            cooldown = random.randint(CoolingRangeStart, CoolingRangeEnd)
            if cooldown > heat[i]:
                heat[i]=0
            else: 
                heat[i]=heat[i]-cooldown
        
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(num_pixels - 1, 2, -1):
            heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2]) / 3
            
        # Step 3.  Randomly ignite new 'sparks' near the bottom
        if random.randint(0,100) < Sparking:
            
            # randomly pick the position of the spark
            y = random.randint(SparkingRangeStart,SparkingRangeEnd)
            # different fire effects 
            heat[y] = random.randint(160,255)

        # Step 4.  Convert heat to LED colors
        for j in range(num_pixels):
            t192 = round((int(heat[j])/255.0)*191)

            # calculate ramp up from
            heatramp = t192 & 63 # 0..63  0x3f=63
            heatramp <<= 2 # scale up to 0..252
            # figure out which third of the spectrum we're in:

            if t192 > 0x80: # hottest 128 = 0x80
                pixels[j] = (255, 255, int(heatramp))
            elif t192 > 0x40: # middle 64 = 0x40
                pixels[j] = (255, int(heatramp), 0)
            else: # coolest
                pixels[j] = (int(heatramp), 0, 0)

    pixels.show()
    time.sleep(SpeedDelay)


def candycane_custom(c1, c2, thisbright, delay, cycles):
    index = 0
    N3  = int(num_pixels/3)
    N6  = int(num_pixels/6)
    N12 = int(num_pixels/12)
    for loop in range(cycles):
        index = index + 1
        cSwap = c1
        c1 = c2
        c2 = cSwap
        for i in range(N6):
            j0 = int((index + i + num_pixels - N12) % num_pixels)
            j1 = int((j0+N6) % num_pixels)
            j2 = int((j1+N6) % num_pixels)
            j3 = int((j2+N6) % num_pixels)
            j4 = int((j3+N6) % num_pixels)
            j5 = int((j4+N6) % num_pixels)
            pixels[j0] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j1] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)
            pixels[j2] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j3] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)
            pixels[j4] = brightnessRGB(c1[0], c1[1], c1[2], int(thisbright*.75))
            pixels[j5] = brightnessRGB(c2[0], c2[1], c2[2], thisbright)

            # show pixel values 
            pixels.show()
            time.sleep(delay)

def RunningLightsPreExisting(WaveDelay, cycles):
    
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for loop in range(cycles):
        
        # change the color level on the existing colors
        for i in range(num_pixels):
            # calculate level
            level = math.sin(i + loop) * 127 + 128

            # change color level on for red, green, and blue
            r = int((level/255)*stripExisting[i])
            g = int((level/255)*stripExisting[i])
            b = int((level/255)*stripExisting[i])
            pixels[i] = (r,g,b)

        pixels.show()
        time.sleep(WaveDelay)


def SnowSparkleExisting(Count, SparkleDelay, SpeedDelay):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for i in range(Count):
        index = random.randint(0,num_pixels-1)
        pixels[index] = (255,255,255)
        pixels.show()
        time.sleep(SparkleDelay)
        pixels[index] = stripExisting[index]
        pixels.show()
        time.sleep(SpeedDelay)


def HalloweenEyesExisting(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    # define eye1 and eye2 location
    StartPoint  = random.randint( 0, num_pixels - (2*EyeWidth) - EyeSpace )
    Start2ndEye = StartPoint + EyeWidth + EyeSpace

    #  set color of eyes for given location
    for i in range(EyeWidth):
        pixels[StartPoint + i] = (red, green, blue)
        pixels[Start2ndEye + i] = (red, green, blue)
    pixels.show()

    # if user wants fading, then fadeout pixel color
    if Fade == True:
        for j in range(Steps, -1, -1):
            r = (j/Steps)*red
            g = (j/Steps)*green
            b = (j/Steps)*blue

            for i in range(EyeWidth):
                pixels[StartPoint + i] = ((int(r), int(g), int(b)))
                pixels[Start2ndEye + i] = ((int(r), int(g), int(b)))

            pixels.show()
            time.sleep(FadeDelay)
    
    # Set all pixels to back
    # set color of eyes for given location
    for i in range(EyeWidth):
        pixels[StartPoint + i] = stripExisting[StartPoint + i]
        pixels[Start2ndEye + i] = stripExisting[Start2ndEye + i]
    pixels.show()

    # pause before changing eye location
    time.sleep(EndPause)


# HeartBeatExisiting - mimics a heart beat pulse, with 2 beats at different speeds. The existing colors 
# on the pixel strip are preserved, rather than a single color.
#j
# HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay,
#                     beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat1Delay, cycles):
# HeartBeatExisiting(3, .005, .003, 0.001, 6, .002, .003, 0.05, 10)
#
#   beat1Step: (1-255) first beat color transition step
#   beat1FadeInDelay: (0-2147483647) first beat fade in trasition speed, in seconds
#   beat1FadeOutDelay: (0-2147483647) first beat fade out trasition speed, in seconds
#   beat1Delay: (0-2147483647)  beat time delay bewteen frist and sencond beat, in seconds
#   beat2Step: (1-255) second beat color transition step
#   beat2FadeInDelay: (0-2147483647) second beat fade in trasition speed, in seconds
#   beat2FadeOutDelay: (0-2147483647) second beat fade out trasition speed, in seconds
#   beat1Delay: (0-2147483647)  beat time delay bewteen sencond and first beat, in seconds
#   cycles: (1-2147483647) number of times this effect will run
def HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat2Step, beat2FadeInDelay, beat2FadeOutDelay, cycles):
    # gather existing colors in strip of pixel
    stripExisting = []
    for i in range(num_pixels):
        stripExisting.append(pixels[i])

    for loop in range(cycles):               

        for ii in range(1, 252, beat1Step): #for ( ii = 1 ; ii <252 ; ii = ii = ii + x)
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat1FadeInDelay)

        for ii in range(252, 3, -beat1Step): #for (int ii = 252 ; ii > 3 ; ii = ii - x){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat1FadeOutDelay)
            
        time.sleep(beat1Delay)
        
        for ii in range(1, 252, beat1Step): #for (int ii = 1 ; ii <255 ; ii = ii = ii + y){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat2FadeInDelay)

        for ii in range(252, 3, -beat1Step): #for (int ii = 255 ; ii > 1 ; ii = ii - y){
            for index in range(num_pixels):
                r = stripExisting[index][0]
                g = stripExisting[index][1]
                b = stripExisting[index][2]
                pixels[index] = brightnessRGB(r,g,b, ii) 
                #pixels.fill( brightnessRGB(redo, greeno, blueo, ii) ) #strip.setBrightness(ii)
            pixels.show()
            time.sleep(beat2FadeOutDelay)
    
        time.sleep(.050) 



while True:
    random.seed(num_pixels)


    # make all pixels Red
    # fill(red, green, blue)
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)
    
    # shows pattern of colors on the given pixels 
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2), ...) 
    xmasColorGroup = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)) 
    colorAllColorGroup(xmasColorGroup) 
    time.sleep(wait_time)


    # shows 2 color every other pixel (red, green)
    # SnowSparkleExisting(Count, SparkleDelay, SpeedDelay)
    colorAll2Color((128,0,128), (255,165,0) )
    SnowSparkleExisting(0, .1, .1)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # RunningLightsPreExisting(WaveDelay, cycles):
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    RunningLightsPreExisting(0, 1000)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    #HeartBeatExisiting(beat1Step, beat1FadeInDelay, beat1FadeOutDelay, beat1Delay, 
    #                   beat2Step, beat2FadeInDelay, beat2FadeOutDelay, beat2Delay, cycles):
    HeartBeatExisiting(3, .005, .003, 0.001, 6, .002, .003, 0.05, 10):


    # makes the strand of pixels show candycane_custom
    # candycane_custom(c1, c2, brightness, delay, cycles)
    candycane_custom((255,255,255), (0,200,0), 255, 0, 500)
    time.sleep(wait_time)

    # makes the strand of pixels show Fire
    # Fire(CoolingRangeStart, CoolingRangeEnd, Sparking, SparkingRangeStart, SparkingRangeEnd, SpeedDelay, FireColor, FireEffect, LoopCount)
    #CoolingRangeStart = 0-255
    #CoolingRangeEnd = 0-255
    #Sparking = 0-100  (0= 0% sparkes randomly added, 100= 100% sparks randomly added)
    #SparkingRangeStart = 0-255 
    #SparkingRangeEnd = 0-255
    #FireColor = 0-2 (0=red, 1=blue , 2=green)
    #FireEffect = 0-2
    FireCustom(0, 12, 25, 0, 10, 0.02, 500) # red fire
    time.sleep(wait_time)



    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    FadeInOut(255, 0, 0, 0.01)
    FadeInOut(0, 255, 0, 0.01)
    FadeInOut(0, 0, 255, 0.01)
    FadeInOut(255, 255, 255, 0.01)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)

    ### HALLOWEEN idea
    # shows 2 color every other pixel (purple, orange)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((128,0,128), (255,165,0) )



