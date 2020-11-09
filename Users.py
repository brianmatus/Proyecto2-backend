class User:

	def __init__ (self, name, lastname, username, password, type):
		self.name = name
		self.lastname = lastname
		self.username = username
		self.password = password
		if (type == None):
			self.type = "cliente"
		else:
			self.type = type

	def getUserAsList(self):
		return {
			"name": self.name,
			"lastname" : self.lastname,
			"username": self.username,
			"password": self.password,
			"type":self.type
		}

class UsersHandler:

	users = []
	loggedUser = None

	@staticmethod
	def addUser(newUser):
		for user in UsersHandler.users:
			if (user.username == newUser.username):
				return False
		UsersHandler.users.append(newUser)
		return True

	@staticmethod
	def removeUserByUsername(username):
		for user in UsersHandler.users:
			if (user.username == username):
				if(user == UsersHandler.loggedUser):
					UsersHandler.loggedUser = None
				UsersHandler.users.remove(user)
				return True
		return False


	#0: sucess
	#2: new username already exist
	#3: user doesn't exist
	@staticmethod
	def modifyUser(pastUsername, newUser):


		theUser = UsersHandler.getUserByUsername(newUser.username)
		if (theUser != None and newUser.username != pastUsername):
			return 2

		print(newUser.username)


		for _user in UsersHandler.users:
			if(_user.username == pastUsername):
				UsersHandler.users.remove(_user)
				UsersHandler.users.append(newUser)
				return 0
		return 3


	#0: success
	#1: No username found
	#2: Incorrect
	@staticmethod
	def login(username, password):
		for user in UsersHandler.users:
			if (user.username == username):
				if(user.password == password):
					UsersHandler.loggedUser = user
					return 0
				else:
					return 2

		return 1
	

	@staticmethod
	def getUserByUsername(username):
		for user in UsersHandler.users:
			if user.username == username:
				return user
		return None


	@staticmethod
	def searchUsers(username, exactMatch):
		list = []

		if (username == "*"):
			return UsersHandler.users

		for user in UsersHandler.users:
			if (exactMatch == "true"):
				if (username == user.username):
					list.append(user)
			else:
				if (username in user.username):
					list.append(user)

		return list


	@staticmethod
	def getUsersAsList(theUsers):
		list = {}
		i = 0
		for user in theUsers:
			list[i] = user.getUserAsList()
			i = i + 1
		return list



		



