# Agent-facing protocols and interfaces alongside or on top of web APIs (status as of 10 October 2026)

*How these notes were gathered: research ran on 2026-10-10. The session's egress policy blocked most vendor sites (modelcontextprotocol.io, linuxfoundation.org, aaif.io, openai.com, stripe.com, owasp.org, simonwillison.net, cloudflare.com, IETF datatracker), and the shared web-search budget ran out partway through. Most facts therefore come from **primary sources fetched from GitHub** (spec repos, changelogs, MAINTAINERS files, CVE List V5 records), the **official MCP blog**, the **live MCP Registry API**, anthropic.com, and cloud.google.com. Claims that rest only on search-engine summaries of secondary articles are marked "(secondary)".*

---

## 1. Model Context Protocol (MCP): spec history, key changes, governance, registry, adoption

### Takeaway
MCP is the de facto standard for exposing tools and data to agents. It now has five dated spec revisions: 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25 and **2026-07-28**. The 2026-07-28 revision is the largest break so far. It makes the core **stateless**: no `initialize` handshake, no `Mcp-Session-Id` header, per-request `_meta`, header-based routing and cacheable list results. It also moves Tasks and UI into a formal **extensions** framework, deprecates Sampling, Roots and Logging, and deprecates DCR in favour of CIMD. Each change moves MCP closer to plain, cacheable, load-balancer-friendly HTTP APIs. Governance moved to the Linux Foundation's **Agentic AI Foundation (AAIF)** on 9 Dec 2025. The official **Registry is still formally "preview"** (API frozen at v0.1), but it already lists about 41k servers.

### Cited Findings

**Spec version history (primary changelogs)**
- **2024-11-05**: initial spec. It is the baseline that the 2025-03-26 changelog diffs against. — [MCP 2025-03-26 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-03-26/changelog.mdx)
- **2025-03-26** added:
  - an OAuth 2.1-based authorization framework;
  - **Streamable HTTP**, replacing the earlier HTTP+SSE transport;
  - JSON-RPC batching;
  - **tool annotations** (read-only/destructive etc.);
  - audio content, a `completions` capability and a progress `message` field.
  — [MCP 2025-03-26 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-03-26/changelog.mdx)
- **2025-06-18**:
  - removed JSON-RPC batching (added only one revision earlier);
  - added **structured tool output**;
  - classified MCP servers as **OAuth Resource Servers**, with Protected Resource Metadata used to discover the authorization server;
  - **required RFC 8707 Resource Indicators** in clients ("to prevent malicious servers from obtaining access tokens");
  - added a new **security best practices** page, **elicitation** and **resource links** in tool results;
  - required the `MCP-Protocol-Version` header on HTTP;
  - added `title` fields and `_meta` on more types.
  — [MCP 2025-06-18 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/changelog.mdx)
- **2025-11-25**, released on MCP's first anniversary:
  - OpenID Connect Discovery support;
  - icons for tools, resources and prompts (SEP-973);
  - **incremental scope consent via `WWW-Authenticate`** (SEP-835);
  - tool-naming guidance (SEP-986);
  - standards-based enum and elicitation schemas (SEP-1330);
  - **URL-mode elicitation** (SEP-1036);
  - **tool calling inside sampling** (`tools`/`toolChoice`, SEP-1577);
  - **OAuth Client ID Metadata Documents (CIMD) as the recommended client registration** (SEP-991);
  - **experimental Tasks** for durable requests with polling and deferred results (SEP-1686);
  - PRM discovery aligned with RFC 9728, with a `.well-known` fallback (SEP-985);
  - JSON Schema 2020-12 as the default dialect (SEP-1613);
  - input-validation errors returned as tool-execution errors so the model can self-correct (SEP-1303);
  - formal governance, Working/Interest Groups and an SDK tiering system (SEP-932/1302/1730).
  — [MCP 2025-11-25 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)
