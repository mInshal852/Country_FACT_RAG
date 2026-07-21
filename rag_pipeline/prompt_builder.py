import os


class PromptBuilder:

    def __init__(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        prompt_path = os.path.join(
            current_dir,
            "prompts",
            "system_prompt.txt",
        )

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def build_prompt(self, query, retrieved_chunks):
        """
        Returns:
            tuple[str, str]
            (system_prompt, user_prompt)
        """

        context = []

        for index, chunk in enumerate(retrieved_chunks, start=1):

            context.append(f"""[Document {index}]
Country: {chunk["metadata"].get("country", "Unknown")}
Section: {chunk["metadata"].get("section", "Unknown")}

{chunk["text"]}
""")

        user_prompt = f"""
Context:
{chr(10).join(context)}

User Question:
{query}
"""

        return self.system_prompt, user_prompt.strip()
