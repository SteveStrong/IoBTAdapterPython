these are the boards we are using 

https://learn.adafruit.com/adafruit-feather-32u4-radio-with-lora-radio-module/using-the-rfm-9x-radio

Links to IDE and libraries
https://www.arduino.cc/en/software
http://www.airspayce.com/mikem/arduino/RadioHead/classRH__RF95.html


that work great   

all the code you need is in this folder

you will need to set up an RX  - receiver board and and the TX - transmiter board   the ardwino code 

Good Adivce but undercontrol...

Before beginning make sure you have your Feather working smoothly, it will make this part a lot easier. Once you have the basic Feather functionality going - you can upload code, blink an LED, use the serial output, etc. you can then upgrade to using the radio itself.  

the code we used to do these tests is in the serial-testing folder.


Once you have both feather-32u4 set up (one TX one RX)   you need to run both python scripts on the target squire,  these scripts connect the radio to the Squire  notice you need to set both Squire URL (which could be LocalHost:80)  and the SerialPort the feather-32u4 is running on.  

maybe COM6 for windows or something like '/dev/tty.usbmodem11301' for Mac or Squire


For RX

    #iobtBaseURL = "http://centralmodel"
    iobtBaseURL = "https://iobtsquire1.azurewebsites.net"

    hub = LoraTXRX("COM6", iobtBaseURL)

    while(True):
        hub.wait_for_RX();

For TX

    #iobtBaseURL = "http://centralmodel"
    iobtBaseURL = "https://iobtsquire2.azurewebsites.net"

    hub = LoraTXRX("COM8", iobtBaseURL)

    while(True):
        hub.wait_for_TX()



once you have the python processing running, launch the squires at the associated URL,  and start sending messages,  change position  whatever