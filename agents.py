from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is missing.")

# model setup
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=2
)

# 1st agent - Search Agent
def search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a professional research assistant.

        Your responsibility is to research the given topic.

        Rules:
        1. Use the web_search tool to search for information.
        2. The tool requires one argument named query.
        3. Search for recent and reliable information.
        4. Analyze the search results carefully.
        5. Summarize the findings accurately.
        6. Never invent information.
        """
    )


# 2nd Agent - Reader Agent
def reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are an expert web content reader.

        Your responsibility is to read webpages and extract
        useful information for research.

        Rules:
        1. Use only the scrape_url tool.
        2. Never call a tool named open, browser, or click.
        3. Extract important facts and explanations.
        4. Preserve source URLs.
        5. Never invent information.
        """
    )


# Writter chain
writter_prompt = ChatPromptTemplate([
    ("system", "You are expert research writter. Writter clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.
    
    Topic : {topic}

    Research Gathered:
    {research}

    Structure the report as:
    - Introduction
    - Key Findings(Minimum 3 well-explained points)
    - Conclusion
    - Sources(list all URLs found in the research)

    Be detailed, factual and professional.""")
])

writter_chain = writter_prompt | llm | StrOutputParser()

# Critic chain

critic_prompt = ChatPromptTemplate([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.
    
    Report:
    {report}
    
    Respond in this exact format:
    
    Score : X/10
    - ...
    - ...
    
    Areas to Improve:
    - ...
    - ...
    
    One line verdict:
    ...""")
])

critic_chain = critic_prompt | llm | StrOutputParser()