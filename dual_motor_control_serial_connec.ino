// By:  Anjali Punnoose
//      LunaLink Systems
//      Fall 2024
// Program for Serial Communication with RPi to Control Motor in both horizontal and vertical directions

// SW5 -> ON
// right (CW)(down) dir = LOW
// left (CCW)(up) dir = HIGH


int pulsePin_Vertical = 39; // Pulse pin
int dirPin_Vertical = 35;   // Direction pin
int pulsePin_Horizontal = 47; // Pulse pin for Horizontal movement motor
int dirPin_Horizontal = 43;   // Direction pin for Horizontal movement motor
bool is_moving = false;

int pulse_delay = 15;
int steps_Vert = 0;
int steps_Horiz = 0;
int step_Count = 0;

String split_word[5];  
String received_data;
//String move_cmd[3] = {"R 3000 U 3000 100", "R 3000 D 3000 100", "L 3000 D 3000 100"};
int ind = 0;

void setup() {
  Serial.begin(38400);  // Start serial communication at 9600 baud 
  pinMode(pulsePin_Vertical, OUTPUT);
  pinMode(dirPin_Vertical, OUTPUT);
  pinMode(pulsePin_Horizontal, OUTPUT);
  pinMode(dirPin_Horizontal, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 1); 
  
//  received_data = "R 2000 D 5000 200"; // for testing
}
  
void loop() {
   
  if (Serial.available() > 0) {
  // Get Data sent from RPi to Arduino
    received_data = Serial.readStringUntil('\n');  // Read the incoming string until newline character

    received_data.trim();  // Trim any extra whitespaces or newlines

    if(received_data == "stop")
    {
      steps_Horiz = 0;
      steps_Vert = 0;
      step_Count = 0;
      pulse_delay = 200;
      return;
    }
    else if( received_data != "")
    {
      // Split Received Sentence into Array of Words
      split_Data(received_data);
     
    // Determine directions desired 
      determine_directions(); 
      received_data = "";
    }

  
  }
  
  // Step Motors
  int retVal = stepMotors(); 
  
  // Send back data from Arduino to RPi
  if (retVal == 1 && is_moving)
  {
    is_moving = false;
    Serial.println("end-motion");
  }

}



int stepMotors(){
//Function to step motors based on number of steps remaining for horizontal and vertical motors
  
//  Serial.println(step_Count);
//  Serial.println(steps_Horiz);
//  Serial.println(steps_Vert);
//  Serial.println(is_moving);

  if(steps_Horiz > steps_Vert)
  {
    if(step_Count < steps_Vert)
    {
        digitalWrite(pulsePin_Vertical, HIGH);
        digitalWrite(pulsePin_Horizontal, HIGH);
        delayMicroseconds(pulse_delay); // Adjust this delay for speed
        digitalWrite(pulsePin_Vertical, LOW);
        digitalWrite(pulsePin_Horizontal, LOW);
        delayMicroseconds(pulse_delay);
        is_moving = true;
        step_Count++;
    }
    else if(step_Count < steps_Horiz)
    {
        digitalWrite(pulsePin_Horizontal, HIGH);
        delayMicroseconds(pulse_delay); // Adjust this delay for speed
        digitalWrite(pulsePin_Horizontal, LOW);
        delayMicroseconds(pulse_delay);
        is_moving = true;
        step_Count++;
    }
    else
    {
      return 1;
    }
  
  }
  else
  {
    if(step_Count < steps_Horiz)
    {
        digitalWrite(pulsePin_Vertical, HIGH);
        digitalWrite(pulsePin_Horizontal, HIGH);
        delayMicroseconds(pulse_delay); // Adjust this delay for speed
        digitalWrite(pulsePin_Vertical, LOW);
        digitalWrite(pulsePin_Horizontal, LOW);
        delayMicroseconds(pulse_delay);
        is_moving = true;
        step_Count++;
   }
    else if(step_Count < steps_Vert)
    {
        digitalWrite(pulsePin_Vertical, HIGH);
        delayMicroseconds(pulse_delay); // Adjust this delay for speed
        digitalWrite(pulsePin_Vertical, LOW);
        delayMicroseconds(pulse_delay);        
        is_moving = true;
        step_Count++;
    }
    else
    {
      return 1;
    }
  }

  return 0;
}

void split_Data(String received_word)
{
// Function to split data received from RPi into separate parts 

  for(int i =0; i< 5; i++) // split the received line into words
    {
      int space_Pos = received_word.indexOf(" ");
      if(space_Pos != -1)
      {
       split_word[i] = received_word.substring(0,space_Pos);
       received_word = received_word.substring(space_Pos+1);
      }
      else if(received_word.length() > 0)
      {
        split_word[i] = received_word;
      }
      else
      {
        break;
      }
    }
}

void determine_directions()
{
  // Function to process separated data to Determine Directions and steps  
    steps_Horiz = split_word[1].toInt(); // Get steps
    if (split_word[0] == "R")
    {
      digitalWrite(dirPin_Horizontal, LOW); // set direction to right
      Serial.print("Right: ");
      Serial.print(steps_Horiz);  
    }
    else if (split_word[0] == "L")
    {
      digitalWrite(dirPin_Horizontal, HIGH); // set direction to left
      Serial.print("Left: ");
      Serial.print(steps_Horiz);
    }
    
    steps_Vert = split_word[3].toInt(); // Get steps
    if (split_word[2] == "D")
    {
      digitalWrite(dirPin_Vertical, LOW); // set direction to down
      Serial.print(" Down: ");
      Serial.print(steps_Vert);  
    }
    else if (split_word[2] == "U")
    {
      digitalWrite(dirPin_Vertical, HIGH); // set direction to up
      Serial.print(" Up: ");
      Serial.print(steps_Vert);
    }
  
    pulse_delay = split_word[4].toInt();
    if(pulse_delay < 15)
    {
      pulse_delay = 200;
    }

    step_Count = 0; 
    Serial.print(" Pulse Delay: ");
    Serial.println(pulse_delay);

    

}
