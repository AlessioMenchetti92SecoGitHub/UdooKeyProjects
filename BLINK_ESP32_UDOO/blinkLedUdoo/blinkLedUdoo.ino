#define BLUE_LED_PIN 32
#define YELLOW_LED_PIN 33

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pins as output.
  pinMode(BLUE_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(BLUE_LED_PIN, HIGH);   // turn the blue LED on (HIGH is the voltage level)
  digitalWrite(YELLOW_LED_PIN, LOW);  // turn the yellow LED off by shifting the voltage LOW
  delay(1000);                        // wait for a second
  digitalWrite(YELLOW_LED_PIN, HIGH); // turn the yellow LED on (HIGH is the voltage level)
  digitalWrite(BLUE_LED_PIN, LOW);    // turn the blue LED off by shifting the voltage LOW
  delay(1000);                        // wait for a second
}
