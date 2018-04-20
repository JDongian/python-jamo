from sys import argv
import re
import json
import check

if __name__ == "__main__":
    filein, fileout = argv[1], argv[2]
    status = check.validate(filein)
    if status == True or len(argv) == 4 and argv[3] == '--nocheck':
        results = []
        with open(filein, 'r') as fin:
            results = re.findall('([\dABCDEF]{4}).*(HANGUL .+)', fin.read())
        with open(fileout, 'w') as fout:
            json.dump({chr(int(code, 16)): name.strip()\
                      for code, name in results}, fout,
                      sort_keys=True, indent=2)
        print("{ok, %s}" % filein)
    else:
        print("{error, {reason, \"%s\"}, {line, \"%s\"}}" %
              (status[2], status[1]))
