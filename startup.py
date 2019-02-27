

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import subprocess
import  time
import datetime
import math
pnconfig = PNConfiguration()

pnconfig.publish_key ='pub-c-9c260cad-9e78-4bea-a3a9-f584ea818532'
pnconfig.subscribe_key = 'sub-c-2e6e94ce-305d-11e9-a223-2ae0221900a7'
pubnub = PubNub(pnconfig)
x=10
def callback(message, status):
	print(message)
avg=0.0
count=0
while x>0:
	x-=1
	count+=1
	time.sleep(1)
	p = subprocess.check_output('lifepo4wered-cli get vbat',shell=True)
	b1=round(float(p)/1000,5)
	p = subprocess.check_output('lifepo4wered-cli get vout',shell=True)
	r1=round(float(p)/1000,5)
	data ={
	"eon":{"Battery Voltage (Volts)":b1,"Raspberry Pi Voltage (Volts)":r1}
	}
	avg=avg+r1
	data2={	"PL":20,"ON":round(avg/count,3),"W":"Working","S":x,"WT":"Not Set Yet"}
	pubnub.publish().channel('test').message(data).pn_async(callback)
	pubnub.publish().channel('test2').message(data2).pn_async(callback)


avg=round(avg/count,5)
now=str(datetime.datetime.now() + datetime.timedelta(minutes = 10))
data3={	"PL":0,"ON":avg,"W":"Sleeping Now","S":0,"WT":now}
pubnub.publish().channel('test2').message(data3).pn_async(callback)

subprocess.call('lifepo4wered-cli set WAKE_TIME 2',shell=True)
subprocess.call('sudo shutdown -h now',shell=True)
