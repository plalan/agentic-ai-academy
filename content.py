"""
content.py — The Agentic AI Academy curriculum.

One source of truth:
  • served to the browser at /api/content
  • indexed by the built-in knowledge engine (engine.py), so the tutor
    answers from the same material the lessons teach
  • exportable as markdown for any other RAG system (export_kb.py)

Text supports **bold** and `code`. Covers the stack most agentic-AI
programmes teach: Python/Jupyter, LangChain, LangGraph, CrewAI,
ChromaDB/FAISS, FastAPI/Streamlit/Docker — plus a security module.
"""

MODULES = [
    # ------------------------------------------------------------------ 0
    {
        "id": "intro",
        "title": "What Is an AI Agent?",
        "icon": "🌱",
        "tagline": "Start here if all of this is new. No code needed.",
        "lessons": [
            {
                "title": "Chatbot, assistant, agent",
                "body": [
                    "A **chatbot** answers. You ask, it replies, and that's the end of it. Everything it does is produce text.",
                    "An **agent** acts. You give it a goal, and it works out the steps, uses tools such as search, a calendar or a database, looks at what came back, and keeps going until the job is done.",
                    "The language model inside can be exactly the same. The difference is what surrounds it: tools it is allowed to use, and a loop that lets it take more than one step.",
                ],
                "analogy": "A chatbot is asking a friend for directions. An agent is hiring a driver: you say where you want to go, and they handle the turns.",
            },
            {
                "title": "The four parts of every agent",
                "body": [
                    "**A model**: the language model that reads the situation and decides what to do next.",
                    "**Tools**: the things it is allowed to do, such as search the web, read a file, send a message or run a query. Without tools, a model can only talk.",
                    "**Memory**: a record of what has happened so far, so step five knows what step two found.",
                    "**A loop with a stop rule**: decide, act, look at the result, repeat. The stop rule says when to finish, or when to give up.",
                ],
            },
            {
                "title": "What agents are good at, and where they fail",
                "body": [
                    "Agents shine at **multi-step work with clear tools**: researching a topic across sources, sorting incoming tickets, checking records against a policy, booking and scheduling.",
                    "They struggle when the goal is vague, when a single mistake is costly, or when nobody checks the result. A model can be **confidently wrong**, and an agent can act on that mistake.",
                    "That is why real agents have **guardrails**: limits on how many steps they take, limits on what they may touch, and a human who approves anything that matters, such as sending money or deleting data.",
                ],
            },
            {
                "title": "How this course works",
                "body": [
                    "Each module has short **lessons**, one hands-on **lab**, and a five-question **quiz**. Labs are where it clicks, so don't skip them.",
                    "You don't have to take every module. Tell the home page where you're starting from and what you want, and it suggests a path. Everything else stays open if you get curious.",
                    "Earn XP as you go. A module badge needs every lesson, the lab, and 4 out of 5 on the quiz.",
                ],
            },
        ],
        "lab": {"type": "agentdemo", "title": "Chatbot or Agent?",
                "intro": "Watch the same request handled by a chatbot and by an agent, then decide which jobs need which."},
        "quiz": [
            {"q": "What most clearly separates an agent from a chatbot?",
             "options": ["It uses a bigger model", "It decides on and takes actions with tools to reach a goal", "It always answers faster", "It never makes mistakes"],
             "answer": 1, "why": "The model can be identical. An agent adds tools and a loop, so it can act, not just reply."},
            {"q": "Which of these is NOT one of the four parts of an agent?",
             "options": ["A model", "Tools", "Memory", "Its own data centre"],
             "answer": 3, "why": "Model, tools, memory and a loop with a stop rule. Where it runs is a separate question."},
            {"q": "Why does an agent need a stop rule?",
             "options": ["To save disk space", "So it finishes, or gives up, instead of looping forever", "Models require one", "To look professional"],
             "answer": 1, "why": "A loop without an exit can run, and spend money, indefinitely."},
            {"q": "An agent is about to send a payment. What is the sensible design?",
             "options": ["Let it send; it's usually right", "Pause and ask a human to approve", "Send two payments to be safe", "Hide the action from the user"],
             "answer": 1, "why": "Anything costly or irreversible should need human approval."},
            {"q": "Which task suits an agent best?",
             "options": ["Explaining what a firewall is", "Checking 200 firewall rules against policy and opening tickets for the violations", "Suggesting a name for a project", "Fixing the grammar in one sentence"],
             "answer": 1, "why": "It has many steps, clear tools and a checkable result. The others are single replies."},
        ],
    },
    # ------------------------------------------------------------------ 1
    {
        "id": "python",
        "title": "Python & Jupyter for Agents",
        "icon": "🐍",
        "tagline": "The language every agent framework speaks.",
        "lessons": [
            {
                "title": "An agent is just a loop",
                "body": [
                    "Strip away the hype and an AI agent is an ordinary program running a loop: send context to a language model, read what it wants to do, run a tool, feed the result back, repeat until done.",
                    "That loop is written in Python almost everywhere. LangChain, LangGraph, CrewAI and LlamaIndex are all Python-first, so the skills that matter are plain ones: **functions**, **dicts and JSON**, **classes**, **type hints**, and enough **async** to wait on slow models without freezing.",
                ],
                "analogy": "Python is the kitchen. The LLM is the chef's judgement. Tools are the knives. The loop is the service: order in, plate out.",
                "code": "while not done:\n    reply = llm.invoke(messages)          # model decides\n    if reply.tool_calls:\n        result = run_tool(reply.tool_calls[0]) # your code acts\n        messages.append(result)            # model sees the outcome\n    else:\n        done = True",
            },
            {
                "title": "Jupyter: the lab notebook",
                "body": [
                    "A notebook runs code in **cells** and keeps every variable alive between them. That makes it perfect for poking at a model, a prompt or an embedding.",
                    "It also creates the classic trap: **hidden state**. Run cells out of order and the notebook shows results your code can no longer reproduce. Before you trust a result, use *Restart & Run All*.",
                    "Rule of thumb: explore in notebooks, ship from `.py` files.",
                ],
                "code": "%pip install -q langchain-ollama\n\nfrom langchain_ollama import ChatOllama\nllm = ChatOllama(model=\"llama3.1\")\nllm.invoke(\"Explain RAG in one line\").content",
            },
            {
                "title": "Structure is safety: type hints and Pydantic",
                "body": [
                    "Models return text. Your program needs structure. **Pydantic** models describe the shape you expect and reject anything that doesn't fit.",
                    "With `with_structured_output`, LangChain turns a Pydantic class into a schema the model must fill, then validates the result for you.",
                ],
                "code": "from pydantic import BaseModel, Field\n\nclass Ticket(BaseModel):\n    severity: str = Field(description=\"low, medium, high or critical\")\n    summary: str\n    needs_human: bool\n\ntriage = llm.with_structured_output(Ticket)\nticket = triage.invoke(\"Customer says backups failed for 3 nights\")",
            },
            {
                "title": "Functions become tools",
                "body": [
                    "A **tool** is four things: a name, a description, a JSON schema for its arguments, and the function itself.",
                    "The model never runs code. It reads the descriptions, asks for a tool by name with arguments, and **your program** decides whether to run it. That is why a clear docstring matters as much as the code.",
                ],
                "code": "from langchain_core.tools import tool\n\n@tool\ndef lookup_cve(cve_id: str) -> str:\n    \"\"\"Return severity and affected products for a CVE id like CVE-2024-3400.\"\"\"\n    return cve_db.get(cve_id, \"not found\")",
            },
        ],
        "lab": {"type": "schema", "title": "Tool Schema Forge",
                "intro": "Turn a Python function into the JSON schema a model actually sees. Pick types, mark what's required, write a description the model can act on."},
        "quiz": [
            {"q": "In tool calling, who actually executes the tool function?",
             "options": ["The LLM provider's servers", "Your program", "The vector database", "The Jupyter kernel, always"],
             "answer": 1, "why": "The model only asks for a call. Your code runs it, which is also where you enforce permissions."},
            {"q": "What is the most common Jupyter pitfall?",
             "options": ["Cells are too slow", "Hidden state from running cells out of order", "It can't import libraries", "It only supports Python 2"],
             "answer": 1, "why": "Variables survive between cells, so out-of-order runs produce results you can't reproduce. Restart & Run All before trusting output."},
            {"q": "What does Pydantic add when used with `with_structured_output`?",
             "options": ["Faster inference", "Validation of the model's output against a typed schema", "Free GPU time", "Automatic retrieval"],
             "answer": 1, "why": "The schema tells the model what to produce, and validation catches anything that doesn't match."},
            {"q": "Why does a tool's docstring matter?",
             "options": ["Python requires it", "The model reads it to decide when and how to call the tool", "It speeds up the function", "It is shown to end users"],
             "answer": 1, "why": "The description is the model's only guide to what the tool does and when to use it."},
            {"q": "Best practice when an experiment in a notebook works?",
             "options": ["Ship the notebook to production", "Move the logic into .py modules with tests", "Delete it", "Convert it to a PDF"],
             "answer": 1, "why": "Notebooks are for exploring. Production code belongs in versioned, testable modules."},
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "langchain",
        "title": "LLMs, Prompts & LangChain",
        "icon": "🔗",
        "tagline": "Talk to models, then snap the pieces together.",
        "lessons": [
            {
                "title": "What a language model actually does",
                "body": [
                    "An LLM predicts the next **token** (roughly ¾ of a word) again and again. Everything it knows about your conversation must fit in its **context window**.",
                    "It has **no memory between calls**. Chat apps feel continuous because the app resends the history every time.",
                    "**Temperature** controls randomness: near 0 for extraction and classification, higher for brainstorming.",
                ],
                "analogy": "A brilliant consultant with total amnesia. Every meeting, you hand over the full file again.",
            },
            {
                "title": "Prompts are programs",
                "body": [
                    "A **system** message sets the role and rules. **User** messages carry the request. Templates turn prompts into reusable functions with variables.",
                    "Two techniques do most of the work: **few-shot** examples (show, don't just tell) and an explicit **output format**.",
                ],
                "code": "from langchain_core.prompts import ChatPromptTemplate\n\nprompt = ChatPromptTemplate.from_messages([\n    (\"system\", \"You are a security analyst. Answer in 3 bullets.\"),\n    (\"human\", \"Summarise the risk of {finding} for a CFO.\"),\n])",
            },
            {
                "title": "LCEL: building with the pipe",
                "body": [
                    "LangChain Expression Language treats every piece as a **Runnable** you can join with `|`. The output of one becomes the input of the next.",
                    "Every chain gets `invoke`, `batch` and `stream` for free. `RunnablePassthrough` and `RunnableParallel` let you fan data in and out, which is exactly how a RAG chain feeds both the question and the retrieved context into one prompt.",
                ],
                "code": "from langchain_core.output_parsers import StrOutputParser\n\nchain = prompt | llm | StrOutputParser()\nprint(chain.invoke({\"finding\": \"unpatched VPN appliance\"}))",
            },
            {
                "title": "Memory is just messages",
                "body": [
                    "Conversation memory is a list of past messages you send back each turn. When it grows too long you **trim** it (keep the last N turns) or **summarise** older turns.",
                    "This Academy's tutor keeps the last 6 turns and folds your previous question into its search, so follow-ups like *\"and how does that compare?\"* still find the right notes.",
                ],
            },
        ],
        "lab": {"type": "lcel", "title": "Pipe Builder",
                "intro": "Build working LCEL chains for real tasks by choosing the right Runnables in the right order."},
        "quiz": [
            {"q": "For extracting fields from an invoice, which temperature is best?",
             "options": ["0 to 0.2", "0.9", "1.5", "It doesn't matter"],
             "answer": 0, "why": "Low temperature makes output more deterministic, which is what extraction needs."},
            {"q": "Does an LLM remember your previous API call?",
             "options": ["Yes, always", "Only on weekends", "No. The app resends the history each time", "Only if temperature is 0"],
             "answer": 2, "why": "Models are stateless between calls. Memory is something your application provides."},
            {"q": "In `prompt | llm | parser`, what does `|` do?",
             "options": ["Runs the three in parallel", "Passes each step's output into the next", "Picks whichever is fastest", "Logical OR"],
             "answer": 1, "why": "The pipe composes Runnables into a sequence."},
            {"q": "Few-shot prompting means…",
             "options": ["Using a small model", "Including worked examples in the prompt", "Asking only a few questions", "Limiting output tokens"],
             "answer": 1, "why": "Examples show the model the pattern you want, which often beats long instructions."},
            {"q": "The conversation no longer fits the context window. What do you do?",
             "options": ["Nothing, models handle it", "Trim older turns or summarise them", "Raise the temperature", "Switch to Jupyter"],
             "answer": 1, "why": "Context is finite. Keep the recent turns and compress or drop the rest."},
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "vectors",
        "title": "Embeddings & Vector Stores",
        "icon": "🧭",
        "tagline": "Meaning, turned into coordinates.",
        "lessons": [
            {
                "title": "Meaning as coordinates",
                "body": [
                    "An **embedding** turns text into a list of numbers. This Academy uses `nomic-embed-text`, which produces **768** numbers per chunk.",
                    "Texts with similar meaning land close together, even when they share no words. Closeness is usually measured with **cosine similarity**: the angle between two vectors, from 1 (same direction) down to 0 (unrelated).",
                ],
                "analogy": "A map where cities are placed by what they're like, not where they are. 'Ransomware' and 'extortion malware' end up as neighbours.",
            },
            {
                "title": "Chunking: cutting the book into index cards",
                "body": [
                    "Documents are split into **chunks** before embedding. Too large and each vector blurs several ideas together. Too small and a chunk loses the context that gives it meaning.",
                    "**Overlap** repeats a little text across boundaries so a sentence cut in half still appears whole somewhere. The Academy's knowledge base uses chunks of about 600 characters with 100 characters of overlap.",
                ],
                "code": "from langchain_text_splitters import RecursiveCharacterTextSplitter\n\nsplitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)\nchunks = splitter.split_text(long_document)",
            },
            {
                "title": "ChromaDB or FAISS?",
                "body": [
                    "**ChromaDB** is a database: it persists to disk, stores metadata, supports filters and collections.",
                    "**FAISS** (from Meta) is a library of very fast similarity-search indexes. It's excellent at raw speed and scale, but persistence and metadata are your job.",
                    "Start with Chroma for apps. Reach for FAISS when you need fine control over the index or millions of vectors in memory.",
                ],
                "code": "# Chroma\nimport chromadb\ncol = chromadb.PersistentClient(path=\"./db\").get_or_create_collection(\"kb\")\ncol.add(ids=[\"1\"], documents=[\"Immutable backups cannot be altered or deleted\"])\ncol.query(query_texts=[\"air-gapped backup\"], n_results=3)\n\n# FAISS via LangChain\nfrom langchain_community.vectorstores import FAISS\nstore = FAISS.from_texts(texts, embeddings)\nstore.similarity_search(\"air-gapped backup\", k=3)",
            },
            {
                "title": "Exact vs approximate search",
                "body": [
                    "Exact search compares the query with every vector. That's perfect and slow once you have millions.",
                    "**Approximate nearest neighbour** indexes such as **HNSW** (a layered graph you hop across) or **IVF** (search only the nearest clusters) give almost the same answers far faster. Chroma uses HNSW under the hood.",
                ],
            },
        ],
        "lab": {"type": "embed", "title": "Embedding Observatory",
                "intro": "Type sentences, embed them with the same model your RAG uses, and see meaning as distance. Then play with chunking."},
        "quiz": [
            {"q": "Cosine similarity measures…",
             "options": ["How many words two texts share", "The angle between two vectors", "Text length", "Spelling mistakes"],
             "answer": 1, "why": "It compares direction, which captures meaning independently of length."},
            {"q": "What happens if chunks are far too large?",
             "options": ["Retrieval gets sharper", "Each vector mixes several ideas, so retrieval gets less precise", "Embedding becomes free", "Nothing"],
             "answer": 1, "why": "A large chunk averages many topics into one vector and wastes context space."},
            {"q": "Why use chunk overlap?",
             "options": ["To save storage", "So text cut at a boundary still appears whole in some chunk", "To confuse attackers", "It's required by Chroma"],
             "answer": 1, "why": "Overlap protects sentences and ideas that straddle a split."},
            {"q": "The key difference between FAISS and ChromaDB?",
             "options": ["FAISS is a search library; Chroma is a database with persistence and metadata", "Chroma is only for images", "FAISS needs the internet", "They are identical"],
             "answer": 0, "why": "FAISS gives you indexes; Chroma wraps storage, metadata and filtering around one."},
            {"q": "HNSW is…",
             "options": ["A tokenizer", "A graph-based approximate nearest-neighbour index", "An LLM", "A prompt format"],
             "answer": 1, "why": "Hierarchical Navigable Small World graphs make vector search fast at scale."},
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "rag",
        "title": "RAG: Retrieval Done Right",
        "icon": "📚",
        "tagline": "Give the model an open-book exam.",
        "lessons": [
            {
                "title": "The open-book exam",
                "body": [
                    "**Retrieval-Augmented Generation**: retrieve relevant chunks, add them to the prompt, then generate. The model answers from your documents instead of from memory.",
                    "Done well, RAG reduces made-up answers, works on private data the model never saw, stays current without retraining, and can **cite its sources**.",
                ],
                "analogy": "A closed-book exam rewards memorisation and bluffing. An open-book exam rewards finding the right page.",
            },
            {
                "title": "Why vector search alone misses things",
                "body": [
                    "Embeddings are great at meaning and weak at **exact terms**: product names, error codes, CVE ids, people's names. 'VX-4400' or 'CVE-2024-3400' can slip past a vector search.",
                    "**BM25** is classic keyword search that rewards rare, matching words. **Hybrid search** runs both and merges them with **Reciprocal Rank Fusion**: each result scores `1 / (60 + rank)` from each list, so items both retrievers like rise to the top.",
                    "The Retrieval Microscope lab shows this live: vector + BM25, fused with RRF.",
                ],
                "code": "def rrf(vector_ranks, keyword_ranks, k=60):\n    scores = {}\n    for ranks in (vector_ranks, keyword_ranks):\n        for doc_id, rank in ranks.items():\n            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)\n    return sorted(scores, key=scores.get, reverse=True)",
            },
            {
                "title": "Metadata and filters",
                "body": [
                    "Every chunk can carry **metadata**: source, date, customer, domain. Filtering before searching keeps answers on topic and is often the cheapest accuracy gain you'll find.",
                    "This Academy tags every chunk with a shelf (course, samples, my-docs), so you can search one shelf at a time.",
                ],
                "code": "col.query(query_embeddings=[q], n_results=8, where={\"domain\": \"security\"})",
            },
            {
                "title": "How to know RAG is working",
                "body": [
                    "Measure two halves separately. **Retrieval**: for a set of test questions, did the right chunk come back in the top *k* (recall@k)? **Generation**: is the answer **faithful** to the retrieved context, and does it actually answer the question?",
                    "Twenty hand-written questions with known answers beat any amount of vibes. Frameworks like RAGAS automate parts of this.",
                ],
            },
        ],
        "lab": {"type": "rag", "title": "Retrieval Microscope",
                "intro": "Search your own knowledge base live. See which chunks the vector search found, which BM25 found, and how fusion ranks them."},
        "quiz": [
            {"q": "What does the R in RAG stand for?",
             "options": ["Reasoning", "Retrieval", "Reinforcement", "Ranking"],
             "answer": 1, "why": "Retrieval-Augmented Generation: fetch relevant text, then generate from it."},
            {"q": "BM25 is especially good at…",
             "options": ["Understanding synonyms", "Exact keyword and rare-term matches", "Image search", "Translation"],
             "answer": 1, "why": "Keyword scoring shines on names, codes and jargon that embeddings blur."},
            {"q": "Reciprocal Rank Fusion combines…",
             "options": ["Two LLMs", "Rankings from multiple retrievers", "Chunks into documents", "GPUs"],
             "answer": 1, "why": "It merges ranked lists so results that rank well in several lists rise to the top."},
            {"q": "A 'faithful' RAG answer is one that…",
             "options": ["Is long", "Is supported by the retrieved context", "Uses no sources", "Agrees with the user"],
             "answer": 1, "why": "Faithfulness means every claim can be traced back to the retrieved text."},
            {"q": "Why filter by metadata before searching?",
             "options": ["To restrict results to the relevant slice, like one customer or domain", "To make embeddings bigger", "To skip the LLM", "It's decorative"],
             "answer": 0, "why": "Filtering removes irrelevant candidates before ranking, which improves precision cheaply."},
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "agents",
        "title": "Agents & the ReAct Loop",
        "icon": "🤖",
        "tagline": "Let the model choose the next step.",
        "lessons": [
            {
                "title": "From chain to agent",
                "body": [
                    "A **chain** follows steps you fixed in advance. An **agent** lets the model choose the next step at runtime: which tool, with what input, and when to stop.",
                    "Every agent has four parts: a **model**, a set of **tools**, **memory** of what has happened so far, and a **stop condition**.",
                ],
            },
            {
                "title": "ReAct: Reason, Act, Observe",
                "body": [
                    "The ReAct pattern (Yao et al., 2022) interleaves thinking and doing: **Thought** (what do I need?), **Action** (call a tool), **Observation** (read the result). Repeat until the answer is clear.",
                    "Writing the reasoning down between actions makes the agent easier to steer and much easier to debug.",
                ],
                "code": "Thought: I need the CVE's affected products.\nAction: lookup_cve(\"CVE-2024-3400\")\nObservation: PAN-OS GlobalProtect, CVSS 10.0\nThought: Now check whether we run it.\nAction: check_inventory(\"PAN-OS\")\nObservation: 2 firewalls on 10.2.9\nThought: I can answer.",
            },
            {
                "title": "Designing tools an agent can use",
                "body": [
                    "Good tools are **small**, **well named** and **specific in their descriptions**. They validate their inputs and return short, useful text rather than a 5,000-line dump.",
                    "Anything with side effects, such as sending email, deleting data or moving money, should require **human approval**.",
                ],
            },
            {
                "title": "Guardrails on the loop",
                "body": [
                    "Agents can loop forever or burn budget. Always set a **maximum number of steps**, timeouts and a cost ceiling, and decide what happens on failure.",
                    "In LangChain 1.x, `create_agent` builds a ReAct-style agent on top of LangGraph.",
                ],
                "code": "from langchain.agents import create_agent\n\nagent = create_agent(\n    model=llm,\n    tools=[lookup_cve, check_inventory],\n    system_prompt=\"You are a careful security assistant.\",\n)\nagent.invoke({\"messages\": [{\"role\": \"user\", \"content\": \"Are we exposed to CVE-2024-3400?\"}]})",
            },
        ],
        "lab": {"type": "react", "title": "Be the Agent",
                "intro": "You are the model. Pick the next action at each step and see how the loop plays out. Fewer, smarter steps score higher."},
        "quiz": [
            {"q": "The key difference between a chain and an agent?",
             "options": ["Agents are always faster", "An agent decides its next step at runtime", "Chains can't call LLMs", "There is none"],
             "answer": 1, "why": "Chains are fixed pipelines; agents choose actions dynamically."},
            {"q": "What is the order of the ReAct loop?",
             "options": ["Act, Observe, Reason", "Thought, Action, Observation", "Retrieve, Embed, Rank", "Plan, Code, Ship"],
             "answer": 1, "why": "Reason about what's needed, act with a tool, then observe the result."},
            {"q": "Why set a maximum number of iterations?",
             "options": ["To prevent endless loops and runaway cost", "Models require it", "To improve embeddings", "For prettier logs"],
             "answer": 0, "why": "Without a ceiling, a confused agent can loop until your budget runs out."},
            {"q": "Which tool should require human approval?",
             "options": ["Search the knowledge base", "Send an email to a customer", "Read a CVE record", "Count tokens"],
             "answer": 1, "why": "Actions with external side effects deserve a human checkpoint."},
            {"q": "A good tool description…",
             "options": ["Is as short as possible", "Says what the tool does, when to use it, and the input format", "Is written for end users", "Is optional"],
             "answer": 1, "why": "The model decides based on the description, so precision there pays off directly."},
        ],
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "langgraph",
        "title": "LangGraph: Agents as State Machines",
        "icon": "🕸️",
        "tagline": "Draw the flow. Let the model drive inside it.",
        "lessons": [
            {
                "title": "Nodes, edges and shared state",
                "body": [
                    "LangGraph models an agent as a graph. **Nodes** are functions. **Edges** say what runs next. A typed **state** dict flows through every node, and each node returns updates to it.",
                    "**Conditional edges** call a routing function that reads the state and picks the next node. Unlike a simple chain, graphs can contain **cycles**, so an agent can loop back and try again.",
                ],
                "code": "from typing import TypedDict\nfrom langgraph.graph import StateGraph, START, END\n\nclass State(TypedDict):\n    question: str\n    context: list\n    good_enough: bool\n\ng = StateGraph(State)\ng.add_node(\"retrieve\", retrieve)\ng.add_node(\"grade\", grade)\ng.add_node(\"answer\", answer)\ng.add_edge(START, \"retrieve\")\ng.add_edge(\"retrieve\", \"grade\")\ng.add_conditional_edges(\"grade\", lambda s: \"answer\" if s[\"good_enough\"] else \"retrieve\")\ng.add_edge(\"answer\", END)\napp = g.compile()",
            },
            {
                "title": "Anatomy of an agentic RAG graph",
                "body": [
                    "A typical agentic RAG bot built with LangGraph has eight nodes. It starts at **classify_intent**, which routes greetings to **direct_answer**, news to **web_search**, and everything else to **retrieve**.",
                    "After retrieval, **evaluate_context** judges whether the chunks are enough. If not, and hops remain (max 3), **refine_query** rewrites the search and loops back to retrieve. Out of hops, it falls back to **web_search_then_generate**. Enough context goes straight to **generate_answer**.",
                ],
            },
            {
                "title": "Checkpoints and humans in the loop",
                "body": [
                    "Compile a graph with a **checkpointer** and LangGraph saves the state after every step, keyed by a `thread_id`. That gives you memory across sessions, crash recovery, and the ability to pause.",
                    "An **interrupt** stops the graph before a risky node so a human can approve, edit the state, or reject, then resume exactly where it stopped.",
                ],
                "code": "from langgraph.checkpoint.memory import InMemorySaver\n\napp = g.compile(checkpointer=InMemorySaver(), interrupt_before=[\"send_email\"])\napp.invoke({\"question\": q}, config={\"configurable\": {\"thread_id\": \"deal-42\"}})",
            },
            {
                "title": "When to reach for a graph",
                "body": [
                    "Use plain chains for straight lines. Use a prebuilt agent for a simple tool loop. Reach for LangGraph when you need **branching**, **retries**, **long-running work**, **human approval**, or **several agents** coordinated by a supervisor.",
                ],
            },
        ],
        "lab": {"type": "graph", "title": "Graph Walker",
                "intro": "Step through a real agentic RAG graph. Pick a question type and watch the state change node by node."},
        "quiz": [
            {"q": "In LangGraph, the 'state' is…",
             "options": ["The GPU memory", "A shared, typed dict that nodes read and update", "The prompt template", "A database table"],
             "answer": 1, "why": "State is the shared data every node receives and returns updates to."},
            {"q": "A conditional edge…",
             "options": ["Always goes to END", "Calls a routing function to choose the next node", "Runs nodes in parallel", "Deletes state"],
             "answer": 1, "why": "Routing functions inspect state and return the name of the next node."},
            {"q": "What lets the agentic RAG graph loop from refine_query back to retrieve?",
             "options": ["LangGraph allows cycles", "A while loop in the prompt", "Chroma triggers", "It can't loop"],
             "answer": 0, "why": "Graphs can contain cycles, which is what makes retry and refinement possible."},
            {"q": "A checkpointer enables…",
             "options": ["Faster embeddings", "Saving state per thread so runs can pause, resume and remember", "Larger context windows", "Free tokens"],
             "answer": 1, "why": "Persisted state is the basis for memory, recovery and human-in-the-loop."},
            {"q": "In the agentic RAG graph, context is judged insufficient and hops remain. Next node?",
             "options": ["generate_answer", "refine_query", "direct_answer", "END"],
             "answer": 1, "why": "It rewrites the query and retrieves again, up to the hop limit."},
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "crewai",
        "title": "CrewAI: Teams of Agents",
        "icon": "👥",
        "tagline": "Specialists with roles, goals and a process.",
        "lessons": [
            {
                "title": "Agents, tasks and the crew",
                "body": [
                    "CrewAI organises work like a team. An **Agent** has a `role`, a `goal` and a `backstory`, plus optional tools. A **Task** has a `description`, an `expected_output` and an assigned agent. A **Crew** combines agents and tasks under a **process**.",
                    "`expected_output` is underrated: it is your definition of done, and the agent works towards it.",
                ],
                "code": "from crewai import Agent, Task, Crew, Process, LLM\n\nllm = LLM(model=\"ollama/llama3.1\", base_url=\"http://localhost:11434\")\n\nresearcher = Agent(role=\"Account Researcher\",\n    goal=\"Find the customer's top 3 data-protection risks\",\n    backstory=\"A sharp presales analyst.\", llm=llm)\nwriter = Agent(role=\"Brief Writer\",\n    goal=\"Turn research into a one-page executive brief\",\n    backstory=\"Writes for busy CIOs.\", llm=llm)\n\nresearch = Task(description=\"Research {company}\", expected_output=\"3 risks with evidence\", agent=researcher)\nbrief = Task(description=\"Write the brief\", expected_output=\"One page, plain English\", agent=writer)\n\ncrew = Crew(agents=[researcher, writer], tasks=[research, brief], process=Process.sequential)\ncrew.kickoff(inputs={\"company\": \"Acme Bank\"})",
            },
            {
                "title": "Sequential or hierarchical?",
                "body": [
                    "**Sequential**: tasks run in order, and each task's output becomes context for the next. It's predictable and the right default.",
                    "**Hierarchical**: a manager agent (set with `manager_llm` or `manager_agent`) plans, delegates tasks to the crew and reviews their work. More flexible, slower, and harder to predict.",
                ],
            },
            {
                "title": "When more agents help, and when they hurt",
                "body": [
                    "Several agents help when the work needs genuinely **different specialisms** or a **separate reviewer** who checks the first agent's output.",
                    "They hurt when one agent would do: every hand-off costs tokens and time, and errors compound down the line. Start with one agent, and add a second only when you can name the job it does better.",
                ],
            },
        ],
        "lab": {"type": "crew", "title": "Crew Builder",
                "intro": "Assemble a crew for a mission, choose a process, and watch the hand-offs. The builder writes the CrewAI code for you."},
        "quiz": [
            {"q": "The three defining fields of a CrewAI Agent?",
             "options": ["name, id, port", "role, goal, backstory", "model, temperature, top_p", "input, output, error"],
             "answer": 1, "why": "Role, goal and backstory shape how the agent approaches its work."},
            {"q": "What does `expected_output` on a Task do?",
             "options": ["Sets the max tokens", "Describes what a finished result looks like", "Chooses the LLM", "Nothing"],
             "answer": 1, "why": "It defines done, which steers the agent and makes review possible."},
            {"q": "A hierarchical process needs…",
             "options": ["A manager LLM or manager agent", "At least 10 agents", "FAISS", "A GPU per agent"],
             "answer": 0, "why": "The manager plans, delegates and validates the crew's work."},
            {"q": "The main downside of adding more agents?",
             "options": ["More cost and latency, and errors compound", "They can't use tools", "They require Java", "None"],
             "answer": 0, "why": "Each hand-off adds tokens, time and another chance for mistakes."},
            {"q": "In a sequential crew, task 2 receives…",
             "options": ["Nothing", "Task 1's output as context", "A random task's output", "Only the user's question"],
             "answer": 1, "why": "Sequential crews pass earlier outputs forward as context."},
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "id": "ship",
        "title": "Shipping: FastAPI, Streamlit & Docker",
        "icon": "🚢",
        "tagline": "From notebook to something people can use.",
        "lessons": [
            {
                "title": "FastAPI: your agent as a service",
                "body": [
                    "FastAPI turns Python functions into HTTP endpoints, validates requests with Pydantic, and generates interactive docs at `/docs` for free.",
                    "This Academy is itself a FastAPI service: open `/docs` on it to look around.",
                ],
                "code": "from fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Ask(BaseModel):\n    question: str\n\n@app.post(\"/ask\")\ndef ask(req: Ask):\n    return {\"answer\": chain.invoke(req.question)}",
            },
            {
                "title": "Streamlit: a UI in an afternoon",
                "body": [
                    "Streamlit builds a web UI from a Python script. `st.chat_input` and `st.chat_message` give you a chat app in a dozen lines, and `st.session_state` keeps values between reruns.",
                    "It's ideal for demos and internal tools. For multi-user production apps, put a proper API behind it.",
                ],
                "code": "import streamlit as st\n\nif \"history\" not in st.session_state:\n    st.session_state.history = []\nif q := st.chat_input(\"Ask the agent\"):\n    st.session_state.history.append((q, agent_answer(q)))\nfor q, a in st.session_state.history:\n    st.chat_message(\"user\").write(q)\n    st.chat_message(\"assistant\").write(a)",
            },
            {
                "title": "Docker: ship the whole kitchen",
                "body": [
                    "An **image** packages code, dependencies and runtime. A **container** is a running image. Each Dockerfile instruction creates a **layer**, and unchanged layers are reused from cache.",
                    "That's why you copy `requirements.txt` and install dependencies **before** copying your code: edit the code and the slow install layer stays cached. **Compose** runs multi-service stacks, and from a container on Docker Desktop `host.docker.internal` reaches Ollama on the host.",
                ],
                "code": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nEXPOSE 8505\nCMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8505\"]",
            },
            {
                "title": "A production checklist",
                "body": [
                    "**Health checks** and timeouts on every model call. **Logging and tracing** so you can replay what the agent did (LangSmith, OpenTelemetry). **Secrets** in environment variables, never in code. **Rate limits** and cost ceilings. An **evaluation set** that runs before every release.",
                ],
            },
        ],
        "lab": {"type": "docker", "title": "Layer Cake",
                "intro": "Put the Dockerfile in an order that builds correctly and caches well, then sort jobs between FastAPI and Streamlit."},
        "quiz": [
            {"q": "Why copy requirements.txt before the rest of the code?",
             "options": ["Alphabetical order", "So the dependency layer stays cached when only code changes", "Docker requires it", "To make the image bigger"],
             "answer": 1, "why": "Layers rebuild only when their inputs change, so slow installs stay cached."},
            {"q": "Where does FastAPI serve its interactive API docs?",
             "options": ["/help", "/docs", "/swagger.exe", "It doesn't"],
             "answer": 1, "why": "FastAPI generates OpenAPI docs at /docs automatically."},
            {"q": "Streamlit's `st.session_state` is used to…",
             "options": ["Store values across reruns for a user's session", "Configure Docker", "Train models", "Define routes"],
             "answer": 0, "why": "Streamlit reruns the script on each interaction; session_state persists data between runs."},
            {"q": "From a container on Docker Desktop for Mac, how do you reach Ollama running on the host?",
             "options": ["localhost:11434", "host.docker.internal:11434", "0.0.0.0", "You can't"],
             "answer": 1, "why": "Inside a container, localhost is the container itself; host.docker.internal is the Mac."},
            {"q": "docker compose is for…",
             "options": ["Writing Python", "Defining and running multi-container applications", "Compressing images", "Embedding text"],
             "answer": 1, "why": "One YAML file describes all services, their ports, volumes and networks."},
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "security",
        "title": "Securing Agents",
        "icon": "🛡️",
        "tagline": "Bonus module: the part most courses skip.",
        "lessons": [
            {
                "title": "The new attack surface",
                "body": [
                    "An agent that reads untrusted text and can take actions is a new kind of insider. The **OWASP Top 10 for LLM Applications (2025)** names the main risks, led by **LLM01 Prompt Injection**, and including **Sensitive Information Disclosure**, **Excessive Agency**, **System Prompt Leakage** and **Vector and Embedding Weaknesses**.",
                ],
            },
            {
                "title": "Direct and indirect injection",
                "body": [
                    "**Direct** injection is the user typing *\"ignore your instructions\"*. **Indirect** injection hides instructions in something the agent reads: a web page, an email, a PDF in the knowledge base, a tool's output.",
                    "Indirect is the dangerous one, because nobody typed it. A single poisoned document in a RAG knowledge base can steer every answer that retrieves it.",
                ],
            },
            {
                "title": "Defence in layers",
                "body": [
                    "No single trick stops injection. Layer them: **least-privilege tools**; **human approval** for actions with side effects; keep untrusted content clearly separated from instructions; **validate outputs** before acting on them; allowlist destinations; log every tool call; and never put secrets in a system prompt, because it can leak.",
                ],
            },
            {
                "title": "Test it like an attacker",
                "body": [
                    "Red-team your agents on a schedule, with a corpus that covers direct, indirect, encoding, multi-turn and tool-abuse attacks. The open-source `llm-injection-harness` (github.com/plalan/llm-injection-harness) runs 114 payloads across 14 categories, with an adaptive attacker mode. Run it before every release, like any other test suite.",
                ],
            },
        ],
        "lab": {"type": "inject", "title": "Injection Spotter",
                "intro": "Each card is something an agent might read. Decide: safe, or an injection attempt? Watch for the indirect ones."},
        "quiz": [
            {"q": "Indirect prompt injection arrives through…",
             "options": ["The user's typed message only", "Content the agent reads: documents, web pages, email, tool output", "The GPU", "Docker logs"],
             "answer": 1, "why": "The attacker plants instructions in data the agent will later ingest."},
            {"q": "'Excessive agency' means…",
             "options": ["The agent is too slow", "The agent has more permissions or autonomy than its job needs", "Too many agents", "High temperature"],
             "answer": 1, "why": "Over-permissioned agents turn a successful injection into real damage."},
            {"q": "The strongest mitigation for risky actions?",
             "options": ["A longer system prompt", "Least privilege plus human approval", "Higher temperature", "More chunks"],
             "answer": 1, "why": "Limit what the agent can do, and require a human for actions with side effects."},
            {"q": "Why is RAG a poisoning risk?",
             "options": ["Vectors are insecure by nature", "Attacker-controlled documents can be retrieved straight into the model's context", "Chroma is closed source", "It isn't"],
             "answer": 1, "why": "Whatever gets ingested can later be retrieved and treated as trusted context."},
            {"q": "Is the system prompt a security boundary?",
             "options": ["Yes, it's hidden", "No. Assume it can leak and keep secrets out of it", "Only for small models", "Only in Docker"],
             "answer": 1, "why": "System prompts are routinely extracted. Never rely on them to protect secrets."},
        ],
    },
]

CAPSTONES = [
    {
        "id": "cap1", "title": "Datasheet Q&A with citations", "icon": "📄",
        "goal": "A RAG assistant over a set of product datasheets that answers with sources.",
        "steps": ["Put the datasheets in knowledge/my-docs and re-index",
                  "Answer with hybrid retrieval and cite the source of every claim",
                  "Write 10 test questions with known answers",
                  "Measure recall@5 and fix the misses"],
    },
    {
        "id": "cap2", "title": "Self-checking research agent", "icon": "🔁",
        "goal": "A LangGraph agent that plans, searches, grades its own evidence and retries before answering.",
        "steps": ["Define the state and 4 nodes: plan, search, grade, answer",
                  "Add a conditional retry edge with a hop limit",
                  "Add a checkpointer and a thread_id",
                  "Add a human approval interrupt before any external action"],
    },
    {
        "id": "cap3", "title": "Presales brief crew", "icon": "🧑‍💼",
        "goal": "A CrewAI crew that turns a company name into a one-page executive brief.",
        "steps": ["Researcher, solution architect, writer and reviewer agents",
                  "Tasks with sharp expected_output fields",
                  "Run it on local llama3.1 via Ollama",
                  "Compare sequential vs hierarchical output and cost"],
    },
    {
        "id": "cap4", "title": "Ship it, securely", "icon": "🔐",
        "goal": "Your agent as a FastAPI + Docker service that survives your own injection harness.",
        "steps": ["FastAPI endpoint with health check and timeouts",
                  "Dockerfile with cached dependency layer, added to compose",
                  "API key + rate limit on the endpoint",
                  "Run llm-injection-harness and reach a resilience score of 80%+"],
    },
]

# ---------------------------------------------------------------------------
# Level and outcome for each module (shown on cards and in the path builder)
# ---------------------------------------------------------------------------
_META = {
    "intro":     ("Beginner",     "Explain what an AI agent is and how it differs from a chatbot."),
    "python":    ("Beginner",     "Turn a Python function into a tool a model can call."),
    "langchain": ("Beginner",     "Write prompts and chain them into a working pipeline."),
    "vectors":   ("Intermediate", "Explain embeddings, and choose a chunk size and a vector store."),
    "rag":       ("Intermediate", "Build retrieval that finds the right text, and know how to test it."),
    "agents":    ("Intermediate", "Design a tool-using agent loop with sensible guardrails."),
    "langgraph": ("Advanced",     "Model an agent as a state graph with branches, loops and checkpoints."),
    "crewai":    ("Advanced",     "Staff a multi-agent crew, and know when not to."),
    "ship":      ("Intermediate", "Package an agent as an API inside a Docker container."),
    "security":  ("Intermediate", "Spot prompt injection and layer defences around an agent."),
}
for _m in MODULES:
    _m["level"], _m["outcome"] = _META[_m["id"]]

# ---------------------------------------------------------------------------
# Onboarding: two questions → a recommended path (nothing is ever hidden)
# ---------------------------------------------------------------------------
ONBOARDING = {
    "questions": [
        {"id": "level", "q": "Where are you starting from?", "options": [
            {"id": "new",   "icon": "🌱", "label": "New to AI and coding",        "hint": "Student, manager, or just curious"},
            {"id": "coder", "icon": "💻", "label": "I can code, LLMs are new",     "hint": "Comfortable with Python or similar"},
            {"id": "llm",   "icon": "🚀", "label": "I've built with LLMs",         "hint": "Prompts and APIs yes, agents not yet"},
        ]},
        {"id": "goal", "q": "What do you want out of this?", "options": [
            {"id": "understand", "icon": "💡", "label": "Understand how agents work", "hint": "Concepts first, light on code"},
            {"id": "build",      "icon": "🛠️", "label": "Build agents myself",        "hint": "The full hands-on route"},
            {"id": "secure",     "icon": "🛡️", "label": "Secure and test agents",     "hint": "Attack surface and defences"},
            {"id": "ship",       "icon": "🚢", "label": "Ship one to production",     "hint": "APIs, containers, checklists"},
        ]},
    ],
    # paths[level][goal] → ordered module ids
    "paths": {
        "new": {
            "understand": ["intro", "langchain", "rag", "agents", "security"],
            "build":      ["intro", "python", "langchain", "vectors", "rag", "agents", "langgraph"],
            "secure":     ["intro", "langchain", "rag", "agents", "security"],
            "ship":       ["intro", "python", "langchain", "agents", "ship"],
        },
        "coder": {
            "understand": ["intro", "langchain", "rag", "agents", "langgraph", "security"],
            "build":      ["python", "langchain", "vectors", "rag", "agents", "langgraph", "crewai"],
            "secure":     ["langchain", "rag", "agents", "langgraph", "security"],
            "ship":       ["langchain", "agents", "ship", "security"],
        },
        "llm": {
            "understand": ["agents", "langgraph", "crewai", "security"],
            "build":      ["rag", "agents", "langgraph", "crewai", "ship"],
            "secure":     ["agents", "langgraph", "security"],
            "ship":       ["agents", "ship", "security"],
        },
    },
    "capstone_for_goal": {"build": "cap2", "secure": "cap4", "ship": "cap4"},
}
