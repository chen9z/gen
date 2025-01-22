import os
import dotenv
import dspy

dotenv.load_dotenv()

lm = dspy.LM(os.getenv("DEFAULT_MODEL"), api_key=os.getenv(
    "DEFAULT_API_KEY"), api_base=os.getenv("DEFAULT_API_BASE"))
dspy.configure(lm=lm)

math = dspy.ChainOfThought("question -> answer: float")
# print(math("9.9 和 9.11 那个大？"))
print(str(math("Two dice are tossed. What is the probability that the sum equals two?")))