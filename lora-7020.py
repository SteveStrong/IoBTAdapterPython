import time
from loratxrx import LoraTXRX

def main():
    
    hub = LoraTXRX("7020_server", "COM9", "http://localhost:7020")
      

    hub.start()
    hub.run()

if __name__ == '__main__':
    main()