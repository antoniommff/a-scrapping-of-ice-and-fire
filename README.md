<p align="center">
    <img src="ice_and_fire/static/images/logo2.png" align="center" width="30%">
</p>
<p align="center"><h1 align="center">AN-INDEX-OF-ICE-AND-FIRE</h1></p>
<p align="center">
	<em><code>This project demonstrates intelligent information access through a Django-based web app. It integrates relational databases, scraping with BeautifulSoup, indexed searches with Whoosh, and various recommendation strategies to deliver a comprehensive and personalized index of A Song of Ice and Fire.</code></em>
</p>
<br>
<p align="center">
	<img src="https://img.shields.io/github/license/antoniommff/ an-index-of-ice-and-fire?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/antoniommff/ an-index-of-ice-and-fire?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/antoniommff/ an-index-of-ice-and-fire?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/antoniommff/ an-index-of-ice-and-fire?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

## Table of Contents

- [ Overview](#overview)
- [ Features](#features)
- [ Project Structure](#project-structure)
  - [ Project Index](#project-index)
- [ Getting Started](#getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)
- [ License](#license)
- [ Acknowledgments](#acknowledgments)

---

## Overview

The purpose of this project is to demonstrate the application of a set of tools for intelligent information access. This web application, developed with ***Django***, integrates various technologies and strategies to offer a comprehensive and accessible index on the *A Song of Ice and Fire* book series.

The technologies used include ***relational databases***, *scraping* techniques using the ***BeautifulSoup*** library, and *indexed searches* with ***Whoosh***. Additionally, multiple ***Recommendation System*** strategies are implemented to provide a personalized user experience.

Check out this YouTube tutorial for a more detailed overview of this project:

<p align="center">
	<a href="https://youtu.be/MxcrkjoKgqg?si=JalFOCSqza1kXmFJ">
		<img src="https://img.youtube.com/vi/MxcrkjoKgqg/0.jpg" alt="An Index of Ice and Fire - Project Overview" width="50%">
	</a>
</p>

---

## Features

This project incorporates all the technologies covered in the subject "Intelligent Access to Information" within the Software Engineering degree of the University of Seville. Below are the main functionalities implemented:

1. **Web Application**  
   Built using the **Django** framework, the project delivers a customized web application focused on the *A Song of Ice and Fire* book series by George R.R. Martin. Special attention was given to creating a unique, personalized user interface beyond Django's default styles.
   <br>

2. **Data Collection**  
   Web scraping searching for the saga's characters, noble houses, and books were collected using Python's **BeautifulSoup** library.  
	- <u>Source 1</u>: Data on 450+ noble houses and their mentions in the books were scraped from *hieloyfuego.fandom.com*.  
    - <u>Source 2</u>: Main character information was scraped from Wikipedia due to the more practical structure for the project's scope.
   <br>

3. **Database**  
   All extracted data is stored in an **SQLite** database. This allows efficient relationship mapping and queries like:  
   - "Show characters belonging to a specific house."  
   - "Show houses mentioned in a specific book."
   <br>

4. **Search Functionality**  
   **Whoosh Indexing** enables fast and efficient searches across characters and houses by entering partial or related information. Indexing also supports optimized storage of summaries without performance trade-offs.
   <br>

5. **Recommendation System**  
   A collaborative filtering-based recommendation system suggests content (e.g., characters) based on user interactions like "Likes" or "Favorites." Users can explore their favorite characters and discover similar ones.
   <br>


---

## Project Structure

```sh
└── an-index-of-ice-and-fire/
    ├── LICENSE
    ├── README.md
    ├── ice_and_fire
    │   ├── 🟠 character	# Models, views and templates of the core objects
    │   ├── 🔵 dataRS.dat	# Recommendation system data
    │   ├── 🔵 db.sqlite3	# Database with all the preloaded data
    │   ├── 🟠 ice_and_fire	# Main web application
    │   ├── 🔵 index1		# Whoosh indexed information for houses
    │   ├── 🔵 index2		# Whoosh indexed information for characters
    │   ├── 🟢 manage.py	# Command-line utility for managing the web app
    │   ├── 🔵 media		# Multimedia resocurces
    │   ├── 🔵 sample_data 	# Row data to bulk the database and the RS
    │   ├── 🟢 static		# Static elements e.g. styles, multimedia, etc.
    │   ├── templates		# Base html templates
    │   └── 🟠 user		# Custom user models
    └── requirements.txt
```


### Project Index
<details open> <!-- ice_and_fire Submodule -->
	<summary><b><code>ICE-AND-FIRE</code></b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/db.sqlite3'>db.sqlite3</a></b></td>
				<td><code>Contains the database for the web application, storing all structured data related to the project.</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/manage.py'>manage.py</a></b></td>
				<td><code>Django's command-line utility for managing the application, including running the server and database migrations.</code></td>
			</tr>
			</table>
			<details>
				<summary><b>ice_and_fire</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/ice_and_fire/asgi.py'>asgi.py</a></b></td>
						<td><code>Configures the ASGI application for handling asynchronous web requests in the Django project.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/ice_and_fire/settings.py'>settings.py</a></b></td>
						<td><code>Central configuration file for the Django application, including database settings and installed apps.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/ice_and_fire/urls.py'>urls.py</a></b></td>
						<td><code>Maps URL patterns to views, enabling navigation throughout the web application.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/ice_and_fire/wsgi.py'>wsgi.py</a></b></td>
						<td><code>Configures the WSGI application for deploying the Django project with a web server.</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>index1</b></summary>
				<blockquote>
					<table>
						<p><code>Whoosh indexed information for houses.</code></p>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>index2</b></summary>
				<blockquote>
					<table>
						<p><code>Whoosh indexed information for characters.</code></p>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>sample_data</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/sample_data/ratings.txt'>ratings.txt</a></b></td>
						<td><code>Sample data file containing user ratings for recommendation system.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/sample_data/users.txt'>users.txt</a></b></td>
						<td><code>Sample data file with user information for the application's authentication or recommendation features.</code></td>
					</tr>
					</table>
				</blockquote>
			</details>
			<details>
				<summary><b>users</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/models.py'>models.py</a></b></td>
						<td><code>Defines the database schema for the custom user data.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/apps.py'>apps.py</a></b></td>
						<td><code>Configures the users app within the Django project.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/forms.py'>forms.py</a></b></td>
						<td><code>Contains form logic for handling user input in the app (log in, log out, sign in, sign out).</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/admin.py'>admin.py</a></b></td>
						<td><code>Django admin interface for managing user data.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/urls.py'>urls.py</a></b></td>
						<td><code>Routes specific to user-related views in the project</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/views.py'>views.py</a></b></td>
						<td><code>Logic behind user-related pages and API endpoints.</code></td>
					</tr>
					</table>
					<details>
						<summary><b>templates</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/templates/profile.html'>profile.html</a></b></td>
								<td><code>Template for displaying user profile details.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/templates/register.html'>register.html</a></b></td>
								<td><code>Template for the user registration page.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/templates/login.html'>login.html</a></b></td>
								<td><code>Template for the user login page.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/templates/edit_profile.html'>edit_profile.html</a></b></td>
								<td><code>Template for editing user profile information.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/users/templates/delete_account.html'>delete_account.html</a></b></td>
								<td><code>Template for deleting a user account.</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>characters</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/populateDB.py'>populateDB.py</a></b></td>
						<td><code>Script for populating the database with characters, books, houses and sample users. It is also where the whoosh schemas are created.</code></td>
					</tr>
										<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/scraping.py'>scraping.py</a></b></td>
						<td><code>Script that scraps all the book, character and house data using BeautifulSoup.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/models.py'>models.py</a></b></td>
						<td><code>Defines the database schema for character, book and house data.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/recommendations.py'>recommendations.py</a></b></td>
						<td><code> Implements logic for generating personalized recommendations.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/apps.py'>apps.py</a></b></td>
						<td><code>Configures the characters app within the Django project.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/forms.py'>forms.py</a></b></td>
						<td><code>Contains form logic for character-related user inputs.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/admin.py'>admin.py</a></b></td>
						<td><code>Django admin interface for managing character, book and house data.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/progress.py'>progress.py</a></b></td>
						<td><code> Tracks the progress of the data scraping and creation.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/urls.py'>urls.py</a></b></td>
						<td><code>Defines the routes for character-related views.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/views.py'>views.py</a></b></td>
						<td><code>Implements logic for character, books and houses web pages and API endpoints.</code></td>
					</tr>
					</table>
					<details>
						<summary><b>templates</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/home.html'>home.html</a></b></td>
								<td><code>Template for the homepage of the web application.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/recommendations.html'>recommendations.html</a></b></td>
								<td><code>Template for displaying user-specific recommendations.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/load.html'>load.html</a></b></td>
								<td><code> Template for loading all the application data (only for administrators).</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/books.html'>books.html</a></b></td>
								<td><code>Template for displaying information about books in the series.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/houses.html'>houses.html</a></b></td>
								<td><code>Template for showcasing the major houses from the book series.</code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/find.html'>find.html</a></b></td>
								<td><code>Template for the search functionality within the app. It redirects the user to the house finder, book finder or character finder. </code></td>
							</tr>
							<tr>
								<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/characters/templates/characters.html'>characters.html</a></b></td>
								<td><code>Template for listing and exploring characters from the series.</code></td>
							</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>templates</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/templates/base.html'>base.html</a></b></td>
						<td><code>General layout template used across the application, including structure, navbar, footer, background and main styles.</code></td>
					</tr>
					<tr>
						<td><b><a href='https://github.com/antoniommff/ an-index-of-ice-and-fire/blob/master/ice_and_fire/templates/base_no_navbar.html'>base_no_navbar.html</a></b></td>
						<td><code>Same general layout template but excluding navbar and booter. It is used for special actions such us logging or registering. </code></td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
</details>

---

## Getting Started

### Prerequisites
Before starting with an-index-of-ice-and-fire, ensure your runtime environment meets the following requirements:

- **Programming Language:** [Python](https://www.python.org/downloads/)
- **Package Manager:** [Pip](https://pip.pypa.io/en/stable/installation/)
- **Database:** [SQLite](https://www.sqlite.org/download.html) / [MySQL](https://dev.mysql.com/downloads/)

<br>

### Installation

<br>

**1. Clone the an-index-of-ice-and-fire repository into a directory of your choice:**
For instance, you may clone the repository into the "Developer" directory on your computer. On a new terminal window, write:
```sh
❯ cd Developer
```
Next, clone the repository from GitHub.
```sh
❯ git clone https://github.com/antoniommff/an-index-of-ice-and-fire
```

Alternatively, you can download the .zip file of the project and extract it as you would with any standard .zip file.

<br>

**2. Install the project dependencies:**
Fist, navegate to the project directory:
```sh
❯ cd an-index-of-ice-and-fire
```

There, create and activate a virtual environment where all the dependencies must be installed:

Using `python` &nbsp; [<img align="center" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white" />](https://www.python.org/)
```sh
❯ python -m venv venv
❯ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Then, install the dependencies:

Using `pip` &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

<br>

**3. Initialize the Django project:**
**Using `python`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white" />](https://www.python.org/)
```sh
❯ python manage.py makemigrations
❯ python3 manage.py migrate
```

<br>

**4. Create a superuser:**
```sh
❯ cd ice-and-fire
❯ python manage.py createsuperuser
```
Follow the prompts to create a user with full administrative privileges. Typically, the following values are used:
```sh
name: Admin
surname: Admin
email: example@mail.com
username: admin
password: 1234
```
If everything is set up correctly, you will be able to log in as an administrator with these credentials when the project is deployed locally.

### Usage
Run  an-index-of-ice-and-fire using the following command:
Using `python` &nbsp; [<img align="center" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white" />](https://www.python.org/)

```sh
❯ python runserver
```

Afterward, you can access the web application locally via the URL: https://127.0.0.1.
<br>
At this point, all data should be preloaded into the system, and you should encounter no issues accessing the information. However, if you are logged in as an administrator (using the credentials provided earlier), you can reload the system data at: https://127.0.0.1/data.

For more detailed instructions on how to use the application, please refer to this [YouTube tutorial]().

---

## License

This project is protected under the [MIT License](https://choosealicense.com/licenses/mit/). For more details, refer to the [LICENSE](https://github.com/antoniommff/ an-index-of-ice-and-fire#MIT-1-ov-file) file.

---

## Acknowledgments

<div style="display: flex; align-items: center;">
  <div style="flex: 0.4; text-align: left;">
    <a href="https://github.com/antoniommff">
      <img src="https://avatars.githubusercontent.com/u/91947070?v=4" width="100px;" alt="Antonio Macías Ferrera"/>
    </a>
  </div>
  <div style="flex: 1; text-align: left;">
    <p>
      This project was made by <a href="https://github.com/antoniommff">Antonio Macías</a>. 
	  <br>
      For direct contact, you can reach me out through: 
      <a href="https://www.linkedin.com/in/antoniommff/">
        <img height="20" src="https://skillicons.dev/icons?i=linkedin"/>
      </a> 
      or 
      <a href="mailto:antoniommff@gmail.com">
        <img height="20" src="https://skillicons.dev/icons?i=gmail"/>
      </a>
	  <br>
	  Take a moment to look at my 
      <a href="http://bento.me/antoniommff">Personal Page</a> to explore my social media.
	</p>
  </div>
</div>