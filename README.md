# Ecommerce-Chatbot

This Ecommerce-Chatbot provides essential services for an ecommerce platform, including order status inquiries, return policy information, and collecting user contact information for human representative interactions. The chatbot ensures efficient customer support by leveraging OpenAI's GPT-4 model integrated with Flask.


<img src="https://github.com/EN555/Ecommerce-Chatbot/assets/61500507/808de3f7-7394-4401-b4c9-c046c2f1ca59" alt="Ecommerce-Chatbot" width="400"/>



## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/Ecommerce-Chatbot.git
   cd Ecommerce-Chatbot
   ```
   
2. **Add your OpenAI API key**:

   Update the docker-compose.yml file with your OpenAI API key:
   ```bash
   OPENAI_API_KEY: your_openai_api_key_here
   ```

## How to Run
Build and run the Docker container:

In the root directory of the project, run the following command to build and start the Docker container:

   ```bash
   docker-compose up --build
   ```

This command will build the Docker image and start the Flask application inside a Docker container.


## Access the application:

Once the container is running, you can access the application in your web browser at http://localhost:5000.

##  Usage
1. Order Status
The chatbot can provide the status of an order. Simply ask for the status and provide the order ID when prompted.
2. Request Human Representative
To speak with a human representative, provide your contact information including full name, email, and phone number.
3. Return Policies
The chatbot can provide information on return policies, including conditions for returning items, non-returnable items, and the refund process.


## Files Description

app.py: The main Flask application file.


templates/index.html: The HTML template for the chatbot UI
.

order_status.csv: A CSV file containing order statuses.

contact_info.csv: A CSV file for storing contact information.



