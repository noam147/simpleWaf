"""here we will check php files"""

from tornado.httputil import HTTPServerRequest
from Attack_Scanner import IAttack_Scanner



class Files_Scanner(IAttack_Scanner):
    @staticmethod
    def scan(data: HTTPServerRequest) -> bool:
        allowed_file_extentions = {".png", ".jpg", ".docx", ".jpeg", ".jiff", ".pdf"}
        files = data.files
        for file in files:
            file_name: str = file.name
            ### find the last accurance of '.' for extension
            index_extension = file_name.rfind(".")
            if index_extension == -1:
                ### the file does not have an extention ###
                pass
            file_extension = file_name[index_extension:].lower()
            if "php" in file_extension:
                ### we do not want php files at all cost ###
                return True

            ### check if in allowed format,
            # but if user mistakenly uploaded file that is not in the format,
            # should we really declare him as an attacker?
            if file_extension not in allowed_file_extentions:
                return True
        return False
