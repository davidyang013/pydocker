'''
Created on May 22, 2015

@author: david
'''
import os
import subprocess
import paramiko
import shlex



def string_to_line(stdout):
    return "\n".join([line.strip() for line in stdout])

class Boot2Docker():
    __b2d_path = None
    __output = None
    __error = None
    __returncode = 0

    def __init__(self, path):
        self.__b2d_path = path

    # def get_path(self):
    #     return self.__b2d_path

    def __clean__(self):
        self.__output = None
        self.__error = None
        self.__returncode = 1

    def __run(self, command):
        command = shlex.split(command)
        try:
            result = subprocess.Popen(command, stdin=subprocess.PIPE,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            (output, code) = result.communicate()
        except:
            return (None, 1)
        return (output, code) 

    def run(self, cmd):
        self.__clean__()
        (self.__output, self.__returncode) = __run(cmd)
        print self.__output
        return 

    def get_state(self):
        
        if self.__b2d_path is None:
            self.__output = "Boot2Docker can't find"
            self.__returncode = 1
            return 
        self.run("boot2docker status")
        return self.__output

    def start(self):
        self.__clean__()
        self.run("boot2docker start")
        return self.__output

    def stop(self):
        self.__clean__()
        self.run("boot2docker stop")
        return self.__output


class Docker():

    __output = None
    __error = None
    __client = None

    def __init__(self, url, port, user, pwd):
        self.url = url
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__client_init()

    def __clean__(self):
        self.__output = None
        self.__error = None 

    def __client_init(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.url,self.port,self.user,self.pwd)
        self.__client = client

    def __run(self, cmd):
        self.__clean__()
        (stdin,stdout,stderr) = self.__client.exec_command(cmd)
        self.__output = string_to_line(stdout.readlines())
        return

    def get_version(self):
        self.__clean__()
        self.__run("docker version")
        v = self.__output
        return v

    ''''
     docker images 
     -a, --all=false      Show all images (by default filter out the intermediate image layers)
     -f, --filter=[]      Provide filter values (i.e. 'dangling=true')
     --no-trunc=false     Don't truncate output
     -q, --quiet=false    Only show numeric IDs
    '''
    def get_images(self, para=None):
        self.__clean__()
        if para is None:
            self.__run("docker images")
        else:
            self.__run("docker images " + para)
        return self.__output

    def get_container(self, para=None):
        self.__clean__()
        if para is None:
            self.__run("docker images")
        else:
            self.__run("docker images " + para)
        reurn self.__output


if __name__ == "__main__":
    # b2d = Boot2Docker("/usr/local/bin/boot2docker")
    # status = b2d.get_state()
    # if status.strip() == "running":
    #     b2d.stop()
    # else :
    #     b2d.start()
    docker = Docker("192.168.59.103",22,"docker", "tcuser")
    # docker.run("docker rm $(docker ps -a -q)")
    docker.get_version()
    print docker.get_images("-q")
