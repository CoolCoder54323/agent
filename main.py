import os
import time

import openai
import streamlit as st
import asyncio
from agents import Agent, Runner

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
agent_task_help = Agent(
    name="Task Help",
    instructions="""Use the list of applications to help complete the users, request. 
                    RESPOND WITH LONGFORM STEP BY STEP MARKDOWN INSTRUCTIONS ON WHAT APPS TO USE, TRY TO MENTION MULTIPLE APPS""",
)

agent_app_help = Agent(
    name="App help",
    instructions="""Use the list of applications to help complete the users, request. 
                    Respond with information about the users app folder, or any questions about an individual app.
                     USE MARKDOWN""",
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

agent_select = st.selectbox("Choose question type",["1.  Question about Applications","2.  Help with task"],width=350)

left, right = st.columns(2, vertical_alignment="bottom")
key_input = left.text_input("optional OPEN_AI KEY")


if right.button("enter"):
    OPENAI_API_KEY = key_input
    os.environ["OPENAI_API_KEY"] = key_input
    success = st.success("Running with new key")

    time.sleep(1)
    success.empty()


if st.button("Generate Tasks"):
    response_placeholder = st.empty()

    with st.spinner("Generating tasks..."):
        agent_n = int(agent_select[0]) - 1

        response = run_async_task(f"Applications:{applications} User Instruction:{user_input}",agent_n)
        success = st.success("Done!")
        time.sleep(1)
        success.empty()
        response_placeholder.markdown(response)

