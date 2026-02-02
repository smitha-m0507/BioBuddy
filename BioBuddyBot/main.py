from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

app = Flask(__name__)

# Initialize Ollama with the Llama2 model
llm = Ollama(model="llama2")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Define the conversation prompt template
template = """
You are a chemical inventory management assistant. Current context:
{history}
Human: {input}
Assistant: Let me help you with that.
"""

PROMPT = PromptTemplate(
    input_variables=["history", "input"], 
    template=template
)

# Path to the Excel file
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "CHEMICAL LIST FINAL.xlsx")

# Utility functions
def check_excel_exists():
    return os.path.exists(EXCEL_PATH)

def save_excel(df):
    try:
        df.to_excel(EXCEL_PATH, index=False)
        return True
    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")
        return False

def load_excel():
    if not check_excel_exists():
        return None
    try:
        return pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return None

def add_sorted_chemical(new_data):
    df = load_excel()
    if df is None:
        return {'ai_response': "The Excel file does not exist or cannot be read.", 'status': 'error'}
    
    if df.empty:
        df = pd.DataFrame([new_data])
    else:
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df = df.sort_values(by='NAME OF THE CHEMICAL', ignore_index=True)
    
    if save_excel(df):
        return {'ai_response': "Chemical added and sorted successfully!", 'status': 'success'}
    return {'ai_response': "Failed to add chemical.", 'status': 'error'}

# Process AI response
def process_ai_response(action=None, data=None):
    df = load_excel()

    if df is None:
        return {'ai_response': "The Excel file does not exist or cannot be read. Please upload a valid file.", 'status': 'error'}

    if df.empty:
        return {'ai_response': "The Excel file is empty. Please add data to get started.", 'status': 'error'}

    try:
        if action == "query":
            chemical_name = data.get('chemical_name')
            column = data.get('column')

            if 'NAME OF THE CHEMICAL' not in df.columns:
                return {'ai_response': "The Excel file does not have the required 'NAME OF THE CHEMICAL' column.", 'status': 'error'}

            if chemical_name not in df['NAME OF THE CHEMICAL'].values:
                return {'ai_response': f"Chemical '{chemical_name}' not found.", 'status': 'error'}

            if column not in df.columns:
                return {'ai_response': f"Column '{column}' not found in the Excel file.", 'status': 'error'}

            result = df.loc[df['NAME OF THE CHEMICAL'] == chemical_name, column].iloc[0]
            return {'ai_response': f"The {column} for {chemical_name} is {result}.", 'status': 'success'}

        elif action == "add":
            new_data = data.get('chemical_data', {})

            if not new_data:
                return {'ai_response': "No data provided for the new chemical.", 'status': 'error'}

            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)

            if save_excel(df):
                return {'ai_response': "Chemical added successfully!", 'status': 'success'}
            return {'ai_response': "Failed to add chemical.", 'status': 'error'}

        elif action == "modify":
            chemical_name = data.get('chemical_name')
            column = data.get('column')
            new_value = data.get('new_value')

            if 'NAME OF THE CHEMICAL' not in df.columns:
                return {'ai_response': "The Excel file does not have the required 'NAME OF THE CHEMICAL' column.", 'status': 'error'}

            if chemical_name not in df['NAME OF THE CHEMICAL'].values:
                return {'ai_response': f"Chemical '{chemical_name}' not found.", 'status': 'error'}

            if column not in df.columns:
                return {'ai_response': f"Column '{column}' not found in the Excel file.", 'status': 'error'}

            df.loc[df['NAME OF THE CHEMICAL'] == chemical_name, column] = new_value

            if save_excel(df):
                return {'ai_response': f"Successfully updated {column} for {chemical_name}!", 'status': 'success'}
            return {'ai_response': "Failed to update chemical.", 'status': 'error'}

        elif action == "delete":
            chemical_name = data.get('chemical_name')

            if 'NAME OF THE CHEMICAL' not in df.columns:
                return {'ai_response': "The Excel file does not have the required 'NAME OF THE CHEMICAL' column.", 'status': 'error'}

            if chemical_name not in df['NAME OF THE CHEMICAL'].values:
                return {'ai_response': f"Chemical '{chemical_name}' not found.", 'status': 'error'}

            df = df[df['NAME OF THE CHEMICAL'] != chemical_name]

            if save_excel(df):
                return {'ai_response': f"Successfully deleted {chemical_name}!", 'status': 'success'}
            return {'ai_response': "Failed to delete chemical.", 'status': 'error'}

        else:
            return {'ai_response': "Invalid action specified.", 'status': 'error'}

    except Exception as e:
        return {'ai_response': f"An error occurred: {str(e)}", 'status': 'error'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    action = data.get('action')
    additional_data = data.get('data')

    response = process_ai_response(action, additional_data)
    return jsonify(response)

@app.route('/get_chemicals')
def get_chemicals():
    df = load_excel()
    if df is None or df.empty or 'NAME OF THE CHEMICAL' not in df.columns:
        return jsonify([])

    chemicals = df['NAME OF THE CHEMICAL'].dropna().tolist()
    return jsonify(chemicals)

@app.route('/get_columns')
def get_columns():
    df = load_excel()
    if df is None or df.empty:
        return jsonify([])

    columns = df.columns.tolist()
    return jsonify(columns)

if __name__ == '__main__':
    app.run(debug=True)