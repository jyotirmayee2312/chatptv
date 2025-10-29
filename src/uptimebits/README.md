# Victoria's Public Transport Assistant

A conversational AI assistant for Victoria's public transport system, built using Strands + LangChain agents with AWS Bedrock.

## Overview

This application provides real-time information about:
- Train timetables and schedules
- Service disruptions and delays
- Route planning assistance
- V/Line and Metro services

## Architecture

- **Agent Framework**: Strands + LangChain integration
- **LLM**: AWS Bedrock (Claude 3 Haiku)
- **Tools**: Custom transport data tools
- **Memory**: Chat history with S3 storage
- **Deployment**: AWS Lambda with SAM

## Prerequisites

- Python 3.11+
- AWS credentials configured
- Required environment variables in `.env` file

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=ap-southeast-2
CHAT_HISTORY_BUCKET=your_s3_bucket
```

## Running Locally

Run the interactive CLI version:

```bash
python main.py
```

### Usage Steps

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Enter message ID** (optional)
   - Provide a custom message ID for chat history
   - Leave blank to auto-generate

3. **Chat with the assistant**
   - Ask about train times: "What trains go from Melbourne Central to Flinders Street?"
   - Check disruptions: "Are there any delays on the Pakenham line?"
   - Plan journeys: "How do I get to Richmond at 5pm today?"

4. **Exit**
   - Type `exit` or `quit` to stop

### Example Session

```
Welcome To Victoria's Public Transport Assistant
(Type 'exit' or 'quit' anytime to stop)

Enter a message_id (or blank to auto-generate): demo123
You: What trains go to Richmond?
Assistant: I can help you find trains to Richmond station...

You: exit
Goodbye! Have a safe journey.
```

## Deployment

Deploy to AWS Lambda using SAM:

```bash
sam build
sam deploy --guided
```

## Features

- Natural language processing for transport queries
- Real-time timetable information
- Service disruption alerts
- Date/time parsing for journey planning
