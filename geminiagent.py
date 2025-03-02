import google.generativeai as genai # Library for interacting with Google Gemini.
import os #Used to access environment variables (API key).
from dotenv import load_dotenv #Loads API keys from the .env file.

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiAgent: #This creates a class-based AI agent for better organization.

    def __init__(self): #Initializing the Agent
        genai.configure(api_key=API_KEY)

    def perceive(self, user_input): # Takes user input and processes it (currently just returns it as-is).
        return user_input

    def decide(self, processed_input): #Generating a Response
        model = genai.GenerativeModel("gemini-1.5-pro") # Creates an AI model instance
        response = model.generate_content(processed_input) #Sends the processed input to the Gemini model and generates a response based on the user's message.
        return response.text

    def act(self, response): #Displaying the Response
        print("AI Agent:", response) #Prints the AI-generated response so the user can see it and in real-world apps, this method could be modified to speak aloud, send an email, or control a device.

    def run(self): #Chat Loop
        print("AI Agent: Hello! Type 'bye' to exit.")
        while True: # Runs the bot constantly until the user types bye
            user_input = input("You: ") #Takes the user input
            if user_input.lower() == "bye": # Stops if the user says bye
                self.act("Goodbye!")
                break
            processed_input = self.perceive(user_input) # process the input
            response = self.decide(processed_input) # generate a response
            self.act(response) # display the output

# Run the agent
if __name__ == "__main__":
    agent = GeminiAgent()
    agent.run()
