

1. Setting Up the Django Application:
•	Clone the Repository: Clone the project from GitHub.
•	Ensure Python is Installed: Make sure Python is installed on your system.
•	Install Dependencies: Install required packages using pip.
•	Configure Installed Apps: Update the Django settings to include necessary apps like django.contrib, rest_framework, and Nimap_App.
2. Database Setup and Migrations:
•	Configure PostgreSQL: Set up a PostgreSQL database with appropriate credentials.
•	Apply Migrations: Run migration commands to set up the database schema.
•	Create Superuser: If needed, create a superuser for the admin panel.
•	Run the Server: Start the Django development server.
3. Using Postman for API Requests:
•	Authenticate: Set up Base Authentication in Postman using your superuser credentials.
•	Access APIs: Use the following API endpoints to interact with the application:
API Endpoints:
	You need provide the basic auth credentials(username,password)
1.	Get List of Clients: Fetch a list of all clients.( http://127.0.0.1:1000/Nimap_App/clients/)
2.	Create a New Client: Add a new client to the system.( http://127.0.0.1:1000/Nimap_App/clients/)
3.	Retrieve Client Info: Get detailed information about a specific client, including assigned projects.( http://127.0.0.1:1000/Nimap_App/clients/1/)
4.	Update Client Info: Edit the details of an existing client.( http://127.0.0.1:1000/Nimap_App/clients/1/)
5.	Delete a Client: Remove a client from the system.( http://127.0.0.1:1000/Nimap_App/clients/5/)
6.	Create a New Project: Add a new project for a client and assign users.( http://127.0.0.1:1000/Nimap_App/clients/1/projects/)
7.	List All Projects for Logged-in User: Get a list of all projects assigned to the currently logged-in user.( http://127.0.0.1:1000/Nimap_App/projects/)





