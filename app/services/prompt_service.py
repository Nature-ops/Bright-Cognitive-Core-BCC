from pathlib import Path


class PromptService:

    def get(self, filename: str) -> str:

        prompt_path = Path("app/prompts") / filename

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()