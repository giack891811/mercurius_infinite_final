import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class LocalAI:
    def __init__(self, model_name="gpt2", device=None):
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🤖 LocalAI loading model: {model_name} ({self.device})")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def rispondi(self, prompt: str, max_new_tokens: int = 128) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.8,
                top_p=0.95
            )
        result = self.tokenizer.decode(output[0], skip_special_tokens=True)
        print(f"[LocalAI] Input: {prompt}\n[LocalAI] Output: {result}")
        self._log_interaction(prompt, result)
        return result

    def _log_interaction(self, prompt, result):
        with open("logs/localai_interactions.log", "a", encoding="utf-8") as f:
            f.write(f"PROMPT: {prompt}\nOUTPUT: {result}\n{'-'*40}\n")

if __name__ == "__main__":
    ai = LocalAI()
    while True:
        txt = input("Prompt> ")
        print(ai.rispondi(txt))
