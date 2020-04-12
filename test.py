import os.path
from os import path


if __name__ == '__main__':
    if path.exists("docs/userinfo.txt"):
        print("User info exits; starting bot...")
    else:
        print("User info not found; prompting for info...")
        token = input("Enter your bot's token: ")
        command_prefix = input("Enter your bot's command prefix: ")
        
        with open("docs/userinfo.txt", 'w') as user_file:
            user_file.write(token + "\n")
            user_file.write(command_prefix)
    