from langchain_community.chat_models import ChatPerplexity
from dotenv import load_dotenv
import os
load_dotenv()


class PerplexityLLM:
    """
    Wrapper for querying the perplexity LLM to get trending product ideas.
    """

    def __init__(self):

        self.llm = ChatPerplexity(perplexity_api_key = os.getenv("PERPLEXITY_KEY"))

    def get_trending_keywords(self, prompt: str = None, top_n: int = 5):

        if not prompt:

            prompt = "List the top 5 trending ecommerce product categories for q3 2025."

            response = self.llm(prompt)

            # Example response: "1. Wireless Earbuds\n2. Smart Watches\n3..."
            keywords = [line.split(". ", 1)[1] for line in response.split("\n") if ". " in line]

            return keywords[:top_n]

# Example usage
if __name__ == "__main__":

    llm = PerplexityLLM()
    print(llm.get_trending_keywords())