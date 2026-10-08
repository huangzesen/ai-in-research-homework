---
name: build-a-harness
description: Guide a student in UCLA's "AI in Research" class (EPSS 254, Fall 2026) through the week 2 homework - getting a model API (their subscription served locally with sub2api, or OpenRouter), building their own minimal agent harness with one bash tool and a web or terminal chat, publishing it on GitHub, and submitting a skill that installs it. Use when the user wants to start, continue, test or submit their week 2 homework or their class harness.
---

# Build your own agent harness (AI in Research, week 2)

## Who you are working with, and your role

The person in front of you is in a UCLA graduate seminar on AI in research: a student, an auditor or a professor, often a physical scientist. Some write code every day; some have rarely used a terminal. The full assignment is `week-2/README.md` in this repository; read it first.

They are building a **harness**: the program around a language model that runs the agent loop. In class they learned that an agent is a loop of stateless API calls, that a tool call is text the program acts on, and that every call resends the whole conversation. This homework makes that concrete. Over the coming weeks the class adds more tools, MCP servers, skills and multi-agent coordination to this same harness, so build it clean and small.

- **They must understand their loop.** You write most of the code, but build it in small steps and explain each one in a sentence or two. At the end they should be able to point at the loop and say what each part does. Don't hand them a finished program in one go.
- **Stop at every CHECKPOINT** and wait for their answer.
- **Secrets stay out of this conversation.** Never ask the student to paste an API key, a password or an OAuth code into the chat, and never print one. They type secrets into a `.env` file or a browser themselves. Logins and approvals are marked **(student does this)**: give them the exact steps and wait.
- **Be honest about failures.** Show the key line of an error, say what it means, fix it.

Say hello, tell them in two sentences what the homework is, and give this plan: (1) get a model API, (2) build the harness in small steps, (3) test it, (4) publish it on GitHub, (5) write the install skill and open the pull request. It usually takes one or two sessions of 1–2 hours.

## Step 0: set up

1. Check `git --version`, `uv --version` and `gh --version`; install what's missing (the week 1 skill, `.agents/skills/build-a-task/SKILL.md`, has the per-platform commands).
2. `gh auth status`. If they aren't logged in: **(student does this)** `gh auth login` in their own terminal.
3. Their copy of the class repository: if `~/ai-in-research-homework` exists, `git pull` there; otherwise `cd ~ && git clone https://github.com/huangzesen/ai-in-research-homework.git`. The harness itself lives in **a separate folder**, `~/<harness-name>`, with its own git repository, not inside the homework repository.

## Step 1: a model API

The harness talks to any OpenAI-compatible Chat Completions endpoint. It needs three settings: `BASE_URL`, `API_KEY`, `MODEL`. Offer the options from `week-2/README.md`:

**A. Their subscription through sub2api (recommended).** Before installing anything, show them the warning in `week-2/README.md` in your own words: this may break their provider's terms, and providers have banned accounts for it. **CHECKPOINT:** they decide whether to take that risk. If not, go to B.

If yes:
1. It needs Docker (Docker Desktop on macOS and Windows). Check `docker --version` and `docker compose version`; if missing, **(student does this)** install Docker Desktop from docker.com and start it.
2. Follow the current "Docker Compose" quick start in https://github.com/Wei-Shaw/sub2api#readme (it changes often; read it, don't work from memory): a folder `~/sub2api-deploy`, its `docker-deploy.sh` script, then `docker compose up -d`.
3. **Before starting it, edit `.env`:** set `BIND_HOST=127.0.0.1`, so only this computer can reach it (the default, `0.0.0.0`, exposes it to the whole network), and `RUN_MODE=simple`, the mode for one person, without billing. If it refuses to start in simple mode, the README says to also set `SIMPLE_MODE_CONFIRM=true`.
4. The admin login is in the logs (`docker compose logs sub2api | grep "Generated admin"`). **(student does this)** They open http://127.0.0.1:8080, log in, add their subscription account with the dashboard's OAuth flow, and create an API key. Only their own account.
5. `BASE_URL=http://127.0.0.1:8080/v1`, and `MODEL` is a model their account offers (`curl -s $BASE_URL/models -H "Authorization: Bearer $API_KEY"` lists them).

**B. OpenRouter.** **(student does this)** Make an account at https://openrouter.ai and create an API key. `BASE_URL=https://openrouter.ai/api/v1`. Pick a model that supports tools: https://openrouter.ai/models?supported_parameters=tools (free ones end in `:free`, limited to 50 requests a day without credits).

**C. Any other OpenAI-compatible key** they have: use that provider's base URL and a model with tool calling.

