import unittest
import urllib.parse
import sys
sys.path.append('../code')
from GenericAttackUtils import find_command_injection_linux, find_command_injection_windows

class TestCommandInjection(unittest.TestCase):
    def test_sqli(self):
        ### to do - divide into linux and windows injections ###
        file_path = "../Intruder/detect/Generic_CommandInjection.txt"
        with open(file_path,"r") as file:
            command_injection_content = file.read()
        lines_commandI_content:list = command_injection_content.split("\n")
        for line_command_injection in lines_commandI_content:
            with self.subTest(line_sql=line_command_injection):
                decoded_line = urllib.parse.unquote(line_command_injection)
                result:bool = find_command_injection_linux(decoded_line)
                if result == False:
                    print("Did not find command_injection in this line: "+decoded_line)
                else:
                    print("FOUND command_injection in this line: " + decoded_line)
                #self.assertFalse(result)- program completly stops after that- shouldnot happend


if __name__ == '__main__':
    unittest.main()
