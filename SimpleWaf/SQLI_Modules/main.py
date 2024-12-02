import SQLI_Scanner
import urllib.parse

def main():
    with open("Intruder/detect/Generic_SQLI.txt","r") as sqli_file:
        # prints the sqli's from the file that the scanner did not detect
        print(str([sqli_statement \
                   for sqli_statement in urllib.parse.unquote(sqli_file.read()).splitlines() \
                   if SQLI_Scanner.SqliScanner.scann(sqli_statement) == False]).replace(',', '\n'))

if __name__ == "__main__":
    main()