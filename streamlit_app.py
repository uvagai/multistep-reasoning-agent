import time
import streamlit as st

from llm_client import MockLLMClient
from agent import solve_with_agent


# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Multi-Step Reasoning Agent",
    layout="centered"
)

st.title("🧠 Multi-Step Reasoning Agent")
st.write(
    "Ask a reasoning or word problem. "
    "The agent will plan, execute, verify, and return a clean answer."
)

# ---------------------------
# Input
# ---------------------------
question = st.text_area(
    "Enter your question:",
    placeholder="A recipe needs 2 cups of flour per batch. How much flour is needed for 3 batches?"
)

# ---------------------------
# Solve Button
# ---------------------------
if st.button("🚀 Solve"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        llm = MockLLMClient()

        with st.spinner("Thinking step-by-step..."):
            start_time = time.time()
            result = solve_with_agent(llm, question)
            end_time = time.time()

        exec_time = round(end_time - start_time, 3)

        # ---------------------------
        # METRICS SECTION
        # ---------------------------
        st.subheader("📊 Metrics")

        col1, col2, col3, col4 = st.columns(4)

        status = result["status"]
        retries = result["metadata"]["retries"]
        checks = result["metadata"]["checks"]
        passed_checks = sum(1 for c in checks if c.get("passed"))

        col1.metric("Status", "✅ Success" if status == "success" else "❌ Failed")
        col2.metric("Retries", retries)
        col3.metric("Checks Passed", f"{passed_checks}/{len(checks)}")
        col4.metric("Execution Time (s)", exec_time)

        # ---------------------------
        # FINAL ANSWER
        # ---------------------------
        st.subheader("✅ Final Answer")
        if result["answer"] is not None:
            st.success(result["answer"])
        else:
            st.error("No confident answer could be produced.")

        # ---------------------------
        # USER-FACING REASONING
        # ---------------------------
        st.subheader("🧩 Reasoning (Short)")
        st.write(result["reasoning_visible_to_user"])

        # ---------------------------
        # DEBUG / LOGS
        # ---------------------------
        with st.expander("🪵 Logs & Debug Info (Evaluation Only)"):
            st.markdown("### 🧠 Planner Output")
            st.code(result["metadata"]["plan"])

            st.markdown("### ✅ Verifier Checks")
            for idx, check in enumerate(checks, start=1):
                st.write(f"**Check {idx}: {check['check_name']}**")
                st.write(f"- Passed: {check['passed']}")
                st.write(f"- Details: {check['details']}")

            st.markdown("### 🔁 Retry Count")
            st.write(retries)

            st.markdown("### 🧾 Full Metadata JSON")
            st.json(result["metadata"])