- The 2025-11-25 release also introduced authorization **extensions**: client credentials for machine-to-machine auth (SEP-1046) and Cross App Access (SEP-990). — [MCP blog, "One Year of MCP", 25 Nov 2025](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
- **2026-07-28 timeline.** The release candidate was locked on **21 May 2026**, followed by a ten-week validation window. The final spec shipped on **28 July 2026**. Beta SDKs for the RC arrived on 29 Jun 2026. — [MCP blog RC post](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/); [MCP blog RSS](https://blog.modelcontextprotocol.io/index.xml)
- **2026-07-28 major changes**, measured against 2025-11-25:
  1. Protocol-level sessions and `Mcp-Session-Id` removed. Cross-call state now uses "explicit, server-minted handles passed as ordinary tool arguments" (SEP-2567).
  2. The `initialize`/`initialized` handshake removed. Every request carries its protocol version and client capabilities in `_meta` (SEP-2575).
  3. New mandatory `server/discover` RPC.
  4. `subscriptions/listen` (one long-lived POST-response stream) replaces the HTTP GET endpoint and `resources/subscribe`.
  5. `ping`, `logging/setLevel` and `notifications/roots/list_changed` removed.
  6. Tasks moved into an official extension `io.modelcontextprotocol/tasks`, with polling via `tasks/get`, a new `tasks/update` and `tasks/list` removed (SEP-2663).
  7. The **Multi Round-Trip Requests (MRTR)** pattern replaces server-initiated `sampling/createMessage`, `elicitation/create` and `roots/list`: the server returns `resultType: "input_required"` and the client retries with `inputResponses` (SEP-2322).
  8. All results carry a required `resultType`.
  9. SSE resumability and redelivery (`Last-Event-ID`) removed. A broken stream means re-issuing the request.

  — [MCP 2026-07-28 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx)
- **2026-07-28 minor changes:**
  - `extensions` field in client and server capabilities;
  - OpenTelemetry trace-context conventions in `_meta` (SEP-414);
  - deterministic `tools/list` ordering "to improve LLM prompt cache hit rates";
  - **required `Mcp-Method`/`Mcp-Name` HTTP headers**, plus `x-mcp-header` for mapping tool params to headers (SEP-2243);
  - **required `ttlMs` and `cacheScope` (public/private) on list and read results** so that clients and shared intermediaries can cache (SEP-2549);
  - RFC 9207 `iss` validation (SEP-2468);
  - `application_type` in DCR (SEP-837);
  - issuer-bound client credentials (SEP-2352);
  - full JSON Schema 2020-12 for input and output schemas, with `structuredContent` allowed to be any JSON (SEP-2106);
  - a partitioned error-code range.

  — [MCP 2026-07-28 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx)
- **2026-07-28 deprecations:**
  - **Roots, Sampling and Logging** (SEP-2577). Suggested migrations: tool params or resource URIs instead of Roots; "integrate directly with LLM provider APIs" instead of Sampling; stderr or OpenTelemetry instead of Logging.
  - The **HTTP+SSE transport**, formally Deprecated (SEP-2596).
  - `includeContext` values `thisServer`/`allServers`.
  - **OAuth Dynamic Client Registration (RFC 7591), in favour of CIMD** (PR #2858).
  - A new feature-lifecycle policy (Active → Deprecated → Removed) with a **minimum 12-month deprecation window**.

  — [MCP 2026-07-28 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx)
- **Why the stateless redesign.** Before it, a remote server "needed sticky sessions, a shared session store, and deep packet inspection at the gateway". Now it "can run behind a plain round-robin load balancer". The goal is a core that "scales on ordinary HTTP infrastructure". The maintainers say breaking releases are "not meant to be the norm". — [MCP blog RC post, 21 May 2026](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)
- **Tier 1 SDKs** supporting 2026-07-28 at release: TypeScript, Python, Go and C#. The Rust SDK is in beta. The official Ruby SDK reached 1.0 on 27 Jul 2026. — [MCP blog, 28 Jul 2026](https://blog.modelcontextprotocol.io/posts/2026-07-28/); [MCP blog RSS](https://blog.modelcontextprotocol.io/index.xml)
- Third-party coverage called it "the biggest MCP spec update", chiefly for agent authentication changes. — [WorkOS (secondary)](https://workos.com/blog/mcp-2026-spec-agent-authentication)

**Extensions: MCP Apps, Tasks, Enterprise-Managed Authorization**
- **MCP Apps** (SEP-1865) was proposed on 21 Nov 2025 and went **live on 26 Jan 2026 as "the first official MCP extension"**, described as production-ready.
  - Mechanism: tools declare UI via `_meta.ui.resourceUri`; UI resources use the `ui://` scheme with bundled HTML/JS and run in **sandboxed iframes**; UI↔host traffic is auditable JSON-RPC over `postMessage`; hosts can require consent for UI-initiated tool calls.
  - It was developed with OpenAI and the MCP-UI creators and "builds on MCP-UI and the OpenAI Apps SDK".
  - Launch clients: Claude (web and desktop), Goose, VS Code Insiders, and ChatGPT ("starting this week").

  — [MCP blog, 26 Jan 2026](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/); [MCP blog, 21 Nov 2025](https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/)
- The MCP Apps repo (`@modelcontextprotocol/ext-apps`, spec dated 2026-01-26) lists ChatGPT, Claude, VS Code and Goose as supported clients. — [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps)
- **Enterprise-Managed Authorization (EMA)** was declared stable on 18 Jun 2026; details are in Q5. The ext-auth repo lists EMA as **Stable** and "Client Credentials" as **Draft**. — [MCP blog, 18 Jun 2026](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/); [modelcontextprotocol/ext-auth](https://github.com/modelcontextprotocol/ext-auth)
- The MCP Bundle format (`.mcpb`) was adopted for portable local servers on 20–21 Nov 2025. — [MCP blog RSS](https://blog.modelcontextprotocol.io/index.xml)

**Roadmap (planned, not shipped)**
- **2026 roadmap (9 Mar 2026)** priorities:
  - transport evolution and scalability, including `.well-known` metadata for connectionless discovery; "not adding more official transports this cycle";
  - agent communication (Tasks lifecycle);
  - governance maturation;
  - enterprise readiness: audit, SSO-integrated auth, gateways, config portability, mostly delivered as extensions.

  Active proposals: SEP-1932 (DPoP) and SEP-1933 (Workload Identity Federation). — [MCP blog, 9 Mar 2026](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- **"The New MCP Roadmap" (22 Aug 2026)**: a Server Card Working Group is in progress, working on `.well-known` discovery without connecting. New priorities:
  1. agentic messaging primitives (server-initiated events, webhooks and channels; maturing Tasks into the core spec);
  2. **HTTP-native transport unification**, extending Streamable HTTP to local servers that run over stdio today;
  3. agent identity (finalising DPoP, Workload Identity Federation, the ID-JAG grant, token exchange; engaging the IETF OAuth and WIMSE groups);
  4. a single contract for `tools/call` results, plus **progressive tool discovery**;
  5. SDK developer experience and conformance.

  No date is given for the next spec release. — [MCP blog, 22 Aug 2026](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)

**Governance**
- On **9 Dec 2025** Anthropic donated MCP to the **Agentic AI Foundation (AAIF)**, a directed fund under the Linux Foundation.
  - Co-founders: Anthropic, Block and OpenAI. Supporters: Google, Microsoft, AWS, Cloudflare and Bloomberg.
  - Founding projects: **MCP, goose (Block) and AGENTS.md (OpenAI)**.
  - The AAIF board handles budget, membership and new projects. MCP maintainers keep technical control through the SEP process.

  — [MCP blog, 9 Dec 2025](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/); [Anthropic announcement](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- Earlier governance milestones: a new governance model (31 Jul 2025), and SEPs moving to pull requests (28 Nov 2025; formalised as SEP-1850 in 2026-07-28). The lead maintainers are David Soria Parra and Den Delimarsky, and the site is copyright "a Series of LF Projects, LLC". — [MCP blog RSS](https://blog.modelcontextprotocol.io/index.xml); [MCP blog, 28 Jul 2026](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- AAIF had **247 member organisations as of 13 Aug 2026**, after adding 57 members, including financial-services and APAC firms. — [Linux Foundation press release (secondary: via search summary; page blocked)](https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-57-new-members-gaining-major-financial-services-players-and-apac-leaders)
- At MCP Dev Summit North America 2026, Jim Zemlin stepped down as interim AAIF Executive Director. — [AAIF blog (secondary: via search summary)](https://aaif.io/blog/mcp-is-now-enterprise-infrastructure-everything-that-happened-at-mcp-dev-summit-north-america-2026/)

**Official MCP Registry**
- Preview launched **8 Sep 2025**. **API freeze at v0.1 on 24 Oct 2025**, "to shape v1 for general availability". As of 10 Oct 2026, the README's development-status section still shows only these two updates; **no GA announcement was found**. — [modelcontextprotocol/registry README](https://github.com/modelcontextprotocol/registry/blob/main/README.md)
- **Own count on 10 Oct 2026** from the live API (`GET /v0.1/servers?version=latest`, fully paginated): **41,332 unique server names**, of which **26,151 advertise remote endpoints** (e.g. `streamable-http`). The count was not filtered by status. Entries use the `server.schema.json` dated 2025-12-11. — [MCP Registry API](https://registry.modelcontextprotocol.io/v0.1/servers)
- For comparison, the registry had "close to 2,000 entries" on 25 Nov 2025. — [MCP blog, 25 Nov 2025](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)

**Adoption**
- **December 2025** (Anthropic, a vendor claim):
  - ">10,000 active public MCP servers";
  - "over 97 million monthly SDK downloads" across Python and TypeScript;
  - client support in ChatGPT, Cursor, Gemini, Microsoft Copilot, VS Code and others;
  - enterprise deployment on AWS, Cloudflare, Google Cloud and Azure;
  - 75+ connectors in Claude's directory.

  — [Anthropic, 9 Dec 2025](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- **July 2026** (maintainer claim): Tier 1 SDKs see "close to half-a-billion downloads a month". The TypeScript and Python SDKs have each passed 1 billion total downloads. Honeycomb reports "nearly 20% of all monthly interactive queries" are now made by agents. — [MCP blog, 28 Jul 2026](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- **Enterprise testimonials (Nov 2025):**
  - Block: Square AI, Moneybot, goose;
  - Microsoft: Foundry tools went "from a small set to thousands";
  - AWS: built into Bedrock, Kiro and AgentCore;
  - GitHub: MCP allowlist enterprise controls;
  - Okta: Cross App Access.

  These are maintainer-curated and promotional. — [MCP blog, 25 Nov 2025](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)

### Inferences
- The 2026-07-28 revision is a deliberate "**re-HTTP-ification**" of MCP:
  - per-request self-description (like REST statelessness);
  - routing metadata in headers (`Mcp-Method`/`Mcp-Name`), so gateways and WAFs can route and police without parsing JSON-RPC bodies;
  - HTTP-style cache semantics (`ttlMs`, `cacheScope` public/private, analogous to `Cache-Control` max-age/private);
  - server-minted handles instead of sessions (like resource IDs).

  For API designers, an MCP server is now very close to an HTTP API with a fixed RPC envelope. The design gap between "API" and "MCP server" has narrowed.
- Deprecating Sampling and Roots takes back two of the "agentic", bidirectional features that distinguished MCP from plain APIs. Together with MRTR, this shows the maintainers chose operational simplicity at scale over richer server→client interaction.
- Download counts (97M/month in Dec 2025, roughly 500M/month in Jul 2026) are inflated by CI and transitive installs. Registry counts include unvetted entries. Both show momentum, not production usage. The roughly 41k registry figure versus "10k active public servers" eight months earlier suggests rapid listing growth, but quality is unknown.
- The registry has been in "preview" for more than 13 months with a frozen v0.1 API while being used in production by integrators. In practice it is a de facto stable API without a formal GA.

### Gaps
- No primary source was reachable for the official MCP clients matrix (modelcontextprotocol.io/clients was blocked). Current client support for the 2026-07-28 revision in ChatGPT, Gemini, Copilot, Cursor and VS Code is not confirmed.
- No reliable independent figure for production MCP server count. The 41,332 is listing count only.
- No date was found for a planned next spec revision or for Registry GA.
- The OpenAI Apps SDK launch date could not be verified in-session (believed to be DevDay, 6 Oct 2025). Its current status relative to MCP Apps is only partly confirmed: ChatGPT supports MCP Apps per [ext-apps](https://github.com/modelcontextprotocol/ext-apps).

---

## 2. Agent2Agent (A2A) protocol: origin, Linux Foundation, versions, ACP merger, Agent Cards, adoption, relation to MCP

### Takeaway
A2A is Google's agent-to-agent protocol, launched in April 2025 and donated to the Linux Foundation in June 2025. It reached **v1.0.0 on 12 March 2026**; the current version is **v1.0.1 (26 May 2026)**. It absorbed IBM's Agent Communication Protocol (ACP) in August 2025. The protocol is now transport-neutral: JSON-RPC 2.0, gRPC and HTTP+JSON/REST bindings, with signed Agent Cards at `/.well-known/agent-card.json`. It positions itself as "horizontal" (agent↔agent), complementing MCP's "vertical" (agent↔tools) role. Organisation counts are high (150+), but independent evidence of cross-vendor production traffic is thinner than for MCP.

### Cited Findings
- **Release history** from the A2A changelog:
  - v0.2.1 (27 May 2025); v0.2.2 (9 Jun 2025); v0.2.5 (30 Jun 2025); v0.2.6 (17 Jul 2025);
  - **v0.3.0 (30 Jul 2025)**;
  - **v1.0.0 (12 Mar 2026)**;
  - **v1.0.1 (26 May 2026)**, which prefers `application/a2a+json` in the HTTP binding and fixes TaskStatus values.

  — [A2A CHANGELOG](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)
- **v0.3.0 changes:**
  - **Agent Card `signatures`** added;
  - well-known URI changed from `agent.json` to **`agent-card.json`**;
  - **mTLS** added to SecuritySchemes, plus an OAuth2 metadata URL; skills can specify security;
  - authenticated extended card fetch.

  — [A2A CHANGELOG](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)
- **v1.0.0 breaking changes:**
  - "Large refactor of specification to separate application protocol definition from mapping to transports";
  - "modernize oauth 2.0 flows – remove implicit/password, add device code / pkce";
  - "Add LF prefix to the package";
  - removal of deprecated proto fields;
  - `extendedAgentCard` moved to `AgentCapabilities`;
  - ProtoJSON enum alignment.

  New features: `tasks/list` with filtering and pagination, native multi-tenancy on gRPC, and SDK backward-compatibility support. — [A2A CHANGELOG](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)
- The spec defines an abstract layer plus **protocol bindings (JSON-RPC, gRPC, HTTP/REST)**. It uses an `A2A-Version` service parameter and cursor-based pagination (`pageToken`/`nextPageToken`), and maps errors to HTTP, gRPC and JSON-RPC codes. — [A2A specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- Governance: "an open source project under the Linux Foundation, contributed by Google", Apache 2.0. — [a2aproject/A2A README](https://github.com/a2aproject/A2A)
- Google donated A2A to the Linux Foundation in June 2025. On 9 Apr 2026 the LF said A2A had **150+ supporting organisations** and integrations across Google, Microsoft and AWS platforms. — [Linux Foundation press release (secondary: via search summary)](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year); [Google Open Source Blog, Apr 2026 (secondary: via search summary)](https://opensource.googleblog.com/2026/04/a-year-of-open-collaboration-celebrating-the-anniversary-of-a2a.html)
- Third-party reports of v1.0: signed Agent Cards using JWS (RFC 7515), and SDKs in Python, JavaScript, Java, Go and .NET. — [bex.co (secondary)](https://bex.co/blog/2026/07/11/a2a-v1-linux-foundation-deploy-agent-handshake); [Tyk (secondary)](https://tyk.io/learning-center/a2a-protocol-architecture-and-technical-specification/)
- **IBM ACP merger.** The i-am-bee/acp README banner says "ACP is now part of A2A under the Linux Foundation!" and links a migration guide. — [i-am-bee/acp](https://github.com/i-am-bee/acp)
  - Secondary sources date the merger to August 2025 (one says 29 Aug 2025; another says IBM announced in September). IBM's Kate Blair joined the A2A TSC. — [Tyk (secondary)](https://tyk.io/learning-center/agent-protocols-a-complete-guide-to-mcp-a2a-and-acp/); [rywalker.com (secondary)](https://rywalker.com/research/acp-agent-communication-protocol)
- **A2A's own framing of MCP:** "MCP is vertical. It deepens a single agent… A2A is horizontal. It connects agents across that boundary… MCP gives each agent depth, and A2A gives your system reach." — [A2A docs: A2A and MCP](https://github.com/a2aproject/A2A/blob/main/docs/topics/a2a-and-mcp.md)
- A2A is a host substrate for commerce. AP2 is "available as an extension for the open-source Agent2Agent (A2A) protocol", and an A2A x402 extension exists. — [AP2 docs index](https://github.com/google-agentic-commerce/AP2/blob/main/docs/index.md); [Google Cloud AP2 announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)

### Inferences
- A2A v1.0 (proto-first, three bindings, OAuth modernisation, signed cards) looks like a conventional enterprise API standard in the style of Google AIP and gRPC transcoding. It is arguably more "web-API-native" than MCP was before 2026.
- The MCP 2026 roadmap's "agentic messaging primitives" (webhooks, channels, Tasks) and Server Cards overlap with A2A's task lifecycle and Agent Cards. The intended "vertical vs horizontal" split is blurring at the edges.
- Adoption claims are counts of "supporting organisations", not traffic. A2A has no equivalent of MCP's registry or SDK download disclosures in the sources reviewed.

### Gaps
- No primary A2A download or production-traffic figures were found. The exact date of the LF donation (believed to be 23 Jun 2025) and the v1.0 press timing (Mar vs Apr 2026) could not be confirmed from LF or Google pages, which were blocked.
- The current A2A TSC membership list was not retrieved.

---

## 3. Other agent protocols and standards: AGNTCY, agents.json, NLWeb, WebMCP, OpenAI Apps SDK, AGENTS.md, Agent Skills, IBM ACP, ANP

### Takeaway
Around MCP and A2A sits a layer of lighter conventions:
- **Instruction and packaging formats**: AGENTS.md and Agent Skills (`SKILL.md`). These are file conventions, not wire protocols, and both are now multi-vendor.
- **Web-surface adapters**: NLWeb (site → MCP server via Schema.org) and **WebMCP** (page-registered tools via `document.modelContext`, now in Chrome 149 and Edge 150 origin trials).
- **Infrastructure stacks**: AGNTCY (LF) and ANP (DID-based).

Single-vendor OpenAPI wrappers such as agents.json and protocols that were merged away (IBM ACP) have faded.

### Cited Findings

**AGENTS.md**
- "A simple, open format for guiding coding agents… a README for agents". — [agentsmd/agents.md](https://github.com/agentsmd/agents.md)
- Donated by OpenAI as a **founding AAIF project** on 9 Dec 2025. — [MCP blog, 9 Dec 2025](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/); [OpenAI announcement (title via search)](https://openai.com/index/agentic-ai-foundation/)

**Agent Skills (SKILL.md)**
- Anthropic introduced Skills on **16 Oct 2025**. On **18 Dec 2025** it "published Agent Skills as an open standard for cross-platform portability" at agentskills.io.
- Skills use **progressive disclosure**: only name and description load at startup, the full `SKILL.md` loads when relevant, and bundled scripts run as tools "for deterministic operations".
- Anthropic says it will explore how Skills "complement MCP servers by teaching agents workflows that involve external tools".
- Security advice: install only from trusted sources, and audit scripts, dependencies and any instructions to reach external network sources.

— [Anthropic Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- Format: a folder with `SKILL.md` (YAML `name`/`description` at minimum, plus instructions) and optional `scripts/`, `references/` and `assets/`. "Originally developed by Anthropic, released as an open standard"; Apache 2.0 / CC-BY-4.0. — [agentskills/agentskills](https://github.com/agentskills/agentskills)
- The agentskills.io client showcase lists **46 products** (Oct 2026), including:
  - ChatGPT & Codex, Gemini CLI, GitHub Copilot, VS Code, Cursor;
  - Claude and Claude Code, Goose, Kiro, Junie, OpenHands, Amp, Factory;
  - Databricks Genie Code, Snowflake Cortex Code, Spring AI, Mistral AI Vibe, Roo Code, Tabnine, Qodo, Pulumi Neo.

  — [agentskills clients.jsx](https://github.com/agentskills/agentskills/blob/main/docs/snippets/clients.jsx)
- Skills are now treated as an attack surface. Snyk Agent Scan (successor to Invariant's mcp-scan) scans `SKILL.md`/skills directories for prompt injection, malware payloads, untrusted content and hard-coded secrets, and published a "technical report on the emerging threats of the agent skill eco-system". — [snyk/agent-scan](https://github.com/snyk/agent-scan)

**WebMCP**
- W3C Web Machine Learning CG incubation. It "lets developers expose web application functionality as 'tools'—JavaScript functions with natural language descriptions and structured schemas", via `document.modelContext.registerTool()`.
- It is explicitly positioned against "backend integrations" (MCP, OpenAPI), which cause "UI disintermediation & context loss" and force "replication of state & auth". A declarative `<form>`-based API is being explored separately.
- Authors are from Microsoft (Walderman, Lee, Nolan) and Google (Bokan, Sagar, Van Opstal); Dominic Farolino drives the spec draft.

— [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp)
- **Implementation status (Oct 2026):**
  - **Origin Trial live in Chrome 149** and **Edge 150**;
  - supported in **ChatGPT Desktop**;
  - experimental in Brave Leo;
  - Firefox and Safari: standards-position issues open;
  - Meta Ray-Ban Display "coming soon".

  — [WebMCP implementation-status.md](https://github.com/webmachinelearning/webmcp/blob/main/implementation-status.md)

**NLWeb**
- "Every NLWeb instance also acts as an MCP server (and soon A2A)" with a core `ask` method returning Schema.org JSON. Its stated aim: "NLWeb is to MCP/A2A what HTML is to HTTP."
- The repo, now under the `nlweb-ai` org, is reorganised into AskAgent, AgentFinder (agent discovery), DataFinder (NL→SQL), ModelRouter and NLWebScorer.

— [nlweb-ai/NLWeb](https://github.com/nlweb-ai/NLWeb)

**AGNTCY**
- A Linux Foundation project building the "Internet of Agents". Components: SLIM (messaging), Identity and Agent Directory. The TSC comes from Cisco (3), Dell, Red Hat, Oracle, Google Cloud and Akamai. — [AGNTCY GitHub org profile](https://github.com/agntcy)

**agents.json (Wildcard)**
- "An open specification that formally describes contracts for API and agent interactions, built on top of the OpenAPI standard." Current version **0.1.0**. — [wild-card-ai/agents-json](https://github.com/wild-card-ai/agents-json)

**ANP (Agent Network Protocol)**
- Aims to be "the HTTP of the Agentic Web era". It builds on W3C DID (`did:wba`, native `did:web`).
- Released core documents are at v1.2: ANP-03 did:wba, ANP-04 naming.
- Still draft: ANP-05 DID-based authorization (draft v0.6), the ANP-06 meta-protocol, and ANP-10 (an **AP2 payment adaptation**).

— [agent-network-protocol/AgentNetworkProtocol](https://github.com/agent-network-protocol/AgentNetworkProtocol)

**IBM ACP**
- Superseded and merged into A2A; see Q2. — [i-am-bee/acp](https://github.com/i-am-bee/acp)
- Naming collision: Zed's "Agent Client Protocol" (editor↔coding-agent) is a separate, active protocol also abbreviated ACP. So is the OpenAI/Stripe *Agentic Commerce* Protocol. — [Tyk/others via search summary (secondary)](https://tyk.io/learning-center/agent-protocols-a-complete-guide-to-mcp-a2a-and-acp/)

### Inferences
- **Skills vs APIs, CLIs and MCP.** A skill is documentation plus scripts loaded on demand. It often wraps an existing CLI or HTTP API with procedural knowledge rather than defining a new wire interface. This is an alternative to a large MCP tool surface, especially as MCP itself plans "progressive discovery" (Aug 2026 roadmap). For API providers, a well-documented CLI or API plus a published Skill is becoming a viable alternative or complement to building an MCP server.
- WebMCP is the most significant new web-platform development. It puts agent tools into the page under the user's existing session and origin, avoiding OAuth to a separate MCP endpoint. It is still origin-trial-only in Chromium browsers, with no Gecko or WebKit commitment.
- agents.json (v0.1.0, OpenAPI-overlay approach) appears to have been overtaken by MCP plus OpenAPI-to-MCP generators. This is an inference: no update data could be retrieved.

### Gaps
- AGENTS.md adoption figures (OpenAI has claimed "60k+ repos") could not be verified; openai.com was blocked.
- NLWeb launch date (believed Microsoft Build, May 2025) and current Microsoft involvement were not verified.
- AGNTCY's LF join date (believed July 2025) and its adoption were not verified.
- Whether WebMCP has moved toward a W3C Working Group was not found.

---

## 4. Agentic commerce and payments protocols: ACP, AP2, UCP, x402, Visa/Mastercard, Cloudflare pay-per-crawl

### Takeaway
Commerce protocols multiplied in late 2025 and are now consolidating into **two checkout stacks**:
- **OpenAI/Stripe ACP**, now with Meta as a lead maintainer;
- **Google/Shopify UCP + AP2**, with Stripe, Meta, Amazon, Microsoft and others on UCP's council.

Underneath them sit payment-credential layers: AP2 mandates (now v0.2 and donated toward FIDO), card-network agent tokens and signatures (Visa TAP), and **x402** (HTTP 402 + stablecoins, v2, foundation-governed). All of them are now **transport-agnostic and bind to MCP/A2A/REST**.

Real-world uptake is uneven. **OpenAI wound down ChatGPT Instant Checkout in March 2026** (secondary), and x402's independent on-chain volume is far below issuer headline counts.

### Cited Findings

**Agentic Commerce Protocol (ACP; OpenAI + Stripe)**
- Status "beta". Lead maintainers: **OpenAI, Stripe, Meta**. Date-based versions:
  - **2025-09-29** (initial);
  - **2025-12-12** (fulfillment);
  - **2026-01-16** (capability negotiation);
  - **2026-01-30** (extensions, discounts, payment handlers);
  - **2026-04-17** ("Cart, feed, orders, authentication, and MCP"; latest stable).

  — [ACP README](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol); [ACP MAINTAINERS](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/MAINTAINERS.md)
- **2026-04-17 contents:**
  - Feed API (`POST /feeds`, `PATCH /feeds/{id}/products`, JSONL ingestion);
  - Cart capability;
  - a discovery **well-known document** with a `transports` field (`rest`, `mcp`);
  - an **MCP transport binding** (OpenRPC schema defining five MCP tools);
  - delegate authentication / 3DS;
  - **mandatory idempotency requirements**;
  - a `supported_versions` field in version-mismatch errors, so agents can negotiate versions.

  The previous version was deprecated. — [ACP changelog 2026-04-17](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/changelog/2026-04-17.md)
- Governance: a TSC, with **OpenAI and Stripe as Founding Maintainers holding last-resort veto**. — [ACP governance.md](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/docs/governance.md)
- ACP and Instant Checkout in ChatGPT launched together on 29 Sep 2025, using Stripe's Shared Payment Token. — [Stripe newsroom (via search)](https://stripe.com/newsroom/news/stripe-openai-instant-checkout); [OpenAI (via search)](https://openai.com/index/buy-it-in-chatgpt/)
- **Retreat (secondary):** in March 2026 OpenAI moved away from in-ChatGPT Instant Checkout toward discovery plus merchant apps.
  - Reported reasons: low uptake ("only 8%" of US adult users tried it in the first month), and Walmart conversion at one-third of its own site.
  - OpenAI reportedly continues developing ACP. Reported dates vary (5, 20 or 25 March 2026).

  — [Shopifreaks (secondary)](https://www.shopifreaks.com/openai-pivots-from-instant-checkout-to-an-app-based-shopping-model-inside-chatgpt/); [Storyboard18 (secondary)](https://storyboard18.com/digital/openai-reduces-chatgpt-shopping-focus-shifts-to-product-discovery-93192.html)

**Universal Commerce Protocol (UCP; Google + Shopify)**
- "Transport Agnostic: … Businesses can offer Capabilities via REST APIs, MCP, or A2A".
  - Capabilities: Checkout, **Identity Linking (OAuth 2.0)**, Order (webhooks) and Payment Token Exchange.
  - "Support for advanced security patterns like AP2 mandates and verifiable credentials".
  - Apache 2.0, with conformance tests.

  — [UCP README](https://github.com/Universal-Commerce-Protocol/ucp)
- The UCP **Shopping Tech Council** includes Google, Shopify, Etsy, **Meta, Amazon, Target, Microsoft, Stripe, Salesforce and Wayfair**. — [UCP MAINTAINERS](https://github.com/Universal-Commerce-Protocol/.github/blob/main/MAINTAINERS.md)
- **Launch (secondary):** 11 Jan 2026.
  - Launch partners: Visa, Mastercard, AmEx, Stripe, Adyen, Best Buy, Home Depot, Macy's, Flipkart and Zalando.
  - Merchant access is phased, US-first, via early access or waitlist. Simplified Merchant Center onboarding was reported for March 2026.

  — [Semrush (secondary)](https://www.semrush.com/blog/universal-commerce-protocol/); [Google blog (via search)](https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/)

**Agent Payments Protocol (AP2; Google)**
- Announced **16 Sep 2025** with 60+ partners, including Adyen, AmEx, Coinbase, Mastercard, PayPal, Revolut, Salesforce, ServiceNow, UnionPay and Worldpay.
  - Uses cryptographically signed **Mandates** as verifiable credentials: an **Intent Mandate** (user's instruction or limits) and a **Cart Mandate** (exact items and price), forming a non-repudiable audit trail.
  - Payment-agnostic (cards, stablecoins, real-time bank transfers), with an **A2A x402 extension** for crypto.

  — [Google Cloud blog, 16 Sep 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
- Version history: **v0.1.0 (16 Sep 2025)**, **v0.2.0 (28 Apr 2026)**. The docs now present AP2 as an extension for **both A2A and UCP**, and link "AP2 v0.2 Release and FIDO Alliance Donation" plus "FIDO Alliance to Develop Standards for Trusted AI Agent Interactions". — [AP2 CHANGELOG](https://github.com/google-agentic-commerce/AP2/blob/main/CHANGELOG.md); [AP2 docs index](https://github.com/google-agentic-commerce/AP2/blob/main/docs/index.md); [AP2 spec v0.2](https://github.com/google-agentic-commerce/AP2/blob/main/docs/ap2/specification.md)

**x402 (HTTP 402 revival)**
- **Protocol Version 2.**
  - Architecture: Types / Logic / Representation, with transports "HTTP, MCP, A2A".
  - Schemes: `exact`, `upto`, `batch-settlement`.
  - Roles: resource server, client and **facilitator** (verification and settlement).
  - Over HTTP, the `PaymentRequired` object travels in a base64 **`PAYMENT-REQUIRED` response header**, and the client pays via a `PAYMENT-SIGNATURE` header.

  — [x402 spec v2](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md)
- The repo now lives in the **x402-foundation** GitHub org. It aims to "support all networks (both crypto & fiat)", with SDK packages for EVM, Solana, Aptos, Stellar, Hedera and others, plus `@x402/mcp`. — [x402-foundation/x402](https://github.com/x402-foundation/x402)
- **Foundation and volume (secondary, conflicting):**
  - Coinbase and Cloudflare co-founded the x402 Foundation in Sep 2025. Other sources date an LF-hosted foundation launch to **2 Apr 2026**, with AWS, Anthropic, Circle and 20+ others.
  - Coinbase claims "169M payments" and "185M+" trailing-year agentic payments (June 2026).
  - CoinDesk reported about **$28k/day** volume in March 2026, and one tracker estimates about half of activity is "gamified".

  — [CoinDesk (secondary)](https://www.coindesk.com/tech/2026/05/05/ai-agents-are-breaking-web-economics-but-cloudflare-says-x402-can-help); [presenc.ai tracker (secondary)](https://presenc.ai/research/x402-protocol-adoption-tracker-2026); [BlockEden (secondary)](https://blockeden.xyz/blog/2026/03/05/x402-foundation-ai-payment-internet/)
- Cloudflare and AWS reportedly embedded x402 at the edge in July 2026. — [InfoQ (secondary; title via search)](https://www.infoq.com/news/2026/07/cloudflare-aws-x402-micropayment/)

**Card networks**
- **Visa Trusted Agent Protocol (TAP):** "a standardized, cryptographic method for an AI agent to prove its identity and associated authorization directly to merchants". The TAP agent generates **RFC 9421** signatures, bound to the merchant domain and operation, with timestamps and nonce for replay protection. It can pass consumer identifiers and Payment Account References. — [visa/trusted-agent-protocol](https://github.com/visa/trusted-agent-protocol)
- Visa and Mastercard appear as AP2 partners and UCP launch partners. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol); [Semrush (secondary)](https://www.semrush.com/blog/universal-commerce-protocol/)

**Cloudflare pay-per-crawl**
- Still **"currently in closed beta"**. A crawler either presents "payment intent via request headers for successful HTTP 200 access, or receive[s] an **HTTP 402 Payment Required** response with pricing". Cloudflare is Merchant of Record, and WAF/Bot Management blocks override "charge". — [Cloudflare docs: What is Pay Per Crawl](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl.mdx)

### Inferences
- **Implications for API design:**
  - HTTP **402** is being revived as a real negotiated status, by both x402 and Cloudflare pay-per-crawl.
  - Price, terms and payment requirements are carried in **response headers**.
  - **Idempotency keys are mandatory** (ACP).
  - **Capability or version discovery** happens via well-known documents and `supported_versions` errors.
  - **Signed requests** (RFC 9421) identify agents.

  APIs intended for agent buyers should be machine-negotiable: pricing, auth requirements and versions should be discoverable in-band.
- **Consolidation signals:** Stripe and Meta sit on both ACP and UCP; ACP added an MCP binding; UCP binds to REST/MCP/A2A; AP2 is now an extension *of* UCP and A2A; x402 is a payment-scheme layer usable by all of them. The likely end-state is a few checkout schemas over common transports, with interchangeable credential layers (AP2 mandates, network tokens, x402).
- OpenAI's reported Instant Checkout retreat suggests a gap between agent-commerce protocols and consumer demand. Protocol activity (ACP releases through April 2026) continued regardless.

### Gaps
- No primary source was reachable for **Mastercard Agent Pay** or **Visa Intelligent Commerce** product status, or for Cloudflare's own x402/"Wallets" announcements.
- The date of AP2's FIDO Alliance donation was not confirmed (likely around v0.2, April 2026).
- Primary confirmation of the Instant Checkout wind-down was not obtained; reported dates conflict.
- Independent x402 volume figures conflict, and none is authoritative.

---

## 5. Agent identity and authorization: MCP OAuth, PRM, CIMD vs DCR, enterprise-managed auth / ID-JAG, Web Bot Auth, "know your agent"

### Takeaway
MCP authorization has converged on **standard OAuth 2.1 resource-server patterns**:
- PRM (RFC 9728) for authorization-server discovery;
- audience-bound tokens (RFC 8707);
- PKCE and RFC 9207 issuer validation;
- **CIMD (URL-as-client_id) preferred, DCR deprecated (2026-07-28)**.

For enterprises, **Enterprise-Managed Authorization (ID-JAG / Okta Cross App Access) is stable since June 2026**. DPoP and workload identity are next. Separately, a **"know your agent" layer is forming around HTTP Message Signatures (RFC 9421)**: Cloudflare Web Bot Auth and Visa TAP, with DIDs in ANP.

### Cited Findings
- **2026-07-28 auth spec:**
  - The MCP server is an OAuth 2.1 resource server and the client an OAuth 2.1 client.
  - Normative references: OAuth 2.1 draft-13, RFC 8414, RFC 7591, RFC 8707, **RFC 9728**, **RFC 9207**, and **draft-ietf-oauth-client-id-metadata-document-00**.
  - Clients and ASes "SHOULD support CIMD". DCR is "MAY… deprecated and retained for backwards compatibility".
  - Servers "MUST implement" PRM (RFC 9728).
  - Registration options: CIMD, pre-registration, or DCR.

  — [MCP authorization spec 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/index.mdx)
- **Token handling (2026-07-28):**
  - Clients MUST use RFC 8707 `resource` with the server's canonical URI.
  - Servers "MUST validate that access tokens were issued specifically for them".
  - "MCP clients MUST NOT send tokens to the MCP server other than ones issued by the MCP server's authorization server… MCP servers MUST NOT accept or transit any other tokens" (a no-token-passthrough rule).
  - Clients record the expected issuer and validate `iss` before redeeming the code.

  — [MCP authorization spec 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/index.mdx)
- **Evolution:**
  - 2025-03-26: OAuth 2.1 framework.
  - 2025-06-18: servers as resource servers with PRM; RFC 8707 required.
  - 2025-11-25: OIDC discovery, incremental consent via `WWW-Authenticate`, CIMD recommended, PRM `.well-known` fallback.
  - 2026-07-28: RFC 9207 `iss`, `application_type`, issuer-bound credentials, DCR deprecated.

  — [2025-03-26](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-03-26/changelog.mdx), [2025-06-18](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/changelog.mdx), [2025-11-25](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx), [2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx) changelogs
- The maintainers acknowledged the old DCR approach was "complex and error-prone"; CIMD lets clients use "a URL that points to a JSON document they manage". — [MCP blog, 25 Nov 2025](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
- **CIMD trust policies:** ASes may allowlist domains, accept any HTTPS `client_id` (for open servers), run reputation or domain-age checks, and display the client hostname prominently "to prevent phishing". SSRF against ASes that fetch CIMDs is called out. — [MCP Security Best Practices 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx)
- **Enterprise-Managed Authorization (stable, 18 Jun 2026):**
  - During SSO, the client obtains an **Identity Assertion JWT Authorization Grant (ID-JAG)** from the IdP and exchanges it at the MCP server's AS. There is no per-server consent screen, and admins set policy by group, role and conditional access in the IdP.
  - IdP: Okta's Cross App Access is first.
  - Clients: Claude, Claude Code, Cowork, and VS Code (preview).
  - Servers: Asana, Atlassian, Canva, Figma, Granola, Linear and Supabase (Slack adding).

  — [MCP blog, 18 Jun 2026](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/)
- **Next (planned):** finalising **DPoP** (SEP-1932) and **Workload Identity Federation** (SEP-1933), defining agent identity and delegation via WIF, the ID-JAG grant and token exchange, and engaging the IETF OAuth and WIMSE WGs. — [MCP blog, 22 Aug 2026](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/); [MCP blog, 9 Mar 2026](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- **A2A auth:** v0.3 added mTLS and OAuth metadata URLs. v1.0 removed implicit/password grants and added device code and PKCE. Agent Cards can be signed. — [A2A CHANGELOG](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)
- **Web Bot Auth (Cloudflare):**
  - "leverages cryptographic signatures in HTTP messages to verify that a request comes from an automated bot", used for Cloudflare's verified bots and agents.
  - Relies on IETF drafts: a key **directory** (`draft-meunier-http-message-signatures-directory`, served at `/.well-known/http-message-signatures-directory`) and a **protocol** draft (`draft-meunier-webbotauth-httpsig-protocol`).
  - Uses Ed25519 keys.

  — [Cloudflare docs: Web Bot Auth](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/bots/reference/bot-verification/web-bot-auth.mdx); [cloudflareresearch/web-bot-auth](https://github.com/cloudflareresearch/web-bot-auth)
- **"Know your agent" in commerce:** Visa TAP asks "Is this a legitimate, trusted, and recognized AI agent? Is it acting on behalf of a specific, authenticated user? Does the agent carry valid instructions…?" It answers with RFC 9421 signatures. — [visa/trusted-agent-protocol](https://github.com/visa/trusted-agent-protocol)
  - AP2 answers the "instructions" part with VC-signed Intent and Cart Mandates. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
  - UCP includes an **Identity Linking (OAuth 2.0)** capability. — [UCP README](https://github.com/Universal-Commerce-Protocol/ucp)
- **Decentralised alternative:** ANP's identity layer uses W3C DIDs (`did:wba`, v1.2 released). DID-based OAuth authorization (ANP-05) is still a draft at v0.6. — [ANP README](https://github.com/agent-network-protocol/AgentNetworkProtocol)

### Inferences
- Three identity questions are being answered by different mechanisms:
  1. **Which software is this client?** CIMD (URL-identified clients), signed Agent Cards, Web Bot Auth key directories.
  2. **Which user or tenant authorised it, and for what?** OAuth with audience binding, ID-JAG for enterprise SSO, AP2 mandates.
  3. **Is this request from that agent?** RFC 9421 HTTP Message Signatures, with DPoP planned for MCP.

  API providers will likely need to support all three: OAuth/PRM for delegated access, signature verification for bot/agent identity at the edge, and possibly mandate verification for payments.
- Deprecating DCR removes the "open registration endpoint" pattern that many API providers resisted. CIMD shifts trust decisions to domain-based policy, a model familiar from web origins.

### Gaps
- The current IETF status of the Web Bot Auth drafts (adopted by a WG? revision numbers as of Oct 2026) and of the ID-JAG draft could not be checked; datatracker was blocked.
- Microsoft Entra's EMA support status is unclear: the MCP post names only Okta as the supported IdP.
- No primary source was found on Mastercard's agent identity scheme (Agent Pay tokens).

---

## 6. Security: prompt injection via tool results, tool poisoning, rug pulls, confused deputy, token passthrough, lethal trifecta, incidents, OWASP guidance

### Takeaway
The agent-protocol threat model has two layers:
- **Classic web/API bugs**: command injection, unauthenticated local HTTP endpoints, path traversal, SSRF, OAuth confused deputy. These produced a **steady stream of critical CVEs in MCP servers and tooling (2025–2026)**.
- **Model-layer manipulation**: indirect prompt injection via tool output, tool poisoning or shadowing, rug pulls, and the "lethal trifecta". This is unsolved by protocol metadata. The MCP maintainers explicitly say tool annotations are "hints, not security guarantees".

OWASP now publishes a GenAI LLM Top 10 **2026** (4 Aug 2026), a Top 10 for Agentic Applications (Dec 2025), and an MCP Top 10 (beta).

### Cited Findings

**Lethal trifecta and the limits of annotations**
- Willison's "lethal trifecta" is the combination of private-data access, exposure to untrusted content, and external communication, which enables exfiltration via injected instructions. "MCP makes such combinations easy, so risk is a property of the session."
- Tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`):
  - **cannot stop prompt injection**;
  - cannot be trusted from untrusted servers ("a server can claim a tool is read-only and still delete files");
  - cannot enforce security.

  "Hard guarantees need network controls or sandboxing."

— [MCP blog, 16 Mar 2026](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/); original framing: [Simon Willison, 16 Jun 2025](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)

**Tool poisoning, shadowing and rug pulls**
- Invariant Labs demos:
  - **direct poisoning** (tool description instructs the agent to leak SSH keys and `mcp.json`);
  - **tool shadowing** (a malicious server alters the behaviour of a trusted server's `send_email`);
  - a **"sleeper rug pull"** (a server that "changes its tool interface only on the second load to a malicious one") used to exfiltrate WhatsApp messages via whatsapp-mcp.

  — [invariantlabs-ai/mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments)
- The scanner lineage (Invariant mcp-scan → **Snyk Agent Scan**) detects prompt injection, tool poisoning, tool shadowing and **toxic flows** in MCP configs, and now also in skills. It auto-discovers configs for Claude Code/Desktop, Cursor, Gemini CLI and Windsurf. — [snyk/agent-scan](https://github.com/snyk/agent-scan)

**MCP Security Best Practices (2026-07-28)**
- Sections:
  - **Confused Deputy**: MCP proxy servers using static client IDs plus DCR plus consent cookies let attackers obtain auth codes; proxies "MUST implement per-client consent".
  - **Token Passthrough**: "explicitly forbidden"; covers audience-validation failures and downstream confused deputy.
  - **SSRF**: including against authorization servers fetching CIMDs.
  - **State Handle Hijacking**: new with stateless MCP; guessable or leaked server-minted handles.
  - **Local MCP Server Compromise**.
  - **OAuth Authorization URL Validation**.
  - **stdio transport security in proxy scenarios**: XSS → stealing the proxy token → spawning arbitrary commands.
  - **Mix-Up Attacks**, **Localhost Redirect URI Impersonation**, **CIMD Trust Policies**, **Scope Minimization**.

  — [MCP Security Best Practices 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx)

**Notable CVEs (primary CVE records)**

2025:
- **CVE-2025-49596** (published 13 Jun 2025; CVSS 4.0: 9.4): MCP Inspector below 0.14.1, RCE "due to lack of authentication between the Inspector client and proxy". — [CVE record](https://www.cve.org/CVERecord?id=CVE-2025-49596)
- **CVE-2025-53109 / CVE-2025-53110** (2 Jul 2025; 7.3): Anthropic reference **Filesystem** server, sandbox escape via symlinks and path-prefix matching. — [CVE-2025-53109](https://www.cve.org/CVERecord?id=CVE-2025-53109); [CVE-2025-53110](https://www.cve.org/CVERecord?id=CVE-2025-53110)
- **CVE-2025-6514** (9 Jul 2025; CVSS 3.1: 9.6): **mcp-remote** OS command injection "when connecting to untrusted MCP servers due to crafted input from the authorization_endpoint response URL". — [CVE record](https://www.cve.org/CVERecord?id=CVE-2025-6514)
- **CVE-2025-68143/68144/68145** (17 Dec 2025; 6.3–6.5): Anthropic reference **mcp-server-git**, covering unvalidated `git_init` paths, argument injection in `git_diff`/`git_checkout` (`--output=` file overwrite), and `--repository` scope bypass. — [CVE-2025-68143](https://www.cve.org/CVERecord?id=CVE-2025-68143); [68144](https://www.cve.org/CVERecord?id=CVE-2025-68144); [68145](https://www.cve.org/CVERecord?id=CVE-2025-68145)

2026:
- **CVE-2026-23744** (16 Jan 2026; 9.8): MCPJam inspector ≤1.4.2 listens on 0.0.0.0, allowing unauthenticated RCE by installing an MCP server. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-23744)
- **CVE-2026-26029** (11 Feb 2026; 7.5): sf-mcp-server (Salesforce CLI wrapper), command injection via `child_process.exec`. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-26029)
- **CVE-2026-27825** (10 Mar 2026; 9.1): mcp-atlassian <0.17.0, arbitrary file write via `download_path`. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-27825)
- **CVE-2026-4192** (15 Mar 2026): quip-mcp-server, command injection, maintainer unresponsive. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-4192)
- **CVE-2026-33032** (30 Mar 2026; 9.8): nginx-ui's MCP integration exposes `/mcp_message` with an empty IP allowlist treated as "allow all", so no authentication. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-33032)
- **CVE-2026-30624** (15 Apr 2026): Agent Zero executes arbitrary `command`/`args` from MCP server JSON config. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-30624)
- **CVE-2026-5029** (12 May 2026; CVSS 4.0: 8.7): Code Runner MCP Server over HTTP transport, unauthenticated `/mcp` on port 3088 leading to arbitrary code execution. — [CVE record](https://www.cve.org/CVERecord?id=CVE-2026-5029)

Aggregates (secondary):
- "30+ MCP CVEs in two months" in early 2026. — [bex.co (secondary)](https://bex.co/blog/2026/09/23/mcp-cve-wave-2026-deploy-mcp-supply-chain)
- Community trackers: [Vulnerable MCP Project](https://vulnerablemcp.info/), [AuthZed MCP breach timeline](https://authzed.com/blog/timeline-mcp-breaches) (not reachable in-session).

**OWASP guidance**
- **OWASP GenAI LLM Top 10 2026**, published **4 Aug 2026**:
  1. Prompt Injection
  2. Sensitive Information Disclosure
  3. **Excessive Agency**
  4. Supply Chain
  5. Data and Model Poisoning
  6. Unbounded Consumption
  7. Misinformation
  8. **Hidden Context Exposure**
  9. Vector and Embedding Weaknesses
  10. Improper Output Handling

  — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10)
- LLM01:2026 explicitly lists "a tool response… **an MCP server's output**" as an indirect-injection vector. Delivery surfaces include "tool output, tool connection channel". Its mitigations include "Hold credentials and state-change capability in application code, not the model… Route privileged calls through a deterministic policy engine". — [LLM01:2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md)
- The original OWASP LLM Top 10 project page is now a "legacy entry point" pointing to the 2026 release. — [OWASP legacy repo](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications)
- **OWASP Top 10 for Agentic Applications (2026)** was published **9 Dec 2025** with risks ASI01–ASI10, including goal hijacking, tool misuse, rogue agents and cascading failures. — [genai.owasp.org (secondary: via search summary)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-application)
- **OWASP MCP Top 10** is in **"Phase 3 – Beta Release and Pilot Testing"**, with the next release planned for **October 2026**:
  - MCP01 Token Mismanagement & Secret Exposure
  - MCP02 Privilege Escalation via Scope Creep
  - MCP03 Tool Poisoning
  - MCP04 Supply Chain & Dependency Tampering
  - MCP05 Command Injection & Execution
  - MCP06 Intent Flow Subversion
  - MCP07 Insufficient AuthN/AuthZ
  - MCP08 Lack of Audit & Telemetry
  - MCP09 Shadow MCP Servers
  - MCP10 Context Injection & Over-Sharing

  — [OWASP/www-project-mcp-top-10](https://github.com/OWASP/www-project-mcp-top-10)

**MCP Apps UI security model**
- Sandboxed iframes, pre-declared templates hosts can review, auditable `postMessage` JSON-RPC, and consent for UI-initiated tool calls. — [MCP blog, 26 Jan 2026](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)

### Inferences
- Most high-severity MCP CVEs are **ordinary web or CLI bugs**: shell exec of untrusted strings, binding to 0.0.0.0 without auth, missing path confinement. They are amplified because MCP servers are often thin wrappers that expose local capabilities to a model processing untrusted input. Standard API hardening (authN on every endpoint, no shell interpolation, path allowlists, egress control) addresses the CVE class. It does not address injection.
- The protocol's direction (stateless handles, header routing, per-request auth) makes MCP endpoints easier to front with standard API gateways and WAFs. Policy enforcement is likely to move to gateways and hosts ("deterministic policy engine", per OWASP LLM01:2026), not to tool metadata.
- Skills widen the supply-chain surface: arbitrary scripts plus natural-language instructions. Scanners now treat `SKILL.md` like an MCP server config.

### Gaps
- Primary write-ups of the 2025 "headline" incidents could not be fetched: the GitHub MCP prompt-injection exfiltration (Invariant, May 2025), the postmark-mcp malicious npm package (Sep 2025), the Asana MCP cross-tenant exposure (Jun 2025), Supabase MCP, and the OX Security "STDIO RCE by design" supply-chain advisory (2026). They are named here only as gaps.
- The full ASI01–ASI10 names of the OWASP Agentic Top 10 could not be verified from a primary source.
- OWASP LLM Top 10 2025 ordering was not retrieved for a diff. "Hidden Context Exposure" appears to be new or renamed in 2026, possibly evolving from 2025's "System Prompt Leakage"; this is unverified.

---

## 7. Convergence vs fragmentation (late 2026)

### Takeaway
**Converging:**
- Tool access is effectively **MCP**, now under neutral LF/AAIF governance and backed by every major model vendor.
- Agent-to-agent is **A2A**, which absorbed IBM ACP.
- Agent instruction and packaging is **AGENTS.md + Agent Skills**.
- Authentication is **standard OAuth 2.1/IETF building blocks**: PRM, CIMD, RFC 8707, RFC 9207, ID-JAG, DPoP; plus RFC 9421 signatures for agent identity.
- Every newer protocol (UCP, ACP, AP2, x402, NLWeb) **binds to MCP and/or A2A and REST** instead of defining new transports.

**Still fragmented:**
- **Commerce**: ACP vs UCP+AP2, plus card-network schemes and x402, with weak demand signals.
- **Discovery**: MCP Registry (preview), Server Cards (in progress), A2A Agent Cards, ACP/UCP well-known docs, NLWeb AgentFinder, AGNTCY Directory.
- **Browser-side tools**: WebMCP is in origin trial in Chromium only.

### Cited Findings
- AAIF co-founded by Anthropic, Block and OpenAI, with Google, Microsoft, AWS, Cloudflare and Bloomberg supporting. Hosts MCP, goose and AGENTS.md. — [MCP blog, 9 Dec 2025](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)
- A2A is LF-hosted; IBM ACP was folded into it. — [a2aproject/A2A](https://github.com/a2aproject/A2A); [i-am-bee/acp](https://github.com/i-am-bee/acp)
- Binding convergence:
  - UCP: "REST APIs, MCP, or A2A" — [UCP](https://github.com/Universal-Commerce-Protocol/ucp)
  - ACP: MCP transport binding and `transports: rest, mcp` in the well-known document — [ACP 2026-04-17](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/changelog/2026-04-17.md)
  - x402 transports: "HTTP, MCP, A2A" — [x402 v2](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md)
  - AP2 as an extension of A2A and UCP — [AP2 docs](https://github.com/google-agentic-commerce/AP2/blob/main/docs/index.md)
  - NLWeb instances are MCP servers — [NLWeb](https://github.com/nlweb-ai/NLWeb)
- Cross-membership in commerce: Meta is an ACP lead maintainer *and* on UCP's council, and Stripe is an ACP founding maintainer *and* on UCP's council. — [ACP MAINTAINERS](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/MAINTAINERS.md); [UCP MAINTAINERS](https://github.com/Universal-Commerce-Protocol/.github/blob/main/MAINTAINERS.md)
- Skills portability: 46 listed clients across Anthropic, OpenAI, Google, GitHub/Microsoft, Cursor, Databricks, Snowflake and others. — [agentskills clients.jsx](https://github.com/agentskills/agentskills/blob/main/docs/snippets/clients.jsx)
- MCP itself is shedding bespoke features in favour of HTTP-native ones: stateless core, cacheable lists, header routing, and planned unification on HTTP transport even for local servers. — [MCP 2026-07-28 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx); [MCP blog, 22 Aug 2026](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/)
- WebMCP explicitly frames itself as an alternative to backend MCP/OpenAPI integrations for interactive web apps. — [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp)

### Inferences
- **For conventional web API designers in late 2026:**
  - The agent-facing surface is increasingly a thin, standards-based layer over existing HTTP APIs: an MCP server (stateless and cacheable), OAuth with PRM and CIMD, optional A2A for agent services, optional commerce schemas.
  - Investment in good HTTP API hygiene carries over directly: idempotency, versioning with negotiable errors, cache semantics, well-known discovery, signed requests, and precise auth scopes.
- **Superseded or abandoned:** IBM ACP (merged); MCP HTTP+SSE transport (deprecated); JSON-RPC batching in MCP (added then removed within a revision); MCP DCR (deprecated); MCP Sampling, Roots and Logging (deprecated); A2A `agent.json` (renamed `agent-card.json`); ChatGPT Instant Checkout as a product (reportedly wound down; ACP the protocol continues).
- **Watch items:**
  - whether MCP Tasks and webhooks plus Server Cards erode A2A's niche;
  - whether WebMCP ships beyond origin trial and gets Gecko/WebKit support;
  - whether ACP and UCP converge as shared members suggest, or stay platform-aligned (ChatGPT vs Google AI Mode);
  - whether DPoP and agent identity work produces an interoperable "agent passport" spanning OAuth, RFC 9421 and AP2 mandates.

### Gaps
- No neutral, quantitative cross-protocol adoption comparison (e.g. MCP vs A2A production traffic) was found.
- No evidence was found either way of a formal ACP–UCP convergence effort, or of A2A joining AAIF (A2A remains a separate LF project in the sources reviewed).
