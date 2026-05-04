from agent.agent_layer import FalconXAgentLayer

agent = FalconXAgentLayer()

result = agent.evaluate(
    source="AI_ASSISTANT",
    message="Open a BTC long trade now",
    requested_action="execute_trade",
    human_approval=False
)

print(result)
