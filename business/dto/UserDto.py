
class UserDto:
    
    def __init__(self):
        self.username = ""
        self.hashed_password = ""
        self.genres = ""
        self.last_notfication_time = ""

    def to_dict(self):
        return {
            'userid': self.username,
            'password': self.hashed_password,
            'genres': self.genres,
            'last_notfication_time': self.last_notfication_time
        }
    


