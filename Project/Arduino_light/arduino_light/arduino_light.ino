#include <Adafruit_NeoPixel.h>

#define LED_PIN_1     4 // D3 for the first LED strip
#define LED_COUNT_1   37 // Number of LEDs in the first strip

#define LED_PIN_2     5 // D4 for the second LED strip
#define LED_COUNT_2   37 // Number of LEDs in the second strip

Adafruit_NeoPixel pixels1(LED_COUNT_1, LED_PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2(LED_COUNT_2, LED_PIN_2, NEO_GRB + NEO_KHZ800);

int LED_BRIGHTNESS = 10; // Adjust this value to control brightness (0-255)

void setup() {
  // Initialize the NeoPixel libraries
  pixels1.begin();
  pixels1.show(); // Initialize all pixels to 'off'
  
  pixels2.begin();
  pixels2.show(); // Initialize all pixels to 'off'

  // Serial communication (for debugging)
  Serial.begin(115200);
  while (!Serial); // Wait for the serial connection to be established
}

void loop() {
  // Control the first LED strip (D3)
  for (int i = 0; i < 255 ;  i++){
    colorWipe(pixels1, pixels1.Color(255, 0, 0), 1, LED_BRIGHTNESS = i); // Red
    delay(1000);
  }
  
  // // Control the second LED strip (D4)
  // colorWipe(pixels2, pixels2.Color(0, 255, 255), 50); // Cyan
  // colorWipe(pixels2, pixels2.Color(255, 255, 0), 50); // Yellow
  // colorWipe(pixels2, pixels2.Color(255, 0, 255), 50); // Magenta

  // You can add more effects or control the LED strips as needed
}

// Fill the dots one after the other with a color for a specific LED strip
void colorWipe(Adafruit_NeoPixel &strip, uint32_t color, int wait, int LED_BRIGHTNESS) {
  for (int i = 0; i < strip.numPixels(); i++) {
    uint8_t r = (color >> 16) & 0xFF; // Extract red component
    uint8_t g = (color >> 8) & 0xFF;  // Extract green component
    uint8_t b = color & 0xFF;         // Extract blue component

    r = (r * LED_BRIGHTNESS) / 255;   // Adjust red component brightness
    g = (g * LED_BRIGHTNESS) / 255;   // Adjust green component brightness
    b = (b * LED_BRIGHTNESS) / 255;   // Adjust blue component brightness

    strip.setPixelColor(i, strip.Color(r, g, b));
    strip.show();
  }
}