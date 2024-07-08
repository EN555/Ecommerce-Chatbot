import json
from bert_score import score
import openai

# Define your react_agent_chat function
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

# Function to simulate the conversation
def simulate_conversation(test_case):
    responses = []
    for input_text in test_case['inputs']:
        response = react_agent_chat("ShopBot", input_text)
        responses.append(response)
    return responses

# Function to evaluate responses using BERTScore
def evaluate_response(expected, actual, threshold=0.85):
    P, R, F1 = score([actual], [expected], lang='en', verbose=True)
    return F1.mean().item() >= threshold

def main():
    # Load the test cases from the JSON file
    with open('test_cases.json', 'r') as file:
        test_cases = json.load(file)

    results = []
    for case in test_cases:
        actual_responses = simulate_conversation(case)
        case_results = [evaluate_response(exp, act) for exp, act in zip(case['expected_responses'], actual_responses)]
        results.append(case_results)

    total_responses = sum([len(case) for case in results])
    correct_responses = sum([sum(case) for case in results])
    accuracy = correct_responses / total_responses

    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Save results to a report
    with open('evaluation_report.txt', 'w') as report_file:
        report_file.write(f'Accuracy: {accuracy * 100:.2f}%\n\n')
        for idx, case in enumerate(test_cases):
            actual_responses = simulate_conversation(case)
            report_file.write(f"Test Case {idx + 1}:\n")
            report_file.write(f"Inputs: {case['inputs']}\n")
            report_file.write(f"Expected Responses: {case['expected_responses']}\n")
            report_file.write(f"Actual Responses: {actual_responses}\n")
            case_results = [evaluate_response(exp, act) for exp, act in zip(case['expected_responses'], actual_responses)]
            report_file.write(f"Results: {case_results}\n\n")

if __name__ == '__main__':
    main()
