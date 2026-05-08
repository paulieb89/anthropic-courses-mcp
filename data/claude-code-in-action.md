# Claude Code in Action

## Source

https://anthropic.skilljar.com/claude-code-in-action

## Contents

- [Introduction](#introduction)
- [What is a coding assistant?](#what-is-a-coding-assistant)
- [Claude Code in action](#claude-code-in-action)
- [Claude Code setup](#claude-code-setup)
- [Project setup](#project-setup)
- [Adding context](#adding-context)
- [Making changes](#making-changes)
- [Course satisfaction survey](#course-satisfaction-survey)
- [Controlling context](#controlling-context)
- [Custom commands](#custom-commands)
- [MCP servers with Claude Code](#mcp-servers-with-claude-code)
- [Github integration](#github-integration)
- [Introducing hooks](#introducing-hooks)
- [Defining hooks](#defining-hooks)
- [Implementing a hook](#implementing-a-hook)
- [Gotchas around hooks](#gotchas-around-hooks)
- [Useful hooks!](#useful-hooks)
- [Another useful hook](#another-useful-hook)
- [The Claude Code SDK](#the-claude-code-sdk)
- [Quiz on Claude Code](#quiz-on-claude-code)
- [Summary and next steps](#summary-and-next-steps)

## Introduction

Source: https://anthropic.skilljar.com/claude-code-in-action/303233

This course provides comprehensive training on using Claude Code for software development tasks, covering the underlying architecture of AI coding assistants, practical implementation techniques, and advanced integration strategies. You'll learn about Claude Code's context management approaches, and how to extend functionality through MCP servers and GitHub integration.

What you'll learn

- Understand coding assistant architecture: Learn how AI assistants interact with codebases through tool integration and the technical foundations that enable code analysis and modification
- Explore Claude Code's tool use system: Discover how to leverage multiple tools in combination to handle complex, multi-step programming tasks across various development scenarios
- Master context management techniques: Learn strategies for maintaining relevant context throughout conversations and effectively referencing project resources for optimal AI assistance
- Implement visual communication workflows: Understand how to use visual inputs to communicate interface changes and leverage advanced planning features for complex codebase modifications
- Create custom automation: Explore how to build reusable custom commands and automations that streamline repetitive development tasks
- Extend functionality with MCP servers: Learn to integrate external tools and services for enhanced capabilities like browser automation and specialized development workflows
- Integrate with GitHub workflows: Understand how to set up automated code review processes and integrate AI assistance into your existing version control workflows
- Apply thinking and planning modes: Learn when and how to use different reasoning approaches for various complexity levels of programming challenges

Prerequisites

- Familiarity with command-line interfaces and terminal operations
- Basic understanding of version control with Git

Who this course is for

- Software developers looking to integrate AI assistance into their coding workflows
- Teams seeking to implement AI-powered GitHub integration for multiple workflows

## What is a coding assistant?

Source: https://anthropic.skilljar.com/claude-code-in-action/303235

Coding Assistant = tool that uses language models to write code and complete development tasks

Core Process:
1. Receives task (e.g., fix bug from error message)
2. Language model gathers context (reads files, understands codebase)
3. Formulates plan to solve issue
4. Takes action (updates files, runs tests)

Key Limitation: Language models only process text input/output - cannot directly read files, run commands, or interact with external systems.

Tool Use System = method enabling language models to perform actions:
- Assistant appends instructions to user request
- Instructions specify formatted responses for actions (e.g., "read file: filename")
- Language model responds with formatted action request
- Assistant executes actual action (reads file, runs command)
- Results sent back to language model for final response

Claude Models Advantage:
- Superior tool use capabilities vs other language models
- Better at understanding tool functions and combining them for complex tasks
- Claude Code is extensible - easy to add new tools
- Better security through direct code search vs indexing that sends codebase to external servers

Essential Points:
- All language models require tool use for non-text generation tasks
- Tool use quality directly impacts coding assistant effectiveness
- Claude's strength in tool use makes it adaptable to development changes

## Claude Code in action

Source: https://anthropic.skilljar.com/claude-code-in-action/303242

Claude Code = AI assistant with tool-based capabilities for code tasks

Default tools = file reading/writing, command execution, basic development operations

Performance optimization demo: Claude analyzed Chalk JavaScript library (5th most downloaded JS package, 429M weekly downloads). Used benchmarks, profiling tools, created todo lists, identified bottlenecks, implemented fixes. Result = 3.9x throughput improvement.

Data analysis demo: Claude performed churn analysis on video streaming platform CSV data using Jupyter notebooks. Executed code cells iteratively, viewed results, customized successive analyses based on findings.

Tool extensibility: Claude Code accepts new tool sets. Example used Playwright MCP server for browser automation. Claude opened browser, took screenshots, updated UI styling, iterated on design improvements.

GitHub integration: Claude Code runs in GitHub Actions, triggered by pull requests/issues. Gets GitHub-specific tools (comments, commits, PR creation). 

Infrastructure review example: Terraform-defined AWS infrastructure with DynamoDB table and S3 bucket shared with external partner. Developer added user email to Lambda function output. Claude Code automatically detected PII exposure risk in pull request review by analyzing infrastructure flow and identifying external data sharing.

Key principle: Claude Code = flexible assistant that grows with team needs through tool expansion rather than fixed functionality.

## Claude Code setup

Source: https://anthropic.skilljar.com/claude-code-in-action/301614

**Time to get Claude Code set up locally!**

 Full setup directions can be found here: [https://code.claude.com/docs/en/quickstart](https://code.claude.com/docs/en/quickstart)

 In short, you'll need to do the following:

 1. `Install Claude Code`  `MacOS (Homebrew): `brew install --cask claude-code`` MacOS, Linux, WSL: `curl -fsSL https://claude.ai/install.sh | bash` Windows CMD: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
2. After installation, run `claude` at your terminal. The first time you run this command you will be prompted to authenticate

 If you're making use of AWS Bedrock or Google Cloud Vertex, there is some additional setup:

 - Special directions for AWS Bedrock: [https://code.claude.com/docs/en/amazon-bedrock](https://code.claude.com/docs/en/amazon-bedrock)
- Special directions for Google Cloud Vertex: [https://code.claude.com/docs/en/google-vertex-ai](https://code.claude.com/docs/en/google-vertex-ai)

## Project setup

Source: https://anthropic.skilljar.com/claude-code-in-action/301615

Working with Claude Code is more interesting if you have a project to work with.

 I've put together a small project to explore with Claude Code. It is the same UI generation app shown in a previous video. **Note:** you don't have to run this project. You can always follow along with the remainder of the course with your own code base if you wish!

 **Setup**

 This project requires a small amount of setup:

 1. Ensure you have Node JS installed locally. [Link to installation directions](https://nodejs.org/en/download).
2. Download the zip file called `uigen.zip` attached to this lecture and extract it
3. In the project directory, run `npm run setup` to install dependencies and set up a local SQLite database
4. **Optional:**this project uses Claude through the Anthropic API to generate UI components. If you want to fully test out the app, you will need to provide an API key to access the Anthropic API. *This is optional. If no API key is provided, the app will still generate some static fake code.*Here's how you can set the api key:  Get an Anthropic API key at [https://console.anthropic.com/](https://console.anthropic.com/) Place your API key in the `.env` file.
5. Start the project by running `npm run dev`

## Adding context

Source: https://anthropic.skilljar.com/claude-code-in-action/303241

Context management = critical for Claude Code effectiveness. Too much irrelevant info decreases performance.

/init command = analyzes entire codebase on first run, creates Claude.md file with project summary/architecture/key files. File contents included in every request.

Three Claude.md file types:
- Project level = shared with team, committed to source control
- Local level = personal instructions, not committed  
- Machine level = global instructions for all projects

Memory mode (# symbol) = edit Claude.md files intelligently with natural language requests

@ symbol = mention specific files to include in requests, provides targeted context instead of letting Claude search

Best practice = reference critical files (like database schemas) in Claude.md so they're always available as context

Goal = provide just enough relevant information for Claude to complete tasks effectively

## Making changes

Source: https://anthropic.skilljar.com/claude-code-in-action/303236

Claude Code Change Management:

Screenshot integration = Control-V (not Command-V on macOS) pastes screenshots to help Claude understand specific UI elements to modify

Performance boosting modes:
- Plan Mode = Shift + Tab twice, makes Claude research more files and create detailed implementation plans before executing
- Thinking Mode = triggered by phrases like "Ultra think", gives Claude extended reasoning budget for complex logic

Planning vs Thinking usage:
- Planning = handles breadth, useful for multi-step tasks requiring wide codebase understanding
- Thinking = handles depth, useful for tricky logic or debugging specific issues
- Can be combined for complex tasks
- Both consume additional tokens (cost consideration)

Git integration = Claude Code can stage/commit changes and write descriptive commit messages

Key workflow: Screenshot problematic area → paste with Control-V → describe desired change → optionally enable Plan/Thinking modes for complex tasks → review and accept implementation

## Course satisfaction survey

Source: https://anthropic.skilljar.com/claude-code-in-action/303701

Interactive survey content was not embedded in the saved course HTML.

## Controlling context

Source: https://anthropic.skilljar.com/claude-code-in-action/303237

Context Control Techniques:

Escape = Stops Claude mid-response to redirect conversation flow. Press once to interrupt current output.

Escape + Memory = Powerful error prevention. Stop Claude, add memory about repeated mistakes using # shortcut to prevent future occurrences.

Double Escape = Conversation rewind. Shows all previous messages, allows jumping back to earlier point while maintaining relevant context and skipping irrelevant debugging/back-and-forth.

Compact Command = Summarizes entire conversation history while preserving Claude's learned knowledge about current task. Use when Claude has gained expertise but conversation has accumulated clutter.

Clear Command = Deletes entire conversation history for fresh start. Use when switching to completely unrelated tasks.

Key Benefits: Maintains focus, reduces distracting context, preserves relevant knowledge, prevents repeated errors. Most effective for long conversations and task transitions.

## Custom commands

Source: https://anthropic.skilljar.com/claude-code-in-action/303234

Custom Commands = user-defined automation commands in Claude Code accessed via forward slash

Location = .Claude/commands/ folder in project directory
File naming = filename becomes command name (audit.md creates /audit command)
Activation = restart Claude Code after creating command files

Command structure = markdown file containing instructions for Claude to execute
Arguments = use $arguments placeholder in command text to accept runtime parameters
Argument types = any string (file paths, descriptive text, etc.)

Use cases = automating repetitive tasks like dependency auditing, test generation, vulnerability fixes
Execution = /commandname in Claude Code interface, optionally followed by argument string

## MCP servers with Claude Code

Source: https://anthropic.skilljar.com/claude-code-in-action/303239

MCP servers = external tools that extend Claude Code capabilities, run locally or remotely.

Playwright MCP server = popular server enabling Claude to control browsers for web automation.

Installation: Terminal command \`claude mcp add [name] [start-command]\` adds MCP server to Claude Code.

Permission management: Initial tool usage requires approval. Auto-approve by adding "MCP__[servername]" to settings.local.json allow array.

Practical example: Claude used Playwright to navigate localhost:3000, generate UI component, analyze styling quality, then automatically update generation prompts based on visual feedback.

Results: Automated prompt refinement produced significantly better component styling, demonstrating MCP servers unlock sophisticated development workflows.

Key benefit: MCP servers enable Claude to perform complex multi-step tasks involving external systems, expanding beyond code editing to full development automation.

## Github integration

Source: https://anthropic.skilljar.com/claude-code-in-action/303240

Claude Code GitHub Integration = official integration allowing Claude to run inside GitHub actions

Setup Process:
- Run "/install GitHub app" command
- Install Claude Code app on GitHub
- Add API key
- Auto-generated pull request adds two GitHub actions

Default Actions:
1. Mention support = @Claude in issues/PRs to assign tasks
2. PR review = automatic code review on new pull requests

Customization:
- Actions are customizable via config files in .github/workflows directory
- Custom instructions = direct context/directions passed to Claude
- MCP server integration = allows Claude to access external tools (like Playwright for browser automation)

Permission Requirements:
- Must explicitly list all permissions for Claude Code in actions
- MCP server tools require individual permission listing (no shortcuts)

Example Use Case:
- Integrated Playwright MCP server for browser testing
- Development server setup before Claude runs
- Claude can visit app in browser, test functionality, create checklists
- Provides automated testing and issue verification

Key Features = mention-based task assignment, automated PR reviews, customizable workflows, MCP server integration for extended functionality

## Introducing hooks

Source: https://anthropic.skilljar.com/claude-code-in-action/312000

Hooks = commands that run before/after Claude executes tools

Pre-tool use hooks = run before tool execution, can inspect and block tool operations, send error messages to Claude
Post-tool use hooks = run after tool execution, perform follow-up operations, provide feedback to Claude

Configuration = added to Claude settings file (global/project/personal) via manual editing or /hooks command

Hook structure = two sections (pre-tool use, post-tool use), each with matcher (specifies which tools to target) and commands to execute

Example uses = auto-format files after creation, run tests after edits, block file access, code quality checks, type checking

Hook commands = receive tool call details, can modify Claude's workflow through blocking or feedback mechanisms

## Defining hooks

Source: https://anthropic.skilljar.com/claude-code-in-action/312002

**Hooks Overview**
Hooks = mechanisms to intercept and control tool calls before/after execution

**Hook Types**
Pre-tool use hook = executes before tool call, can block execution
Post-tool use hook = executes after tool call, cannot block execution

**Hook Implementation Process**
1. Choose hook type (pre vs post)
2. Identify target tool names to monitor
3. Write command to receive tool call data via stdin as JSON
4. Parse JSON containing tool_name and input parameters
5. Exit with appropriate code to signal intent

**Exit Codes**
Exit 0 = allow tool call to proceed
Exit 2 = block tool call (pre-tool use only)
Standard error output = feedback message sent to Claude when blocking

**Tool Call Data Structure**
JSON object containing:
- tool_name (e.g., "read", "grep")
- input parameters (e.g., file_path)

**Common Use Case**
Blocking file access by monitoring "read" and "grep" tools that can access file contents

**Tool Discovery**
Ask Claude directly for list of available tool names rather than memorizing them

Hooks = mechanisms to control Claude's tool usage by running custom commands before/after tool calls

Pre-tool use hook = executes before tool call, can block with exit code 2
Post-tool use hook = executes after tool call, cannot block

Hook process:
1. Claude sends tool call data as JSON via stdin to your command
2. Command parses JSON containing tool_name and input arguments  
3. Command exits with code 0 (allow) or 2 (block for pre-hooks only)
4. Exit code 2 sends stderr output as feedback to Claude

Tool call data format = JSON object with tool name and input parameters

Common tools that read files = "read" tool and "grep" tool

Hook use case example = blocking Claude from reading sensitive .env file by watching for read/grep tools targeting that file path

Setup = define command in project, Claude automatically executes it when relevant tool calls occur

## Implementing a hook

Source: https://anthropic.skilljar.com/claude-code-in-action/312003

**Custom Hook Implementation**

Hook purpose = prevent Claude from reading .env file contents

**Configuration Setup**
- Location = .clod/settings.local.json
- Hook type = pre-tool use hook (blocks before execution)
- Matcher = "read|grep" (pipe symbol separates tool names)
- Command = "node ./hooks/read_hook.js"

**Implementation Details**
- Hook receives JSON object via stdin containing: session ID, tool name, tool input, file path
- Logic: if file path includes ".env" → exit with code 2 + log error to stderr
- Error output goes to stderr for Claude feedback
- Exit code 2 = blocked operation

**Key Requirements**
- Must restart Claude after hook changes
- Console.error() sends feedback to Claude via stderr
- Hook works for both read and grep tools
- File path checking: tool_input.path with fallback handling

**Testing Results**
- Successfully blocks .env file access
- Claude recognizes prevention by read hook
- Works for both read and grep operations

**Hook Implementation Process:**

Hook = custom script that intercepts and controls tool usage in Clod

**Configuration (settings.local.json):**
- Pre-tool use hooks = run before tool execution
- Post-tool use hooks = run after tool execution
- Matcher = specifies which tools to intercept (e.g., "read|grep")
- Command = script to execute when matched tools are called

**Implementation Steps:**
1. Add hook config to settings.local.json with matcher and command
2. Create hook script (e.g., read_hook.js) that receives JSON input via stdin
3. JSON input contains: session ID, tool name, tool input, file path
4. Script logic: check if file path includes ".env"
5. If blocked file detected: console.error() message + process.exit(2)
6. Exit code 2 = blocks tool execution

**Key Technical Details:**
- Hook script receives tool data as JSON from stdin
- Use console.error() to send feedback to Clod (logs to stderr)
- Must restart Clod after hook changes
- Hook applies to all specified tools (read, grep, etc.)
- Fallback path checking via tool_input.path for compatibility

**Result:** Successfully prevents Clod from reading .env files while providing user feedback about blocked operations.

## Gotchas around hooks

Source: https://anthropic.skilljar.com/claude-code-in-action/312423

You may notice that after running the `npm run dev` command there are two `settings.json` files in the `.claude` directory. Let me explain what's going on there.

 The Claude Code documentation lists some recommendations around hooks security:

  One of the recommendations is to use absolute paths (rather than relative paths) for scripts. This helps mitigate [path interception](https://attack.mitre.org/techniques/T1574/007/) and [binary planting](https://owasp.org/www-community/attacks/Binary_planting) attacks.

 This recommendation also makes it much more challenging to share `settings.json` files. The reason is simple: the absolute path to any of the hook scripts on **your** machine will likely be different from the absolute **path** on my machine, simply because we will probably place the project in separate directories.

 To solve this problem, our project has a `settings.example.json` file. Inside of it, the script references contain a `$PWD` placeholder. When we run `npm run setup`, some dependencies are installed, but it also runs an `init-claude.js` script placed inside the scripts directory. This script will replace those `$PWD` placeholder with the absolute path to the project on your machine, copy the `settings.example.json` file, and rename it to `settings.local.json`.

 This script allows us to share settings.json files but still use the recommended absolute paths!

## Useful hooks!

Source: https://anthropic.skilljar.com/claude-code-in-action/312004

**Useful Hooks for Claude Code Projects**

**Problem**: Claude Code often misses type errors and creates duplicate code, especially in larger projects.

**Hook 1: TypeScript Type Checker Hook**
- **Purpose**: Catch type errors immediately after file edits
- **Implementation**: Run \`tsc --no-emit\` after TypeScript file changes via post-tool-use hook
- **Process**: Detects type errors → feeds errors back to Claude → Claude fixes call sites automatically
- **Benefits**: Prevents broken function calls when signatures change
- **Adaptable**: Works for any typed language with type checker, or use tests for untyped languages

**Hook 2: Duplicate Code Prevention Hook**
- **Problem**: Claude creates new queries/functions instead of reusing existing ones, especially in complex tasks
- **Solution**: Launch separate Claude instance to review changes in specific directories (e.g., queries folder)
- **Process**: 
  1. Detect edits to watched directory
  2. Launch new Claude instance via TypeScript SDK
  3. Compare new code against existing code
  4. If duplicate found, exit with code 2 + feedback
  5. Original Claude receives feedback and reuses existing code
- **Trade-offs**: Extra time/cost vs cleaner codebase
- **Recommendation**: Only watch critical directories to minimize overhead

**Key Takeaway**: Hooks = automated feedback loops that catch common Claude Code weaknesses (type errors, code duplication) by running additional checks and feeding results back to Claude for self-correction.

## Another useful hook

Source: https://anthropic.skilljar.com/claude-code-in-action/312427

There are more hooks beyond the `PreToolUse` and `PostToolUse` hooks discussed in this course. There are also:

 - `Notification` - Runs when Claude Code sends a notification, which occurs when Claude needs permission to use a tool, or after Claude Code has been idle for 60 seconds
- `Stop` - Runs when Claude Code has finished responding
- `SubagentStop` - Runs when a subagent (these are displayed as a "Task" in the UI) has finished
- `PreCompact` - Runs before a compact operation occurs, either manual or automatic
- `UserPromptSubmit` - Runs when the user submits a prompt, before Claude processes it
- `SessionStart` - Runs when starting or resuming a session
- `SessionEnd` - Runs when a session ends

 **Here's the confusing part:**

 1. The stdin input to your commands will change based upon the type of hook being executed (`PreToolUse`, `PostToolUse`, `Notification`, etc)
2. The `tool_input` contained in that will differ based upon the tool that was called (in the case of `PreToolUse` and `PostToolUse` hooks)

 For example, here's a sample of some stdin input to a hook, where the hook is a `PostToolUse` that was watching for uses of the `TodoWrite` tool. For reference, that is the tool that Claude uses to keep track of to-do items.

 ```
{
  "session_id": "9ecf22fa-edf8-4332-ae85-b6d5456eda64",
  "transcript_path": "<path_to_transcript>",
  "hook_event_name": "PostToolUse",
  "tool_name": "TodoWrite",
  "tool_input": {
    "todos": [{ "content": "write a readme", "status": "pending", "priority": "medium", "id": "1" }]
  },
  "tool_response": {
    "oldTodos": [],
    "newTodos": [{ "content": "write a readme", "status": "pending", "priority": "medium", "id": "1" }]
  }
}
```

 And for comparison, here's an example of the input to a `Stop` hook:

 ```
{
  "session_id": "af9f50b6-f042-4773-b3e2-c3a4814765ce",
  "transcript_path": "<path_to_transcript>",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

 **As you can see, the stdin input to your command will differ significantly based upon the hook (`PreToolUse`, `PostToolUse`, `Stop`, etc) *and* the matcher used (in the case of `PreToolUse` and `PostToolUse`). This can make writing hooks challenging - you might not know the exact structure of the input to your command!**

 To handle this challenge, try making a helper hook like this:

 ```
"PostToolUse": [ // Or "PreToolUse" or "Stop", etc
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "jq . > post-log.json"
      }
    ]
  },
]
```

 Notice the provided command. It will write the input to this hook to the `post-log.json` file, which allows you to inspect exactly what would have been fed into your command! **This makes it a lot easier for you to understand what data your command should inspect.**

## The Claude Code SDK

Source: https://anthropic.skilljar.com/claude-code-in-action/312001

Claude Code SDK = programmatic interface for Claude Code with CLI, TypeScript, and Python libraries. Contains same tools as terminal version.

Primary use case = integration into larger pipelines/workflows to add intelligence to existing processes.

Default permissions = read-only (files, directories, grep operations). Write permissions require manual configuration via options.allowTools array or .Claude directory settings.

SDK execution shows raw conversation between local Claude Code and language model, with final response as last message.

Key implementation pattern = add write permissions by specifying tools like "edit" in options.allowTools when making query calls.

Best suited for = helper commands, scripts, and hooks within existing projects rather than standalone usage.

Claude Code SDK = programmatic interface to use Claude Code via CLI, TypeScript, or Python libraries. Same tools as terminal version.

Primary use case = integration into larger pipelines/workflows to add intelligence to processes.

Key characteristics:
- Default permissions = read-only (files, directories, grep operations)
- Write permissions = must be manually enabled via query options or settings file
- Raw conversation output = shows message-by-message exchange between local Claude Code and language model

Best applications = helper commands, scripts, hooks within existing projects rather than standalone use.

Output format = conversational messages with final response from Claude as last message.

## Quiz on Claude Code

Source: https://anthropic.skilljar.com/claude-code-in-action/308391

Interactive quiz content was not embedded in the saved course HTML.

## Summary and next steps

Source: https://anthropic.skilljar.com/claude-code-in-action/303238

This closing lesson was not embedded in the saved Skilljar page, so the original export only captured a video placeholder. The summary below is reconstructed from the course overview and the lesson notes embedded for the rest of the course.

Key takeaways:
- Claude Code is a tool-using coding assistant, so good results depend on giving it the right context, permissions, and feedback loops.
- Setup matters: start from a working local environment, use a real project, and make Claude aware of important files and conventions.
- Context control matters as much as raw model capability. Use `/init`, `Claude.md`, `@` mentions, compacting, and conversation resets to keep the model focused.
- For harder changes, combine screenshots, planning, and deeper reasoning modes so Claude can inspect the codebase broadly before it edits.
- Custom commands, hooks, MCP servers, GitHub Actions, and the SDK all extend Claude Code beyond the default terminal workflow.
- Hooks and follow-up checks are useful because they catch the errors Claude is most likely to make, such as broken types, duplicate code, or unsafe file access.

Practical next steps:
- Try Claude Code on a repository you know well enough to review critically.
- Add lightweight project instructions in `Claude.md` before handing it larger tasks.
- Start with narrow workflows such as setup help, targeted edits, tests, or reviews, then expand into MCP, hooks, and GitHub automation once the basics are reliable.
- Treat the SDK and hook system as ways to integrate Claude Code into existing engineering workflows instead of replacing them wholesale.
