# FILE 2 DRIVE - Drive URL Shortener 🔥

This a drive url shortener used to hide your original file ID and share with your friends. Powered by your google Drive API.

## installing

### The SIMPLE WAY

STEP 1:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
STEP 2:
GET YOUR APP CREDENTIALS
STEP 3:
put these variable in the heroku env. variables.
STEP 4:
Boom!.... your done!


### The Legacy Way
Simply clone the repository and run the main file:

```sh
git clone https://github.com/prdpjngd/file2drive.git
cd file2drive
virtualenv -p /usr/bin/python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### get your  CREDENTIALS👇
```
STEP 1: Turn on drive API
Goto https://developers.google.com/drive/api/v3/quickstart/js
then Click on "Enable the Drive API" button and it will give you client_id & client_secret

STEP 2: Create a API key
on the same page of step 1 -
click on button "Create API key" it will give you API key.
```

### Variable Explanations

##### Mandatory Variables

* `client_id or c_i`: This is client_id your google api account (cloud console)
* `client_secret or c_s`: This is client_secret for any transection of API
* `mya or API KEY`: API key for google apps uses. ( shows your ID )




## Credits, and Thanks to

* [MR.MARVEL](https://telegram.dog/hello2hack) for Perfect UX.
