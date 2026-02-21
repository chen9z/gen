import json

from model.llm_model import *


def get_weather(city: str):
    if city == "北京":
        return str({"temperature": 25, "condition": "晴朗"})
    else:
        return str({"temperature": 30, "condition": "多云"})


if __name__ == '__main__':
    messages = [{"role": "user", "content": "上海的天气怎样？"}]
    response = get_response_tool(messages,
                                 tools=[
                                     {
                                         "type": "function",
                                         "function": {
                                             "name": "get_weather",
                                             "description": "get the weather of city",
                                             "parameters": {
                                                 "type": "object",
                                                 "properties": {
                                                     "city": {
                                                         "type": "string",
                                                         "description": "The city"
                                                     },
                                                 },
                                                 "required": ["city"]
                                             }
                                         }
                                     }
                                 ]
                                 )
    response_message = response.choices[0].message
    print(response_message)
    messages.append(response_message)
    tool_calls = response_message.tool_calls
    if tool_calls:
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_query_string = json.loads(tool_calls[0].function.arguments)["city"]

        if tool_function_name == 'get_weather':
            result = get_weather(tool_query_string)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": tool_function_name,
                "content": result
            })
            final_response = get_response_tool(messages=messages)
            print(final_response.choices[0].message.content)
