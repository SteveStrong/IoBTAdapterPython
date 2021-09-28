
from loratxrxsync import LoraTXRX

def main():
    
    LoraTXRX("COM4", 57600, "http://localhost:6010")


if __name__ == '__main__':
    main()