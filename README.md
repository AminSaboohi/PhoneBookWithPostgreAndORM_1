# Phonebook Project 
## Overview 
This project is a comprehensive solution for managing a phonebook database. It utilizes the Peewee ORM to connect to a PostgreSQL database, creating and manipulating tables designed for a phonebook application. Additionally, it imports city and state information from a JSON file into the corresponding tables. The project features a GUI built with Tkinter, allowing users to input and retrieve information interactively. Data display is handled through the command line, presenting results in a structured table format upon user request. 
## Features 
- Database Integration: Connects to a PostgreSQL database using Peewee ORM for efficient data handling. - Data Import: Imports city and state data from a JSON file into the database, ensuring a rich dataset for phonebook entries. - GUI: Features a user-friendly graphical interface built with Tkinter for data input and interaction. - Data Display: Offers a command-line data presentation, displaying the phonebook entries in a table format when the user opts to view the data. 
## Getting Started 
### Prerequisites Ensure you have Python installed on your system. This project requires Python 3.6 or newer. 
### Installation 
1. Clone the repository to your local machine: 

git clone [https://github.com/yourusername/phonebook-project.git](https://github.com/AminSaboohi/PhoneBookWithPostgreAndORM_1.git)

￼Copy code

2. Navigate to the project directory: 

cd phonebook-project

￼Copy code

3. Install the required libraries: 

pip install -r requirements.txt

￼Copy code

### Setting Up the Database 
1. Create a PostgreSQL database for the project.
2. Rename sample_setting.py to local_setting.py.
3. Follow the instructions in sample_setting.py to configure your database connection settings in local_setting.py. ### Running the Application To start the application, run: 

python main.py

￼Copy code

This will launch the GUI, where you can start entering and viewing phonebook entries. 
## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues to propose changes or report bugs. 
## License
This project is licensed under the MIT License - see the LICENSE file for details. 


