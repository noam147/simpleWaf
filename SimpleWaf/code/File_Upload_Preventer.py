"""here we will not check for the file types, this is in the Attack scanner"""
"""here we will eascape speacial characters in the file name"""
"""here we will delete the ; char from the file to prevent reverse shell"""
from Attack_Preventer import Attack_Scanner
from tornado.httputil import HTTPServerRequest
import urllib.parse
class File_Upload_Preventer(Attack_Scanner):
    @staticmethod
    def replace_file_name(name:str) -> str:
        curr_name = name
        curr_name = urllib.parse.unquote(curr_name)#get the actual string

        ### delete slashes and semicolumn###
        curr_name = curr_name.replace("/","")
        curr_name = curr_name.replace("\\","")
        curr_name = curr_name.replace(";","")
        if len(curr_name) == 0:
            return "UNNAMEDFILE"
        return curr_name
    @staticmethod
    def edit_request(request: HTTPServerRequest,pref_of_web) -> HTTPServerRequest:
        if isinstance(pref_of_web, bool):
            if pref_of_web == False:
                # if web does not want protection
                return request
        """iterate over files and change their name by removing special chars"""
        if 'files' in request.files:
            # Iterate through the files sent in the request
            for file_name, file_data_list in request.files.items():
                for file_data in file_data_list:
                    original_filename = file_data['filename']
                    file_name['filename'] = File_Upload_Preventer.replace_file_name(original_filename)
        return request
