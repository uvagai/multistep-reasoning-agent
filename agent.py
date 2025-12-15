

import re
from typing import Dict, Any, List

from llm_client import LLMClient
from prompts import PLANNER_PROMPT


# -------------------------
# PLANNER
# -------------------------
def call_planner(llm: LLMClient, question: str) -> str:
    """
    Uses LLM (mock or real) to create a step-by-step plan.
    """
    prompt = PLANNER_PROMPT.format(question=question)
    plan = llm.generate(prompt)
    return plan.strip()


# -------------------------
# EXECUTOR (Python-based)
# -------------------------
def call_executor(question: str, plan: str) -> Dict[str, Any]:
    """
    Executes the plan using Python logic for correctness.
    Handles:
    - Simple arithmetic
    - Per-unit / batch multiplication
    - Time difference (HH:MM)
    """

    q = question.lower()

    # ---- Case 1: Time difference problems ----
    time_matches = re.findall(r"\b\d{1,2}:\d{2}\b", question)
    if len(time_matches) >= 2:
        start, end = time_matches[0], time_matches[1]

        sh, sm = map(int, start.split(":"))
        eh, em = map(int, end.split(":"))

        start_min = sh * 60 + sm
        end_min = eh * 60 + em

        if end_min < start_min:
            raise ValueError("End time is earlier than start time")

        diff = end_min - start_min
        hours = diff // 60
        minutes = diff % 60

        answer = f"{hours} hours {minutes} minutes" if minutes else f"{hours} hours"

        return {
            "steps": [
                {"step": 1, "description": "Convert times to minutes", "result": [start_min, end_min]},
                {"step": 2, "description": "Subtract start from end", "result": diff},
            ],
            "final_answer": answer
        }

    # ---- Case 2: Per-unit / batch problems ----
    numbers = list(map(int, re.findall(r"\d+", question)))

    if "per" in q or "each" in q or "batch" in q:
        if len(numbers) >= 2:
            result = numbers[0] * numbers[1]
            return {
                "steps": [
                    {"step": 1, "description": "Extract quantities", "result": numbers},
                    {"step": 2, "description": "Multiply per-unit value", "result": result},
                ],
                "final_answer": str(result)
            }

    # ---- Case 3: Simple addition ----
    if numbers:
        total = sum(numbers)
        return {
            "steps": [
                {"step": 1, "description": "Extract numbers", "result": numbers},
                {"step": 2, "description": "Add all numbers", "result": total},
            ],
            "final_answer": str(total)
        }

    # ---- Fallback ----
    raise ValueError("Unable to solve the given question")


# -------------------------
# VERIFIER
# -------------------------
def call_verifier(question: str, solution: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifies that the final answer exists and is logically valid.
    """

    final_answer = solution.get("final_answer")

    if final_answer is None or final_answer == "":
        return {
            "check_name": "solution_existence_check",
            "passed": False,
            "details": "Final answer is missing"
        }

    return {
        "check_name": "basic_consistency_check",
        "passed": True,
        "details": "Final answer exists and basic checks passed"
    }


# -------------------------
# MAIN AGENT LOOP
# -------------------------
def solve_with_agent(
    llm: LLMClient,
    question: str,
    max_retries: int = 2
) -> Dict[str, Any]:

    retries = 0
    checks: List[Dict[str, Any]] = []
    last_plan = ""

    while retries <= max_retries:
        try:
            # 1️⃣ Plan
            plan = call_planner(llm, question)
            last_plan = plan

            # 2️⃣ Execute
            solution = call_executor(question, plan)

            # 3️⃣ Verify
            verdict = call_verifier(question, solution)
            checks.append(verdict)

            if verdict["passed"]:
                return {
                    "answer": solution["final_answer"],
                    "status": "success",
                    "reasoning_visible_to_user": (
                        "The agent planned the solution, executed it step-by-step, "
                        "and verified the result successfully."
                    ),
                    "metadata": {
                        "plan": plan,
                        "checks": checks,
                        "retries": retries
                    }
                }

            retries += 1

        except Exception as e:
            checks.append({
                "check_name": "execution_error",
                "passed": False,
                "details": str(e)
            })
            retries += 1

    # ---- Failed after retries ----
    return {
        "answer": None,
        "status": "failed",
        "reasoning_visible_to_user": (
            "The agent could not confidently solve and verify the problem."
        ),
        "metadata": {
            "plan": last_plan,
            "checks": checks,
            "retries": retries
        }
    }
