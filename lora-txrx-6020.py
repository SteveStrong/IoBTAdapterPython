
from loratxrxduplex import LoraTXRX

def main():
    
    hub = LoraTXRX("COM5", 57600, "http://localhost:6020", "6020")

    hub.start()
    # hub.ping("Lora radio is listening COM5")
    hub.run()

if __name__ == '__main__':
    main()