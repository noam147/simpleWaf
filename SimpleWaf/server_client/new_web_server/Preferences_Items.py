class Preferences_Items:
    def __init__(self,preferences:list):
        #example of input is:
        #[("mySite.com",2,False,True,2,True,1,80,False)]

        preferences:tuple = preferences[0]### get the actuall data tuple
        self.host_name:str = preferences[0]
        self.sql_level:int = preferences[1]
        self.xss_defence:bool = preferences[2]
        self.hpp_defence:bool = preferences[3]
        self.file_attack_level:int = preferences[4]
        self.to_send_email:bool = preferences[5]
        self.os_level:int = preferences[6]
        self.port:int = preferences[7]
        self.isHttps:bool = preferences[8]#if false we will do http...

    def to_string(self) -> str:
        return (
            f"Preferences Of {self.host_name}:\n"
            f"Host Name: {self.host_name}\n"
            f"SQL Level: {self.sql_level}\n"
            f"XSS Defence: {'Enabled' if self.xss_defence else 'Disabled'}\n"
            f"HPP Defence: {'Enabled' if self.hpp_defence else 'Disabled'}\n"
            f"File Attack Level: {self.file_attack_level}\n"
            f"Send Email When Attacked: {'Yes' if self.to_send_email else 'No'}\n"
            f"OS Level: {self.os_level}\n"
            f"Port: {self.port}\n"
            f"Protocol: {'HTTPS' if self.isHttps else 'HTTP'}"
        )

    def to_dict(self) -> dict:
        return {
            "host_name": self.host_name,
            "sql_level": self.sql_level,
            "xss_defence": self.xss_defence,
            "hpp_defence": self.hpp_defence,
            "file_attack_level": self.file_attack_level,
            "to_send_email": self.to_send_email,
            "os_level": self.os_level,
            "port": self.port,
            "isHttps": self.isHttps
        }

