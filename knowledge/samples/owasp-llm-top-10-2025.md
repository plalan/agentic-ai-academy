# OWASP Top 10 for LLM Applications (2025) — summary notes

A plain-language summary of the ten risk categories in the OWASP Top 10 for Large Language Model Applications, 2025 edition. See the OWASP GenAI Security Project for the full text.

## LLM01: Prompt Injection

Inputs that change the model's behaviour in ways the developer did not intend. Direct injection comes from the user's own message. Indirect injection hides instructions in content the model reads, such as web pages, documents, emails or tool outputs.

## LLM02: Sensitive Information Disclosure

The model reveals personal data, credentials, confidential business data or proprietary details through its answers. Limit what data the model can access and filter what it returns.

## LLM03: Supply Chain

Risks from third-party models, datasets, plugins and libraries, including tampered model weights and vulnerable dependencies.

## LLM04: Data and Model Poisoning

Training, fine-tuning or embedding data is manipulated to plant backdoors, biases or false behaviour.

## LLM05: Improper Output Handling

Model output is passed to other systems without validation, leading to problems such as cross-site scripting, SQL injection or command execution.

## LLM06: Excessive Agency

An agent has more functions, permissions or autonomy than its job needs, so a manipulated model can take damaging actions. Mitigate with least privilege and human approval for high-impact actions.

## LLM07: System Prompt Leakage

System prompts are extracted by users. Never place secrets, credentials or security controls in a system prompt.

## LLM08: Vector and Embedding Weaknesses

Risks in retrieval-augmented generation: poisoned documents in the vector store, data leaking across tenants, and embedding inversion.

## LLM09: Misinformation

The model produces false or misleading content that appears credible, including hallucinated facts, sources and code packages.

## LLM10: Unbounded Consumption

Uncontrolled use of the model leads to denial of service, runaway costs or model extraction. Use rate limits, quotas and timeouts.
