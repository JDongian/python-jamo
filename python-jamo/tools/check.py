import re


def validate(filename):
    with open(filename, 'r') as fin:
        last_code = 0
        for line in fin:
            try:
                results = re.findall('([\dABCDEF]{4})(.*)(HANGUL .+)', line)
                if results:
                    code, char, name = (int(results[0][0], 16),
                                        results[0][1].strip(),
                                        results[0][2])
                    if last_code == 0:
                        last_code = code
                    else:
                        if code != last_code+1:
                            return False, line, "Skipped code."
                        if code != ord(char):
                            return False, line, "Code mismatch."
                        last_code += 1
            except:
                print("Error checking line: \"{}\"".format(line))
                exit(1)
        return True


if __name__ ==  "__main__":
    from sys import argv
    status = validate(argv[1])
    if status == True:
        print("{ok, %s}" % argv[1])
    else:
        print("{error, {reason, \"%s\"}, {line, \"%s\"}}" %
              (status[2], status[1]))
