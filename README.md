# ArduinoHID-Scripter
A GUI tool that generates Arduino HID scripts from mnemonics.

# Supported Arduino Boards
The following boards are working on a microcontroller named ```ATMEGA32U4```.<br>
```32``` means it has 32 Kb memory, ```U``` means it has built-in USB Communication and ```4``` means 4 Kb of memory consumed by bootleader.<br>
It has a built-in USB Communication so that it can act as ```Keyboard```, ```Mouse```, ```Game Controller``` etc.<br>
List of supported boards : <br>
<ul>
  <li>Arduino Leonardo</li>
  <li>Arduion Micro</li>
  <li>Arduino Pro Micro</li>
</ul>

# Credits
The mnemoics used in this tool is heavily inspired by <a href="https://github.com/hak5">Hak5</a> Ducky Script.<br>

# Demo Video

https://github.com/wirebits/ArduinoHID-Scripter/assets/159493381/7eb83c57-96db-4053-98e1-03ee21dff9fd

# Setup and Installation of Arduino IDE
1. Download Arduino IDE from <a href="https://www.arduino.cc/en/software">here</a> according to your Operating System.<br>
2. Install it.<br>

# Mnemonic Table
<table>
 <tr>
  <th>Mnemonics</th>
  <th>Description</th>
  <th>Example</th>
 </tr>
 <tr>
  <th>TYPE</th>
  <th>It add text want to type in the code.</th>
  <th>TYPE Hello World!</th>
 </tr>
 <tr>
  <th>PRESS</th>
  <th>It press and hold the key(s) and then release all key(s).</th>
  <th>PRESS GUI R</th>
 </tr>
 <tr>
  <th>WAIT</th>
  <th>It add time in the code.<br>Time is in milliseconds.<br>1000 = 1 second.</th>
  <th>WAIT 1000</th>
 </tr>
</table>

# Example
Mnemonic for Open Notepad and Type

```
WAIT 1000
PRESS GUI R
WAIT 1000
TYPE notepad
WAIT 1000
PRESS ENTER
TYPE This is a test for arduino script developed by ArduinoHID Scripter!
```
after click on ```Convert``` button, the arduino script of the following mnemonic is :<br>

```
#include<Keyboard.h>
void setup()
{
 Keyboard.begin();
 delay(1000);
 Keyboard.press(KEY_LEFT_GUI);
 Keyboard.press('r');
 Keyboard.releaseAll();
 delay(1000);
 Keyboard.print("notepad");
 delay(1000);
 Keyboard.press(KEY_RETURN);
 Keyboard.releaseAll();
 Keyboard.print("This is a test for arduino script developed by ArduinoHID Scripter!");
 Keyboard.end();
}
void loop()
{
 //Nothing to do here ;)
}
```
Just copy this code and paste it in the Arduino IDE.<br>
# Tested Systems
The tool is currently tested on : <br>
1. Windows (10)<br>
The testing is going on different systems.

# Install and Run
1. Download or Clone the Repository.<br>
2. Open the folder and just double click on ArduinoHIDScripter.py file.<br>
3. Type the mnemonics in the left window.<br>
4. Click on ```Convert``` button to get corresponding arduino script.<br>
5. Click on ```Copy``` button to copy the arduino script to the clipboard.<br>
6. Paste the code in the Arduino IDE.<br>
7. Connect your board to the PC/Laptop.<br>
8. Compile the code.<br>
9. Select the board from the ```Tools```.<br>
10. Select the port number of that board.<br>
11. Upload the code.<br>
-Be Careful! As it is uploaded the script start executing.<br>

<h1>Key Features</h1>
<b>1. Simple and clean GUI.</b><br>
<b>2. Two large windows one for mnemonics and other for arduino code.</b><br>
<b>3. Convert Button - Convert mnemonics to arduino script.</b><br>
<b>4. Copy Button - Copy arduino script to the clipboard so that it can paste anywhere.</b><br>
<b>5. Reset Button - Clear all data from both windows.</b><br>
<b>6. Save Button - Save arduino scripts on the system for future use.</b><br>
<b>7. Exit Button - Close the application.</b><br>
