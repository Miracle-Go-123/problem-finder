# Problem Finder

**Problem Finder** is a tool designed to analyze documents and chat logs, identify discrepancies, and provide actionable insights. It leverages Azure OpenAI and CrewAI for automated problem detection and reporting.

## Features

- **Document Analysis**: Extracts detailed information from documents using Azure Vision API.
- **Chat Analysis**: Identifies inconsistencies in chat logs.
- **Comparison**: Cross-references extracted document data with chat logs.
- **Summarization**: Generates concise summaries of identified issues.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Miracle-Go-123/problem-finder.git
   ```
2. Navigate to the project directory:
   ```bash
   cd problem-finder
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare input data:
   - **Documents**: List of URLs pointing to document images.
   - **Chat**: JSON-formatted chat logs.
   - **Checklist**: Rules for comparison.
2. Start the server:
   ```bash
   uvicorn app:app --reload
   ```
3. Use the `/kickoff` endpoint to initiate analysis and `/status/{job_id}` to check progress.

## Configuration

- **Agents**: Defined in `config/agents.yaml` for task-specific roles.
- **Tasks**: Defined in `config/tasks.yaml` for detailed workflows.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and submit a pull request.
