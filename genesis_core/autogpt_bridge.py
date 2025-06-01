import subprocess
import os

def run_autogpt(task_prompt: str):
    os.chdir("AutoGPT")
    with open("input.txt", "w") as f:
        f.write(task_prompt)

    result = subprocess.run(["python", "-m", "autogpt"], capture_output=True, text=True)
    return result.stdout
