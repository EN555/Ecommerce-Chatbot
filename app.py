from flask import Flask, request, render_template, jsonify
import csv
import os
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.prompts import PromptTemplate
import json
import re
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
import ast



app = Flask(__name__)

# File paths for storing data
ORDER_STATUS_FILE = "order_status.csv"
CONTACT_INFO_FILE = "contact_info.csv"

# Ensure the files exist
if not os.path.exists(ORDER_STATUS_FILE):
    with open(ORDER_STATUS_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["order_id", "status"])

if not os.path.exists(CONTACT_INFO_FILE):
    with open(CONTACT_INFO_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "email", "phone"])


# --------- 1. Retrive oredr status: ---------
@tool
def get_order_status(order_id: str) -> str:
    '''When a user asks for the status of an order, the agent should return the order status.
    Args:
        order_id: customer's order id - should include only digits!
    '''
    print(order_id)
    order_id = re.sub(r'\D', '', order_id)
    print(order_id)
    with open(ORDER_STATUS_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(order_id == row[0])
            if row[0] == order_id:
                return row[1]
    return "Order ID not found."


# --------- 2: save contact info: ---------
@tool
def save_contact_info(contact_info: str) -> str:
    # https://stackoverflow.com/questions/78051789/validation-error-while-using-multi-input-tools-in-react-agent-relating-to-numb
    '''Gather contact information for users who want to
    interact with a person. Contact information should include full name, email, and phone
    number. Save the information to a CSV file with a single row in the same folder as the
    execution file.
    Args:
        contact_info: {name: customer's name, email: customer's email, phone: customer's phone}
    '''
    pattern = r'[^{\}]+(?=\{)|(?<=\})[^{\}]+'
    contact_info = re.sub(pattern, '', contact_info)
    contact_info_dict = ast.literal_eval(contact_info)
    name = contact_info_dict.get('name')
    email = contact_info_dict.get('email')
    phone = contact_info_dict.get('phone')
    with open(CONTACT_INFO_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, phone])
    return "The information has been saved in the system!"



openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

llm = ChatOpenAI(
    model_name='gpt-4o',
    temperature=0.6,
    openai_api_key=openai_api_key
)

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=10,
    return_messages=True
)


def get_final_prompt(bot_name):
    name_prompt = f"The Assistant also known as {bot_name}.\n"
    information = """
    You are an ecommerce chatbot, and you need to support the following requests from users:

    1. Order Status:
     When a user asks for the status of an order, the agent should ask for the order_id and then respond with the order status. Use the 'get_order_status' function with the order_id to get the status. If the order_id is missing, ask the user for it.
    For Example:
    Thought: I need the order ID to check the status.
    Action: get_order_status
    Action Input: Please provide your order ID so that I can check the status for you.

    2. Request Human Representative: When a user asks for talking with a human, ask them to provide contact information. Contact information should include full name, email, and phone number. Save the information using the 'save_contact_info' function. If any contact information is missing, ask the user for the missing details.
    Example:
    Thought: I need the user's contact information to proceed.
    Action: save_contact_info
    Action Input: Please provide your full name, email, and phone number so that I can save your contact information.
    """

    info = """
    1. Order Status:
    Thought: I need the order ID to check the status.
    Action: get_order_status
    Action Input: order_id - only digits, for example "12345", if have chracters like ''' remove them
    Note most of the time you can just return question to the user, 
    for example, user can ask you information on his order, and you just return him to insert the order id
    another example, user can ask to talk with human, and you need to ask him to return his name,email and his phone number.
    so in those case the format is 
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    You need to bee familiar on those rules:
    Return Policies:
    Q: What is the return policy for items purchased at our store?
        A: You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.
    Q: Are there any items that cannot be returned under this policy?
        A: Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details.
    Q: How will I receive my refund?
        A: Refunds will be issued to the original form of payment. If you paid by credit card, the refund will be credited to your card. If you paid by cash or check, you will receive a cash refund.
    on usert question from this type you only use:
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    """

    prompt = hub.pull("hwchase17/react-chat")
    prompt.template = info + "\n" + str(prompt.template)
    return prompt


def react_agent_chat(botname, user_query):
    save_contact_info_tool = Tool(
        name="save_contact_info",
        func=save_contact_info,
        description='Use this tool with dictionary argument like "{{"name": "Guy", "email": "guy@gmail.com", "phone": "34567890"}} when you need to keep contact information'
    )
    tools = [get_order_status, save_contact_info_tool]
    final_prompt = get_final_prompt(bot_name=botname)
    # Construct the ReAct agent
    agent = create_react_agent(llm, tools, final_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=conversational_memory, handle_parsing_errors=True, max_iterations=15)
    agent_response = agent_executor.invoke({"input": user_query})
    return agent_response['output']


def chatbot_response(user_query, context):
    return react_agent_chat("Jone", user_query), None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_query = request.json['query']
    context = request.json['context']
    response, new_context = chatbot_response(user_query, context)
    return jsonify({'response': response, 'context': new_context})

if __name__ == '__main__':
    app.run(debug=True)
