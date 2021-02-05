import os
from pywebostv.discovery import * 
from pywebostv.connection import *
from pywebostv.controls import *

def getTvClient():
	store = {'client_key': 'd123747cbbfa54a322dad4343163f646'}
	while True:
		try:
			client = WebOSClient("192.168.0.22")
			client.connect()
			for status in client.register(store):
				if status == WebOSClient.PROMPTED:
					print("Please accept the connect on the TV!")
				elif status == WebOSClient.REGISTERED:
					print("Registration successful!")
					return client
		except:
			tvPower('a')
			time.sleep(2)

def changeSourceTv(a):
    client = getTvClient()
    source_control = SourceControl(client)
    source_control.set_source(source_control.list_sources()[a])


changeSourceTv(2)