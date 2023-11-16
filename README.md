# postman-flask-generator

Can create a python flask app.py with template files from a postman collection.

Replace `WOW.postman_collection_v2.json` with your own postman file and change the values in `generate-endpoint.py` to make it work.

```
./cleanup.sh
python3 generate-endpoint.py
python3 app.py
```

`generate-endpoint.py` defaults to using the example `WOW.postman_collection_v2.json`, if you have your own collection move it to this directory and then set that file as an argument:

```
python3 generate-endpoint.py mycollectionname.postman_collection.json
```

Then run the nightvision script in another terminal

```
nightvision login
./nightvision.sh
```