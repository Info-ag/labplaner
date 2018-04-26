# Labplaner
Labplaner is a web application specifically build for the [Life-Science Lab Heidelberg](https://www.life-science-lab.org).  
It combines multiple polls into one to avoid conflicts and provides you with an optimal date for the next meeting.

## Usage
Clone or download the repository.  
What you need:
 - **Python >= 3.6**
 - **MySQL** or SQLite

Make sure the requirements are installed using `pip`:
```bash
sudo python3 -m pip install -r requirements.txt
```

You might want to setup the MySQL Database:
```bash
sudo sh setupdb.sh
```

Prepare the database:
```bash
FLASK_APP=src/app.py python3 -m flask db init
FLASK_APP=src/app.py python3 -m flask db merge -m "init"
FLASK_APP=src/app.py python3 -m flask db upgrade
```

Finally, you can run the server:
```bash
FLASK_APP=src/app.py python3 -m flask run
```

## Development
Follow the same steps as in **Usage**. You migth need to `merge` and `upgrade` the database everytime you change the model.

### Structure
```text
├── LICENSE
├── README.md
├── clear-db.sh
├── requirements.txt
├── setupdb.sh
└── src                         # Main source code
    ├── algorithm.py            # Algorithm for finding the best date
    ├── app.py                  # Entry point
    ├── blueprints              # Routes
    │   ├── auth.py
    │   └── api
    │       └── v1
    │           └── api.py
    ├── dbconfig.py             # DB configuration
    ├── models                  # DB models
    │   └── user.py
    ├── static                  # Static files
    │   ├── css
    │   └── js
    ├── templates               # Jinja Templates
    │   ├── base.html
    │   └── index.html
    └── utils.py                # Helper functions
```

### Contribute
Pull requests are alyways welcome! Feel free to fork the project and improve it.
## License

   Copyright 2018 Life-Science Lab <Informatik-ag@life-science-lab.net>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
