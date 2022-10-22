This is a parsing tool developed with syntax agnostic learning techniques, capable of parsing and evaluating a natural language query to return a boolean result. This was implemetned as a part of a capstone research project in the final year of college in 2020. 

## Context
Program Synthesis refers to the task of constructing a program in a specific programming language, given its intent in a particular format. This emerging field can be applied in diverse domains and is currently being investigated with different techniques. A program synthesizer would simplify the efforts of programmers and help them focus on the program's core logic, without worrying about language syntax and other domain specifics. We applied the concepts of program synthesis in the context of solving a propositional logic word problem. We have developed a tool that is capable of understanding, parsing and evaluating a propositional logic word problem. With the user's natural language input, this tool processes the query and evaluates truth values of the question expressions. The working of the tool can be explained in three major phases: natural language processing, machine learning to obtain postfix notations of the Boolean expressions involved, and further evaluation of the postfix notations to determine the answers. Our goal was to explore the domain agnostic capabilities of our program-synthesis-based techniques of learning used in the implementation of this tool.

### Publication Details
Paper: [Domain Specific Program Synthesis](https://ieeexplore.ieee.org/document/9544738) <br />
Published in: 2021 Asian Conference on Innovation in Technology (ASIANCON) <br />
Publisher: IEEE<br />
Conference Location: PUNE, India<br />
Date of Conference: 27-29 August 2021<br />
Date Added to IEEE Xplore: 04 October 2021<br />

#### Authors:
* **Archana P** - [GitHub](https://github.com/ArchPrak) - [Email](mailto:arch.2421@gmail.com)
* **Harish PB**  - [GitHub](https://github.com/harishpb26) - [Email](mailto:harishpb.26@gmail.com)
* **Navneetha Rajan** - [GitHub](https://github.com/navneetha08) - [Email](mailto:navneetha.rajan1999@gmail.com)
* **Sparsha P** - [GitHub](https://github.com/sparsha-p) - [Email](mailto:sparshaprashanth3@gmail.com)


## Installation Manual
* Clone the repository ` $ git clone https://github.com/ArchPrak/capstone/`
* Install virtualenv package
  * `$ cd capstone`
  * `$ sudo apt-get install python-virtualenv`
* Create a new virtual environment modelvenv `$ virtualenv -p python3 modelvenv`
* Activate the environment `$ source modelvenv/bin/activate`
* Install the model requirements `(modelvenv) $ pip install -r modelvenv-requirements.txt`
* Deactivate the environment
`(modelvenv) $ deactivate`
* Create another virtual environment venv and activate the environment
  * `$ virtualenv -p python3 venv`
  * `$ source venv/bin/activate`
* Install the requirements
`(venv) $ pip install -r requirements.txt`

## User Manual

* Run the app
`(venv) $ python src/app.py`
* Open http://localhost:5000/ in your browser
* Navigate to the Home page
* Navigate to either to Boolean domain or SQL domain
* Insert facts and questions and click Solve in case of the Boolean domain
* Facts received and evaluated result is displayed
* Insert query description in case of the SQL domain
* SQL query and rows of the database displayed in form of table

