# Image Recognition API
Image Recognition API using tensorflow &amp; deeplearning.


| Resources             | Protocol | Path      | Parameter                                                 | Status code                                                             | Description                                   |
|-----------------------|----------|-----------|-----------------------------------------------------------|-------------------------------------------------------------------------|-----------------------------------------------|
| Register<br>user      | POST     | /register | username: String<br>pw: String                            | 200 OK<br>301 User already exist                                        | Register a user                               |
| Classify image        | POST     | /classify | username: String<br>pw: String<br>URL: String             | 200 OK<br>301 Invalid user<br>302 Invalid password<br>303 Out of tokens | Classify image                                |
| Refill Tokens of user | POST     | /refill   | username: String<br>admin_pw: String<br>refillAmount: int | 200 OK<br>301 Invalid username<br>302 Invalid admin_password            | Increase/decrease the limit of tokens of user |

## Test on Postman

Body -> raw -> JSON
```
{
    "username": "Hamza",
    "password":"xyz",
    "admin_pw":"abc123",
    "refill":6,
    "url": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Plains_Zebra_Equus_quagga.jpg"
}
```

## Docker
```
docker-compose build 
docker-compose up
```
