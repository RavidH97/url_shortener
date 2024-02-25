# URL Shortener Application

## Overview:

This is a URL shortener service built using Django and MongoDB. 
The application allows the user to shorten long URLs into shorter links. 

### Implementation:
This project implements a simple load balancer using basic HTTPServer, it is designed to distribute incoming HTTP requests across multiple worker servers (implemented with Django) in round robin.
The load balancer distributes the requests using redirect and the workers are doing the actual work (the shorten of the URL and the communication with the DB).

## Features:

Shorten long URLs into shorter links.
Redirect users from short URLs to their original long URLs.
MongoDB is used as the database backend for data storage.

## Setup:

### Prerequisites:

Python 3.x
Django, pymongo version (3.12.1) and djongo installed. (You can install them via pip):
MongoDB server installed

### Installation:

1. Clone the repository
2. Enter the project repository
3. Run db migration script:
   mongosh urling mongo/create.js
4. Start the Django development server:
   python run_all_servers.py <number_of_workers>

## Usage:

Use the application with the cilent, open <path_to_project>/index.html
or with the API at http://localhost:8000 in your web browser.

### When using the client:

Open the URL Shortener client in your web browser at path open <path_to_project>/index.html .
Enter the original URL that you want to shorten into the provided input field.
Enter your email address (for tracking the users).
Click on the "Shorten URL" button.
You will be provided with the shortened URL.
Share the shortened URL with others.

### When using the API:

Use the following API to create and get the shortened URL:

URL: http://localhost:8000/shorten
Method: GET
Parameters:
original_url (required): The original URL that needs to be shortened.
user_email (required): Email address of the user requesting the shortened URL.

For example:
http://localhost:8000/shorten?original_url=https://www.taylorswift.com/&user_email=ravidh@example.com

### Future implementation:
In the future, I plan to upgrade the load balancer setup by implementing a better Manager-Workers model.
Instead of just redirecting requests, the manager will actively monitor and handle them using communication queues like SQS.
This upgrade will enable the system to better manage resources by starting and stopping workers base on use. 
Also, this will allow me to use a better way to decide which worker should handle a request (instead of the current round robin), like directing requests to servers with the least load.
