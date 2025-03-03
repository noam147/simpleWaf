"""here we will check php files"""

from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner
import urllib.parse
from GenericAttackUtils import StrictnessLevel,get_strictness_from_int
ATTACKER_RETURN = ["ATTACKER!"]
def get_content_dispostion_from_headers(data: HTTPServerRequest):
    keyword = "boundary="
    bytes_boundary = b""
    """example of input: b'--------------------------43b7b827abba990e\r\nContent-Disposition: form-data; name="file"; filename="exampleFile.txt"\r\nContent-Type: text/plain\r\n\r\nthis is an example file for the testing in file uploads\r\nyay\r\n--------------------------43b7b827abba990e--\r\n'"""
    headers = data.headers
    for key,value in headers.items():
        if key !="Content-Type":
            continue
        index = value.find(keyword)
        if index == -1:
            return b""
        str_boundary:str = value[index+len(keyword):]
        str_boundary = str_boundary.strip()#remove any spaces
        bytes_boundary = str_boundary.encode()
        return b"--"+bytes_boundary+b"\r\n"#does not need to keep checking
    return bytes_boundary

def get_full_body_back(parts,bytes_boundary):
    bytes_msg = b""
    for cell in parts:
        bytes_msg += cell
        bytes_msg += bytes_boundary
    return bytes_msg
def get_files_properties(data: HTTPServerRequest) -> list[str]:
    filenames:list[str] = []
    bytes_boundary = get_content_dispostion_from_headers(data)
    if bytes_boundary == b"":
        return []
    variables_in_body = data.body.split(bytes_boundary)#todo check if the boundary isnt the same on header with the server handling: for testing
    if len(variables_in_body) == 0 or len(variables_in_body) == 1:
        ### if for some reasons the headers say this is a speicifc type but it actuaaly isnt
        return []
    #del parts[0]
    #del parts[-1]
    for properties_of_var in variables_in_body:
        ### iterates on each 'var' in body

        curr = properties_of_var.strip()
        if not curr:
            continue#empty part

        try:
            headers,actual_data = properties_of_var.split(b"\r\n\r\n")#todo check if this only on windows(the \r\n)
        except Exception:
            continue
        ### serach for files ###
        keyword = b"filename"
        index = headers.find(keyword)

        if index == -1:
            ### if this is just a var like username of something like that, we do not care. we want jjust files ###
            continue

        ### get the name of file on str ###
        name_of_file:bytes = headers[index+len(keyword):]
        temp_str_filename:str = name_of_file.decode()
        actual_name = temp_str_filename.split("\"")#the file name before this looks like this: '="exa%22mple\\\\%22File.txt"\r\nContent-Type: text/plain'

        if len(actual_name) != 3:#if for some reason there are more than 3 " - does not suppose to happend at all
            return ATTACKER_RETURN

        ### this is the REAL file name! ###
        str_filename = actual_name[1]
        filenames.append(str_filename)

    return filenames

class Files_Scanner(IAttack_Scanner):


    @staticmethod
    def search_file_traversal(data : HTTPServerRequest) -> bool:
        url:str = data.uri
        decoded_url:str = urllib.parse.unquote(url)
        #prase the url and check for ../#
        return "../" in decoded_url or "..\\" in decoded_url

    @staticmethod
    def search_file_formats(data: HTTPServerRequest) -> bool:
        ### we still didn't implement the defend level in param in func ###
        attack_defend_level = 2

        filenames = get_files_properties(data)
        if filenames == ATTACKER_RETURN:
            return True  ###if during the file prasing something that really does not suppose to happen actually happend

        allowed_file_extensions = [".png", ".jpg", ".docx", ".jpeg", ".jiff", ".pdf", ".txt"]
        for file_name in filenames:
            ### find the last accurance of '.' for extension
            index_extension = file_name.rfind(".")
            if index_extension == -1:
                ### the file does not have an extention ###
                continue  ###we will not block files without extensions
            file_extension = file_name[index_extension:].lower()
            if "php" in file_extension and attack_defend_level > 0:
                ### we do not want php files at all cost (just if the web explicitily allows)###
                return True

            ### check if in allowed format,
            # but if user mistakenly uploaded file that is not in the format,
            # should we really declare him as an attacker?
            if file_extension not in allowed_file_extensions:
                if attack_defend_level > 1:  # for website pref table
                    return True
        return False
    @staticmethod
    def scan(data: HTTPServerRequest, pref_of_web) -> bool:
        """levels for -
        block anyone who tries php files - 1
        block anyone who tries to upload files that are not in the waf format - 2"""
        if isinstance(pref_of_web, int):
            strictness = get_strictness_from_int(pref_of_web)
        else:
            print("error on file upload. check type of pref")
            strictness = StrictnessLevel.STRICT
        if strictness != StrictnessLevel.LOW:
            if Files_Scanner.search_file_traversal(data):
                return True
            if Files_Scanner.search_file_formats(data):
                return True
        return False

