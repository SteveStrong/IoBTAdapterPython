import time
from loratxrx import LoraTXRX

def main():
    
    hub = LoraTXRX("7010_server", "COM8", "http://localhost:7010")
      

    hub.start()
    hub.run()

if __name__ == '__main__':
    main()