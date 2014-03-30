import os

if(os.path.isfile('./setenv.sh')):
        f = open("setenv.sh", "r")
        lines = f.readlines()
        for line in lines:
            if line[0] != '#':
                command = line.split()
                command = command[1].split('=')
                os.environ[command[0]]=command[1][1:-1]
#Because LiClipse is not working with os.getenv
def set_configs():
    print 'config variables set'