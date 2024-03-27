import logging
import sys

import llm_model
from rag_query import QueryModel
from spliter import SentenceSpliter

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

prompt_template = """
You are a large language AI assistant. You are given a user question, and please write clean, concise and accurate answer to the question.
Your answer must be correct, accurate and written by an expert using an unbiased and professional tone. Please limit to 1024 tokens.
Do not give any information that is not related to the question, and do not repeat. 
Say "information is missing on" followed by the related topic, if the given context do not provide sufficient information.
your answer must be written with **Chinese**

Here are the set of contexts:

{context}

Remember, don't blindly repeat the contexts verbatim.
And here is the user question:
"""

if __name__ == '__main__':
    query_model = QueryModel()
    connection_name = "ymxt"
    with open("./data/ymxt.txt", "r") as f:
        data = f.read()
        spliter = SentenceSpliter(2000, 200)
        results = spliter.split_text(data)
        query_model.encode(connection_name, results)

        while True:
            prompt = input("请输入问题：")
            if prompt == "exit":
                break
            results = query_model.query(connection_name, prompt, 10)
            for result in results:
                print(f"Results: {result} \n\n")

            system_prompt = prompt_template.format(
                context="\n\n".join(response.payload.get("text") for response in results))
            print("System Prompt: \n", system_prompt)
            print(llm_model.get_response_message_with_groq(system_prompt))
