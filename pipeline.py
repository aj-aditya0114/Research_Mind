from agents import search_agent, reader_agent, writter_chain, critic_chain
from image_generator_agent import image_generator_agent

def run_research_pipeline(topic : str)-> dict:
    state = {}

   # STEP 1 - SEARCH AGENT

    print("\n"+" = "*50)
    print("step 1 - search agent is working...")
    print("="*50)

    search_agent_instance = search_agent()
    search_result = search_agent_instance.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    # STEP 2 - READER AGENT

    print("\n"+" ="*50)
    print("step - 2 reader agent s scraping top resources...")
    print("="*50)

    reader_agent_instance = reader_agent()
    reader_result = reader_agent_instance.invoke({
        "messages": [("user",
                      f"Based on the following search results about '{topic}', "
                      f"pick the most relevant URL and scrape it for deeper content. \n\n"
                      f"Search Results: \n{state['search_results'][:800]}"
                      )]
    })


    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n Scraped content: \n", state['scraped_content'])

    # STEP 3 - WRITER CHAIN

    print("\n"+" ="*50)
    print("step - 3 - Writter agent is drafting the report...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
    )

    state['report'] = writter_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report \n", state['report'])

    # STEP 4 - IMAGE GENERATOR AGENT

    print("\n" + "=" * 50)
    print("STEP 4 - Image Generator Agent is working...")
    print("=" * 50)
    try:

        state["generated_images"] = image_generator_agent(
            report=state["report"],
            max_images=5
        )
        print("\nGenerated Images:")
        for image in state["generated_images"]:
            print({
                "section": image["section_heading"],
                "caption": image["caption"],
                "image_path": image["image_path"],
                "status": image["status"]
            })
    except Exception as error:
        print(f"\nImage Generator Agent Error: {error}")
        state["generated_images"] = []

    # STEP 5 - CRITIC CHAIN
    print("\n"+" ="*50)
    print("step - 4 - Critic is reviewing the report...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)