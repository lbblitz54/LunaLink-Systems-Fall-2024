// By:  Anjali Punnoose
//      LunaLink Systems
//      Fall 2024
// Program to Move Motor directly in 1 direction for set steps


// SW5 -> ON
// right (CW) dir = LOW
// left (CCW) dir = HIGH

int pulsePin = 39; // Pulse pin
int dirPin = 35;   // Direction pin


int tempCount = 0;
int steps = 5000;
int delay = 200;


void setup() {
  pinMode(pulsePin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  //digitalWrite(dirPin, HIGH); // Set direction
  Serial.begin(38400);
}

void loop() {
  
  digitalWrite(dirPin, HIGH);

  while(tempCount < steps)
  {
      digitalWrite(pulsePin, HIGH);
      delayMicroseconds(delay); // Adjust this delay for speed
      digitalWrite(pulsePin, LOW);
      delayMicroseconds(delay);
      tempCount++;
  }
  Serial.println("Finished");
  

}
