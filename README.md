<!-- ABOUT THE PROJECT -->
## About The Project

A simple Online_Shop project with Django class based views


<!-- GETTING STARTED -->
## Getting Started

To get this repository, run the following command inside your git enabled terminal.
  ```sh
  git clone https://github.com/mirrzad/Online_Shop
  ```

<!-- Setup -->
## Setup

Create an enviroment in order to keep the repo dependencies seperated from your local machine.

 ```sh
  python -m venv venv
  ```
Make sure to install the dependencies of the project through the requirements.txt file.
 ```sh
  pip install -r requirements.txt
  ```
Once you have installed django and other packages, go to the cloned repo directory
and run the following command

 ```sh
  python manage.py makemigrations
  ```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command

 ```sh
  python manage.py migrate
  ```

Now we just need to start the server and then we can start using our simple Online_Shop App. 
Start the server by following command

 ```sh
  python manage.py runserver
  ```

Once the server is up and running, head over to http://127.0.0.1:8000 to launch the App.



<!-- LICENSE -->
## License

Distributed under the MIT License.

