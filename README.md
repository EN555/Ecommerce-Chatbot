# Ecommerce-Chatbot

This project is a conversational agent chatbot built using Flask and integrated with OpenAI's GPT-4 model. The chatbot provides support for order status inquiries, requests for human representatives, and return policy information.


<img src="https://github.com/EN555/Ecommerce-Chatbot/assets/61500507/808de3f7-7394-4401-b4c9-c046c2f1ca59" alt="Ecommerce-Chatbot" width="400"/>

## Project Structure

Ecommerce-Chatbot/
├── Dockerfile
├── docker-compose.yml
├── app.py
├── templates/
│ └── index.html
├── order_status.csv
├── contact_info.csv
└── requirements.txt

markdown
Copy code

## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/Ecommerce-Chatbot.git
   cd Ecommerce-Chatbot
Add your OpenAI API key:

Update the docker-compose.yml file with your OpenAI API key:

yaml
Copy code
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      FLASK_ENV: development
      OPENAI_API_KEY: your_openai_api_key_here
How to Run
Build and run the Docker container:

In the root directory of the project, run the following command to build and start the Docker container:

bash
Copy code
docker-compose up --build
This command will build the Docker image and start the Flask application inside a Docker container.

Access the application:

Once the container is running, you can access the application in your web browser at http://localhost:5000.

Usage
Order Status
The chatbot can provide the status of an order. Simply ask for the status and provide the order ID when prompted.
Request Human Representative
To speak with a human representative, provide your contact information including full name, email, and phone number.
Return Policies
The chatbot can provide information on return policies, including conditions for returning items, non-returnable items, and the refund process.
Files Description
Dockerfile: Defines the environment and steps to set up the application.
docker-compose.yml: Manages and runs the Docker container.
app.py: The main Flask application file.
templates/index.html: The HTML template for the chatbot UI.
order_status.csv: A CSV file containing order statuses.
contact_info.csv: A CSV file for storing contact information.
requirements.txt: Lists the Python dependencies required for the application.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

csharp
Copy code

You can copy this content and save it into a `README.md` file in your project directory
