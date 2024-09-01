import os
import sys
import asyncio
import json
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add parent directory to sys.path for importing app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app

# Function to load environment variables into the app module
def load_env_into_module(module_name, prefix=''):
    load_dotenv()
    module = __import__(module_name)
    for key, value in os.environ.items():
        if key.startswith(prefix):
            setattr(module, key[len(prefix):], value)

load_env_into_module("app")

# Some settings required in app.py
app.SHOULD_STREAM = False
app.SHOULD_USE_DATA = app.should_use_data()

# Path to the input file containing QA pairs
generated_data_path = r"path/to/qa_input_file.json"

try:
    with open(generated_data_path, 'r') as file:
        data = json.load(file)
except Exception as e:
    logging.error(f"Failed to load input data from {generated_data_path}: {e}")
    sys.exit(1)

# Asynchronous function to process the data and write the results to a file
async def process(data: list, file):
    for qa_pairs_obj in data:
        qa_pairs = qa_pairs_obj.get("qa_pairs", [])
        for qa_pair in qa_pairs:
            question = qa_pair.get("question", "")
            if not question:
                logging.warning("Question is missing or empty in QA pair. Skipping...")
                continue

            messages = [{"role": "user", "content": question}]
            logging.info(f"Processing question: {question}")

            request = {"messages": messages, "id": "1"}

            try:
                response = await app.complete_chat_request(request)
            except Exception as e:
                logging.error(f"API call failed for question '{question}': {e}")
                continue

            try:
                messages = response["choices"][0]["messages"]

                tool_message = next((msg["content"] for msg in messages if msg["role"] == "tool"), None)
                assistant_message = next((msg["content"] for msg in messages if msg["role"] == "assistant"), None)

                if not assistant_message:
                    logging.warning(f"No assistant response found for question '{question}'. Skipping...")
                    continue

                # Construct data for AI studio evaluation
                user_message = {"role": "user", "content": question}
                assistant_message_obj = {"role": "assistant", "content": assistant_message}

                # Prepare citations
                if tool_message:
                    try:
                        citations = json.loads(tool_message)
                        assistant_message_obj["context"] = citations
                    except json.JSONDecodeError:
                        logging.warning(f"Failed to parse tool message as JSON for question '{question}'. Ignoring citations.")

                # Create output
                evaluation_data = {"messages": [user_message, assistant_message_obj]}

                # Incrementally write out to the JSONL file
                file.write(json.dumps(evaluation_data) + "\n")
                file.flush()

            except (KeyError, ValueError) as e:
                logging.error(f"Error processing response for question '{question}': {e}")
                continue

# Path to the output file
evaluation_data_file_path = r"path/to/output_file.jsonl"

try:
    with open(evaluation_data_file_path, "w") as file:
        asyncio.run(process(data, file))
except Exception as e:
    logging.error(f"Failed to process data or write output to {evaluation_data_file_path}: {e}")







import os
import sys
import asyncio
import json
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add parent directory to sys.path for importing app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app

# Function to load environment variables into the app module
def load_env_into_module(module_name, prefix=''):
    load_dotenv()
    module = __import__(module_name)
    for key, value in os.environ.items():
        if key.startswith(prefix):
            setattr(module, key[len(prefix):], value)

load_env_into_module("app")

# Some settings required in app.py
app.SHOULD_STREAM = False
app.SHOULD_USE_DATA = app.should_use_data()

# Path to the input file containing QA pairs
generated_data_path = r"path/to/qa_input_file.json"

try:
    with open(generated_data_path, 'r') as file:
        data = json.load(file)
except Exception as e:
    logging.error(f"Failed to load input data from {generated_data_path}: {e}")
    sys.exit(1)

# Asynchronous function to process the data and write the results to a file
async def process(data: list, file):
    for qa_pairs_obj in data:
        qa_pairs = qa_pairs_obj.get("qa_pairs", [])
        for qa_pair in qa_pairs:
            question = qa_pair.get("question", "")
            if not question:
                logging.warning("Question is missing or empty in QA pair. Skipping...")
                continue

            messages = [{"role": "user", "content": question}]
            logging.info(f"Processing question: {question}")

            request = {"messages": messages, "id": "1"}

            try:
                response = await app.complete_chat_request(request)
            except Exception as e:
                logging.error(f"API call failed for question '{question}': {e}")
                continue

            try:
                messages = response["choices"][0]["messages"]

                tool_message = next((msg["content"] for msg in messages if msg["role"] == "tool"), None)
                assistant_message = next((msg["content"] for msg in messages if msg["role"] == "assistant"), None)

                if not assistant_message:
                    logging.warning(f"No assistant response found for question '{question}'. Skipping...")
                    continue

                # Construct data for AI studio evaluation
                user_message = {"role": "user", "content": question}
                assistant_message_obj = {"role": "assistant", "content": assistant_message}

                # Prepare citations
                if tool_message:
                    try:
                        citations = json.loads(tool_message)
                        assistant_message_obj["context"] = citations
                    except json.JSONDecodeError:
                        logging.warning(f"Failed to parse tool message as JSON for question '{question}'. Ignoring citations.")

                # Create output
                evaluation_data = {"messages": [user_message, assistant_message_obj]}

                # Incrementally write out to the JSONL file
                file.write(json.dumps(evaluation_data) + "\n")
                file.flush()

            except (KeyError, ValueError) as e:
                logging.error(f"Error processing response for question '{question}': {e}")
                continue

# Path to the output file
evaluation_data_file_path = r"path/to/output_file.jsonl"

try:
    with open(evaluation_data_file_path, "w") as file:
        asyncio.run(process(data, file))
except Exception as e:
    logging.error(f"Failed to process data or write output to {evaluation_data_file_path}: {e}")