In the harness folder, create `.env` with the three settings, and add `.env` to `.gitignore` **before the first commit**. **(student does this)** They type the key into `.env` themselves. Also commit a `.env.example` with placeholder values.

Test with one request before writing any harness code: a plain chat completion, then one with a `tools` list, checking that a `tool_calls` reply comes back. If tool calls don't work with their model, choose another model now.

## Step 2: build the harness, in this order

Use whatever language they're comfortable with; Python with `uv` is the default. Use the `openai` client library (`OpenAI(base_url=…, api_key=…)`) or plain HTTP. **No agent frameworks**: no LangChain, OpenAI Agents SDK, Claude Agent SDK or similar. Writing the loop is the homework.

After each step, run it, show the student, and explain what changed.

1. **One call.** Send a system prompt and one user message; print the reply and the `usage` numbers (prompt tokens, cached tokens if `prompt_tokens_details.cached_tokens` is present, completion tokens). Keep the system prompt in its own file, `system_prompt.md`, so they can edit it.
2. **A conversation.** A list of messages that grows with each turn, resent in full on every call. Point out that this is "every call resends everything" from class.
3. **The `bash` tool.** One JSON-schema tool definition: name `bash`, one required string parameter `command`, and a description that tells the model what it's for. Its implementation runs the command in a working folder with a time limit (e.g. 60 s), captures stdout and stderr, returns them with the exit code, and keeps only the last ~10,000 characters of long output. On Windows, run commands through PowerShell (or WSL bash) and say so in the tool's description.
4. **The loop.** Call the model with the tool. If the reply has `tool_calls`, run each, append a `tool` message with the matching `tool_call_id`, and call again. If it's plain text, show it and wait for the next message. Cap tool rounds per question (e.g. 20) so a confused model can't loop forever. **CHECKPOINT:** show the student the loop in the code and have them explain it back to you in their own words; fill in what they miss.
5. **Ask before running.** Before each command, show it and ask yes or no. On no, return "The user declined to run this command." as the tool result. Keep this on by default; an "approve everything" switch is fine if it's off by default.
6. **The interface.** A local web page (recommended), served on `127.0.0.1` only: a chat box, the model's replies, each command with Approve and Deny buttons, its output, and the token counts per call. Or a terminal chat, which is equally fine. Let the student choose. **CHECKPOINT** on how it looks.

Then add a short `README.md` (what it is, how to run it) and a license (MIT unless they prefer another).

## Step 3: test

Try together, with the approval prompt on:
- "What files are in this folder?" (one tool call)
- "How much free disk space do I have, and which folder in my home directory is biggest?" (several calls in a row)
- A command that fails, e.g. "Run the program `doesnotexist`": the model should see the error and recover.
- Deny a command and see what the model does.
- Watch the token counts grow across turns, and the cached count when the provider reports it.

Fix what breaks. Commit as you go, with plain messages.

## Step 4: publish the harness

1. Check what will become public: `git status`, `git log --stat`, and search the repository for keys (`git grep -n -I -e "sk-" -e "API_KEY="` should show only `.env.example` placeholders). `.env` must not be tracked.
2. **CHECKPOINT:** the student agrees to publish. **(student does this, or you run it once they say yes)** `gh repo create <harness-name> --public --source . --push`.

## Step 5: the install skill and the pull request

1. Create the branch `week-2-<github-username>` in their clone of the homework repository, using their fork (`gh repo fork --remote` if they don't have one yet).
2. Write `week-2/submissions/<github-username>/SKILL.md`, a skill for an AI agent:

   ```markdown
   ---
   name: <harness-name>
   description: Install and run <harness-name>, <their name>'s agent harness (AI in Research, week 2): <one line on what it is and its interface>.
   ---
   # <harness-name>

   Repository: https://github.com/<github-username>/<harness-name>

   ## Install
   ## Configure (BASE_URL, API_KEY, MODEL; never commit .env)
   ## Run
   ## Check that it works (one question that makes it call bash, and what the user should see)
   ```

   Every command an agent needs, for macOS, Linux and Windows where they differ.
3. **Test the skill:** clone their public repository into a fresh temporary folder, follow the skill exactly as written, and fix the skill (or the harness) where it breaks. Then delete the temporary folder.
4. Commit only that file, push the branch, and open the pull request with `gh pr create`. The description says which AI helped them, and how. **CHECKPOINT** before opening it.

The class's CI only accepts changes under `week-2/submissions/<their-username>/`.

## Before ending any session

Say where things stand and what's next, in two sentences. If the work isn't finished, write that note in the harness repository's `README.md` under a "Status" heading, so the next session can pick it up.
