import requests
import sys
data=requests.get("http://10.0.20.135:8000/items/kw")
print(len(data.content))
print(sys.getsizeof(data.content))