from smolagents import CodeAgent, VisitWebpageTool, HfApiModel

agent = CodeAgent(
    tools=[VisitWebpageTool()],
    model=HfApiModel(),
    additional_authorized_imports=["requests", "markdownify"],
    use_e2b_executor=True
)


if __name__ == '__main__':
    agent.run("What was Abraham Lincoln's preferred pet?")