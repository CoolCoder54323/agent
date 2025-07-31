import os
import time

import openai
import streamlit as st
import asyncio
from agents import Agent, Runner

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
agent_task_help = Agent(
    name="Task Help",
    instructions="""Use the provided list of applications to help fulfill the user's request. 
                    Respond with detailed, longform, step-by-step instructions in Markdown format that explain which 
                    apps to use and how to use them. Try to incorporate multiple relevant apps in the response whenever possible.

                    Requirements:
                    - Format the entire response using Markdown.
                    - Provide clear, step-by-step instructions.
                    - Mention multiple apps from the list when appropriate.
                    - Use headings (e.g., ## Step 1) and bold app names for readability.
                    - Include short descriptions of what each app does and why it's being used.
                    - Ensure the final instructions are logical, easy to follow, and fully address the user's task.
                    """,
)

agent_app_help = Agent(
    name="App help",
    instructions="""Use the provided list of applications to fulfill the user's request.
                    Respond with relevant information about the user's app folder.

                    Requirements:
                        Format all responses using Markdown.
                        Include app names in bold.
                        If listing multiple apps, use a bulleted list.
                        Use known details and instructions about specific apps.
                        Keep responses concise and informative.""",
)

agents = [agent_task_help,agent_app_help]

async def generate_tasks(goal,agent):

    result = await Runner.run(agents[agent], goal)
    return result.final_output


def run_async_task(goal,agent):
    return asyncio.run(generate_tasks(goal,agent))



st.set_page_config(page_title="AGENT", layout="centered")
st.title("Mac Application helper")

user_input = st.text_area("Enter your prompt:", height=200)

applications = os.listdir("/Applications")

agent_select = st.selectbox("Choose question type",["1.  Help with task","2.  Question about Applications"],width=350)

left, right = st.columns(2, vertical_alignment="bottom")
key_input = left.text_input("optional OPEN_AI KEY")


if right.button("enter"):
    OPENAI_API_KEY = key_input
    os.environ["OPENAI_API_KEY"] = key_input
    success = st.success("Running with new key")

    time.sleep(1)
    success.empty()


if st.button("Submit Prompt"):
    response_placeholder = st.empty()

    with st.spinner("writing..."):
        agent_n = int(agent_select[0]) - 1

        response = run_async_task(f"Applications:{applications} User Instruction:{user_input}",agent_n)
        success = st.success("Done!")
        time.sleep(1)
        success.empty()
        response_placeholder.markdown(response)

