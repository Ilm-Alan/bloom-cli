# ACP Setup

Bloom can be used in text editors and IDEs that support [Agent Client Protocol](https://agentclientprotocol.com/overview/clients). Bloom includes the `bloom-acp` tool.
Once you have set up `bloom` with the API keys, you are ready to use `bloom-acp` in your editor. Below are setup instructions for editors that support ACP.

## JetBrains IDEs

1. Add the following snippet to your JetBrains IDE acp.json ([documentation](https://www.jetbrains.com/help/ai-assistant/acp.html)):

```json
{
  "agent_servers": {
    "Bloom": {
      "command": "bloom-acp",
    }
  }
}
```

2. In the AI Chat agent selector, select the new Bloom agent and start the conversation.

## Neovim (using avante.nvim)

Add Bloom in the acp_providers section of your configuration

```lua
{
  acp_providers = {
    ["bloom-cli"] = {
      command = "bloom-acp",
      env = {
         POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY"), -- necessary if you setup Bloom manually
      },
    }
  }
}
```
