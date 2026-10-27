class User:
     def __init__(self, name=None, email=None, password=None):
          self.__name = name
          self.__email = email
          self.__password = password

     def get_name(self):
          return self.__name

     def get_email(self):
          return self.__email

     def get_password(self):
          return self.__password
