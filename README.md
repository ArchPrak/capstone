Installation Manual
• Clone the repository

$ git clone https://github.com/sparsha-p/Capstone1
$ cd Capstone1
• Install virtualenv package

$ sudo apt-get install python-virtualenv
• Create a new virtual environment modelvenv
$ virtualenv -p python3 modelvenv

• Activate the environment

$ source modelvenv/bin/activate
• Install the model requirements

(modelvenv) $ pip install -r modelvenv-requirements.txt

• Deactivate the environment
(modelvenv) $ deactivate

• Create another virtual environment venv and activate the environment

$ virtualenv -p python3 venv
$ source venv/bin/activate
• Install the requirements

(venv) $ pip install -r requirements.txt

• Run the app

(venv) $ python src/app.py

_____________________________________________________________________________________
Dept. of CSE Jan - May, 2021 Page No. 42
User Manual
• Open http://localhost:5000/ in your browser
• Navigate to the Home page
• Navigate to either to Boolean domain or SQL domain
• Insert facts and questions and click Solve in case of the Boolean domain
• Facts received and evaluated result is displayed
• Insert query description in case of the SQL domain
• SQL query and rows of the database displayed in form of table

Integration and deployment
Flask has been used to integrate and deploy our app as a client-server architecture. Flask is a popular
micro web framework in Python that uses REST API’s to communicate via HTTP. REST stands for
Representational State Transfer that defines a set of rules for an application to exchange data. REST is
stateless, cacheable and provides a uniform interface between the components. Flask implements REST
by default.
The benepar module used in the pre-processing supports Tensorflow 1.x while the encoder-decoder
model runs on Tensorflow 2.x. We use virtual environments to overcome this issue since different
versions of Tensorflow are required to achieve various tasks. A virtual environment is a copy of the
Python interpreter that creates an isolated environment. To solve this problem, we have created two
virtual environments. One to run the Flask app, pre-process the query and evaluate the questions and
the other to train the model and predict.
The qa function uses GET request to render the index page that contains a form to accept the user’s
facts and questions. On the other hand, the upload function uses POST request to retrieve the contents
of the form, run different pre-processing and machine learning models and evaluate the questions then
returns the rendered index page displaying the result. The sql function uses GET request to render the
sql page that contains a form to accept the description of the user query. This function also uses POST
request to retrieve the description, run different pre-processing and encoder-decoder models to obtain
the SQL query that is run on the database and displayed onto the frontend.
