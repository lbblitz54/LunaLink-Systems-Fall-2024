// By:  Anjali Punnoose
//      LunaLink Systems
//      Fall 2024
// Program to Move 2 Motors directly and simultaneously for the same number of steps


// SW5 -> ON
// right (CW)(down) dir = LOW
// left (CCW)(up) dir = HIGH

int pulsePin_Vertical = 41; // Pulse pin
int dirPin_Vertical = 43;   // Direction pin
int pulsePin_Horizontal = 35; // Pulse pin for Horizontal movement motor
int dirPin_Horizontal = 33;   // Direction pin for Horizontal movement motor

int pulseDelay_Vertical = 50;


int tempCount = 0;
int steps = 20000;


void setup() {
  pinMode(pulsePin_Vertical, OUTPUT);
  pinMode(dirPin_Vertical, OUTPUT);
  pinMode(pulsePin_Horizontal, OUTPUT);
  pinMode(dirPin_Horizontal, OUTPUT);
  

  Serial.begin(9600);
}

void loop() {
  
  digitalWrite(dirPin_Vertical, HIGH);
  digitalWrite(dirPin_Horizontal, HIGH);


  while(tempCount < steps)
  {
      digitalWrite(pulsePin_Vertical, HIGH);
      digitalWrite(pulsePin_Horizontal, HIGH);
      delayMicroseconds(pulseDelay_Vertical); // Adjust this delay for speed
      digitalWrite(pulsePin_Vertical, LOW);
      digitalWrite(pulsePin_Horizontal, LOW);
      delayMicroseconds(pulseDelay_Vertical);
      tempCount++;
  }
  

}
