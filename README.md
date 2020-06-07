**StackHack**
=============


    Build your way from frontend to backend using Stackhack1.0




**features**
---------------------------------
    *Daily email updates about you pending tasks.
    *Email validation with the dns so that the app can't be bluffed with wrong email.
    *Login using github is provided which is an important feature for future updates of the application.




**using**
--------

```
git clone https://github.com/lims-with-autorecommendation/StackHack/
cd StackHack

if you are using pipenv
pipenv install
pipenv run python3 run.py

else
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt && pip3 install -r requirements.txt
python3 run.py
```






**TODO**
--------

- [x] Use flask-restful to interact with REST-API.
- [x] Improve UI using bootstrap.
- [x] Add login using github.
- [ ] Come up with an algorithm to sort task on the basis of priority due_date label and status.


**Contributing**
----------------
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

