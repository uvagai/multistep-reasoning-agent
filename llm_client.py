

from typing import Any


class LLMClient:
    """
    Base LLM client. Can be replaced later with real OpenAI calls.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement generate()")


class MockLLMClient(LLMClient):
    """
    Mock implementation just to make the agent run without real API.
    """

    def generate(self, prompt: str) -> str:
        # Very simple pattern-based mock for now.

        # If it's a planner prompt (contains 'Plan:' and 'Question:')
        if "Plan:" in prompt and "Question:" in prompt:
            return (
                "1. Parse the question and identify key numbers and relationships.\n"
                "2. Extract quantities such as counts, times, or amounts.\n"
                "3. Perform the necessary arithmetic or time calculations.\n"
                "4. Validate that the result is consistent with the question.\n"
                "5. Format and return the final answer."
            )

        # If it's an executor prompt (we expect JSON with 'steps' and 'final_answer')
        if "OUTPUT JSON:" in prompt and '"steps"' in prompt:
            # Just return a fake JSON with steps and final_answer = "3"
            return """
{
  "steps": [
    {"step": 1, "description": "Mock calculation step 1", "result": 1},
    {"step": 2, "description": "Mock calculation step 2", "result": 2}
  ],
  "final_answer": "3"
}
"""

        # If it's a verifier prompt (we expect pass/fail JSON)
        if "PROPOSED SOLUTION:" in prompt:
            return """
{
  "passed": true,
  "check_name": "consistency_check",
  "details": "Mock verifier: assuming solution is consistent."
}
"""

        # Fallback
        return "Mock response"
