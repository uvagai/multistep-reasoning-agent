

from typing import Dict, Any
from llm_client import MockLLMClient
from agent import solve_with_agent


def solve(question: str) -> Dict[str, Any]:
    """
    Public function that other files or notebooks can call.
    """
    llm = MockLLMClient()
    return solve_with_agent(llm, question)


if __name__ == "__main__":
    print("Multi-Step Reasoning Agent (Mock LLM)")
    user_q = input("Enter your question: ")
    result = solve(user_q)
    print("\nFinal JSON output:")
    print(result)
