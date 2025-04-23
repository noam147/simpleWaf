class Preferences_Items:
    def __init__(self,preferences:list):
        preferences:tuple = preferences[0]### get the actuall data tuple
        if len(preferences) != 9:
            print(f"should not happen. pref of {preferences[0]} is corrupted")
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