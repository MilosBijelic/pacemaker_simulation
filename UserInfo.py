

class UserInfo:
    
        # opens a .txt file and reads the data.
        # creates a dictionary that looks like:
        # {'username' : {'password' : "", 'pulse_width' : "", 'pulse_amplitude' : "", 'heart_rate' : "", 'chamber_to_pace' : ""}, ...}
        def __init__(self, path):

            self.userinfo = {}
            self.path = path

            f = open(self.path, "r")
            data = f.readlines()
                    
            for i in range(0, len(data)):
                data[i] = data[i].strip().split() # splits on whitespace
                self.userinfo[data[i][0]] = {'password' :        data[i][1],
                                             'pulse_width' :     data[i][2],
                                             'pulse_amplitude':  data[i][3],
                                             'heart_rate':       data[i][4],
                                             'chamber_to_pace':  data[i][5]}
            f.close()

                    
        # saves userinfo variable into the text file given by path
        def save_file(self):

            f = open(self.path, "w")
            for key in self.userinfo.keys():
                user = self.userinfo[key]
                f.write(str(key) + "\t" + str(user['password']) + "\t" + str(user['pulse_width']) + "\t" + str(user['pulse_amplitude']) + "\t" + str(user['heart_rate']) + "\t" + str(user['chamber_to_pace']) + "\n")
            f.close()

            return "File saved."

        # clears the contents of the file
        def reset_file(self):
            f = open(self.path, "w")
            f.close()

            self.userinfo = {}

            return "File Reset."

        # checks if the username has already been created.
        # initalizes parameters to 0.
        def register(self, user, password):
            
            if user in self.userinfo.keys():
                return "This username has already been used."

            self.userinfo[user] = {  'password' :        password,
                                     'pulse_width' :     0,
                                     'pulse_amplitude':  0,
                                     'heart_rate':       0,
                                     'chamber_to_pace':  0  }

            return "User created."

        # checks if username and password is correct
        # returns string with an error message or "Login successful."
        def login(self, user, password):
            
            if user not in self.userinfo.keys():
                return "This user does not exist."
            elif self.userinfo[user]['password'] != password:
                return "The password is incorrect."
            elif self.userinfo[user]['password'] == password:
                return "Login successful."

        # updates the user with the given parameters.
        # must call save_file() before closing the program.
        def update_user(self, user, pulse_width, pulse_amplitude, heart_rate, chamber_to_pace):
            
            if user not in self.userinfo.keys():
                return "This user does not exist,"

            self.userinfo[user]['pulse_width']       = pulse_width
            self.userinfo[user]['pulse_amplitude']   = pulse_amplitude
            self.userinfo[user]['heart_rate']        = heart_rate
            self.userinfo[user]['chamber_to_pace']   = chamber_to_pace

            return "User updated."

        # returns user parameters as a list
        def get_user_info(self, user):

            if user not in self.userinfo.keys():
                return "This user does not exist."

            return self.userinfo[user]['pulse_width'], self.userinfo[user]['pulse_amplitude'], self.userinfo[user]['heart_rate'], self.userinfo[user]['chamber_to_pace']




## DEMO
userinfo = UserInfo("userinfo.txt")

print(userinfo.reset_file())

print(userinfo.register("John", "sjfdssof"))
print(userinfo.register("Alex", "gfsdaafdsa"))
print(userinfo.register("Mark", "dsadas"))
print(userinfo.register("John", "fgagfdsfas")) # duplicate

print(userinfo.update_user("Alex", .2, .4, 60, "VOO"))

print(userinfo.login("Alex", "gfsdaafdsa")) # correct password 
print(userinfo.login("Alex", "fmndjshnfsda")) # wrong password
print(userinfo.login("fdahjt", 'ouiyukytrWFQA')) # doesn't exist

print(userinfo.get_user_info('Alex'))

userinfo.save_file() # write to .txt file



