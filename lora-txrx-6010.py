
from loratxrxduplex import LoraTXRX

def main():
    
    hub = LoraTXRX("COM4", 57600, "http://localhost:6010", "6010")

    hub.start()
    # hub.ping("Lora radio is listening")
    hub.run()

if __name__ == '__main__':
    main()