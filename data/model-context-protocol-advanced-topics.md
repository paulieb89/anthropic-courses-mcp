# Model Context Protocol: Advanced Topics

## Source

https://anthropic.skilljar.com/model-context-protocol-advanced-topics

## Contents

- [Let's get started!](#lets-get-started)
- [Sampling](#sampling)
- [Sampling walkthrough](#sampling-walkthrough)
- [Log and progress notifications](#log-and-progress-notifications)
- [Notifications walkthrough](#notifications-walkthrough)
- [Roots](#roots)
- [Roots walkthrough](#roots-walkthrough)
- [Survey](#survey)
- [JSON message types](#json-message-types)
- [The STDIO transport](#the-stdio-transport)
- [The StreamableHTTP transport](#the-streamablehttp-transport)
- [StreamableHTTP in depth](#streamablehttp-in-depth)
- [State and the StreamableHTTP transport](#state-and-the-streamablehttp-transport)
- [Assessment on MCP concepts](#assessment-on-mcp-concepts)
- [Wrapping up](#wrapping-up)

## Let's get started!

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296349

This course covers the technical implementation of MCP servers and clients, from basic message passing to production deployment strategies. You'll learn how MCP enables language models like Claude to interact with external tools and data sources through standardized protocols, transports, and message formats.

## Sampling

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296288

Sampling = technique allowing MCP servers to request language model text generation from clients instead of directly accessing LLMs themselves.

Purpose = shifts LLM access responsibility from server to client, avoiding need for servers to handle API keys, authentication, or token costs.

Architecture = Server creates message request → Client receives via sampling callback → Client calls LLM → Client returns generated text to server.

Benefits = eliminates server complexity for LLM integration, removes API key requirements from servers, prevents unauthorized token usage on public servers.

Implementation = Server uses create_message() function with message list, Client implements sampling callback to handle LLM requests and return create_message_result.

Primary use case = publicly accessible MCP servers that need LLM capabilities without direct LLM access or associated costs/security concerns.

## Sampling walkthrough

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295172

← Previous Next →

## Log and progress notifications

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296284

Log and Progress Notifications = MCP server feature that provides real-time feedback during tool execution to improve user experience.

Implementation on server side:
- Tool functions automatically receive context argument as last parameter
- Context object provides methods: info() for logging, report_progress() for progress updates
- Calling these methods automatically sends messages back to client

Implementation on client side:
- Create callback function for logging statements
- Create separate callback for progress updates
- Pass logging callback to client session
- Pass progress callback to call_tool function
- Callbacks handle how to display information to user (terminal output, web UI, etc.)

Key benefits:
- Prevents user confusion about stalled/failed tool calls
- Provides visibility into long-running operations
- Real-time feedback during tool execution

Optional feature = can be omitted if not needed, purely for UX enhancement.

## Notifications walkthrough

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/291036

← Previous Next →

## Roots

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296289

MCP Roots = codified way for users to grant server access to specific files/folders

Problem without roots: User says "convert bikin.mp4" but Claude can't locate file in complex filesystem without full path. Requiring full paths inconvenient for users.

Solution with roots: Add 3 tools to MCP server:
- ConvertVideo (original tool)
- ReadDirectory (lists files/folders in directory)  
- ListRoots (returns available roots)

Root = file/folder user grants permission to access beforehand (via command line args when starting server)

Implementation requirement: Tools must check that accessed files/folders are contained within granted roots using function like is_path_allowed()

Two main benefits:
1. Permission control - limits server access to authorized areas only
2. Autonomous discovery - Claude can search through available roots to find files without user providing full paths

Key limitation: MCP SDK doesn't automatically enforce root restrictions. Server developer must implement access checks manually.

ListRoots tool optional - can alternatively include root list in prompt directly. Tool pattern allows Claude to dynamically check available roots when needed.

## Roots walkthrough

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/295839

← Previous Next →

## Survey

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/297276

Interactive survey content was not embedded in the saved course HTML.

## JSON message types

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296290

JSON Message Types in MCP:

MCP communication = JSON messages between clients and servers. Each message type has distinct purpose.

Message categories:
- Request/Result pairs = Always come together (call_tool_request + call_tool_result, initialize_request + initialize_result)
- Notifications = Events that don't need responses (progress_notification, logging_message_notification, tool_change_notification)

Message direction classification:
- Client messages = Sent by MCP client to server
- Server messages = Sent by MCP server to client

Key insight: Servers can send messages TO clients (server requests, server notifications). This directional capability becomes critical limitation in streamable HTTP transport.

Schema definition = TypeScript file in MCP spec repository (schema.ts). Not executable code, just type descriptions for convenience.

Message structure = JSON-RPC format with method, params, ID fields.

## The STDIO transport

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296291

MCP Transport = mechanism for moving JSON messages between client and server

Stdio Transport = transport where client launches server as separate process, communicates via standard input/output streams

Communication mechanism: Client writes to server's stdin, reads from server's stdout. Server writes to stdout, reads from stdin.

Advantages: Bidirectional communication - either client or server can initiate requests at any time

Limitations: Only works when client and server run on same physical machine

Message exchange patterns:
- Client-to-server request: Write to stdin, read response from stdout
- Server-to-client request: Server writes to stdout, client responds via stdin

Required initialization sequence:
1. Initialize request (client to server)
2. Initialize result (server to client) 
3. Initialize notification (client to server, no response required)

Message types:
- Requests = expect responses
- Notifications = no response required
- Results = responses to requests

Key characteristic: Full bidirectional communication support - both parties can initiate requests

Contrast with HTTP transport: HTTP transport has limitations on server-initiated requests that stdio transport doesn't have

## The StreamableHTTP transport

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296287

StreamableHTTP Transport = MCP transport enabling client-server communication over HTTP connections, allows remote server hosting unlike standard I/O transport which requires same-machine operation.

Key advantage = Remote hosting capability - servers can be publicly accessible at URLs like mcpserver.com, expanding MCP server possibilities.

Critical limitation = Restricted server-to-client messaging functionality due to HTTP's unidirectional nature - clients easily request from servers, but servers cannot easily initiate requests to clients.

Two key settings impact functionality:
- stateless HTTP (default: false)
- JSON response (default: false)

Setting these to true = Reduced functionality, breaks progress bars, logging notifications, progress notifications, and sampling requests.

HTTP communication constraint = Server doesn't know client address and client may not be publicly accessible, making server-initiated requests challenging.

Affected message types when using HTTP = Sampling requests, listing routes, progress notifications, logging notifications - all require server-to-client communication.

Common deployment issue = Application works fine locally with standard I/O transport but fails when deployed with HTTP transport due to these messaging restrictions.

Solution exists = StreamableHTTP transport has workarounds for server-to-client communication challenges, but with caveats.

## StreamableHTTP in depth

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296286

StreamableHTTP Transport = HTTP-based MCP transport using server-sent events (SSE) to enable server-to-client communication

Core Problem: MCP requires server-to-client requests (sampling, notifications, logging) but HTTP naturally supports only client-to-server requests

Workaround Solution: Uses SSE connections to allow server streaming messages to client

Session ID = Random identifier assigned during initialization, included in all subsequent requests as HTTP header

Initialization Flow:
1. Client sends initialize request
2. Server responds with result + MCP session ID header
3. Client sends initialized notification with session ID
4. Client optionally makes GET request with session ID to establish SSE connection

Two SSE Connections:
1. Long-lived SSE connection = For server-initiated requests (sampling, notifications)
2. Short-lived SSE connection = For specific tool call responses, automatically closed after result

Message Routing:
- Progress notifications → Long-lived SSE connection
- Logging messages + tool results → Short-lived SSE connection tied to specific request

Key Limitation: Setting certain flags to true breaks the workaround, making StreamableHTTP complex to understand and use properly

Critical Point: SSE responses enable bidirectional communication over HTTP by keeping connections open and streaming individual messages from server to client

## State and the StreamableHTTP transport

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296285

**Stateless HTTP Flag**

Stateless HTTP = flag set to true when MCP server needs horizontal scaling across multiple instances with load balancer

**Why needed**: Single server instance can't handle high traffic. Horizontal scaling uses multiple server copies + load balancer routing requests randomly.

**Problem without stateless**: Client needs 2 connections (GET SSE for server-to-client requests, POST for client-to-server). Load balancer may route these to different server instances. If tool on Server A needs sampling request, it must go through GET SSE connection on Server B - requires complex coordination.

**Effect of stateless=true**:
- No session IDs assigned to clients
- Server cannot track individual clients
- GET SSE response pathway disabled (server cannot send requests to client)
- Eliminates sampling, progress logging, resource subscriptions
- No client initialization required (skips initialize request + notification)
- Reduces server traffic

**JSON Response Flag**

JSON response = flag disabling streaming responses on POST requests

**Effect of JSON response=true**:
- POST responses return final result as plain JSON only
- No intermediate streaming messages
- No progress/log statements during execution
- Client waits for complete tool execution before receiving response

**Key Takeaway**: Both flags significantly change server behavior. Use same transport in development as planned for production to avoid deployment issues.

## Assessment on MCP concepts

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296301

Interactive assessment content was not embedded in the saved course HTML.

## Wrapping up

Source: https://anthropic.skilljar.com/model-context-protocol-advanced-topics/296350

Closing lesson text was not embedded in the saved course HTML.
