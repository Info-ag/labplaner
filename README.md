# Labplaner
[![Build Status](https://travis-ci.org/Info-ag/labplaner.svg?branch=master)](https://travis-ci.org/Info-ag/labplaner)

Labplaner is a web application specifically build for the [Life-Science Lab Heidelberg](https://www.life-science-lab.org).  
It combines multiple polls into one to avoid conflicts and provides you with an optimal date for the next meeting.

## Usage
Clone or download the repository.  
What you need:
 - **Python >= 3.6**
 - **MySQL** or SQLite

Make sure the requirements are installed using `pip`:
```bash
python3 -m pip install -r requirements.txt
```

You might want to setup the MySQL Database:
```bash
./setupdb.sh
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

For a clean setup run:
```bash
./clear-db.sh
```

### Structure
```text
├── LICENSE
├── README.md
├── requirements.txt
├── setupdb.sh                  # Setup MySQL/MariaDB database
├── clear-db.sh                 # Reset SQLite database
├── config
    └── development.json        # Config file while developing
└── src                         # Main source code
    ├── app.py                  # Entry point
    ├── blueprints              # Route
    │   ├── ag.py
    │   ├── auth.py
    │   ├── cal.py
    │   └── api
    │       └── v1
    │           ├── api.py
    │           ├── user.py
    │           ├── ag.py
    │           ├── date.py
    │           └── event.py
    ├── dbconfig.py             # DB configuration
    ├── models                  # DB models
    │   ├── user.py
    │   ├── ag.py
    │   ├── date.py
    │   ├── event.py
    │   └── associations.py
    ├── static                  # Static files
    │   ├── css
    │   │   ├── docs.min.css
    │   │   ├── main.css
    │   │   ├── spectre-exp.min.css
    │   │   ├── spectre-icons.min.css
    │   │   └── spectre.min.css
    │   └── js
    │       ├── cal.js
    │       ├── jquery.min.js
    │       └── pages
    │           ├── ag
    │           │   ├── add.js
    │           │   ├── dashboard.js
    │           │   ├── invite.js
    │           │   └── event
    │           │      └── add.js
    │           └── auth
    │               ├── login.js
    │               └── signup.js
    ├── templates               # Jinja Templates
    │   ├── base.html
    │   ├── base_sidebar.html
    │   ├── index.html
    │   ├── ag
    │   │   ├── add.html
    │   │   ├── dashboard.html
    │   │   ├── invite.html
    │   │   └── event
    │   │      └── add.html
    │   ├── api
    │   │   └── v1
    │   │       └── index.html
    │   ├── auth
    │   │   ├── login.html
    │   │   └── signup.html
    │   └── cal
    │       └── index.html
    ├── algorithm.py            # Algorithm for finding the best date
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
