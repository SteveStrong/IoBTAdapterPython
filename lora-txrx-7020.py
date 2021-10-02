
from loratxrxduplex import LoraTXRX

def main():
    
    hub = LoraTXRX("COM9", 57600, "http://localhost:7020", "7020")

    hub.start()
    # hub.ping("Lora radio is listening COM5")
    hub.run()

if __name__ == '__main__':
    main()