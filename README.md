# austral-lui
This is a python program that uses the tkinter module to create a GUI for austral-data that is in charge of the following:
1.  Display and selection of raw or corrected lidar profiles  
    a. Loads raw data licel files  
    b. Processes raw data to obtain the filtered or averaged data  
    c. Display filtered or averaged data  
    d. Use some scale tools to adjust the display  
    e. Delete precise files to fine-tune avergae precision
2. Visualization of the calibration procedure  
    a. Loads raw calibration licel files  
    b. Processes raw data to obtain the filtered +45° and -45° ratio data  
    c. Asks interval and processes the V* calibration coefficient  
    d. Use some scale tools to adjust the display  
    e. Verifies the V* calibration coefficient using another file

## Built With
- `Python 3.10`

## Pre-requistes for the windows system:
- Ubuntu 20.04 and above (Jammy:22.04 LTS preferable)
- Python 3.10
- Make sure git ssh keys are set up correctly
- xming
- update: sudo apt update
- upgeade: sudo apt upgrade -y
- make: sudo apt install make
- pip: sudo apt install python3 pip
- virtual environment: sudo apt install python3-virtualenv
- venv: sudo apt install python3.10-env
- ktinker: sudo apt install python3-tk

## Installation
- Open your terminal or command line
- Clone the Repository into your system: `git clone git@github.com:Vagyasri/austral-lui.git`
- cd into the Repository: `cd austral-lui`
- Run `make` -- This will create a virtual environmrnt and install the following in your virtual environment:
  - requirements
  - 'pypr2'
  - 'austral-scientific-layer' 


### Installing the prerequisites independently :
- Run `make install-dev` - This will install 'pypr2', 'austral-scientific-layer', 'austral-data-samples' at one go.
- Run `make install-pkg` - This will install 'pypr2', 'austral-scientific-layer' in the virtual environment.
- Run `make install-samples` - This will install 'austral-data-samples'
- Run `make install-pypr2` - This will install 'pypr2'
- Run `make install-asl` - This will install 'austral-scientific-layer'

## Run project:
- Run `make run`

## Run the tests:
- Run `make tests` - All tests at one go
- Run `make xtest` - Specify the test(eg: make xtest TEST=tests/test_licel_treatment.py)

## Run tests:
- cd into the Repository: `cd austral-lui`
- Activate Virtual Environment: `. austral-lui-env/bin/activate`
- Test *test_main.py*: `pytest test_main.py`
- Test *test_licel_treatment.py*: `pytest test_licel_treatment.py`

#### Install tkinter module:
    - `brew install python-tk` for mac
    - `sudo apt install python3-tk` for linux

## Author

👤 **Jeanlin Neuts**

- GitHub: [@Jeanlin](https://github.com/Peaneuts8)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Start by:

- Forking the project
- Cloning the project to your local machine
- cd into the Youtube-Replica project directory
- Run git checkout -b your-branch-name
- Make your contributions
- Push your branch up to your forked repository
- Open a Pull Request with a detailed description to the development branch of the original project for a review

Feel free to check the [issues page](https://github.com/Vagyasri/austral-lui/issues), contribute to the Project by creating an issue.