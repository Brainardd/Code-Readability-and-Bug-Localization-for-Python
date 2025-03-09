import pickle
import tempfile
import subprocess
import timeit
import sys
import os
import ast
import re
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the trained model and tokenizer
MODEL_PATH = "CRModel.keras"
TOKENIZER_PATH = "python_tokenizer.pkl"

def load_model_and_tokenizer():
    global model, tokenizer
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, "rb") as handle:
        tokenizer = pickle.load(handle)

load_model_and_tokenizer()

def clean_python_code(code):
    if not isinstance(code, str) or len(code.strip()) == 0:
        return "EMPTY_CODE"

    code = code.replace('\t', '    ')
    code = re.sub(r'#.*', '', code)
    code = re.sub(r'""".*?"""|\'\'\'.*?\'\'\'', '', code, flags=re.DOTALL)
    code = re.sub(r'(\b(if|for|while|def|class)\b[^\n]*)(?<!:)\n', r'\1:\n', code)
    code = re.sub(r'(\b(def|class)\b[^\n]*:)(\n\s*\n)', r'\1\n    pass\n', code)

    code = re.sub(r'\s*([,:\])}])', r'\1', code)
    code = re.sub(r'([{[(])\s*', r'\1', code)

    return code.strip()


def predict_readability(code_snippet):
    """
    Predicts if the given code snippet is readable.
    """
    try:
        ast.parse(code_snippet)  # Only checks syntax validity, not correctness
    except SyntaxError:
        return "❌UNREADABLE❌"  # Mark as unreadable if the syntax is completely broken
    
    cleaned_code = clean_python_code(code_snippet)
    sequence = tokenizer.texts_to_sequences([cleaned_code])
    padded_sequence = pad_sequences(sequence, maxlen=500, padding='post')
    
    prediction = model.predict([padded_sequence])
    score = prediction[0][0]
    
    return "✅READABLE✅" if score > 0.5 else "⚠️MAY BE HARD TO READ⚠️"


def check_bugs(code):
    """Run pylint on the provided code snippet and return formatted results."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        result = subprocess.run([
            "pylint", "--disable=all", "--enable=E,F", temp_file_path
        ], capture_output=True, text=True, check=False)

        os.remove(temp_file_path)
        output = result.stdout.strip()

        if "E" in output or "F" in output:
            return f"❌ Bugs Found:\n{output}"
        else:
            return "✅ No major issues detected."

    except FileNotFoundError:
        return "⚠️ Pylint is missing! Install it with: `pip install pylint`."
    except Exception as e:
        return f"⚠️ Error running Pylint: {str(e)}"


def measure_complexity(code):
    """Measures execution time and memory usage of the given code."""
    exec_globals = {}
    indented_code = "\n    ".join(code.splitlines())
    wrapped_code = f"def temp_function():\n    {indented_code}"
    try:
        exec(wrapped_code, exec_globals)
        temp_function = exec_globals["temp_function"]
        execution_time = timeit.timeit(temp_function, number=1000)
        memory_usage = sys.getsizeof(temp_function)
        return f" Execution Time: {execution_time:.6f} sec\n Memory Usage: {memory_usage} bytes"
    except Exception as e:
        return f"⚠️ Error in complexity analysis: {str(e)}"

def run_code(code_snippet):
    """Executes the given code snippet and returns its output."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as temp_file:
            temp_file.write(code_snippet)
            temp_file_path = temp_file.name

        result = subprocess.run(["python", temp_file_path], capture_output=True, text=True, check=False)
        os.remove(temp_file_path)

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"⚠️ Error executing code: {str(e)}"