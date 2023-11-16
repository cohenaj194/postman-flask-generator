# postman-flask-generator

Can create a python flask app.py with template files from a postman collection.

Replace `WOW.postman_collection_v2.json` with your own postman file and change the values in `generate-endpoint.py` to make it work.

```
python3 generate-endpoint.py
python3 app.py
```

Then run the nightvision script in another terminal

```
nightvision login
./nightvision.sh
```