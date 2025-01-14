from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
import json
from pathlib import Path
from typing import List, Dict, Any

from problemfinder.tools.customized_vision_tool import CustomizedVisionTool
from dotenv import load_dotenv
import os

load_dotenv()

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
llm = f"azure/{deployment_name}"

vision_tool = CustomizedVisionTool()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ProblemFinder():
	"""ProblemFinder crew that analyzes documents and chat for problems"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff
	def prepare_data(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Prepare input data for the problem finder.
		Expected inputs:
		- documents: List[str] - List of document URLs
		- chat: List[Dict] - Chat history in JSON format
		"""
		# Validate inputs
		if not isinstance(inputs.get('documents'), list):
			raise ValueError("'documents' must be a list of URLs")
		if not isinstance(inputs.get('chat'), list):
			raise ValueError("'chat' must be a list of chat messages")

		# Return validated inputs directly
		return inputs
	
	@agent
	def info_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['info_extractor'],
			verbose=True,
			tools=[vision_tool],
			llm=llm
		)
	
	@agent
	def chat_problem_finder(self) -> Agent:
		return Agent(
			config=self.agents_config['chat_problem_finder'],
			verbose=True,
			llm=llm
		)
	
	@agent
	def comparator(self) -> Agent:
		return Agent(
			config=self.agents_config['comparator'],
			verbose=True,
			llm=llm
		)
	
	@agent
	def reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['reviewer'],
			verbose=True,
			llm=llm
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
		config['expected_output'] = "json_string_array"
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
			memory=False
		)