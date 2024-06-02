from transformers import AutoTokenizer, AutoModel


def chat_stream(tokenizer, model, inputs, history=[]):
    for input in inputs:
        response, history = model.chat(tokenizer, input, history=history)
        yield response, history


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-128k", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b-128k", trust_remote_code=True).half().cuda().eval()

    response, history = model.chat(tokenizer, "你好", history=[])
    print(response)
    response = model.g(tokenizer, "你好，给我讲一个 1000 字的短篇小说", history=history)
    print(response)
