#include <Adafruit_NeoPixel.h>

#define NUMPIXELS 60 // The amount of LEDs in our Strip
#define PIN        6 // The PIN which receives & sends Data

#include <AlaLedRgb.h>

AlaLedRgb rgbStrip;

void setup()
{
  // Initializing our WS2812B LED Strip
  rgbStrip.initWS2812B(NUMPIXELS, PIN);
  
  // Optional, Standard Animation if theres no "A" parameter in the clientSide.py software
  rgbStrip.setAnimation(ALA_FADECOLORSLOOP, 5000, alaPalRgb);
}

void loop()
{
  rgbStrip.runAnimation();
}
