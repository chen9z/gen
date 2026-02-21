import asyncio
import logging
from typing import List

import aiohttp

from model import llm_model
from model.llm_model import get_ollama_response_async
from tools import fetch_webpage_text, search_web


async def generate_search_queries_async(query: str) -> List[str]:
    prompt = """
    you are an expert research assistant. Given the user's query, generate up to four distinct,
    precise search queries that would help gather comprehensive information on the topic.
    return only a Python list of strings, for example: ['query1','query2','query3']
    """

    messages = [
        {
            "role": "system",
            "content": "You are a helpful and precise research assistant.",
        },
        {"role": "user", "content": f"User Query: {query}\n\n{prompt}"},
    ]

    response = await get_ollama_response_async(messages=messages)
    search_queries = eval(response)
    if search_queries and isinstance(search_queries, list):
        return search_queries
    return []


async def get_new_search_queries_async(
        user_query, previous_search_queries, all_contexts
):
    context_combined = "\n".join(all_contexts)
    prompt = (
        "You are an analytical research assistant. Based on the original query, the search queries performed so far, "
        "and the extracted contexts from webpages, determine if further research is needed. "
        "If further research is needed, provide up to four new search queries as a Python list (for example, "
        "['new query1', 'new query2']). If you believe no further research is needed, respond with exactly ."
        "\nOutput only a Python list or the token  without any additional text."
    )
    messages = [
        {"role": "system", "content": "You are a systematic research planner."},
        {
            "role": "user",
            "content": f"User Query: {user_query}\nPrevious Search Queries: {previous_search_queries}\n\nExtracted Relevant Contexts:\n{context_combined}\n\n{prompt}",
        },
    ]

    response = await llm_model.get_ollama_response_async(messages)
    if response:
        cleaned = response.strip()
        if cleaned == "":
            return cleaned
        try:
            new_queries = eval(cleaned)
            if isinstance(new_queries, list):
                return new_queries
        except Exception as e:
            print(f"Error parse new queries response:{cleaned}")
            return []


async def generate_final_report_async(user_query, all_contexts):
    """
    Generate the final comprehensive report using all gathered contexts.
    """
    context_combined = "\n".join(all_contexts)
    prompt = (
        "You are an expert researcher and report writer. Based on the gathered contexts below and the original query, "
        "write a comprehensive, well-structured, and detailed report that addresses the query thoroughly. "
        "Include all relevant insights and conclusions without extraneous commentary."
    )
    messages = [
        {"role": "system", "content": "You are a skilled report writer."},
        {
            "role": "user",
            "content": f"User Query: {user_query}\n\nGathered Relevant Contexts:\n{context_combined}\n\n{prompt}",
        },
    ]
    report = await llm_model.get_ollama_response_async(messages)
    return report


async def extract_relevant_context_async(user_query, search_query, page_text):
    prompt = """
    You are an expert information extractor. Given the user's query, the search query that led to this page, 
    and the webpage content, extract all pieces of information that are relevant to answering the user's query.
    Return only the relevant context as plain text without commentary.
    """

    messages = [
        {
            "role": "system",
            "content": "You are an expert in extracting and summarizing relevant information.",
        },
        {
            "role": "user",
            "content": f"User Query: {user_query}\nSearch Query: {search_query}\n\nWebpage Content (first 20000 characters):\n{page_text[:20000]}\n\n{prompt}",
        },
    ]

    report = await llm_model.get_ollama_response_async(messages)
    return report


async def is_page_userful_async(query, page_text):
    prompt = """
    You are a critical research evaluator. Given the user's query and the content of a webpage,
    determine if the webpage contains information relevant and useful for addressing the query.
    Respond with exactly one word: 'Yes' if the page is useful, or 'No' if it is not. Do not include any extra text.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a strict and concise evaluator of research relevance.",
        },
        {
            "role": "user",
            "content": f"User Query: {query}\n\nWebpage Content (first 20000 characters):\n{page_text[:20000]}\n\n{prompt}",
        },
    ]

    response = await llm_model.get_ollama_response_async(messages)
    if response:
        answer = response.strip()
        if answer in ["Yes", "No"]:
            return "Yes" == answer
    return False


async def process_link(link, user_query, search_query):
    print(f"Fetching content from {link}")
    page_text = await fetch_webpage_text(link)
    if not page_text:
        return None
    if not await is_page_userful_async(user_query, page_text):
        return None
    return await extract_relevant_context_async(user_query, search_query, page_text)


async def main():
    user_query = input("Enter your research query:").strip()
    all_contexts = []
    all_search_queries = []
    iteration = 0
    iteration_limit = 3

    async with aiohttp.ClientSession() as session:
        new_search_queries = await generate_search_queries_async(user_query)
        if not new_search_queries:
            print(f"No Search queries were generated by LLM")
            return
        all_search_queries.extend(new_search_queries)
        while iteration < iteration_limit:
            print(f"=== Iteration: {iteration} ===")
            iteration_context = []
            search_tasks = [fetch_webpage_text(query) for query in new_search_queries]
            search_results = await asyncio.gather(*search_tasks)

            unique_links = {}
            for idx, links in enumerate(search_results):
                query = new_search_queries[idx]
                for link in links:
                    if link not in unique_links:
                        unique_links[link] = query

            print(f"Aggregated {len(unique_links)} unique links from this iteration.")

            link_tasks = [
                process_link(link, user_query, unique_links[link])
                for link in unique_links
            ]

            link_results = await asyncio.gather(*link_tasks)

            for res in link_results:
                if res:
                    iteration_context.append(res)

            if iteration_context:
                all_contexts.extend(iteration_context)
            else:
                print("No useful contexts were found in this iteration")

            new_search_queries = await get_new_search_queries_async(
                user_query, new_search_queries, all_contexts
            )

            if new_search_queries == "":
                print("LLM indicated that no further research in needed")
                break
            if new_search_queries:
                print("LLM provided new search queries:", new_search_queries)
                all_search_queries.extend(new_search_queries)
                iteration += 1
            else:
                print("LLM did not provide any new search queries. Ending the loop.")
                break

        print("Geerate final report...")
        final_report = await generate_final_report_async(user_query, all_contexts)
        print("\n=== FINAL REPORT === \n")
        print(final_report)


async def main():
    queries = await generate_search_queries_async("最新的 jdk 版本")
    if not queries:
        logging.error("search no results")
    for q in queries:
        results = await search_web(q)
        if not results:
            continue
        print(f"query: {q}")
        for r in results:
            print(f"title: {r['title']} - url: {r['url']}")


if __name__ == "__main__":
    asyncio.run(main())
