# Designing APIs and Tools for AI Agents vs Human Developers: Current Thinking and Debates (2024 to October 2026)

> Method note for the report writer: The egress proxy blocked direct page fetches for most domains in this session. Only anthropic.com pages could be fetched and read in full. Everything else (Cloudflare, Vercel, GitHub changelog, Postman, Simon Willison, Armin Ronacher, Mario Zechner, Kin Lane, Nordic APIs, Thoughtworks and others) comes from search-engine result summaries and excerpts that pointed at the cited URLs. Treat exact quotes from non-Anthropic sources as "reported" rather than verified verbatim. Evidence labels used below: **[EVAL]** means vendor-run evals or benchmarks with numbers; **[PRACTITIONER]** means a production experience report with some numbers; **[OPINION]** means an argument or position with no measurement.

## Q1. What concrete guidance exists for designing tools and APIs for agents?

### Takeaway
By late 2025 the main vendors and practitioners had converged on a clear set of principles: few task-level tools rather than one tool per endpoint; namespaced, unambiguous names; descriptions written as prompts; high-signal, token-budgeted responses (with pagination, truncation and a concise/detailed switch); human-readable IDs; and errors that tell the agent what to do next. Anthropic's Sept 2025 post is the most-cited source and is backed by internal evals. Through 2026 the frontier moved from "design better tools" to "load fewer tool definitions and let the model write code against the API" (tool search, code mode, programmatic tool calling).

### Cited Findings

**Anthropic, "Writing effective tools for agents — with agents" (Ken Aizawa et al., Sept 11 2025)** — [EVAL, partly qualitative]
- Framing: tools are "a contract between deterministic systems and non-deterministic agents" and should not be designed like conventional APIs. Key line: "Agents are only as effective as the tools we give them." — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Consolidation: avoid tools that "simply wrap API endpoints". Build a few tools for high-impact workflows, e.g. `schedule_event` instead of separate list and create tools, `search_logs` instead of `read_logs`, and `get_customer_context` instead of several getters. "Too many tools or overlapping tools can also distract agents." — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Namespacing: prefix by service and resource (e.g. `asana_search`, `asana_projects_search`). Anthropic found that prefix vs suffix naming "had non-trivial effects" on its evals and advises testing it. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Meaningful context: return `name` and `file_type` rather than `uuid` or `mime_type`. Resolving UUIDs to natural-language names or 0-indexed IDs "reduced hallucinations and improved retrieval precision." — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- `response_format` enum (`"concise"` or `"detailed"`): in a Slack example, the detailed response was 206 tokens and the concise one was 72, about one-third. Use detailed only when the IDs are needed for follow-up calls. Response format (XML, JSON or Markdown) affects performance and should be tested. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Token efficiency: use pagination, range selection, filtering, truncation and sensible defaults. Claude Code caps tool responses at 25,000 tokens by default. When truncating, tell the agent how to narrow its query. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Errors: replace opaque codes and tracebacks with specific, actionable guidance, with correctly formatted examples. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Descriptions as prompts: describe a tool "as you would to a new hire". Use unambiguous parameter names (`user_id` rather than `user`), strict data models, and MCP annotations that flag destructive or open-world tools. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Evidence: Claude Sonnet 3.5 reached state of the art on SWE-bench Verified after "precise refinements to tool descriptions". No exact score is given. Claude-optimised Slack and Asana MCP servers sometimes beat expert-written ones on held-out test sets (shown in charts, with no numbers in the text). A web-search tool description fix stopped Claude from needlessly adding "2025" to queries. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Method: prototype as a local MCP server, write realistic multi-call eval tasks, use lenient verifiers, and track accuracy, runtime, call counts, tokens and errors. Then feed the transcripts back to Claude to improve the tools, using held-out sets to avoid overfitting. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)

**Anthropic, "Effective context engineering for AI agents" (Sept 29 2025)** — [OPINION, informed by internal experience]
- Curate "a minimal viable set of tools". "Bloated tool sets that cover too much functionality" are a common failure mode. The heuristic: "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better." Tools should be "self-contained, robust to error, and extremely clear with respect to their intended use". Prefer "lightweight identifiers" and just-in-time loading over preloading data. — [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Anthropic, "Code execution with MCP" (Adam Jones and Conor Kelly, Nov 4 2025)** — [EVAL, single illustrative example]
- Argument: loading every tool definition and passing intermediate results through the model does not scale. "Agents scale better by writing code to call tools instead." — [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)
- Pattern: present MCP tools as a filesystem of code files (e.g. `servers/salesforce/updateRecord.ts`), add a `search_tools` function with a detail-level parameter, and filter or aggregate data in the sandbox. Example: the agent sees 5 rows of a 10,000-row sheet. Save reusable functions as Skills (SKILL.md). The MCP client can tokenise PII (`[EMAIL_1]`) so the model never sees it. — [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)
- Number: about 150,000 tokens fell to about 2,000 tokens ("98.7%") in one Google Drive-to-Salesforce example. That is one illustration, not a benchmark. Caveat: code execution "introduces its own complexity" and needs sandboxing, resource limits and monitoring. — [Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)

**Anthropic, "Introducing advanced tool use" (Nov 24 2025, beta)** — [EVAL]
- Token overhead: a typical five-server setup (GitHub 35 tools at about 26K tokens, Slack 11 at about 21K, Sentry, Grafana, Splunk) totals 58 tools and about 55K tokens. Adding Jira (about 17K) takes it past 100K. Anthropic has seen definitions take "134K tokens before optimization". — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- Tool Search Tool (`defer_loading`): about 85% fewer tokens. On MCP evals, Opus 4 rose from 49% to 74% and Opus 4.5 from 79.5% to 88.1%. Recommended when definitions exceed about 10K tokens or there are 10 or more tools. — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- Programmatic Tool Calling: average tokens fell from 43,588 to 27,297 (37%) on complex research tasks, with modest accuracy gains (GIA 46.5% to 51.2%). — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- Tool Use Examples (sample calls embedded in definitions): accuracy rose from 72% to 90% on complex parameter handling in internal tests. Useful where JSON Schema cannot express usage conventions. — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)

