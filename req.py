import requests
import time

base = "http://127.0.0.1:5002/"
alphanumeric = {"1":'o','2':'t','3':"t",'4':"f",'5':"f",'6':"s",'7':"s",'8':"e",'9':"n",'0':"z",'.':"d"}
time = time.time()
slug = ""
for i in str(time):
    slug += alphanumeric[i]
    print(slug)
response = requests.post(base +"shorter/",json={"android_link":"this is android link","ios_link":"this ios Link","web_link":"anythign"})
print(response.json())
print(time)