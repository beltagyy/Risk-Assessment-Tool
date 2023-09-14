Risk Assessment Tool
Overview
The Risk Assessment Tool is a simple web application developed using Flask that enables users to record, categorize, and assess risks. It also supports user registration and login functionality.

Features
User Registration and Login: Users can sign up and securely log in to access the tool.
Risk Management:
Add risks with descriptions, impact, and likelihood values.
Categorize risks.
Calculate a risk score based on impact and likelihood.
Comment on specific risks.
Assign a status to risks (e.g., Open, Closed, In Progress).
Setup Instructions
Ensure you have Python and Flask installed.
Clone or download the project.
Navigate to the project directory in your terminal or command prompt.
Run the following command to install necessary packages:
Copy code
pip install flask flask-login
Run app.py:
Copy code
python app.py
Open a web browser and go to http://127.0.0.1:5000/ to access the tool.
Register a new user account and start using the Risk Assessment Tool.
Development Steps
Initialization:

Set up Flask.
Create an SQLite database for risks.
Build a basic UI to add and list risks.
User Management:

Create user registration and login forms.
Hash and verify passwords for security.
Store user information in the SQLite database.
Risk Categories:

Extend the SQLite database to support risk categories.
Allow users to categorize risks when adding them.
Display risk categories in the risk list.
Comments or Notes for Risks:

Allow users to add comments or notes to specific risks.
Display comments in the risk list.
Risk Status:

Define different statuses for risks (e.g., Open, Closed, In Progress).
Allow users to assign a status when adding a risk.
Display the risk status in the risk list.
Future Enhancements
Risk editing and deletion.
User profiles and roles.
Reporting and visualization tools for risks.