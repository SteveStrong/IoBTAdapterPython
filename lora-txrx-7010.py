
from loratxrxduplex import LoraTXRX

def main():
    
    hub = LoraTXRX("COM8", 57600, "http://localhost:7010", "7010")
      
    ##hub = LoraTXRX("COM4", 57600, "http://10.8.0.202:80", "202")

    hub.start()
    # hub.ping("Lora radio is listening")
    hub.run()

if __name__ == '__main__':
    main()