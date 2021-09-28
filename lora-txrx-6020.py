
from loratxrxsync import LoraTXRX

def main():
    
    LoraTXRX("COM5", 57600, "http://localhost:6020")


if __name__ == '__main__':
    main()