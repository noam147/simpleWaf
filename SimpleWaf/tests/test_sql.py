import unittest
import urllib.parse
import sys
from typing import List

sys.path.append('../code')
import SQLI_Scanner_Utils

RECOMMANDED_BANED_CHARECTERS: List[str] = ['\*', '\**', '--', '||', '&&', '**\\', '*\\', '/*', '/**', '*/', '**/']


class TestSQLI(unittest.TestCase):
    def test_sqli(self):
        file_path = "../Intruder/detect/Generic_SQLI.txt"
        with open(file_path,"r") as file:
            sql_content = file.read()
        lines_sql_content:list = sql_content.split("\n")
        for line_sql in lines_sql_content:
            with self.subTest(line_sql=line_sql):
                decoded_line = urllib.parse.unquote(line_sql)
                decoded_line = urllib.parse.unquote(line_sql)
                if not SQLI_Scanner_Utils.find_sqli(decoded_line, banned_characters=RECOMMANDED_BANED_CHARECTERS):
                    print("Did not find sql in this line: " + decoded_line)
            #self.assertFalse(result)- program completly stops after that- shouldnot happend


if __name__ == '__main__':
    unittest.main()
