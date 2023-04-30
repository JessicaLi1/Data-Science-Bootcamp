import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))
        
def reg_user():
    # Request input of a new username
        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            
        else:
            while True:
                new_username = input("New Username: ")

        # Request input of a new password
                new_password = input("New Password: ")

        #check if username already exists
                if new_username in username_password.keys():
                    print("Username exists")
                    continue
                else:
                    break

            if not check_username_and_password(new_username, new_password):
            # Username or password is not safe for storage - continue
                return False
                   
        # Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
                print("New user added")

            # Add to dictionary and write to file
                username_password[new_username] = new_password
                write_usernames_to_file(username_password)

        # Otherwise you present a relevant message.
            else:
                print("Passwords do no match")


def add_task():
         # Ask for username
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            #continue

        # Get title of task and ensure safe for storage
        while True:
            task_title = input("Title of Task: ")
            if validate_string(task_title):
                break

        # Get description of task and ensure safe for storage
        while True:
            task_description = input("Description of Task: ")
            if validate_string(task_description):
                break

        # Obtain and parse due date
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Obtain and parse current date
        curr_date = date.today()
        
        # Create a new Task object and append to list of tasks
        new_task = Task(task_username, task_title, task_description, due_date_time, curr_date, False)
        task_list.append(new_task)

        # Write to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully added.")
                   

def view_all():
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def edit_task(old_data, new_data): #define function to replace new data for old data
    with open("tasks.txt", "r") as task_file:
        data = task_file.read()
        data = data.replace(old_data, new_data)
    with open("tasks.txt", "w") as task_file:
        task_file.write(data)

def view_mine():
    print("-----------------------------------")
    has_task = False
    
    #display numbered tasks   
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(f"Task No. {(task_list.index(t))+1}") #assign each task a number
            print(t.display())
            print("-----------------------------------")

    if not has_task: #check if has tasks
            print("You have no tasks.")
            print("-----------------------------------")
    
    #option to edit the task
    while has_task == True: #stay in this menu if user has tasks so that they can edit other tasks after finishing with one, unless they press -1 to return to upper menu

        #user chooses task and editing option
        option=int(input("Enter task No. to select a task, or enter -1 to return to the main menu:\n "))
        if option in range(len(task_list)+1): 
            option = option - 1 #find intended task by index
            print(task_list[option].display())
            edit_options = input("Please select from the following options:\nc - mark the task as complete\ne - edit the task\n")

            #mark as complete
            if edit_options == "c":   
                old_status = task_list[option].to_string() #get the string of the object
                task_list[option].completed = True #change value of the instance variable to change the status to completed
                new_status = task_list[option].to_string() #generate new string for object
                edit_task(old_status, new_status) #call function to edit txt
                print("Task complete")

            #edit task
            elif edit_options == "e":
                if task_list[option].completed != True:
                    choice = input('Please choose what to edit:\nu - username\nd - due date\n')
                    #change user
                    if choice == 'u':
                        new_username_choice = input("Enter the new user assigned this task: ")
                        #put object data into a list and modify the list
                        old_username = task_list[option].to_string()
                        old_list = task_list[option].to_string().split(';') 
                        new_username = ';'.join([new_username_choice]+old_list[1:])
                        edit_task(old_username, new_username)
                        task_list[option].username = new_username_choice #change the objects that the program gathered
                        print("Username change complete")

                    #change due date
                    elif choice == "d":
                        new_date_entry = input("Enter the new due date this task (YYYY-MM-DD): ")
                        new_date_choice = datetime.strptime(new_date_entry, DATETIME_STRING_FORMAT) #change date data type
                        old_date = task_list[option].to_string()
                        old_list1 = task_list[option].to_string().split(';')
                        new_date = ';'.join(old_list1[:3]+[str(new_date_entry)]+ old_list1[4:])
                        edit_task(old_date, new_date)
                        task_list[option].due_date = new_date_choice #change due date of the existing data that the program gathered
                        print("Due date changed")

                else:
                    print("Task already completed. You cannot edit this task.")

        #end loop and return to menu if user put in -1
        elif option == -1:
            return False 

        else:
            print("Invalid input, please try again:")
    
