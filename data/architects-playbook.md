ENTERPRISE LLM
ARCHITECTURE

|
|
Design Patterns, Anti-Patterns, and

System Workflows for Production
Deployments

The Architect's Playbook

Four Domains of Al Architecture

Structured Data Extraction
High Volume, Strict Schemas, Batch Pipelines

t
ey "entity": "Order",
"id": 101,
"status": "confirmed",
"items": ["A", "B°]
i

Customer Support Orchestration
Stateful, Human-in-the-Loop, Policy Constraints

& ALAGENT costes. cox
ORCHESTRATOR @ APPROVED

POLICY_VIOLATION
HUMAN REVIEWER

Developer Productivity

Dynamic Tasks, Iterative Context, Advanced
Tool Use

® project/
Bsre/
Bi components/

$> help git comuit

B package. json

ot

Multi-Agent Systems

Parallel Processing, Shared Memory,
Cross-Agent Synthesis

‘SYNTHESTS_EXCHANGE.

Nea NEHORY. we,
‘SHARED_HENORY_WRITE| = ‘SYNTHESTS_ EXCHANGE

Wa NENORY =

‘SYNTHESTS_EXCHANGE

The Architect's Hierarchy of Constraints

Mitigated by Latency
Parallelization
& Caching

Enforced by

Application-Layer / j \

Intercepts | \ Accuracy
(Not Prompts) \ \ \ 7

Mitigated by
Structured

Intermediates &
Few-Shot Prompts

Mitigated by
Batch APIs &
Context Pruning
Routing for Cost and SLA

Rule: Never default to real-time for asynchronous needs.

Incoming
Documents

SLA

Urgent Goiehe Standard
Exceptions Monthly
(< 30m SLA) Reports

Real-time
Messages API

Urgent Real-time Messages API
Exceptions (High Cost, Instant Latency)
Standard Message Batches API
Workflows (50% Cost Savings)
Continuous | Submit batches every 6 hours
Arrival containing documents from

(30h SLA)

that window.

Designing Resilient Schemas

Anti-Pattern: Fragile Expansion

Continuously expanding enums as edge cases arise.

hitectural Pattern: Resilient Catch-Alls

Add an other value to the enum, paired with a detail string field.

// Fragile Schema with Restricted Enum

"type": "object",
“properties”: {
“property_type": {
"type": string’
["house",

»

‘apartment", “condo”, “townhouse"]

quired": ["property_type"]
}

// Fails validation:
1/ “property.type'
// “property_type":

"studio"
“converted warehouse"

VALIDATION
ERROR

Unexpected Types.

// Resilient Schema with Catch-ALL

ring",

house", “apartment”, “condo”, “townhouse”, “other™]

"property_type_detail": {

“type” ae

"description": "Specifics for ‘other’ types”
}

i
“required”: [“property_type"]

VALIDATION
SUCCESS

Data Captured

// Successfully processes:
// “property type": “other”,
// “property_type_detail”: “studio

Data Evolution Rule
For amended documents, redesign schemas so amended fields capture
multiple values, each with a source location and effective date, rather than
overwriting original terms. Validate this approach against the problem of
extracting both original and amended contract clauses.

‘Original Contract, Clause 4.1", "
"iwendwent 1, Clause 2", “effective date”:

Enforcing Mathematical Consistency

The Problem: 18% of invoice extractions show line items that don't match the grand total due to OCR or extraction errors.

Line Item 1:
$120.50
(OCR error:
$120.50)

Line Item 2:
$85.00

Line Item 3: f

7) Invoice #12345
Date: 2023-10-27

Bill To:
‘Acme Corp.

Vendor:
Services Inc.

Description ‘Quantity | Unit Price | Tota

$45.25

(Extraction error:
$4,525)

[ Subtotal: $250.75 | ¢

Mismatch

Grand
Total on
Document

Schema Solution: Redundancy

{
"invoice_id
"Line_items

"12345",
[

{ "description": "Item 1", "amount":
"Item 2", "amount": 85.00 },
"Item 3", "amount": 4.525 }

{ "description
{ "description":

1,
"calculated_total": 210.025, <—

"stated_total": 260.60, <—_
"currency": "USD" a

120.50 },

Derived by model
summing items

Extracted directly
from page

The Solution: Schema Redundancy

B Routing Action: Flag the record for human review ONLY
when calculated_total != stated_total.

Normalization and Null Handling

Base Prompt

—) Null Handling Instruction

—

Format Normalization

Input:
Extract attendee count and materials.

Model Output (Problematic):

ti
“attendee_count": "566", // Plausible Hallucil
“materials”: “cotton blend" // Inconsistent F

y x

Problem: Plausible Hallucinations

When fields are nullable, models may invent
plausible data (e.g., attendee count: 500) if not
explicitly instructed.

Pattern: Add explicit prompt instructions to
return null if not directly stated.

Updated Prompt:

Extract attendee count and materials. If attendee
count or materials are not mentioned in the text,
return “null”.

Corrected Output:

{ v
“attendee_count": null, // Correctly Handled
“materials": “cotton blend"

}
Sy “a

Problem: Inconsistent Formats

For materials ("cotton blend” vs "Cotton/Polyester
mix"), provide few-shot examples showing 2-3
complete input-output pairs with standardized
formats. Do not rely on temperature 0 alone.

Soluti

Fe\

hot Standardi

Final Prompt with Examples:

Extract attendee count and materials. If not
mentioned, return "null’. Materials must be
standardized.

Examples:

Input: "Made of cotton blend." -> Output:
{\"materials": \"Cotton Blend"}

Input: "Cotton/Polyester mix” -> Output:
{\"naterials": \"Cotton/Polyester Mix"}

Final Output:

{
“attendee_count"; null, “7

“materials": “Cotton Blend" // Standardized

y

The Limits of Automated Retry

The Pattern: Appending specific validation errors to the prompt and retrying resolves
most failures in 2-3 attempts.

Q Effective: Formatting Errors X Ineffective: Missing Information

Al Al
\Generation, \Generation,

Prompt with

idati Prompt with ee seas
Error Feedback validetee rv) Error Feedback Validea a x)
Successful Max Retries
Output Exceeded

Prompt with Error
appended the ex!
error message

*< _validation
Failure

The Exception: Retries are least effective for missing
information (e.g., trying to extract full author lists when
Fixing nested objects vs flat arrays. the source says “et al.” and points to an unprovided
Resolving locale-formatted strings. external document). Recognize when to fail fast.

oe

Calibrating Human-in-the-Loop

Requirement: Implementation:
Automate extractions with model Have the model output field-lLevel confidence scores. Ground this
confidence >90%. implementation detail in the solution for reducing semantic errors.

Human Review Queue Sy Automated Downstream

0% 50% 90% 100%
Extraction Confidence Scores (0% to 100%)

ritical Validation Step: Analyze accuracy by document type and field to verify high-confidence

extractions perform consistently across all segments, not just in aggregate, before deploying.

Zero-Tolerance Compliance

The Trap: Relying on emphatic system prompts ("CRITICAL POLICY: NEVER

process >$500") still yields a 3% failure rate.

Application-
Layer
Intercept

process_refund ($847)

{e) Human
cra Escalation

The Architectural Standard:

Implement an application-layer
hook to intercept tool calls.

When the process amount
exceeds the threshold, block
it server-side and invoke
escalation.

Model discretion is removed.

Resuming Asynchronous Sessions

The Problem: Resuming a session hours later leads to the model confidently stating outdated status (e.g., "Expected

resolution: 24h" from a previous tool call).

©

Turn 1-32 (4 hours ago) Asynchronous Delay

Human Turn

*tool_result
"status": "PENDING",
“expected_resolution": "24h"}

Assistant Turn

Turn 33 (Resumption)

*tool_result® {
“status”: "PENDING",
‘pected_resolution": "24h"}

“tool_result’

‘pected_resolution": “24h"}

Assistant Turn

Human Turn Human Turn
Assistant Turn Assistant Turn
Programmatic Human Turn

Filter
Assistant Turn,

“tool_result”

“tool_result™

u

“tool_call”

The Solution: Resume with full conversation history, but programmatically filter out previous * tool_result~
messages. Keep only human/assistant turns so the agent is forced to re-fetch needed data upon resumption. This
ensures returning customers always receive fresh, current information, preventing the use of stale data.

Tool Context Pruning

The Bloat: Repeatedly calling Lookup_order fills the context window with verbose
shipping and payment data when only the return status is needed.

Application-Side Filter

Raw API Response
(40+ fields)

Pruned Context

The Pattern: Application-
side filtering.

Extract only relevant fields
(items, purchase data, return
window, status) from each
existing order response, rem-
oving verbose details before
the conversation to proceed.

This strategy aligns with
managing multiple extensive
tool responses in a support
session.

Graceful Tool Failure

User Tool Server

Tool Call (e.g., lookup_order)

a
"isError": true,
"errorCategory": "transient", ——_—_—_——=
"isRetryable": true

}

Polite Response (e.g., "I'm experiencing

a delay, please try again later.")

© Anti-Pattern: Throwing application exceptions that crash the agent, or returning empty strings. LH

© Correct Pattern: Return the error message in the tool result content with the “isError’ flag set to true. |

The Escalation Handoff

| want a human NOW. Complex Policy Issue

escalate_to_human Context Gathering

Immediate Escalation (get_customer)

Honor it immediately. Do not First ensure account context Payload Data Flow

ask for more clarification. tools are called.

The Payload: Structured Summary

Do not dump raw transcripts. Pass a structured summary: Customer ID, Root
Cause, Amount, Recommended Action.

UST-847392",

‘Duplicate charges due to gateway timeout.",

847.60 USD",

“recommended_action": "Approve refund for 847.00 USD and notify customer."

¥

Compressing Long Sessions

The Challenge: A single session covers a refund inquiry, a subscription question, and a payment
update across 48 turns. Context limits approach.

Context Window

i 8) (8) (82) (RE) (8) (a) (a) Ht

H Uy dae al] ey] gry ey tey-| gd i

H AU FUEL eu EW EL) GUE ¢ H

— a BH 3 TH EH EH GH Ss i

A PTTTT ATT ETL ATT ATT ATT A i

! r WH Nay |e I
L i L i! - i,
Narrative Summary of Resolved Issues Full Verbatim Message History Active Issue

@ The Strategy: Summarize earlier, resolved turns into a narrative description, preserving the full
message history verbatim only for the active, unresolved issue.

Correct Pattern: Return the error message in the tool result content with the ‘isError’ flag set to true.

MCP Tool Specificity

The Trap: Providing a broad custom tool (analyze_dependencies) alongside built-in tools like
Grep. The agent defaults to Grep.

Anti-Pattern: Monolithic Tool Architect's Pattern: Granular Tools
eco eco
$ Agent execution... $ Agent execution...
Agent uses built-in Grep to search imports. Agent uses custom tool for dependencies.

P +> - List_imports
{name: analyze_dependencies} +> - resolve_transitive_deps
> - detect_circular_deps

‘The Fixes |

Split broad tools into highly granular, single-purpose tools. Enhance MCP tool descriptions to
explicitly detail capabilities, expected outputs, and when to prefer them over text manipulation,
This applies similarly to adopting custom refactoring tools over standard Bash/sed.

Directed Codebase Exploration

Anti-Pattern: Using the Read tool to sequentially load thousands of lines of code.

( Search Error |
Handler
Examine
Database
Quer

2}

Middleware

Inefficient & Context-Heavy:
Overloads context window with
unrelated data.

The Strategy: Start broad,
then pinpoint.

For Architecture (New Ss
Engineer, 800+ Files):
« Read CLAUDE .md/README

first, then ask the human
engineer for priority files.

For Intermittent Bugs oo
(Tracing Errors): Q
« Have the agent dynamically

generate investigation
subtasks based on what it
discovers at each step,

adapting the plan as new
errors emerge.

Branching Reality

The Problem: Exploring two distinct refactoring approaches or testing strategies in
a single thread confuses the agent and mixes context.

Branch A: Microservice Extraction

Extract Core Define API Create
Logic Interface Microservice

R Yesterday's
-Q Analysis Branch B: In-Place Refactor

Simplify Optimize Data Refactor
Methods Flow Authentication

| The Command:

Use fork_session to create two separate branches from a foundational analysis. This allows
independent, deep exploration of A/B scenarios without context contamination.

The Scratchpad Pattern

The Decay: In extended exploration sessions (30+ mins), accumulated token bloat causes the agent to give
inconsistent answers about early discoveries. Engineers report having to repeat module information.

ee

Source File A
W "Shedte Sructure
TAPTEndpoint¥
= Decision, Use Pattern 2 Continuous Reference for
Architectural Map: Subsequent Questions
Source File B Decisions:
\
Scratchpad.md
Source File C

Raw Message History

The Pattern: Have the agent actively maintain a scratchpad file recording key findings, architectural maps, and
decisions. It references this dense, structured file for subsequent questions.

Resumption in Dynamic Environments

The Scenario: An engineer resumes an exploration session, but 3 of the 12 files the agent read yesterday have been altered by a teammate's PR.

Session Transcripts (Yesterday)

e~
Bre

P File C (Original)
Dre D (Original) Ir

(Dp ree corsn

i] File L

.” File D
(Modified)

Resumed Session (Today)

oC File A

File B
File C ay
(Modified)

an

il

Agent Context

File E
(Modified) (Updated Today)
B File L

The Action

Resume the session from its previous transcript, but explicitly inform the agent which specific files or functions changed for targeted re-

analysis. Do not force a complete re-read, and do not pretend nothing changed.

resume_session --update_context={files:['File C',

‘File D',

"File E'], changes: 'renamed utility functions'}

Shared Memory Architecture

Anti-Pattern: Daisy-chaining full conversation logs between subagents.
This scales token costs exponentially.

Shared Vector Store

The Architect's Pattern: Decouple state from invocation. Have
subagents index their outputs into a shared vector store. When

executing, subsequent agents use semantic search to retrieve only
relevant prior findings. This architecture prevents state loss when a
multi-agent pipeline crashes mid-processing.

Forcing Execution Order

UT 2r)5)(-1) An agent needs to extract metadata before calling enrichment tools, but occasionally calls enrichment

tools first, leading to failures.

{

"model": "claude-3-opus-20240229",
"max_tokens": 1024,
"messages": [
{"role": "user", "content": "Extract metadata from this paper and then look up its DOI."}
1,
THUSS [P
{"name": “extract_metadata", "description":
{"name": "Lookup_citations", "description":

1,

name": "“extract_m

}

Ue Do not rely on prompt begging. Use the API's constraints. Set tool_choice for the first API call

to guarantee the pipeline executes in the required order. This ensures structured metadata extraction
happens before any DOI lookup or enrichment.

Structured Intermediate Representations

The Loss: Passing raw text from financial and news agents to a synthesis agent
results in tables losing clarity and news losing narrative flow.

Financial

Agent (Structured JSON) Format JSON

ee - {
Conversion "claim": "
= News Layer "evidence"

Agent (Prose Summaries) Standardizes outputs to a "source":
_————————————— common intermediate "confidence": ...
Sl representation }

&9> Patent
Agent (Structured Lists)

@

— >| Synthesis Agent

Agent (Executive Briefings)

Citation Rule: To prevent lost attributions, require all subagents to output structured claim-source
mappings that the synthesis agent is instructed to preserve.

Parallelization & Caching

Serial Processi
Sequential Processing of 12 Precedents

To 1+#20s T+40s T+60s T+80s 7+100s T#120s T+140s T+160s T+180s|

The Problem: Processing each precedent sequentially in a complex legal case takes over 3 minutes, creating unacceptable latency.

Parallel Execution

Parallel Subagent [1]
Parallel Subagent [2]
Paratlet Subagent [3]
Parallel Subagent [4]

j YE Paratlet Subagent [5] c\N \ eyiece
Coordinator es, Parallel Subagent [6] y S\N

Nw Parallel Subagent [7] F (2; Prompt Caching
Parallel Subagent [8]
Parallel Subagent [9]

Parallel Subagent [3]
Paraltsl Subagent [2]

Te T+Ss T+10s TH15s, T+20s T+25s T+30s
Subagent Parallelism Prompt Caching

When processing independent data (e.g., 12 legal precedents), the When follow-up summaries consistently take 40+ seconds passing 80K+
coordinator must spawn parallel subagents, each handling a subset, then tokens of accumulated findings, enable prompt caching on the synthesis

aggregate results. subagent to drastically reduce transfer overhead.

Goal-Oriented

Delegation

The Trap: Giving a web search subagent detailed step-by-step procedural instructions causes it to fail rigidly
on emerging topics or miss tangential sources.

Procedural Micromanagement

Goal-Oriented Delegation

Coordinator Agent

i
Web Search Subagent

> Step 1: Search X.
> Step 2: Read Y.
> Step 3: Extract Z.

|

Failure/Missed Value
Rigid, Not Adaptable

Coordinator Agent

—
Web Search Subagent

+ Target: Coverage Breadth.
&
+ Criteria: Recency.

|

Adaptable, High-Value Results
Self-Directed Strategy

The Architect’s Approach:

Specify research goals and quality criteria rather than procedural steps.
Let the specialized subagent determine its own search strategy. Keep

tool interfaces generic but add enum parameters (e.g.,
analysis_type: extraction | summarization) to guide behavior.

tool: 'analyze_document',

params: {

analysis_type: ‘extraction’ | ‘summarization’

}

The Architect's Reference Matrix

P Developer 6
pad Data Extraction Customer Support Productivity Multi-Agent

a ia oe

Compliance/Control

Accuracy

cll
The Production Architecture Blueprint

Granular Application

Real-time Intercepts

Synthesis

Intelligence at Execution Layer
Validation Guardrails Result Aggregation
Policy Enforcement Formatting

the edges.
[atch | = Schema Checks Delivery

Pattern
Router

Batch
Strict typing in oe

the middle.

Se Application intercepts
guarding the core.

State Management (Pruning + Shared Vector)

Pruning Logic Shared Vector Store
(pruning) (data)

& Context Window Management

—

Shared memory
sustaining the lifecycle.

