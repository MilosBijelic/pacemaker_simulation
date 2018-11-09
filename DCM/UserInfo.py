

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
                inp = str(key) + "\t%(password)s\t%(pulse_width)s\t%(pulse_amplitude)s\t%(heart_rate)s\t%(chamber_to_pace)s\n"
                inp %= self.userinfo[key]
                f.write(inp)
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

            self.save_file()

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

