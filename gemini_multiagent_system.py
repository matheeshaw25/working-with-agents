import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from litellm import completion

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Verify API key is loaded correctly
if not API_KEY:
    raise ValueError("ERROR: Google Gemini API key is missing. Please check your .env file.")

# Set the environment variable for LiteLLM
os.environ["GEMINI_API_KEY"] = API_KEY

# ✅ Define the Question Handler Agent
question_handler = Agent(
    role="Question Handler",
    goal="Understand user queries and assign tasks.",
    backstory="A highly efficient AI designed to process user queries and delegate tasks.",
    verbose=True,
    allow_delegation=True,
    llm="gemini/gemini-1.5-pro"
)

# ✅ Define the Researcher Agent
researcher = Agent(
    role="Researcher",
    goal="Find relevant answers using Gemini AI.",
    backstory="An AI specialized in researching and providing accurate information to users.",
    verbose=True,
    llm="gemini/gemini-1.5-pro"
)

# ✅ Define the Summarizer Agent
summarizer = Agent(
    role="Summarizer",
    goal="Summarize long AI responses into a concise, well-structured format.",
    backstory="A highly intelligent AI that specializes in summarizing complex information into easy-to-understand responses.",
    verbose=True,
    llm="gemini/gemini-1.5-pro"
)

# ✅ Define a Task for the Researcher
def fetch_information(task_input):
    messages = [
        {"role": "user", "content": task_input}
    ]
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=messages,
        api_key=API_KEY  # Pass the API key directly
    )
    long_text = response['choices'][0]['message']['content']

    # ✅ Pass the response to the Summarizer before returning it
    summarized_text = summarize_response(long_text)
    return summarized_text

research_task = Task(
    description="Find and summarize information about: {question}",
    agent=researcher,
    function=fetch_information,
    expected_output="A well-structured summary of the topic with key details."
)

# ✅ Define a Task for the Summarizer
def summarize_response(task_input):
    messages = [
        {"role": "user", "content": f"Summarize the following information: {task_input}"}
    ]
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=messages,
        api_key=API_KEY
    )
    return response['choices'][0]['message']['content']

summary_task = Task(
    description="Summarize long AI responses to improve readability.",
    agent=summarizer,
    function=summarize_response,
    expected_output="A concise summary of the given text, retaining key details."
)

# ✅ Create a Crew (Multi-Agent System)
crew = Crew(
    agents=[question_handler, researcher, summarizer],  # ✅ Added Summarizer
    tasks=[research_task, summary_task],  # ✅ Added Summarization Task
    verbose=True
)

# ✅ Run the multi-agent system
if __name__ == "__main__":
    print("Multi-Agent AI System Ready! Type your question below.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        result = crew.kickoff(inputs={"question": user_query})
        print("AI Response:", result)
