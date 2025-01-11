import sys
from parser import Parser


if __name__ == '__main__':
    p = Parser(True)
    if len(sys.argv) == 1:
        p.help()
        exit(0)
    p.read_template()
    p.write_output()
    
    
    




