# Week 2: build your own agent

**Due before class on Wednesday, October 14, 2026.**

In class we took an agent apart: an agent is a loop of API calls, and a tool call is just text your program acts on. This week you build that loop yourself: a small program, a **harness**, that chats with you and can run shell commands. It has exactly one tool, `bash`. Over the coming weeks we'll grow everyone's harness with more tools, MCP servers, skills and other agents.

An AI coding agent writes most of the code with you. You make the decisions, and by the end you can point at the loop and explain every step.

## Start

1. Open an AI coding agent (Claude Code, Codex, Cursor, GitHub Copilot, …) in a folder under your home directory.
2. Give it this:

   > Read https://class.xhelio.ai/week-2/homework.md and help me with my homework.

It helps you get a model API, build and test the harness, publish it, and open your pull request.

**You'll need:** a [GitHub account](https://github.com/signup), [uv](https://docs.astral.sh/uv/), an AI coding agent, and a model API: see below. macOS, Linux or Windows.

## Your harness

A program in its own public GitHub repository that:

1. **Talks to a model** through an OpenAI-compatible API (`/v1/chat/completions`). The base URL, the API key and the model name come from environment variables, never from the code.
2. **Runs the agent loop** you saw in class: send the conversation and the tool; if the reply is a tool call, run it, append the result, and call again; if it's text, show it and wait for you.
3. **Has one tool, `bash`:** it runs a shell command and returns the output and the exit code, with a time limit, and cuts very long output short.
4. **Asks you before each command** runs. Saying no tells the model you declined.
5. **Chats with you** in a local web page (recommended) or in the terminal.
6. **Shows each call's token usage**: input, cached input when the API reports it, and output.

Write the loop yourself, with your AI agent's help. No agent frameworks (LangChain, the OpenAI Agents SDK, the Claude Agent SDK and the like): the point is to see that the loop is a dozen lines. Keep it small; a few hundred lines is plenty.

## Getting a model API

- **Your subscription, served locally with [sub2api](https://github.com/Wei-Shaw/sub2api) (recommended).** sub2api runs on your own computer and turns a subscription you already pay for (ChatGPT, Claude, Gemini, …) into an API that only you use.

  > **Warning: this can get your account banned.** Using a subscription this way may break your provider's terms. OpenAI's Codex lead [said in August 2026](https://x.com/thsottiaux/status/2090675027670978569) that many users flagged by their fraud-prevention systems were using sub2api. Anthropic's [Claude Code terms](https://code.claude.com/docs/en/legal-and-compliance) forbid routing requests through Free, Pro or Max credentials, and Google's [Gemini CLI terms](https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/tos-privacy.md) say third-party access with Gemini CLI's sign-in may get an account suspended. sub2api's own README says the risk is yours. If you use it: only your own account, only on your own computer, never shared, and never reachable from the network. If you'd rather not take the risk, use OpenRouter.

- **[OpenRouter](https://openrouter.ai).** One key for hundreds of models, OpenAI-compatible at `https://openrouter.ai/api/v1`. Some models are free (`:free`): 50 requests a day, or 1,000 a day once you've bought $10 of credits. An agent loop makes several requests per question, so 50 goes fast.
- **Any other OpenAI-compatible API key** you have (OpenAI, Gemini, DeepSeek, …) works too.

## What you submit

A pull request adding one file, `week-2/submissions/<your-github-username>/SKILL.md`: a skill that tells an AI agent how to install your harness from your public repository, configure it, run it, and check that it works. Someone else's agent should be able to follow it on a fresh computer. Say in your pull request which AI helped you, and how.

It counts when the repository is public, the skill works, and the harness does everything in the list above.

## Over the quarter

Your harness grows with the course: more tools, then MCP servers, skills, and finally several agents working together.
