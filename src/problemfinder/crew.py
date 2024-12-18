from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
import json
from pathlib import Path

from problemfinder.tools.customized_vision_tool import CustomizedVisionTool

vision_tool = CustomizedVisionTool()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ProblemFinder():
	"""ProblemFinder crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff
	def prepare_data(self, inputs):
		"""
		Prepare chat log and uploaded documents data for the problem finder
		"""
		chat_path = Path("assets") / "chat.json"
		docs_path = Path("assets") / "document.json"
		
		with open(chat_path, "r") as file:    
			chat = json.load(file)
		
		with open(docs_path, "r") as file:    
			uploaded_documents = json.load(file)
		
		modified_inputs = {
			"chat": chat,
			"documents": uploaded_documents,
		}

		return modified_inputs
	
	@agent
	def info_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['info_extractor'],
			verbose=True,
			tools=[vision_tool]
		)
	
	@agent
	def chat_problem_finder(self) -> Agent:
		return Agent(
			config=self.agents_config['chat_problem_finder'],
			verbose=True,
		)
	
	@agent
	def comparator(self) -> Agent:
		return Agent(
			config=self.agents_config['comparator'],
			verbose=True,
		)
	
	@agent
	def reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['reviewer'],
			verbose=True,
		)
	
	@task
	def info_extractor_task(self) -> Task:
		config=self.tasks_config['info_extractor_task']
		return Task(
			config=config,
		)
	
	@task
	def chat_problem_finder_task(self) -> Task:
		config=self.tasks_config['chat_problem_finder_task']
		return Task(
			config=config,
		)
	
	@task
	def comparator_task(self) -> Task:
		config=self.tasks_config['comparator_task']
		return Task(
			config=config,
		)
	
	@task
	def reviewer_task(self) -> Task:
		config=self.tasks_config['reviewer_task']
		config['expected_output'] = "list"
		return Task(
			config=config,
		)
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=False,
		)