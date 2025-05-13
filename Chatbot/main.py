from langchain_core.messages import HumanMessage
# This is a simple chatbot that uses the LangChain library to create an AI assistant.
# It can perform basic arithmetic calculations and greet the user.
from langchain_openai import ChatOpenAI
# the above library is used to create a chat model
from langchain.tools import tool
# the above library is used to create tools for the chatbot
from langgraph.prebuilt import create_react_agent
# the above library is used to create a react agent for the chatbot
from dotenv import load_dotenv
# we are using the dotenv library to load environment variables from a .env file
load_dotenv()
# we are calling the dotenv function to load the environment variables
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmeric calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"
    
@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    print("Tool has been called.")
    return f"Hello {name}, I hope you are well today"

# the below function is used to initialize the chatbot
def main():
    
    model = ChatOpenAI(temperature=0)
    # the above line is used to create a chat model with a temperature of 0
    # the temperature parameter controls the randomness of the model's output
    tools = [calculator, say_hello]
    # the above line is used to create a list of tools for the chatbot
    agent_executor = create_react_agent(model, tools)
    # the above line is used to create a react agent for the chatbot
    
    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")
    # we are keeping a while loop to continue interacting wit the user until they quit. strip() is used to remove any leading or trailing whitespace from the input
    while True:
        user_input = input("\nYou: ").strip()
        # here is the user input..
        if user_input == "quit":
            break
        # the below is the assistant's response to the user input, end="" is used to avoid a new line after the print statement
        print("\nAssistant: ", end="")
        # the below line is used to stream the response from the agent executor
        # the stream method is used to get the response from the agent executor in human readable format
        # the messages parameter is used to pass the user input to the agent executor
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            # the below line is used to check if the chunk is a message from the agent
            # if the chunk is a message from the agent, we print the content of the message
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()
        
if __name__ == "__main__":
    main()
                