# prompts.py

PLANNER_PROMPT = """
You are a planning assistant for a reasoning agent.

Given a user question, your job is to output a CLEAR, NUMBERED step-by-step plan
for how to solve it. Do NOT solve the problem. Only plan.

FORMAT:
Return only the plan as plain text, like:
1. ...
2. ...
3. ...

EXAMPLES:

Question: Alice has 3 red apples and twice as many green apples as red. How many apples does she have in total?
Plan:
1. Identify the number of red apples (3).
2. Compute the number of green apples as 2 × red apples.
3. Add red and green apples to get total.
4. Return the total number of apples.

Question: A train leaves at 14:30 and arrives at 18:05. How long is the journey?
Plan:
1. Extract the departure time (14:30) and arrival time (18:05).
2. Convert both times to minutes since midnight.
3. Subtract departure minutes from arrival minutes.
4. Convert the difference back into hours and minutes.
5. Return the duration as hours and minutes.

Now generate a plan for this question:

Question: {question}
Plan:
"""

EXECUTOR_PROMPT = """
You are the execution engine of a reasoning agent.

You MUST return a JSON object with this structure:

{{
  "steps": [
    {{"step": 1, "description": "...", "result": "..."}},
    {{"step": 2, "description": "...", "result": "..."}}
  ],
  "final_answer": "<short final answer>"
}}

QUESTION:
{question}

PLAN:
{plan}

OUTPUT JSON:
"""

VERIFIER_PROMPT = """
You are the verifier of a reasoning agent.

You MUST output a JSON object:

{{
  "passed": true or false,
  "check_name": "consistency_check",
  "details": "Short explanation"
}}

QUESTION:
{question}

PROPOSED SOLUTION:
{solution}

OUTPUT JSON:
"""
