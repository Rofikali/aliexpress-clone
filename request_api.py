import requests

url = "http://localhost:8000/api/v1/register/"
data = {
    "email": "testing3@gmail.com",
    "username":"test3",
    "password": "testing@#$1",
    "phone": "7897897898",
    "roll": "Buyer",
}
req = requests.post(url=url, data=data)
# res = req.text

print("res is here ", req.text)
print()
print('************************************')
print('status', req.status_code)
print('status success ', req.success)
print('message ', req.message)
print('message requested id ', req.request.id)
