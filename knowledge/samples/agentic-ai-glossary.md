# Agentic AI glossary

Agent: a program in which a language model decides the next step at runtime, such as which tool to call, with what input and when to stop.

Checkpointer: in LangGraph, a component that saves the graph's state after every step, keyed by a thread id, enabling memory, recovery and human-in-the-loop pauses.

Chunk: a piece of a document, typically a few hundred characters, embedded and stored separately so it can be retrieved on its own.

Context window: the maximum amount of text, measured in tokens, that a model can consider at once, including the prompt, history and retrieved documents.

Crew: in CrewAI, a group of agents with roles, goals and backstories, working through tasks under a sequential or hierarchical process.

Embedding: a list of numbers representing the meaning of a piece of text, so that texts with similar meaning are close together.

Few-shot prompting: including worked examples in the prompt to show the model the pattern you want.

Guardrail: a check that constrains an agent, such as a maximum number of steps, an output validator or a required human approval.

Hallucination: a fluent but false statement produced by a model, such as an invented fact, source or API.

HNSW: Hierarchical Navigable Small World, a graph-based approximate nearest-neighbour index used by many vector databases.

Hybrid search: combining keyword search such as BM25 with vector search, usually by fusing their rankings.

LCEL: LangChain Expression Language, which composes Runnables with the pipe operator, for example prompt | llm | parser.

MCP: Model Context Protocol, an open protocol for connecting models and agents to tools and data sources through a standard interface.

ReAct: a pattern in which a model alternates Thought, Action and Observation steps until it can answer.

Reciprocal Rank Fusion (RRF): a way to merge ranked lists by giving each item a score of 1 / (k + rank) from every list it appears in, commonly with k = 60.

Reranker: a model that re-scores retrieved chunks against the query for better precision before they reach the LLM.

State graph: in LangGraph, a graph of nodes (functions) and edges that pass a shared, typed state between them, with conditional edges and cycles.

Temperature: a setting that controls randomness in generation; low values for extraction and classification, higher values for creative work.

Tool calling: a model returning a structured request to run a named function with arguments, which the application then executes.
