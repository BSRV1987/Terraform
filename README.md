# Terraform
# If you are to use this solution , use your own aws keys and paste access key and value in main.tf file.
=======
# Problem Statement 

input is an example battery sensor data that is encoded <br>
Written a Python lambda function that takes as input an event:<br>
{<br>
 "device": string,<br>
 "payload": string<br>
}<br>
and logs the data to stdout in the following format:<br>
{<br>
 "device": string,<br>
 "time": integer,<br>
 "state": string,<br>
 "state_of_charge": float,<br>
 "temperature": float<br>
}<br>
2). Terraform<br>
Deployed the lambda function using Terraform<br>
Encoding<br>
The data is transmitted as a hexadecimal string. Every payload consists of 8 bytes. Due to space optimization, the information is not byte aligned. <br>
A field can start in the middle of a byte. We therfore need bit operations to decode the payload. The payload is not signed and encoded in little <br>
Endian.<br>

The following sentence describes the data fields contained in the payload and their bit positions. 8 BYTES=64 BITS<br>
****type 0-4 BITS , time 4-43 BITS , STATE 44-47 , STATEOFCHARGE 48-55 , BATTERY TEMPERATURE 56-63****
 
For instance, type is encoded on 4 bits in the first byte. state of charge is encoded on 8 bits (1 byte) on the 6th byte.<br>
Time<br>
time represents the timestamp of the data. It is defined in seconds since UNIX epoch.<br>
State<br>
state is a string, with the following corresponding values:<br>
0: "power off"<br>
1: "power on"<br>
2: "discharge"<br>
3: "charge"<br>
4: "charge complete"<br>
5: "host mode"<br>
6: "shutdown"<br>
7: "error"<br>
8: "undefined"<br>
State of charge<br>
state of charge represents the charge of the battery. It is a float with values between 0 and 100 and a 0.5 precision. To store it as an integer <br>
it was multiplied by 2.<br>
Battery temperature<br>
battery temperature represents the temperature of the battery. Values can vary between -20 and 100. The precision is 0.5. To store it as an <br>
integer we added 20 and multiplied it by 2.<br>
Test data<br>
input:<br>
F1E6E63676C75000<br>
output:<br>
{<br>
 "time": 1668181615,<br>
 "state": "error",<br>
 "state_of_charge": 99.5,<br>
 "temperature": 20.0<br>
}<br>
input:<br>
9164293726C85400<br>
output:<br>
{<br>
 "time": 1668453961,<br>
 "state": "discharge",<br>
 "state_of_charge": 100.0,<br>
 "temperature": 22.0<br>
}<br>
input:<br>
6188293726C75C00<br>
output:<br>
{<br>
 "time": 1668454534,<br>
 "state": "discharge",<br>
 "state_of_charge": 99.5,<br>
 "temperature": 26.0<br>
<br>
