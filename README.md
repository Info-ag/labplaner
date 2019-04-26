# Labplaner
[![Build Status](https://travis-ci.org/Info-ag/labplaner.svg?branch=master)](https://travis-ci.org/Info-ag/labplaner)

Labplaner is a web application specifically build for the [Life-Science Lab Heidelberg](https://www.life-science-lab.org).  
It combines multiple polls into one to avoid conflicts and provides you with an optimal date for the next meeting.

## Requirements and Setup
 - **Python** >= 3.6
 - **MySQL** or SQLite
 - **redis**

You might want to use `virtualenv` to set up a local development enviroment:
```bash
# install virtualenv
pip3 install virtualenv
# .. or pip or python -m pip or python3 -m pip

# create a virtual enviroment
virtualenv venv

. venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Inside the `config` folder, you need the following files:
 - `base.cfg` for your base configuration, that is shared across `dev`, `test` and `prod`
 - `dev.cfg` for your development specific configuration
 - `test.cfg` for your test specific configuration
 - `prod.cfg` for your production specific configuration
 - `secret.cfg` *(optional)* for secrets **NEVER INCLUDE THIS IN YOU COMMIT**

You can use the `secret-template.cfg` to create your own `secret.cfg` configuration.

You can change the default location of those config files using the following enviroment variables:
 - `BASE_CONFIG` (default: `config/base.cfg`)
 - `CONFIG` (default: `config/dev.cfg`)
 - `TEST_CONFIG` (default: `config/test.cfg`)
 - `SECRET` (default: `config/secret.cfg`)

Additional enviroment variables:
 - `ENV` (default: `development`, can be either `development`, `test`, `production`)

### Run
Make sure to run `redis-server` and your database implementation, then run huey and the app:
```bash
# tasks:
huey_consumer run_huey.huey
# main application:
python run.py
```

### Test
We use `unittest` and `selenium` for testing labplaner.
You will have to install `selenium` first (see [Selenium-Python Installation](https://selenium-python.readthedocs.io/installation.html))

#### Run tests
```
python -m unittest test/test_labplaner.py   # for backend/flask tests
python -m unittest test/test_frontend.py    # for selenium tests
# or any other test file
```

### Contribute
Pull requests are alyways welcome! Feel free to fork the project and improve it.

## License

   Copyright 2018-2019 Life-Science Lab <Informatik-ag@life-science-lab.net>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
