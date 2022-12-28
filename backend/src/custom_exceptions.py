class EntityWasNotStored(Exception):
    pass

class UserPermissionException(Exception):
    def __init__(self,message:str | None = None):
        self.default_err_msg = 'User specified permission is not recognized.'
        if message:
            return super().__init__(self,message)
        else:
            return super().__init__(self,self.default_err_msg)