
class User:
    #the role should be either administartor, agent or secretary    
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role
        self.is_authenticated = False

