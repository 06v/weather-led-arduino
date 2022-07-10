#include <Adafruit_NeoPixel.h>

#define NUMPIXELS 60 // The amount of LEDs in our Strip
#define PIN        6 // The PIN which receives & sends Data

#include <AlaLedRgb.h>

AlaLedRgb rgbStrip;

void setup()
{
  // Initialisieren unseres WS2812G RGB Strips
  rgbStrip.initWS2812(NUMPIXELS, PIN);
  
  // Optional, Standard Animation falls keine vorgebeben in unserem PySerial Programm
  rgbStrip.setAnimation(ALA_FADECOLORSLOOP, 5000, alaPalRgb);
}

void loop()
{
  rgbStrip.runAnimation();
}