#define function to generate report
def gen_report():
    num_tasks = len(task_list)
    num_completed = 0
    num_uncompleted = 0
    num_overdue = 0
    #count different items through for loop
    for tk in task_list:
        if tk.completed == True:
            num_completed=num_completed+1
        else:
            num_uncompleted=num_uncompleted+1
            if tk.due_date < datetime.today(): #find overdue tasks from uncompleted tasks
                    num_overdue = num_overdue+1
    #calculate percentages
    percent_incomplete = round((num_uncompleted/num_tasks)*100,2)
    percent_overdue = round((num_overdue/num_tasks)*100,2)
    #write into file
    with open("task_overview.txt", "w") as overview:           
        overview.write(f"Total number of tasks: {num_tasks}\nTotal number of completed tasks:{num_completed}\nTotal number of uncompleted tasks:{num_uncompleted}\nTotal number of tasks that are overdue:{num_overdue}\nPercentage of tasks that are incomplete:{percent_incomplete}%\nPercentage of tasks that are overdue:{percent_overdue}%")

    #write second file
    with open('user_overview.txt', 'w') as f:
            f.write(f"Total number of tasks: {num_tasks}\nNumber of users: {len(username_password.keys())}\n") #write task number and user number
    for user in username_password.keys():
        with open('user_overview.txt', 'a') as f:
            f.write(f"\nUsername: {user}\n") #write username
        user_stat = {}
        tasks = []
        i = 0
        #put one user's tasks into a list
        for t_u in task_list:
            if t_u.username == user:
                i = 1+i
                tasks.append(t_u)
        user_stat["total number of tasks for the user"]=i #put into a dictionary
        try:
            user_stat["percentage of total task number assigned to user(%)"]=round((i/len(task_list))*100,2)
        except: #in case division by 0
            user_stat["percentage of total task number assigned to user(%)"]='N/A'
        i = 0

        #put the user's incomplete tasks into a list
        incomp_tasks = []
        for x in tasks:
            if x.completed == True:
                i = i+1
            else:
                incomp_tasks.append(x)
        try:
            user_stat["assigned task complete percentage(%)"]=round((i/len(tasks))*100,2)#calculate incomplete percentage and put into dictionary
        except:
            user_stat["assigned task complete percentage(%)"]='N/A'

        #find out how many still need to be completed/are overdue
        i = 0
        j = 0
        for x in incomp_tasks:
            if x.due_date < datetime.today():
                i = i+1
            else:
                j = j+1
        try:
            user_stat["percentage of tasks assigned that must still be completed(%)"]=round((j/len(incomp_tasks))*100,2)
        except:
            user_stat["percentage of tasks assigned that must still be completed(%)"]='N/A'
        try:
            user_stat["percentage of tasks assigned that are overdue(%)"]=round((i/len(incomp_tasks))*100,2)
        except:
            user_stat["percentage of tasks assigned that are overdue(%)"]='N/A'

        #write dictionary elements into the file
        with open('user_overview.txt', 'a') as f:
            for key, value in user_stat.items(): 
                f.write(f'{key}: {value}\n')

def display_stat():
#read task_overview file into a dict
        with open("task_overview.txt", 'r') as task_report:
            task_data = task_report.read().split("\n")
        task_stat = {}
        for item in task_data:
            stat_name, stat = item.split(':')
            task_stat[stat_name] = stat
        #read user_overview file into a list
        with open("user_overview.txt", 'r') as user_report:
            user_data = user_report.read().split("\n\n")
        
        #print items in a readable way
        print("-----------------------------------")
        print("Task overview:\n")
        for key, value in task_stat.items():
            print(key+": "+value)
        print("-----------------------------------")
        print("User overview:\n")
        for x in user_data:
            print(x,"\n")         
        print("-----------------------------------")

#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Please select one of the following options:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if menu == 'r': # Register new user (if admin)
        reg_user()

    elif menu == 'a': # Add a new task
        # Prompt a user for the following: 
        #     A username of the person whom the task is assigned to,
        #     A title of a task,
        #     A description of the task and 
        #     the due date of the task.

       add_task()

    elif menu == 'va': # View all tasks
        view_all()

    elif menu == 'vm': # View my tasks
        view_mine()

    elif menu == 'gr': # generate report files
        gen_report()

    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics
        if not os.path.exists("task_overview.txt") or os.path.exists("user_overview.txt"):
            gen_report() #generate report if any one of them doesn't exist
        display_stat()
        
    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")