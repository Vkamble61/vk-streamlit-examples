import os
import yaml
from crewai import Agent, Task, LLM
from dotenv import load_dotenv
from tools import ContentRetrievalTool
# Load environment variables
load_dotenv()

# Load configuration files
def load_config(config_file):
    """Load YAML configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', config_file)
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Define CrewAI Agents
def create_agents():
    """Create the research and answer agents from config."""
    
    # Load agent configurations
    agents_config = load_config('agents.yaml')
    
    # Initialize the tool
    content_tool = ContentRetrievalTool()
    
    # Configure LLM with system message to restrict to source-only answers
    llm = LLM(
        model="gpt-4o-mini",
        temperature=0,
    )
    
    # Research Agent - retrieves relevant information
    research_agent = Agent(
        role=agents_config['research_agent']['role'],
        goal=agents_config['research_agent']['goal'],
        backstory=agents_config['research_agent']['backstory'],
        tools=[content_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,  # Limit iterations to force tool usage
    )
    
    # Answer Agent - synthesizes information into answers
    answer_agent = Agent(
        role=agents_config['answer_agent']['role'],
        goal=agents_config['answer_agent']['goal'],
        backstory=agents_config['answer_agent']['backstory'],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        memory=False  # Disable memory to prevent using past general knowledge
    )
    
    return research_agent, answer_agent

# Define CrewAI Tasks
def create_tasks(research_agent, answer_agent, user_question):
    """Create tasks for the crew to execute from config."""
    
    # Load task configurations
    tasks_config = load_config('tasks.yaml')
    
    # Task 1: Research relevant information
    research_task = Task(
        description=tasks_config['research_task']['description'].format(user_question=user_question),
        agent=research_agent,
        expected_output=tasks_config['research_task']['expected_output']
    )
    
    # Task 2: Synthesize answer
    answer_task = Task(
        description=tasks_config['answer_task']['description'].format(user_question=user_question),
        agent=answer_agent,
        expected_output=tasks_config['answer_task']['expected_output'],
        context=[research_task]
    )
    
    return [research_task, answer_task]