**Cloudflare "Code Mode"** — [EVAL, vendor numbers]
- The original post, "Code Mode: the better way to use MCP" (Sept 26 2025), opens: "It turns out we've all been using MCP wrong." Its approach converts MCP tools into a TypeScript API and lets the model write code against it, run in a Workers sandbox through Dynamic Worker Loading. The post was not retrieved; this is per the search excerpt and Kenton Varda's thread. — [Cloudflare blog listing](https://www.blog.cloudflare.com/author/sunil); [Kenton Varda thread](https://threadreaderapp.com/user/KentonVarda)
- Cloudflare's docs give the rationale that models have seen "millions of lines of real-world code" but only contrived tool-calling examples. They say Code Mode is best for chaining calls, composition and multi-step workflows, and that simple single calls are fine with normal tool calling. — [Cloudflare docs](https://developers.cloudflare.com/agents/api-reference/codemode)
- Follow-up post, "Code Mode: give agents an entire API in 1,000 tokens" (Feb 2026; covered by InfoQ in Apr 2026): the whole Cloudflare API is exposed through two tools, `search()` (the agent queries the OpenAPI spec with JS) and `execute()`. Cloudflare reports about 1.17M tokens for a conventional MCP server versus about 1,000 tokens, a 99.9% cut. A third party puts the naive baseline at about 244K tokens. The API token is kept out of the code isolate. — [Cloudflare blog](https://blog.cloudflare.com/code-mode-mcp/); [InfoQ](https://www.infoq.com/news/2026/04/cloudflare-code-mode-mcp-server/); [cloudflare/mcp AGENTS.md](https://github.com/cloudflare/mcp/blob/main/AGENTS.md)
- Cloudflare's MCP server portals added a code-mode "search and execute" option (changelog dated Mar 26 2026). — [Cloudflare changelog](https://developers.cloudflare.com/changelog/post/2026-03-26-mcp-portal-code-mode/index.md); [Cloudflare enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/)

**Block, "Playbook for Designing MCP Servers" (June 16 2025; based on 60+ internal MCP servers)** — [PRACTITIONER]
- Design workflow-first, working back from the job to be done rather than wrapping endpoints. Combine several internal API calls into one high-level tool. Avoid granular endpoints like `GET /user`, which give "verbose, poorly scoped outputs". Treat names, descriptions and parameters as prompts, and validate complex parameters with a schema library. — [Block Engineering](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)

**GitHub MCP server (Sam Morrow and GitHub changelog, Oct 2025 to Jan 2026)** — [PRACTITIONER, vendor numbers]
- GitHub tried toolsets and dynamic tool selection. Dynamic selection "worked well" but invalidated the model's prompt cache every time the tool set changed, so the team moved toward "progressive discovery" instead. It cut the default tool count by 49%, consolidated CRUD tools, and cut output tokens by more than 75% on tools like `list_pull_requests`. — [Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1)
- Consolidation examples: `create_issue` and `update_issue` merged into `issue_write` with a `method` parameter. The Projects toolset was cut to `projects_list`, `projects_get` and `projects_write`, saving about 23K tokens (50%). Loading just 3 to 10 frequently used tools gives an estimated 60 to 90% context reduction compared with the default toolsets. — [GitHub Changelog, Dec 10 2025](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/); [GitHub Changelog, Jan 28 2026](https://github.blog/changelog/2026-01-28-github-mcp-server-new-projects-tools-oauth-scope-filtering-and-new-features/); [GitHub Changelog, Oct 29 2025](https://github.blog/changelog/2025-10-29-github-mcp-server-now-comes-with-server-instructions-better-tools-and-more/)

**Vercel, "We removed 80% of our agent's tools" (about Dec 2025)** — [PRACTITIONER]
- Vercel's internal text-to-SQL agent d0 had specialised tools (schema lookup, query validation, error recovery) plus heavy prompt engineering. They were replaced with a single "execute bash" tool over a file-based semantic layer. Reported results: success rose from 80% to 100%, with fewer steps, about 37% fewer tokens (40% in a social post) and 3.5x faster responses. Malte Ubl summarised it as "Bash is all you need". The team describes the shift as from "tool-heavy" to "context-heavy" design. — [Vercel blog](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools); [Malte Ubl on X](https://x.com/cramforce/status/2003225558277345330)

**Neon** — [PRACTITIONER]
- "A raw REST operation is not automatically a good agent tool." Neon takes a hybrid approach: schemas generated from OpenAPI give broad Management API coverage, and 19 hand-written opinionated tools handle workflows such as running SQL and safe migrations. An earlier Neon post on auto-generating MCP from OpenAPI concluded that effective MCP design means "thinking about the workflows you want the agent to perform". — [Neon blog](https://neon.com/blog/give-your-agent-neon-tools); [Neon: Auto-generating MCP servers from OpenAPI](https://neon.com/blog/autogenerating-mcp-servers-openai-schemas); [John Maeda notes on Neon/MCP and AX, June 2025](https://maeda.pm/2025/06/23/learnings-from-neon-mcp-and-ax/)

**OpenAI function-calling guide** — [OPINION/vendor guidance; seen only via mirrors]
- "Aim for fewer than 20 functions at any one time, though this is just a soft suggestion." Evaluate performance at different function counts, "always enable" `strict: true` structured outputs, and add examples and edge cases to descriptions. This was seen through a mirror of OpenAI's guide, not the official page. — [mirror of OpenAI guide](https://docs.apiyi.com/en/api-capabilities/openai/function-calling)

**Google Gemini function calling** — [OPINION/vendor guidance]
- Official docs ask for a "comprehensive" description of each function's purpose and a clear purpose and format for each parameter. — [Google AI docs](https://ai.google.dev/docs/function_calling)
- A third-party Gemini guide advises the opposite of GitHub's consolidation: each function should "do one thing well", without combined "manage" create/update/delete functions. This is an unresolved tension (see Inferences). — [gemini_ex guide](https://hexdocs.pm/gemini_ex/function_calling.html)

**"Agent Experience" (AX) as a term** — [OPINION]
- Netlify CEO Mathias (Matt) Biilmann coined "AX" in January 2025 ("Introducing AX"). It covers how well agents can find a service, call it reliably and recover from failures, as distinct from DX for human developers. A "One Year of AX" follow-up came in January 2026. — [Netlify](https://www.netlify.com/agent-experience/); [ShiftMag](https://shiftmag.dev/agent-experience-ax-5045/)

**Safety and destructive actions**
- Anthropic recommends MCP tool annotations to flag destructive or open-world tools. — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- The MCP spec of 2025-11-25 added URL-mode elicitation, which sends the user to a browser for sensitive steps (OAuth, API keys) so the client never handles the secrets. It also added experimental durable "Tasks" for long-running work with polling (SEP-1686). The 2026-07-28 revision makes MCP stateless, removes the initialize handshake, and changes how URL elicitation completion is signalled (the client retries the original request). — [WorkOS on 2025-11-25 spec](https://workos.com/blog/mcp-2025-11-25-spec-update); [MCP changelog 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/changelog); [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)

### Inferences
- The best-evidenced principles are tool consolidation and curation, token-budgeted responses, and deferred loading of tool definitions. Anthropic's tool-search numbers (49% to 74%, 79.5% to 88.1%) and GitHub's and Vercel's production numbers all support them, though every number is vendor-reported and none is independently replicated.
- "Meaningful IDs over UUIDs", `response_format`, and "actionable errors" rest mainly on Anthropic's qualitative eval claims, with no published effect sizes. They are sensible but less quantified.
- There is a real tension between "consolidate CRUD into one tool with a method param" (GitHub's `issue_write`) and "one function, one job" (Gemini community guidance) and least-privilege safety. Consolidated write tools mix destructive and non-destructive operations, which makes per-tool approval and annotations coarser.
- Idempotency keys and dry-run modes appear far less in agent-specific guidance than in classic API design literature. I found no eval-backed source on them for agents (see Gaps).

### Gaps
- Could not retrieve the full text of Cloudflare's Sept 2025 Code Mode post, Block's playbook, Vercel's post or the OpenAI and Google official guides. Their quotes are from search summaries.
- No source found with eval evidence specifically for idempotency keys, dry-run or preview modes, or confirmation patterns for destructive agent actions beyond MCP annotations and elicitation.
- No Stripe primary engineering post on MCP or agent toolkit design was found; only Scalekit's third-party comparison ([Scalekit](https://www.scalekit.com/blog/stripe-mcp-vs-api)).

## Q2. The "CLI vs MCP vs API" debate: arguments, shifts over time, and evidence

### Takeaway
Sentiment ran in three phases. Early 2025 was the MCP hype phase. From mid-2025 into the first half of 2026 came a strong "MCP is overkill, just use CLIs, scripts and Skills" backlash, driven by token overhead and coding agents' fluency with bash (Ronacher, Zechner, Willison, Holmes, Vercel, and Perplexity's March 2026 move). By the second half of 2026 the views were converging: the protocol survives, but as a code-mode or search-based backend with progressive disclosure. CLIs and Skills win for local coding agents, while MCP is kept for governed, remote, authenticated or non-coding contexts. The emblem of this shift is Pi 1.0 (Oct 1 2026), the "anti-MCP" agent, adding MCP support through Codemode.

### Cited Findings

**Pro-CLI, scripts and code side**
- Armin Ronacher, "Tools: Code Is All You Need" (July 3 2025): MCP is not truly composable ("most composition happens through inference"), and it "demands too much context". He used only one MCP server (Playwright) and CLIs for everything else. — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/7/3/tools/) [OPINION]
- Ronacher, "Your MCP Doesn't Need 30 Tools: It Needs Code" (Aug 18 2025): proposes MCP servers that expose a single tool accepting code. He also concedes CLI problems: CLIs are platform-dependent, version-dependent and sometimes undocumented. — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/8/18/code-mcps/) [OPINION]
- Mario Zechner, "What if you don't need MCP at all?" (Nov 2 2025): replaces browser MCP servers with a README plus four small Puppeteer Node scripts invoked through bash. A tool inspired by the post cites 13.7K tokens (Playwright MCP) and 18.0K tokens (Chrome DevTools MCP) loaded per session. — [mariozechner.at](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/); [HN discussion](https://news.ycombinator.com/item?id=45947444); [browse-tool README](https://github.com/nino-chavez/browse-tool) [OPINION + rough numbers]
- Simon Willison, "Claude Skills are awesome, maybe a bigger deal than MCP" (Oct 16 2025): MCP's high token usage is its "most significant limitation". He said he had mostly stopped using MCP for coding agents, preferring CLI utilities and libraries such as Playwright Python. — [Techmeme summary of Willison post](https://www.techmeme.com/251017/p14); [Willison on X](https://x.com/simonw/status/1978935386496995811) [OPINION]
- Eric Holmes, "MCP is dead. Long live the CLI" (Feb 28 2026, top of HN): "LLMs are really good at using command-line tools. They've been trained on millions of man pages, Stack Overflow answers, and GitHub repos full of shell scripts." Complaints reported: context cost, debuggability, composability, auth friction and operational overhead. — [summary/translation](https://velog.io/@surim014/mcp-is-dead-long-live-the-cli); [Is MCP dead? analysis](https://mcpplaygroundonline.com/blog/is-mcp-dead-cli-debate) [OPINION]
- Perplexity CTO Denis Yarats, Ask 2026 conference (Mar 11 2026), reportedly said Perplexity is moving away from MCP internally toward direct APIs and CLIs, citing schema context cost and auth friction. Perplexity still hosts a public MCP server. The widely repeated "72% context waste" figure is not Perplexity's own: it comes from Apideck (3 MCP servers, about 40 tools, about 143K of 200K tokens), a worst case. — [agent-engineering.dev](https://www.agent-engineering.dev/article/why-perplexity-is-stepping-back-from-the-model-context-protocol-mcp-internally); [Aakash Gupta on X](https://x.com/aakashgupta/status/2031950037031510161); [Paweł Huryn on X](https://x.com/PawelHuryn/status/2032360024589164929) [secondary reports]
- "Why MCP was always a bad idea" (around Sept 20 2026, HN): agents now write scripts, call HTTP APIs directly and discover CLIs through `--help`, so the post argues for standardising on plain HTTP APIs and CLIs. — [zeli.app aggregator](https://zeli.app/es/story/49779329) [OPINION; original author not verified]

**Benchmarks (all vendor or third party; none peer-reviewed)**
- Scalekit (2026): 75 runs on Claude Sonnet 4 compared the `gh` CLI with GitHub's MCP server. Success was 100% for the CLI and 72% for MCP; 7 of 25 MCP runs failed, mostly from timeouts and remote server issues. MCP used 4 to 32x more tokens. On the simplest task the CLI used 1,365 tokens and MCP 44,026, mostly schema overhead (43 tool definitions injected, 1 or 2 used). A secondary summary says an 800-token markdown "gh tips" skill outperformed 28K tokens of MCP schemas. The reported tool count conflicts (43 vs 93). Critics say the failures were infrastructure problems, not protocol problems. — [Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use); [Firecrawl summary](https://www.firecrawl.dev/blog/mcp-vs-cli) [EVAL, small n]
- Arize (2026): Claude Opus 4.6 in the Claude Agent SDK on GitHub tasks, 500 trials across MCP, Skills, CLI and baseline arms. Correctness was tightly clustered: MCP 0.834, skill variants 0.826 and 0.833, and bare-Claude baseline 0.845. Skills beat the baseline on cost and latency. On the hardest tier MCP reportedly cost more than 6x the skills and took 5x longer. Arize's conclusion: "the question was wrong". Use MCP for querying data, skills for doing work, and the CLI for scripting and CI. — [Arize](https://arize.com/blog/mcp-vs-cli-skills-for-agents-what-our-eval-found-and-which-you-should-use/) [EVAL]
- Vercel d0: replacing specialised tools with bash raised success from 80% to 100% and used about 37 to 40% fewer tokens. — [Vercel](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools) [PRACTITIONER]

**Pro-MCP and middle-ground side**
- Sam Morrow (GitHub), "MCP Doesn't Have a Context Problem": critics conflate "the laziest possible MCP implementation with the protocol itself". Progressive discovery fixes the token problem. — [sam-morrow.com](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1) [OPINION + GitHub numbers]
- Charles Chen, "MCP is Dead; Long Live MCP!" (Mar 2026): MCP is the wrong choice for a class of use cases, but "there is a deep misunderstanding of where and how CLI tools can yield savings". — [chrlschn.dev](https://chrlschn.dev/blog/2026/03/mcp-is-dead-long-live-mcp/) [OPINION]
- Simon Willison, HN comment (Sept 2026): for a full terminal agent with unrestricted internet access "there's almost no reason to use MCPs". But for tightly controlled agents MCP helps control which services are reachable, keeps API keys away from the agent, and supports audit logging. "Thinking MCP is obsolete because full coding agents don't need it misses out on all of the other things we might want to build." — [simonwillison.net](https://simonwillison.net/2026/Sep/20/hn-49779718/) [OPINION; this shows his own view softening]
- Security and governance: the CLI has no integration layer and "inherits whatever ambient permissions the shell user has". The services most business users need do not have CLIs. — [palma.ai](https://palma.ai/blog/mcp-vs-cli-not-the-same-thing); [repello.ai](https://repello.ai/blog/mcp-vs-cli) [OPINION]
- Kin Lane, "Agents Should Write Code to Integrate, Not Infer It at Runtime" (Sept 1 2026): have agents author deterministic, reviewable, testable integration code once rather than reinterpreting API responses at runtime through MCP each time. "Spend the model's intelligence on authoring, not on interpreting the same response for the ten-thousandth time." — [API Evangelist](https://apievangelist.com/2026/09/01/agents-should-write-code-to-integrate-not-infer/) [OPINION]

**Convergence: code mode and Skills as the synthesis (late 2025 to Oct 2026)**
- Anthropic launched Agent Skills (SKILL.md folders with progressive disclosure: name and description at startup, full body on match, scripts on demand) in Oct 2025. It was released as an open standard at agentskills.io (reportedly Dec 2025), with reported adoption by OpenAI Codex, Cursor, GitHub Copilot and others. Adoption counts vary, from about 25 to 40+ platforms. — [agentskills.io](https://agentskills.io/); [codeagentsalpha guide](https://codeagentsalpha.substack.com/p/claude-agent-skills-complete-getting); [inference.sh](https://inference.sh/blog/skills-agent-skills-overview)
- Pi 1.0 (Oct 1 2026), the coding agent associated with Zechner (acquired by Ronacher's company Earendil in April 2026), reversed its long-standing refusal to support MCP. It adds MCP support through "Codemode": one tool runs model-written JS in a sandbox (reportedly QuickJS) and only the script's output returns to the model. Ronacher's "What is Codemode" (Oct 6 2026) revisits his earlier scripts-over-MCP advice. Open issues he flags: MCP servers often do not target codemode-aware harnesses, nested codemode-in-MCP is awkward, and durability and binary data remain unsolved. — [The Register, Oct 2 2026](https://www.theregister.com/ai-and-ml/2026/10/02/pi-coding-agent-pulls-a-180-and-adds-mcp-support/5300678); [lucumr.pocoo.org](https://lucumr.pocoo.org/2026/10/6/codemode/); [daily.dev summary](https://daily.dev/posts/what-is-codemode-sldlxw1ny)
- Kin Lane's Oct 6 2026 post "Twenty-Four Agent Bundles And Not One MCP Server" counts 24 agent integration bundles from one vendor, none of which included an MCP server. Lane calls this unanimous. — [API Evangelist](https://apievangelist.com/2026/10/06/twenty-four-agent-bundles-and-not-one-mcp-server/)

### Inferences
- Both sides largely accept the token-overhead facts. The disagreement is about whether that overhead is intrinsic to MCP or an artefact of naive servers and clients. Tool search, `defer_loading`, code mode and GitHub's consolidation all cut overhead by 50 to 99.9% per the vendors, which undercuts the "intrinsic" claim.
- The CLI advantage is strongest for local coding agents with shell access and well-known CLIs in their training data (`gh`, `git`, `kubectl`). It is weakest for remote or SaaS integrations without CLIs, for multi-tenant auth, and for governed enterprise agents where credential isolation and audit matter.
- For API providers in 2026 the practical takeaway is to ship several surfaces from one well-described API. These include a good CLI with `--help` and JSON output, an OpenAPI spec usable by code-mode search, Skills or markdown docs, and optionally a curated or code-mode MCP server.
- The evidence base is thin: Scalekit had 75 runs on one model and one task family, and Arize had 500 trials on GitHub tasks. Correctness differences in the larger Arize eval were small, which suggests the main difference is cost and latency rather than success rate.

### Gaps
- Could not verify Eric Holmes's original post text, the exact Perplexity statements (only secondary reports), or the original author of "Why MCP was always a bad idea".
- No independent, multi-model benchmark comparing CLI, MCP, code mode and Skills across diverse (non-GitHub) tasks was found.

## Q3. Is "just wrap your OpenAPI as MCP" good or bad practice? Tool-count limits and dynamic tool loading

### Takeaway
There is a strong consensus that a 1:1 endpoint-to-tool wrapper is a poor final design. Thoughtworks put "naive API-to-MCP conversion" on Hold (Nov 2025), and Anthropic, Block, FastMCP's author, Neon, Erik Wilde and Nordic APIs all argue against it. Generating from OpenAPI is still widely accepted as a starting point to be curated, or as the backing catalogue for search, execute or code-mode servers. In code mode the OpenAPI spec itself becomes the agent's discovery surface. Tool-count guidance is soft: OpenAI says under about 20, and Anthropic recommends tool search above about 10 tools or 10K tokens of definitions.

### Cited Findings
- Thoughtworks Technology Radar Vol. 33 (Nov 2025) put "naive API-to-MCP conversion" in **Hold**: "We advise against this naive API-to-MCP conversion". Its reasons: APIs designed for human developers consist of "granular, atomic actions" that drive up tokens and degrade agent performance when chained, and internal APIs can expose sensitive data or destructive operations with no "reliable, deterministic safeguard". It recommends a dedicated, secure MCP server built on existing APIs, and names MCP link and FastAPI-MCP as conversion tools. — [Thoughtworks Radar](https://www.thoughtworks.com/radar/techniques/naive-api-to-mcp-conversion) (localised copies such as [de-de](https://www.thoughtworks.com/de-de/radar/techniques/naive-api-to-mcp-conversion)) [expert OPINION]
- Jeremiah Lowin (FastMCP and Prefect), "Stop Converting Your REST APIs to MCP" and the AI Engineer 2025 talk "Your MCP Server is Bad (and You Should Feel Bad)": "stop thinking about endpoints and start thinking about products". FastMCP docs say "LLMs achieve significantly better performance with well-designed and curated MCP servers than with auto-converted OpenAPI servers". OpenAPI conversion is recommended for bootstrapping and prototyping, not for mirroring. Lowin describes an agent hallucinating a `get_all_users_with_blue_eyes` endpoint because 50 other user tools made it seem plausible. — [jlowin.dev](https://jlowin.dev/blog/stop-converting-rest-apis-to-mcp); [FastMCP OpenAPI docs](https://gofastmcp.com/v2/integrations/openapi); [AI Engineer talk](https://ai.engineer/talks/your-mcp-server-is-bad-and-you-should-feel-bad) [PRACTITIONER OPINION]
- Nordic APIs, "Why MCP Shouldn't Wrap an API One-to-One": an API with 200 endpoints becomes 200 tools, and "every extra endpoint is a tax paid in tokens and latency". — [Nordic APIs](https://nordicapis.com/why-mcp-shouldnt-wrap-an-api-one-to-one/) [OPINION]
- Counterpoint: one source reports that 76.5% of tool calls succeeded out of the box on generated servers, and generation is "easy to automate using OpenAPI". This source was not verified. — [agentpatterns.ai](https://agentpatterns.ai/standards/openapi-agent-tool-spec/) [weak EVAL]
- Neon follows the hybrid pattern: generated tools for broad coverage plus 19 hand-written workflow tools. — [Neon](https://neon.com/blog/give-your-agent-neon-tools)
- Anthropic: avoid tools that "simply wrap API endpoints". — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- Tool-count limits: OpenAI's guide says "Aim for fewer than 20 functions at any one time, though this is just a soft suggestion" ([mirror](https://docs.apiyi.com/en/api-capabilities/openai/function-calling)). Anthropic recommends Tool Search when there are 10+ tools or definitions over about 10K tokens ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)). GitHub cut its default tool count by 49%, and Scalekit's comparison cites a reduction to 52 default tools ([Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1); [web search summary of kaxil.substack](https://kaxil.substack.com/p/mcp-vs-cli-vs-rest)).
- Dynamic loading trade-off: GitHub found that dynamic tool selection invalidated prompt caching each time the tool list changed. Anthropic's `defer_loading` Tool Search is designed to keep definitions out of the prefix. — [Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1); [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)
- Code mode turns OpenAPI into an asset again. Cloudflare's `search()` tool lets the model query the full OpenAPI spec with JS, and `execute()` calls the API. The whole API fits in about 1,000 tokens of tool definitions. — [Cloudflare](https://blog.cloudflare.com/code-mode-mcp/)
- Erik Wilde: MCP will not fix a poorly designed API foundation, and a genuinely agent-friendly GitHub API "might also just have around 70 operations". — [Deep Engineering #48](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards) [OPINION]

### Inferences
- The answer to "wrap OpenAPI as MCP?" in 2026 depends on the architecture:
  - A classic tool-calling MCP server with 1:1 tools is bad practice.
  - A curated, task-level subset generated from OpenAPI is acceptable.
  - Exposing the full OpenAPI catalogue through search plus code execution (Cloudflare) is emerging best practice for large APIs.
- In all three cases, OpenAPI quality (descriptions, examples, operation summaries) is load-bearing because the agent reads it directly.

### Gaps
- No independent benchmark compares naive generated vs curated vs code-mode MCP servers for the same API.
- The publication date of Lowin's "Stop Converting..." post was not confirmed.

## Q4. How are classic API design principles being re-evaluated for agents?

### Takeaway
The agent shift has revived old ideas: hypermedia and HATEOAS, self-description, and rich OpenAPI descriptions with examples. It has also added new concerns: docs as an agent interface (llms.txt, markdown endpoints), token- or cost-based rate limiting, machine payments (x402), human approval through elicitation, and async tasks. Most of this is argued from first principles or by vendors. Only tool descriptions and examples have eval support, and llms.txt has evidence *against* its value for crawlers.

### Cited Findings

**Hypermedia / HATEOAS revival** [OPINION]
- Nordic APIs, "HATEOAS: The API Design Style That Was Waiting for AI": hypermedia addresses agent problems such as tool selection, context and runtime discovery. Mike Amundsen's GRAIL framework (Goal-Resolution through Affordance-Informed Logic) demonstrates hypermedia for AI agents. It lets agents "try things, fail gracefully, learn what's needed, and then continue on". A GRAIL client "can discover all this at runtime without any prior knowledge". — [Nordic APIs](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)
- Kin Lane: an AI agent navigating an API at runtime is "exactly the use case hypermedia was designed for". Hypermedia "was perhaps just early". — [API Evangelist hypermedia guidance](https://guidance.apievangelist.com/store/hypermedia/)
- Academic framing: "Revisiting Hypermedia, The Forgotten Web" (TechRxiv, Feb 11 2026). — [TechRxiv](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177078147.70240970)
- Counterpoint: Kin Lane's Sept 2026 position favours agents authoring deterministic code once over runtime inference. That cuts against fully runtime-driven hypermedia navigation for production integrations. — [API Evangelist](https://apievangelist.com/2026/09/01/agents-should-write-code-to-integrate-not-infer/)

**GraphQL for agents** [vendor OPINION]
- Apollo (March 2026 blog series) presents a typed GraphQL schema as the "data contract layer". It argues that introspection gives runtime discovery, and that field selection avoids over-fetching tokens. Apollo MCP Server exposes curated `.graphql` operations or persisted queries as typed MCP tools and validates each call against the schema. — [Apollo](https://apollographql.com/blog/building-a-secure-ai-agent-api-stack-with-graphql-apollo-skills-and-mcp-server); [Apollo](https://www.apollographql.com/blog/apollo-mcp-server/how-to-build-ai-agents-using-your-graphql-schema)
- No independent benchmark of GraphQL vs REST for agents was found.

**Rich OpenAPI and self-description** [mixed]
- Tool Use Examples raised accuracy from 72% to 90% on complex parameters (Anthropic internal). This is the strongest evidence that examples in specs and definitions matter. — [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use) [EVAL]
- Erik Wilde points to OpenAPI 3.2's hierarchical tags, which can link API elements to data dictionaries and ontologies. He argues agents struggle with ambiguous semantics and overlapping operations without machine-readable contracts and guardrails. — [Deep Engineering](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards) [OPINION]
- Erik Wilde's checklist at apidays London (Sept 2025) treats agents as another class of user: "provide operations that aggregate multiple steps into a single call", with flattened data structures. Jentic released an "AI-readiness" scoring tool for APIs, and Wilde presented a six-dimension AI-readiness scoring model at apidays Paris (Dec 2025). — [Ikenna newsletter](https://newsletter.ikenna.co.uk/p/issue-54-api-readiness-for-ai-a-seven-point-checklist); [API Platforms for Scale](https://www.apiplatformsforscale.com/p/heading-to-fost-apidays-paris-conference) [OPINION]

**Docs as interface: llms.txt and markdown docs**
- Crawler evidence is negative. Limy analysed 515M LLM-bot events over 90 days and found only 408 requests for `/llms.txt`. Ahrefs reportedly found that 97% of llms.txt files got zero requests across 137,210 domains (May 2026). SE Ranking found about 10% adoption across 300K domains. No study shows a citation or ranking effect, and Google says the file does nothing for Search. — [Limy](https://limy.ai/blog/llms-txt-in-2026-the-full-guide); [digitalapplied](https://www.digitalapplied.com/blog/llms-txt-in-practice-adoption-evidence-2026); [geoly.ai](https://www.geoly.ai/blog/does-llms-txt-work) [vendor data]
- Pieter Levels reportedly called MCP "just as useless of an idea as llms.txt" during the Feb 2026 debate. — [mcpplaygroundonline](https://mcpplaygroundonline.com/blog/is-mcp-dead-cli-debate)
- Netlify publishes a markdown twin of its AX page (`/agent-experience.md`), an example of the "markdown docs endpoint" pattern. — [Netlify .md](https://www.netlify.com/agent-experience.md)
- The pattern of a README plus small scripts (Zechner) and SKILL.md files (Anthropic) treats documentation itself as the agent's tool interface. — [mariozechner.at](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/); [agentskills.io](https://agentskills.io/)

**Rate limiting, quotas and bursty agent traffic** [vendor OPINION]
- Agent workflows chain 10 to 20 sequential calls, so one 429 can fail the whole task, and bursty agent traffic "can look like DDoS". Recommendations: token buckets, limits based on tokens, compute or cost rather than request counts, per-task spend caps, exponential backoff with jitter, retry budgets, and central quota coordination across agents. — [Zuplo](https://zuplo.com/learning-center/token-based-rate-limiting-ai-agents); [fast.io](https://fast.io/resources/ai-agent-rate-limiting/); [truto](https://truto.one/blog/how-to-handle-third-party-api-rate-limits-when-an-ai-agent-is-scraping-data/)
- Postman's 2025 survey found that "unauthorized or excessive API calls" by rogue agents are the top security worry (50.8%). See Q6. — [Postman 2025](https://www.postman.com/state-of-api/2025/)

**Pricing and payments for agent traffic** [mixed; volume figures unaudited]
- x402 (Coinbase whitepaper May 2025) revives HTTP 402 for per-call stablecoin payments. The x402 Foundation was announced by Coinbase and Cloudflare in Sept 2025 and formalised under the Linux Foundation in April 2026, with 22 members including AWS, Google, Microsoft, Stripe and Visa. Transaction-volume claims conflict (about 75M by Dec 2025 vs 119M+ on Base by Mar 2026). One tracker rates x402 "early production… still niche on the open web". — [blockeden](https://blockeden.xyz/blog/2026/04/01/x402-protocol-http-402-ai-agent-commerce-stablecoin-payments/); [21shares](https://www.21shares.com/fr/insights/http-402-ai-agent-payments); [Lumar agentic-readiness](https://agentic-readiness.lumar.io/docs/commerce/x402)
- Zdenek Nemec (Superface, Sept 2026): "agents will onboard into transactional APIs long before they onboard into Salesforce or a shipping company". Simple transactional APIs (weather, SMS) are easy for agents to buy and use, while enterprise onboarding is years away. — [API Evangelist conversation](https://conversations.apievangelist.com/store/2026-09-25-zdenek-nemec) [OPINION]

**Human in the loop, auth and async**
- MCP 2025-11-25 added URL-mode elicitation (out-of-band user consent and credential entry) and experimental Tasks for long-running work. The 2026-07-28 revision made the protocol stateless and changed how elicitation completion is signalled. — [WorkOS](https://workos.com/blog/mcp-2025-11-25-spec-update); [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- Willison's case for MCP in controlled agents rests on keeping API keys away from the agent, allow-listing reachable services and audit logging. He also coined "lethal trifecta" (June 2025) for agents that combine private data, untrusted content and external communication. — [simonwillison.net](https://simonwillison.net/2026/Sep/20/hn-49779718/)
- Stripe's MCP server supports both OAuth and restricted API keys as bearer tokens for headless agents. MCP cannot consume Stripe's event stream, so event-driven work stays on the API. — [Scalekit on Stripe](https://www.scalekit.com/blog/stripe-mcp-vs-api) [third party]

**Versioning and breaking changes with LLM consumers**
- No substantive source found (see Gaps).

### Inferences
- Hypermedia's revival is mostly a thought-leader argument. Code mode (the agent reads the OpenAPI spec and writes code) and Skills (the agent reads markdown) are what practitioners actually shipped in 2025–26. Both are forms of runtime self-description, but via documents and specs rather than in-band links.
- llms.txt's poor showing for *search crawlers* says little about *coding agents* fetching docs on demand. The 2025–26 data is about SEO crawlers, so the two use cases should not be conflated.
- Since agents re-read descriptions on every call, wording changes in tool descriptions effectively change behaviour. Anthropic's "2025" query bug is an example. This suggests description changes deserve change control like code, though I found no source formalising this.

### Gaps
- No credible source found on semantic versioning or breaking-change policy specifically for LLM consumers, e.g. whether description edits count as breaking changes.
- No eval-backed source found on agent-specific idempotency or dry-run designs.
- No independent data quantifying agent share of API traffic by provider (only Postman's "AI-related API calls" growth figure, via a secondary source, and single-company anecdotes).

## Q5. Views from API-community thought leaders and analysts

### Takeaway
The API establishment broadly says agents raise the bar on existing API design discipline rather than replace it: good contracts, governance, portals and workflows. They are generally sceptical that MCP alone fixes anything. Kin Lane is the most prolific voice: he runs MCP in production but favours deterministic agent-authored code, Skills and Arazzo workflows. Wilde stresses AI-readiness scoring and OpenAPI semantics. Amundsen champions affordances and hypermedia. Gartner's main quantified prediction dates from March 2024. For several named people (Lauret, Sturgeon, Higginbotham) I found no agent-specific statements.

### Cited Findings
- **Kin Lane (API Evangelist):**
  - July 22 2026: he runs MCP across his own properties as "one agent surface among several", alongside Agent Skills and Arazzo workflows. — [API Evangelist](https://apievangelist.com/2026/07/22/how-i-actually-use-mcp-across-api-evangelist/)
  - July 24 2026: governing what agents are allowed to consume is becoming mandatory. — [API Evangelist](https://apievangelist.com/2026/07/24/governing-what-agents-are-allowed-to-consume/)
  - Aug 26 2026: "Next MCP API Design". — [API Evangelist](https://apievangelist.com/2026/08/26/next-mcp-api-design/)
  - Sept 1 2026: agents should write code rather than infer integrations at runtime. — [API Evangelist](https://apievangelist.com/2026/09/01/agents-should-write-code-to-integrate-not-infer/)
  - Sept 25 2026: critiques the "We Are All In On Agentic" shame game. — [API Evangelist](https://apievangelist.com/2026/09/25/the-we-are-all-in-on-agentic-shame-game/)
  - Oct 6 2026: 24 agent bundles from one vendor, none with an MCP server. — [API Evangelist](https://apievangelist.com/2026/10/06/twenty-four-agent-bundles-and-not-one-mcp-server/)
  - May 2026 (New Stack interview): "The API portal is the clearest signal of whether your company can handle AI agents." — [The New Stack](https://thenewstack.io/mcp-api-governance-readiness/)
- **Erik Wilde** (Jentic; earlier listed at INNOQ and Axway):
  - API readiness for AI talk, apidays London (Sept 22–24 2025). — [Ikenna](https://newsletter.ikenna.co.uk/p/issue-54-api-readiness-for-ai-a-seven-point-checklist)
  - Six-dimension AI-readiness scoring model, apidays Paris (Dec 9–11 2025). — [API Platforms for Scale](https://www.apiplatformsforscale.com/p/heading-to-fost-apidays-paris-conference)
  - "MCP will not fix a poorly designed API foundation"; an agent-friendly GitHub API "might just have around 70 operations". — [Deep Engineering #48](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards); [Deep Engineering](https://deepengineering.substack.com/p/building-agent-ready-apis-in-production)
- **Mike Amundsen:**
  - GRAIL hypermedia-for-agents framework (see Q4). — [Nordic APIs](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)
  - Treblle webinar: AI agents, LLMs and MCP tools "are set to become the biggest API consumers we've ever seen". He co-authored the eBook "Preparing Your APIs for AI Agents". — [Treblle](https://treblle.com/blog/ai-api-design-mike-amundsen-webinar-takeways)
  - Forthcoming O'Reilly book "AI-Driven API Design" (2026), based on his workshops; O'Reilly course "Making Your APIs AI Ready". — [mamund Substack](https://mamund.substack.com/p/ai-driven-api-design-goes-on-the)
- **Kevin Swiber:** "MCP is not going to replace APIs". Secondary summary only. — [Zuplo MCP Week roundup](https://zuplo.com/blog/mcp-week-roundup)
- **Zdenek Nemec (Superface):**
  - "APIs for AI: Have We Failed?" talk, arguing we should "stop building APIs unless we change how we do it". — [SlideShare](https://www.slideshare.net/slideshow/apis-for-ai-have-we-failed-by-zdenek-nemec/272887081)
  - Sept 2026: transactional APIs first, enterprise agent onboarding years away. — [API Evangelist conversations](https://conversations.apievangelist.com/store/2026-09-25-zdenek-nemec)
  - Zuplo describes his MCP Week post as "sobering insights from real-world testing" of agents vs expectations. — [Zuplo](https://zuplo.com/blog/mcp-week-roundup)
- **Arnaud Lauret (API Handyman):** now an API industry researcher and governance lead at Postman. No agent-specific statements found. — [Nordic APIs speaker page](https://nordicapis.com/speakers/arnaud-lauret/); [Postman blog](https://blog.postman.com/why-this-api-handyman-joined-postman/)
- **Phil Sturgeon, James Higginbotham:** no agent- or MCP-specific positions found in searches.
- **Thoughtworks:** naive API-to-MCP conversion on Hold (Radar Vol. 33, Nov 2025). — [Thoughtworks](https://www.thoughtworks.com/radar/techniques/naive-api-to-mcp-conversion)
- **Gartner:**
  - Mar 20 2024: "more than 30% of the increase in demand for APIs will come from AI and tools using LLMs by 2026". — [Gartner](https://www.gartner.com/en/newsroom/press-releases/2024-03-20-gartner-predicts-more-than-30-percent-of-the-increase-in-demand-for-apis-will-come-from-ai-and-tools-using-llms-by-2026)
  - Aug 26 2025: 40% of enterprise apps will feature task-specific AI agents by end of 2026, up from under 5% in 2025. — [Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025)
  - "Predicts 2026: AI Agents, MCP and Governance Are Transforming Analytics" (Nov 19 2025). — [Gartner doc](https://www.gartner.com/en/documents/7197230)
  - "75% of API gateway vendors will integrate MCP features by end of 2026" is attributed to Gartner by Zuplo but not found in a Gartner release. Unverified. — [Zuplo](https://zuplo.com/blog/gartner-75-percent-api-gateways-mcp)
- **apidays:** London 2025 (Sept 22–24) and Paris (Dec 9–11 2025) featured AI-readiness talks (Wilde). — [apidays London 2025 archive](https://www.apidays.global/archive/2025/london)

### Inferences
- The API community's distinctive contribution is governance: which agents may consume what, plus portals, contracts and workflows (Arazzo). AI-lab and tooling voices focus on token efficiency and model ergonomics. A report could frame these as complementary "outside-in" (API provider) and "inside-out" (agent builder) perspectives.
- Lane's 2026 stance, which tests whether agents can write deterministic code, aligns with Anthropic's, Cloudflare's and Ronacher's code-execution direction. This is an unusual convergence of the API-establishment and AI-tooling camps.

### Gaps
- Could not find agent-specific positions from Phil Sturgeon, James Higginbotham or Arnaud Lauret, nor any Forrester position.
- Postman CEO Abhinav Asthana's quotes on the 2025 report could not be retrieved; the Business Wire page was unreachable.
- No apidays 2026 talk list was retrieved.

## Q6. Survey data on agents and APIs

### Takeaway
Postman's 2025 State of the API report (Oct 8 2025; 5,700+ respondents) is the main quantitative source. About 24% of developers design APIs with agents in mind, about 70% are aware of MCP but only 10% use it regularly, and rogue or excessive agent calls are the top security concern (about 51%). A 2026 Postman report is reported second-hand with 40% YoY growth in AI-related API calls, but its figures could not be verified against Postman.

### Cited Findings
- Postman 2025 State of the API (7th annual; published Oct 8 2025; over 5,700 respondents):
  - 24.3% of developers design APIs with AI agents in mind: 35% in APAC vs 22% elsewhere.
  - 89% use generative AI tools.
  - 50.8% cite unauthorised or excessive agent API calls as the top security worry.
  - 49% worry about AI accessing sensitive data, and 45.95% about AI leaking credentials.
  - — [Business Wire press release](https://secure.businesswire.com/news/home/20251008162423/en/One-in-Four-Developers-Now-Design-APIs-for-AI-Agents-According-to-Postmans-2025-State-of-the-API-Report); [Nordic APIs deep dive](https://nordicapis.com/a-deep-dive-into-the-state-of-the-api-2025/); [iTWire](https://itwire.com/it-industry-news/market/asia-pacific-%e2%80%98leads-the-rest-of-the-world-as-the-most-ai-ready-software-market%e2%80%99-report)
- MCP awareness and use: 70% aware, 10% using regularly. — [Postman 2025 report page](https://www.postman.com/state-of-api/2025/); [PDF](https://voyager.postman.com/doc/postman-state-of-the-api-report-2025.pdf)
- "2026 Postman State of the API" (secondary, Levo):
  - 40% YoY growth in AI-related API calls.
  - 24% design for agents.
  - "two thirds" aware of MCP, 10% regular use, 24% planning to explore.
  - Stale docs and weak testing are not improving.
  - The MCP numbers duplicate 2025's, so verification is needed. — [Levo](https://www.levo.ai/resources/blogs/postman-state-of-api-report)
- MCP ecosystem scale (single secondary blog, unverified): 97M+ monthly SDK downloads, 5,800+ verified servers, and Linux Foundation governance. — [agentmarketcap](https://agentmarketcap.ai/blog/2026/04/13/perplexity-abandons-mcp-rest-api-protocol-debate-2026)
- Security vendor 1H 2026 report: 48.9% of organisations are "entirely blind" to machine-to-machine traffic. — [Security Boulevard](https://securityboulevard.com/2026/04/the-era-of-agentic-security-is-here-key-findings-from-the-1h-2026-state-of-ai-and-api-security-report/)
- Single-platform anecdote: 79% of posts on PostEverywhere were created through its API or MCP rather than the web UI. — [PostEverywhere](https://posteverywhere.ai/blog/state-of-ai-agents-in-social-media)

### Inferences
- The developer-survey picture is "awareness high, deliberate agent-oriented design low". Only about a quarter design for agents, which leaves room for the curation and AX practices in Q1. Security and governance concerns lead the agenda.
- The 10% regular MCP usage figure in 2025 fits the late-2025 backlash narrative. No reliable 2026 primary number shows whether it rose.

### Gaps
- Could not access Postman's 2026 report directly to confirm the figures.
- No Kong, Nordic APIs or Forrester survey quantifying agent share of API traffic was found in the time available.
- No primary data from API providers (e.g. Stripe, Twilio, GitHub) on the share of their traffic coming from agents.
