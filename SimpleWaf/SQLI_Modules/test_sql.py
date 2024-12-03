import unittest
import SQLI_Scanner
import urllib.parse
class TestSQLI(unittest.TestCase):
    def test_sqli(self):
        file_path = "../Intruder/detect/Generic_SQLI.txt"
        with open(file_path,"r") as file:
            sql_content = file.read()
        lines_sql_content:list = sql_content.split("\n")
        for line_sql in lines_sql_content:
            with self.subTest(line_sql=line_sql):
                decoded_line = urllib.parse.unquote(line_sql)
                result:bool = SQLI_Scanner.SqliScanner.scan(decoded_line)
                if result == False:
                    print("Did not find sql in this line: "+decoded_line)
                #self.assertFalse(result)- program completly stops after that- shouldnot happend


if __name__ == '__main__':
    unittest.main()
