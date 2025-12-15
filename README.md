# multistep-reasoning-agent
Multi-Step Reasoning Agent with Self-Checking

This project implements a multi-step reasoning agent that can solve structured word problems by planning, executing, and verifying its own solutions before returning a final answer.

The system is designed to mimic human-like reasoning while keeping the user-facing output clean and minimal, and exposing internal metadata only for debugging and evaluation.

**🚀 Features**

✅ Multi-phase agent architecture (Planner → Executor → Verifier)

✅ Self-checking with retry mechanism

✅ Deterministic execution using Python (accurate results)

✅ LLM-based planning (mocked, easily swappable with OpenAI)

✅ Clean JSON output schema

✅ Interactive Streamlit UI

✅ Runtime metrics & structured logs

**🏗️ Architecture Overview**

The agent works in three internal phases:

**1️⃣ Planner**

Uses an LLM (currently mocked)

Breaks the question into a step-by-step plan

Does not solve the problem

**2️⃣ Executor**

Uses Python logic to follow the plan

Performs arithmetic and time calculations

Produces intermediate steps and a final answer

**3️⃣ Verifier**

Validates the solution

Ensures a final answer exists and is logically consistent

If verification fails, the agent retries (limited attempts)

**📁 Project Structure**

multi_step_reasoning_agent/

├── agent.py            
├── llm_client.py       
├── prompts.py         
├── main.py             
├── streamlit_app.py    
├── tests.py            
└── README.md           


**🖥️ Streamlit UI**

The Streamlit app provides:

Question input box

Final answer display

Runtime metrics:

Status

Retries

Verification checks

Execution time

Expandable logs:

Planner output

Verifier checks

Full metadata

**▶️ How to Run the Project**

1️⃣ Install dependencies

pip install streamlit

2️⃣ Run Streamlit UI

From the project folder:

streamlit run streamlit_app.py

3️⃣ Run via CLI (optional)
python main.py

4️⃣ Run Test Suite
python tests.py

**🧪 Example Questions**

A recipe needs 2 cups of flour per batch. How much flour is needed for 3 batches?

If a train leaves at 14:30 and arrives at 18:05, how long is the journey?

Alice has 3 red apples and twice as many green apples. How many apples does she have in total?

**🤖 LLM Usage (Mock vs OpenAI)**

This project currently uses a Mock LLM client for planning

The architecture is fully swappable with real LLMs (OpenAI, Gemini, Anthropic)

This avoids API costs while keeping the design production-ready

With more time, a real OpenAI client can be plugged in with minimal changes.

**🧠 Design Decisions**

LLM for planning, Python for execution → ensures accuracy

Verification step prevents incorrect outputs

Retry mechanism improves robustness

Clear separation of concerns improves maintainability

**🚧 Future Improvements**

Add real OpenAI API integration

Support more complex logic (equations, scheduling)

Stronger verifier (independent re-solving)

Persist logs and metrics

Multi-question history in UI

**🏁 Summary**

This project demonstrates how to build a robust reasoning agent that:

Thinks before solving

Verifies its own work

Produces clean, reliable answers

Is suitable for real-world AI systems
