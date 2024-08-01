from skpy import Skype
from skpy import SkypeAuthException
from skpy import SkypeConnection
import os, sys, getopt
import glob
import os

def scanFolder():
    checked_folder = r"" #Input the folder path you want to search
    folders = [f for f in glob.glob(os.path.join(checked_folder, '*')) if os.path.isdir(f)]  # find all subdirectories using glob.glob
    try: # if a folder is found, choose the one with the latest creation time
            latest_folder = max(folders, key=os.path.getctime)
            print ('*Get latest_folder*: 'f'{latest_folder}')
    except SkypeAuthException:
            print("❌Not found any folder")

    return latest_folder

def login(username, password, token_file='.tokens-app'):
    sk = Skype(connect=False)
    sk.conn.setTokenFile(token_file)
    try:
        sk.conn.readToken()
        print('*Get Token*')
    except SkypeAuthException:
        sk.conn.setUserPwd(username, password)
        sk.conn.getSkypeToken()

    return sk

def send_message(sk, group_id, msg):
    result_flag = False
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        chat_channel = sk.chats[group_id]
        chat_channel.sendMsg(msg)
        result_flag = True
        print('*send_message send success*')
    except Exception as e:
        print('❌send_message send failed,', e)

    return result_flag

def upload_file(sk, group_id, pathToFile, fileName):
    result_flag = False
    try:
        sk.conn.verifyToken(SkypeConnection.Auth.SkypeToken)
        chat_channel = sk.chats[group_id]
        chat_channel.sendFile(open(pathToFile, "rb"), fileName, image=False)
        result_flag = True
        print('*upload_file send success*')
    except Exception as e:
        print('❌upload_file send failed,', e)

    return result_flag

def main(argv):
    usr_name = '' #input your account
    usr_pwd = '' #'input your password
    from_gId = '' #input group id
    to_gId = '' #input group id
    Synopsis = '-u <username> -p <password> -f <groupID> -t <groupID>'

    try:
        opts, arg = getopt.gnu_getopt(argv, 'u:p:f:t:hv')
    except getopt.GetoptError:
        print (f'❌{Synopsis}')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (f'❌{Synopsis}')
            sys.exit()
        elif opt in ("-u"):
            usr_name = arg
        elif opt in ("-p"):
            usr_pwd = arg
        elif opt in ("-f"):
            from_gId = arg
        elif opt in ("-t"):
            to_gId = arg

    if not usr_name or not usr_pwd or not from_gId or not to_gId:
        print (f'❌{Synopsis}')
        sys.exit(2)

    latest_folder = scanFolder()
    sk = login(usr_name, usr_pwd)

    folder_path = f'{latest_folder}\\index.html'
    file_createTime = latest_folder.split('\\')[3]
    send_message(sk, to_gId, f"📢The latest report's creation time：{file_createTime}\r\n Path：{folder_path}")
    upload_file(sk, to_gId, folder_path, 'index.html')

main(sys.argv[1:])
