class UserData:
    """
    User data base class. 
    Information about the title, description, login, password, mail is stored here. 
    
    The library does not depend on the attributes, but depends only on the methods `to_dict` and `from_dict`. 
    
    So feel free to create another class with other attributes you need.
    """
    
    def __init__(self, title: str = '', login: str = '', password: str = '', email: str = '', description: str = ''):
        self.title = title
        self.login = login
        self.password = password
        self.email = email
        self.description = description

    def to_dict(self):
        return {
            "title": self.title,
            "login": self.login,
            "password": self.password,
            "email": self.email,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def __str__(self):
        string = f"Title: {self.title},\n"
        if(len(self.email) != 0):
            string += f"\tEmail: {self.email}\n"
        if(len(self.description) != 0):
            string += f"\tDescription: {self.description}\n"
        pass_with_stars = '*' * (50 if (len(self.password) > 50) else len(self.password))
        string += f"\tLogin: {self.login}\n\tPassword: {pass_with_stars}"
        return string
