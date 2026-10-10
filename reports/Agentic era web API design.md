# Agents Send Web API Design Back to Fundamentals

As of October 2026, the state of the art in web API design runs on two tracks that rarely meet. One is a stable classic canon of books and style guides that says almost nothing about AI agents. The other is a fast-moving agent layer documented in protocol specs, vendor engineering posts and practitioner blogs. On the classic side, Arnaud Lauret's *The Design of Web APIs, Second Edition* (June 2025) is the only freshly revised design textbook. The actively maintained style guides from Google, Zalando and Microsoft show no agent rules in their 2026 commits, and no major publisher has yet shipped a book on designing APIs for agent consumers. The agent layer, meanwhile, has consolidated quickly. The Model Context Protocol (MCP) is the de facto tool protocol and now sits under Linux Foundation governance. Its July 2026 revision made it stateless and cacheable, so an MCP server is now effectively an ordinary HTTP API with a fixed message envelope. A2A reached 1.0 for agent-to-agent traffic, and Agent Skills became an open format supported by 46 clients. Design guidance has converged on four practices:

- a few task-level tools instead of one tool per endpoint;
- responses kept within a token budget;
- errors that tell the agent what to do next;
- descriptions written as prompts.

The loud 2025–26 "CLI versus MCP" fight has settled into a layered answer:

- code mode and progressive discovery for large APIs;
- CLIs and Skills for coding agents;
- curated remote MCP where authentication, credential isolation and audit matter.

The practical upshot is that agents reward classic API discipline far more than any new protocol: precise OpenAPI descriptions, standard error formats, idempotency, rate-limit signalling and standard OAuth metadata. The caveat is that nearly every number behind current agent-era guidance comes from vendors and has not been independently replicated.

## A 2021-era canon still anchors the shelf and says nothing about agents

### Lauret's 2025 second edition is the only freshly revised design textbook

Most of the core web API reading list in late 2026 is four to five years old. The one significant new edition is **Arnaud Lauret's *The Design of Web APIs, Second Edition* (Manning, June 2025)**. It is a rewrite covering requirements gathering, OpenAPI with JSON Schema, standardising design decisions "with rationale and automation", and versioning and breaking changes ([Manning](https://manning.com/books/the-design-of-web-apis-second-edition)). That makes it the only end-to-end design textbook written for current OpenAPI tooling. Its listings do not say whether it covers agent consumers. No second edition of JJ Geewax's *API Design Patterns* has appeared, and no third edition of *Continuous API Management*, so the rest of the working shelf dates from 2021–2022.

| Need | Book | Published | Why it still earns shelf space |
|---|---|---|---|
| End-to-end design process, OpenAPI | Lauret, *The Design of Web APIs*, 2nd ed. ([Manning](https://manning.com/books/the-design-of-web-apis-second-edition)) | Jun 2025 | Only design textbook revised for current OpenAPI and JSON Schema tooling |
| Resource-oriented conventions | Geewax, *API Design Patterns* ([O'Reilly](https://www.oreilly.com/library/view/api-design-patterns/9781617295850/Text/copyright.xhtml)) | Jul 2021 | Book companion to Google's AIPs |
| Pattern language and decision records | Zimmermann, Stocker, Lübke, Zdun, Pautasso, *Patterns for API Design* ([authors' site](https://microservice-api-patterns.org/book)) | Nov 2022 | 44 patterns, plus 29 recurring design decisions with options and criteria |
| Value-driven design | Higginbotham, *Principles of Web API Design* ([Pearson](https://pearson.com/store/p/principles-of-web-api-design-delivering-value-with-apis-and-microservices/P200000007278)) | Dec 2021 | Design process for APIs and microservices |
| Hypermedia and evolvability | Amundsen, *RESTful Web API Patterns and Practices Cookbook* ([O'Reilly](https://oreilly.com/library/view/restful-web-api/9781098106737)) | Oct 2022 | Its principles of discovery, composition and longevity, plus machine-readable metadata, are what agents now need |
| Governance at scale | Medjaoui, Wilde, Mitra, Amundsen, *Continuous API Management*, 2nd ed. ([O'Reilly](https://oreilly.com/library/view/continuous-api-management/9781098103514)) | Oct 2021 | Maturity models for single APIs and whole API landscapes |
| API as product | Pedro, *Building an API Product* ([O'Reilly](https://www.oreilly.com/library/view/building-an-api/9781837630448/)) | Jan 2024 | Persona-led strategy, from design to retirement |
| Platform architecture | Gough, Bryant, Auburn, *Mastering API Architecture* ([O'Reilly](https://www.oreilly.com/library/view/-/9781492090625)) | Oct 2022 | Gateways, service mesh, threat modelling |
| Testing | Winteringham, *Testing Web APIs* ([Books-A-Million](https://www.booksamillion.com/p/Testing-Web-APIs/Mark-Winteringham/9781617299537)) | Dec 2022 | Risk-based, contract and production testing |
| Security | Madden, *API Security in Action* ([Simon & Schuster](https://www.simonandschuster.ca/books/API-Security-in-Action/Neil-Madden/9781638356646)) | Nov 2020 | Still the definitive developer-level API security text |

Behind that shelf sit the foundational texts. Roy Fielding's 2000 dissertation is still the primary source on REST constraints ([UC Irvine](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)), and *RESTful Web APIs* (2013) remains the grounding in hypermedia ([TUM catalog](https://search.ub.tum.de/vufind/Record/ZDB-30-ORH-047586400)). Books on specific API styles have aged worst. Marc-André Giroux's *Production Ready GraphQL* (2020) ([author](https://xuorig.medium.com/production-ready-graphql-is-now-available-9987c9422be7)) and *gRPC: Up and Running* (2020) ([O'Reilly](https://oreilly.com/library/view/grpc-up-and/9781492058328)) both predate the September 2025 GraphQL spec edition and the newer Protobuf editions. For those styles, the official specs are now the current references.

### Active style guides keep evolving but have not written agent rules

Three public style guides are clearly alive:

- **Google's AIPs** had commits through 7 October 2026, including a June 2026 change to AIP-136 that allows complex GETs to be sent as POST ([GitHub](https://github.com/aip-dev/google.aip.dev/commits/master)).
- **Zalando's RESTful API Guidelines** last changed on 29 September 2026, clarifying the end-to-end meaning of HTTP status codes ([GitHub](https://github.com/zalando/restful-api-guidelines/commits/main)).
- **Microsoft's REST API Guidelines** are moderately active. The vNext branch now holds separate Azure and Microsoft Graph guides, and nullable-enum guidance was merged in August 2026 ([GitHub](https://github.com/microsoft/api-guidelines)).

By contrast, the Heroku HTTP API Design Guide is frozen; its last commit, in January 2024, fixed a README link ([GitHub](https://github.com/interagent/http-api-design/commits/master)). Lauret himself says his API Stylebook index of public guides needs a refresh ([API Stylebook](https://apistylebook.com/about/)).

Stripe still publishes no formal guide, but it remains the reference for how to evolve an API. It uses date-based versions pinned per account. Since 2024-09-30.acacia it has shipped monthly non-breaking releases plus twice-yearly named releases that may break clients ([Stripe](https://stripe.com/ae/blog/api-versioning); [brandur.org](https://brandur.org/api-upgrades)).

**No recent commit title in the three active guides mentions AI, LLMs, agents or MCP.** This check covered commit titles only, not the full text. Any team that wants rules on tool granularity, error wording or description quality must write them on top of these guides itself.

### Agent-era knowledge lives in engineering posts, specs and talks

No major publisher had released a book on designing web APIs for agent consumers by October 2026. The likeliest first canonical title is Mike Amundsen's ***AI-Driven API Design*** (O'Reilly). His bios describe it as his current book project, but no publication date or early-release listing was found ([Sessionize](https://sessionize.com/mike-amundsen); [Substack](https://mamund.substack.com/p/ai-driven-api-design)). His free Treblle ebook, *Preparing your APIs for AI Agents*, covers "intention over interface" and rich metadata that lets agents decide on their own ([Treblle](https://treblle.com/ebooks/preparing-your-apis-for-ai-agents)).

The de facto textbook is a blog post: **Anthropic's "Writing effective tools for agents — with agents" (September 2025)**. It covers which tools to build, namespacing, token-efficient responses and improving tools through evaluation ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)).

MCP-specific books arrived quickly and are ageing just as fast. Packt's 2025 titles, such as Christoffer Noring's *Learn Model Context Protocol with Python* (October 2025), predate the July 2026 stateless redesign ([Packt](https://www.packtpub.com/en-us/product/learn-model-context-protocol-with-python-9781806103225)). Kyle Stratis's *AI Agents with MCP* (O'Reilly, September–October 2026) is the only one confirmed to target the 2026-07-28 spec ([O'Reilly](https://www.oreilly.com/library/view/ai-agents-with/9798341639546/)).

Broader agent-engineering books treat APIs as one topic among many. Examples are Michael Albada's *Building Applications with AI Agents* (O'Reilly, 2025) ([O'Reilly](https://www.oreilly.com/library/view/building-applications-with/9781098176495/)) and Nicole Koenigstein's *AI Agents: The Definitive Guide* (O'Reilly early release, September 2026), which covers API contracts and interface isolation for tools ([O'Reilly](https://www.oreilly.com/library/view/ai-agents-the/0642572247775/)).

Free courses split the same way. The notable ones teach how to build with MCP: the DeepLearning.AI course made with Anthropic ([DeepLearning.AI](https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic)) and the Hugging Face MCP course ([Hugging Face](https://huggingface.co/learn/mcp-course/en/unit0/introduction)). No free course on API *design* stands out, so the free canon for design is still the style guides and Fielding.

The community's thought leaders have all reframed their work around agents, mostly through talks, newsletters and interviews rather than books:

- **Nordic APIs** has themed its 2026 Summit in Stockholm (13–14 October) "Evolving APIs for the Agentic Era" ([Nordic APIs](https://nordicapis.com/)).
- **Kin Lane**, now a co-founder of Naftiko, argues that many AI-tooling problems "boil down to API design problems" ([Nordic APIs](https://nordicapis.com/kin-lane-on-ai-and-the-future-of-apis/)). He also says "the API portal is the clearest signal of whether your company can handle AI agents" ([The New Stack](https://thenewstack.io/mcp-api-governance-readiness/)).
- **Erik Wilde** left INNOQ in September 2025 to lead enterprise strategy at Jentic, a company focused on making API landscapes usable by agents ([Agile Brand Guide](https://agilebrandguide.com/jentic-welcomes-api-pioneer-erik-wilde-as-head-of-enterprise-strategy/)). He says MCP will not fix a poorly designed API ([Deep Engineering](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards)).

Some older institutions have faded. Stoplight's API Intersection podcast ended in January 2024 after the SmartBear merger ([Muck Rack](https://muckrack.com/podcast/api-intersection/)).

## Standards bodies assembled an agent-readiness toolkit piece by piece

### OpenAPI added streaming and workflows and now explores intent signalling

**OpenAPI 3.2.0 (dated 19 September 2025)** is the current feature release and is fully backward compatible with 3.1. It adds:

- streaming media (Server-Sent Events and JSON Lines) via `itemSchema`;
- the `QUERY` method, plus `additionalOperations` for other methods;
- hierarchical tags and a `$self` identity field;
- OAuth device flow and OAuth metadata URLs.

([OAS 3.2.0](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md); [Redocly](https://redocly.com/blog/openapi-3-2))

Streaming descriptions matter for agents: a token stream or event feed can now be described precisely, so tool generators no longer have to treat it as an opaque string. Version 3.3.0 is in development with no release date ([OAS v3.3-dev](https://github.com/OAI/OpenAPI-Specification/blob/v3.3-dev/src/oas.md)).

The long-promised OpenAPI 4.0 ("Moonwalk") has no end date. The OpenAPI Initiative (OAI) now says there may never be a 4.0 and calls Moonwalk an "ideas engine" that feeds the 3.x line ([OAI](https://www.openapis.org/?p=4090)). Its February 2026 newsletter says Moonwalk treats **LLMs as a new class of API client**. Moonwalk spent the first half of 2026 on metadata that would make OpenAPI documents "agent-ready", including capability discovery and intent signalling ([OAI newsletter](https://www.openapis.org/blog/2026/02/10/openapi-initiative-newsletter-february-2026)).

The OAI's working bridge to agents today is **Arazzo**, its workflow spec. **Arazzo 1.1.0 (17 May 2026)** adds AsyncAPI steps, `dependsOn` and `timeout`, and JSONPath/XPath selectors ([Arazzo 1.1.0](https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.1.0.md)). Its README lists "deterministic API invocation by AI-based LLMs" as a use case ([Arazzo README](https://github.com/OAI/Arazzo-Specification)), and its roadmap targets MCP and A2A step types ([OAI newsletter](https://www.openapis.org/blog/2026/06/09/openapi-initiative-newsletter-june-2026)).

**Overlay 1.1.0** (January 2026) adds a `copy` action ([Overlay 1.1.0](https://github.com/OAI/Overlay-Specification/blob/main/versions/1.1.0.md)). Overlays are the natural standards-based way to add LLM-oriented descriptions to an existing spec without forking it. However, no standard vocabulary for such hints exists. Each OpenAPI-to-MCP converter invents its own `x-mcp` extension, and their meanings conflict ([agentfront](https://github.com/agentfront/mcp-from-openapi); [apis.io](https://apis.io/2026/09/25/redocly-documents-mcp-servers-in-openapi-and-its-own-agent-door-is-undocumented/)).

### GraphQL became the only major spec changed for AI consumers

The **GraphQL September 2025 edition**, the first since October 2021, adds OneOf input objects, schema coordinates, and "descriptions on documents, in motivation for AI-consumers" ([GraphQL changelog](https://github.com/graphql/graphql-spec/blob/main/changelogs/September2025.md)). That makes GraphQL the only major API specification with a normative change made explicitly for AI clients. `@defer` and `@stream` are still not in the spec.

**JSON Schema** is the common language of every LLM tool definition, and MCP has made it its default dialect since November 2025 ([MCP changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)). Yet it is still at **draft 2020-12**, six years on. A new IETF jsonschema working group, active since 30 April 2026, aims to publish it as a Proposed Standard by May 2027 ([JSON Schema blog](https://json-schema.org/blog/posts/ietf-cooperation); [IETF datatracker](https://datatracker.ietf.org/group/jsonschema/history/)).

Other formats moved less. AsyncAPI 3.1.0 (January 2026) is a minor release that adds a ROS 2 binding ([AsyncAPI](https://github.com/asyncapi/website/blob/master/markdown/blog/release-notes-3.1.0.md)). Microsoft's TypeSpec is now 1.x GA, but its MCP server emitters are still in preview ([TypeSpec](https://typespec.io/blog/2025-05-30-typespec-mcp/)).

### HTTP standards cover errors and discovery, but retries and quotas remain drafts

The IETF has quietly published most of the building blocks an agent-friendly HTTP API needs. The gap is telling: the two mechanisms autonomous agents need most, safe retries and quota awareness, are still drafts.

| Building block | Status, Oct 2026 | Why agents care |
|---|---|---|
| Problem Details, RFC 9457 | RFC, Jul 2023 ([RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)) | Machine-readable errors an agent can act on |
| Deprecation header, RFC 9745 (with Sunset, RFC 8594) | RFC, Mar 2025 ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html)) | Lifecycle signals arrive in the response itself |
| api-catalog, RFC 9727 | RFC, Jun 2025 ([RFC 9727](https://www.rfc-editor.org/rfc/rfc9727.html)) | `/.well-known/api-catalog` points to API descriptions |
| QUERY method, RFC 10008 | RFC, Jun 2026; already modelled in OAS 3.2 ([InfoQ](https://www.infoq.com/news/2026/09/http-query-method/)) | Safe, idempotent, cacheable complex reads |
| RateLimit headers | Draft -11, May 2026; IESG approval unconfirmed ([IETF](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/)) | Back-off signals for bursty agent traffic |
| Idempotency-Key header | Draft -07, Oct 2025 ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header)) | Safe automatic retries |
| OAuth 2.1 | Draft -16, Sep 2026 ([IETF](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)) | Normative base of MCP authorization |
| Protected Resource Metadata, RFC 9728 | RFC, Apr 2025 ([RFC 9728](https://www.rfc-editor.org/rfc/rfc9728.html)) | MCP servers must publish it |
| Client ID Metadata Documents | WG draft -02, Jul 2026 ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-02)) | MCP's preferred way for clients to register |
| HTTP Message Signatures for bots | WG draft -00, Sep 2026, built on RFC 9421 ([IETF](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/)) | Verifiable agent identity at the network edge |

Both unfinished drafts are already standard practice. Payment platforms widely implement the Idempotency-Key draft ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header)), and the Agentic Commerce Protocol now makes idempotency mandatory ([ACP changelog](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/changelog/2026-04-17.md)). Designers should implement both drafts in their latest form and expect small syntax changes.

### Agent delegation has no adopted IETF standard before 2027

Authorization tells the same story. **OAuth 2.1 is still an Internet-Draft** (-16, September 2026), with a December 2026 milestone for submission to the IESG ([IETF](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)). MCP nonetheless cites it as a normative reference.

What agents actually rely on are published RFCs:

- the Security Best Current Practice (RFC 9700);
- Protected Resource Metadata (RFC 9728);
- Resource Indicators (RFC 8707);
- DPoP (RFC 9449);
- Rich Authorization Requests, or RAR (RFC 9396);
- Token Exchange (RFC 8693).

To these they add one working-group draft, Client ID Metadata Documents (CIMD), revised in July 2026. CIMD lets a client identify itself with an HTTPS URL that points to a JSON metadata document ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-02)).

Standards for agents acting on a user's behalf (delegation) are a crowd of individual drafts, none adopted by a working group ([Forkast](https://forkast.news/the-ietf-published-a-draft-for-agent-identity-the-market-already-shipped/)). The IETF held a working-group-forming BoF for agent communication protocols ("agentproto") at IETF 126 in July 2026 ([IETF](https://datatracker.ietf.org/wg/agentproto/about/)). A companion BoF on agent discovery was not chartered ([Forkast](https://forkast.news/ietf-defers-dawn-charter-despite-12-drafts-and-broad-industry-support/)). The OpenID Foundation's AI identity group publishes analysis but does not write specifications ([OIDF whitepaper](https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf)).

Until at least 2027, API providers should build agent delegation on Token Exchange, RAR, and short-lived tokens bound to a single audience.

### llms.txt serves coding agents, not search crawlers

At the content layer, **llms.txt** was revised to "v2" in August 2026. The revision adds discovery through the standard `describedby` and `alternate` link relations, and files that apply only to a path ([llms-txt changes](https://github.com/AnswerDotAI/llms-txt/blob/main/nbs/changes.qmd)). About 10% of roughly 300,000 surveyed domains publish one, but crawler data is bleak. One study reportedly found that 97% of files received zero requests ([byfaro.ai](https://byfaro.ai/blog/ai-crawlers-ignore-llmstxt-97-of-the-time-so-stop-making-one)), and another counted 408 requests in more than 500 million bot events ([Limy](https://limy.ai/blog/llms-txt-in-2026-the-full-guide)). The consumer that demonstrably reads these files is coding agents fetching documentation, so for API providers their value is in developer docs, not search visibility.

The neighbouring IETF work is slow. The AI usage-preference vocabulary (aipref) missed its August 2026 milestone without reaching consensus ([IETF](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/)). The webbotauth group adopted its first working-group draft, built on RFC 9421 HTTP Message Signatures, only on 1 September 2026 ([IETF](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/)).

## MCP won the tool layer, then rebuilt itself as plain HTTP

### Five revisions in 20 months ended in a stateless, cacheable core

MCP has had five dated spec revisions. The 2025 releases added features in three steps:

- **March 2025:** OAuth 2.1 authorization, Streamable HTTP and tool annotations.
- **June 2025:** structured tool output, elicitation, and mandatory RFC 8707 resource indicators.
- **November 2025:** CIMD as the recommended way for clients to register, URL-mode elicitation for consent outside the client, experimental long-running Tasks, and JSON Schema 2020-12 as the default dialect.

([2025-03-26](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-03-26/changelog.mdx); [2025-06-18](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/changelog.mdx); [2025-11-25](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx))

**The 2026-07-28 revision is the largest break.** It:

- removes protocol sessions and the `initialize` handshake;
- moves the protocol version and client capabilities into metadata on every request;
- replaces sessions with "explicit, server-minted handles passed as ordinary tool arguments";
- requires `Mcp-Method` and `Mcp-Name` HTTP headers, so gateways can route requests without parsing bodies;
- requires `ttlMs` and a public/private `cacheScope` on list and read results;
- orders `tools/list` deterministically "to improve LLM prompt cache hit rates".

([MCP 2026-07-28 changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx))

The same revision deprecates Sampling, Roots and Logging, three features that set MCP apart from plain APIs. It also deprecates Dynamic Client Registration (DCR) in favour of CIMD, under a new policy that guarantees at least 12 months between deprecation and removal ([MCP changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx)).

The maintainers' reasons are operational. Remote servers used to need "sticky sessions, a shared session store, and deep packet inspection at the gateway"; now they can run "behind a plain round-robin load balancer" ([MCP blog](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)). In effect, MCP has been rebuilt on HTTP's own conventions: stateless requests, routing in headers, cache semantics and resource-like handles. The design gap between "an API" and "an MCP server" has narrowed to a fixed message envelope.

### 41,000 registry listings show momentum, not production depth

Anthropic donated MCP to the Linux Foundation's new **Agentic AI Foundation (AAIF)** on 9 December 2025. Anthropic co-founded the foundation with Block and OpenAI, and its first projects were MCP, goose and AGENTS.md ([MCP blog](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)).

The official **MCP Registry** has been in "preview" since September 2025, with its API frozen at v0.1. No general-availability announcement had appeared by October 2026 ([registry README](https://github.com/modelcontextprotocol/registry/blob/main/README.md)). A full crawl of the live registry API on 10 October 2026 counted **41,332 unique server names, 26,151 of them advertising remote endpoints** ([MCP Registry API](https://registry.modelcontextprotocol.io/v0.1/servers)). In November 2025 the registry had "close to 2,000 entries" ([MCP blog](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)).

Monthly SDK downloads rose from 97 million in December 2025 ([Anthropic](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)) to "close to half-a-billion" in July 2026, according to the maintainers ([MCP blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)). CI installs inflate the download figures and unvetted listings inflate the registry count, so both measure momentum rather than production use.

The first official extension, **MCP Apps** (January 2026), was built with OpenAI and draws on MCP-UI and OpenAI's Apps SDK. It renders tool UIs in sandboxed iframes in Claude, ChatGPT, VS Code and Goose ([MCP blog](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)). The August 2026 roadmap prioritises three things:

- `.well-known` server cards, so clients can discover servers without connecting;
- HTTP transport for local servers;
- progressive tool discovery.

([MCP roadmap](https://blog.modelcontextprotocol.io/posts/mcp-roadmap/))

### A2A, Skills and WebMCP fill the horizontal, procedural and in-browser gaps

**Agent2Agent (A2A).** Google donated this agent-to-agent protocol to the Linux Foundation in June 2025. A2A absorbed IBM's Agent Communication Protocol and reached **v1.0.0 on 12 March 2026**, followed by v1.0.1 in May ([A2A changelog](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md); [i-am-bee/acp](https://github.com/i-am-bee/acp)). Version 1.0:

- separates the application protocol from its JSON-RPC, gRPC and HTTP+JSON bindings;
- drops the implicit and password OAuth grants;
- publishes signed Agent Cards at `/.well-known/agent-card.json`.

The result looks like a conventional enterprise API standard in the mould of Google's AIPs and gRPC. A2A describes the division of labour this way: "MCP is vertical… A2A is horizontal" ([A2A docs](https://github.com/a2aproject/A2A/blob/main/docs/topics/a2a-and-mcp.md)). MCP's planned webhooks, Tasks and server cards are blurring that line. A2A claims more than 150 supporting organisations ([Linux Foundation](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)) but discloses no traffic figures.

**Agent Skills.** Anthropic introduced `SKILL.md` folders in October 2025 and opened the format in December 2025 ([Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)). Skills load progressively: the agent sees only the name and description at first, loads the full body when relevant, and runs bundled scripts on demand. The agentskills.io showcase now lists **46 client products**, including ChatGPT and Codex, Gemini CLI, GitHub Copilot, Cursor and Claude Code ([agentskills](https://github.com/agentskills/agentskills/blob/main/docs/snippets/clients.jsx)). A Skill usually wraps an existing CLI or HTTP API with know-how about how to use it, rather than defining a new wire interface.

**WebMCP.** This W3C community incubation, by authors from Microsoft and Google, lets a web page register tools through `document.modelContext.registerTool()`. The tools run under the user's existing browser session. Its authors position it explicitly against backend integrations through MCP or OpenAPI. It is in origin trials in Chrome 149 and Edge 150, with no commitment yet from Firefox or Safari ([WebMCP](https://github.com/webmachinelearning/webmcp); [implementation status](https://github.com/webmachinelearning/webmcp/blob/main/implementation-status.md)).

### Commerce protocols revive HTTP 402 while consumer demand lags

Agentic commerce is the most commercially active agent vertical, and its protocols are consolidating into two checkout stacks:

- the **Agentic Commerce Protocol (ACP)** from OpenAI and Stripe, now with Meta as a lead maintainer ([ACP maintainers](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/MAINTAINERS.md));
- the **Universal Commerce Protocol (UCP)** from Google and Shopify, whose council includes Stripe, Meta, Amazon and Microsoft ([UCP maintainers](https://github.com/Universal-Commerce-Protocol/.github/blob/main/MAINTAINERS.md)).

Beneath them sit payment layers. Google's AP2 uses signed payment mandates (v0.2, April 2026) ([AP2 changelog](https://github.com/google-agentic-commerce/AP2/blob/main/CHANGELOG.md)). **x402** revives HTTP 402 Payment Required, using a `PAYMENT-REQUIRED` response header, and works over HTTP, MCP and A2A ([x402 v2 spec](https://github.com/x402-foundation/x402/blob/main/specs/x402-specification-v2.md)). Cloudflare's pay-per-crawl, still in closed beta, also answers unpaid crawlers with a 402 and pricing ([Cloudflare docs](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl.mdx)).

ACP's April 2026 version holds lessons for any API ([ACP changelog](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol/blob/main/changelog/2026-04-17.md)). It:

- mandates idempotency;
- advertises its `rest` and `mcp` transports in a well-known document;
- returns `supported_versions` in version-mismatch errors, so agents can negotiate a version.

Demand has not kept pace with the specs. OpenAI reportedly wound down ChatGPT Instant Checkout in March 2026 after weak uptake ([Shopifreaks](https://www.shopifreaks.com/openai-pivots-from-instant-checkout-to-an-app-based-shopping-model-inside-chatgpt/)). CoinDesk reported x402 volume of around $28,000 a day that month, far below the issuers' headline counts ([CoinDesk](https://www.coindesk.com/tech/2026/05/05/ai-agents-are-breaking-web-economics-but-cloudflare-says-x402-can-help)).

### Identity converges on OAuth metadata while prompt injection stays unsolved

MCP's 2026-07-28 authorization spec reads like a profile of an OAuth resource server ([MCP authorization](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/index.mdx)):

- servers **must** publish RFC 9728 Protected Resource Metadata;
- clients **must** bind each token to the target server with RFC 8707;
- servers must reject tokens issued for anyone else ("no token passthrough");
- CIMD is preferred, and DCR is deprecated.

For enterprises, **Enterprise-Managed Authorization** became stable on 18 June 2026. During single sign-on, the client obtains an Identity Assertion JWT Authorization Grant (ID-JAG) from the corporate identity provider, so users see no per-server consent screen. Okta supports it first, and servers from Asana, Atlassian, Canva, Figma, Linear and Supabase have adopted it ([MCP blog](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/)).

A separate "know your agent" layer is forming around RFC 9421 HTTP Message Signatures. Both Cloudflare's Web Bot Auth ([Cloudflare docs](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/bots/reference/bot-verification/web-bot-auth.mdx)) and Visa's Trusted Agent Protocol ([Visa](https://github.com/visa/trusted-agent-protocol)) use it.

Security is the weakest layer. Simon Willison's "lethal trifecta" remains the governing threat model: private data, untrusted content and external communication in one session ([Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)). The MCP maintainers state that tool annotations such as `readOnlyHint` "cannot stop prompt injection" and that "hard guarantees need network controls or sandboxing" ([MCP blog](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)).

Most critical MCP vulnerabilities are ordinary web bugs, made worse because the servers expose local capabilities to a model. Examples:

- OS command injection in mcp-remote (CVE-2025-6514, CVSS 9.6) ([CVE](https://www.cve.org/CVERecord?id=CVE-2025-6514));
- missing authentication between the MCP Inspector client and its proxy, allowing remote code execution (CVE-2025-49596) ([CVE](https://www.cve.org/CVERecord?id=CVE-2025-49596));
- an MCP endpoint that treated an empty IP allowlist as "allow all" (CVE-2026-33032, CVSS 9.8) ([CVE](https://www.cve.org/CVERecord?id=CVE-2026-33032)).

OWASP's **LLM Top 10 2026** (August 2026) names "an MCP server's output" as a route for indirect prompt injection. It advises holding "credentials and state-change capability in application code, not the model", behind a deterministic policy engine ([OWASP](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md)). A dedicated OWASP MCP Top 10 is in beta ([OWASP](https://github.com/OWASP/www-project-mcp-top-10)).

## Task-level tools beat endpoint mirrors, mostly on vendor evidence

Guidance on designing for agent consumers has converged since late 2025. Anthropic's tool-writing guide calls tools "a contract between deterministic systems and non-deterministic agents" and warns against tools that "simply wrap API endpoints" ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)). Its advice:

- build `schedule_event` rather than separate list and create tools, and `search_logs` rather than `read_logs`;
- prefix tool names by service and resource;
- return human-readable names instead of UUIDs;
- offer a `response_format` switch (a detailed Slack response cost 206 tokens versus 72 for the concise one);
- paginate and truncate, and tell the agent how to narrow its query;
- replace opaque error codes with actionable guidance.

Anthropic's companion context-engineering post adds a test: "if a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better" ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

Production reports point the same way:

- **Block's** playbook, drawn from more than 60 internal MCP servers, says to start from the workflow rather than the endpoints ([Block](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)).
- **GitHub** cut its MCP server's default tool count by 49% and merged CRUD tools such as `create_issue` and `update_issue` into one `issue_write` tool. It also cut output tokens by more than 75% on tools like `list_pull_requests` ([Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1); [GitHub changelog](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/)).
- **Vercel** replaced most of its text-to-SQL agent's specialised tools with a single bash tool over a file-based semantic layer. It reported success rising from 80% to 100%, with responses 3.5 times faster ([Vercel](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)).
- **Neon** runs a hybrid: generated tools for broad coverage, plus 19 hand-written tools for workflows ([Neon](https://neon.com/blog/give-your-agent-neon-tools)).

The anti-pattern now has institutional backing. Thoughtworks put **"naive API-to-MCP conversion" on Hold** in its November 2025 Technology Radar. Its reasoning: APIs built for humans consist of "granular, atomic actions" that inflate token use and can expose destructive operations with no deterministic safeguard ([Thoughtworks](https://www.thoughtworks.com/radar/techniques/naive-api-to-mcp-conversion)). Jeremiah Lowin, author of FastMCP, tells builders to "stop thinking about endpoints and start thinking about products", and recommends converting from OpenAPI only to bootstrap a server ([jlowin.dev](https://jlowin.dev/blog/stop-converting-rest-apis-to-mcp)). Erik Wilde estimates that a genuinely agent-friendly GitHub API "might also just have around 70 operations" ([Deep Engineering](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards)).

Limits on tool count remain soft. OpenAI suggests fewer than 20 functions at a time ([OpenAI guide, via mirror](https://docs.apiyi.com/en/api-capabilities/openai/function-calling)). Anthropic recommends loading tool definitions on demand once they exceed about 10,000 tokens or ten tools ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)).

The guidance sounds uniformly confident, but the evidence behind each rule varies widely:

| Rule | Main source | Evidence |
|---|---|---|
| Load tool definitions on demand (tool search) | Anthropic | Internal eval on MCP tasks: Opus 4 rose from 49% to 74%, Opus 4.5 from 79.5% to 88.1%; about 85% fewer tokens ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)) |
| Embed example calls in tool definitions | Anthropic | Internal eval: 72% to 90% accuracy on complex parameters ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)) |
| Consolidate into task-level tools | GitHub, Vercel, Block | Production reports: 49% fewer tools and 75% fewer output tokens; success up from 80% to 100% ([Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1); [Vercel](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)) |
| Concise response modes | Anthropic | A single example: 206 vs 72 tokens ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)) |
| Readable IDs, actionable errors | Anthropic | Qualitative eval claims with no effect sizes ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)) |
| Hypermedia links for runtime discovery | Amundsen, Lane | Argument only ([Nordic APIs](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)) |
| Idempotency keys and dry-run modes for agents | Classic literature, ACP | No agent-specific eval found |

Classic principles are being re-examined rather than discarded:

- **Hypermedia is back.** Nordic APIs calls HATEOAS "the API design style that was waiting for AI". It cites Amundsen's GRAIL framework, in which a client discovers available actions at runtime "without any prior knowledge" ([Nordic APIs](https://nordicapis.com/hateoas-the-api-design-style-that-was-waiting-for-ai/)). Kin Lane suggests hypermedia "was perhaps just early" ([API Evangelist](https://guidance.apievangelist.com/store/hypermedia/)).
- **GraphQL vendors are pitching for agents.** Apollo presents typed GraphQL schemas and persisted operations as the agent's data contract layer ([Apollo](https://www.apollographql.com/blog/apollo-mcp-server/how-to-build-ai-agents-using-your-graphql-schema)). No independent benchmark against REST exists.
- **The discipline has a name.** Netlify CEO Matt Biilmann coined **"agent experience" (AX)** in January 2025 ([Netlify](https://www.netlify.com/agent-experience/)).
- **Rate limiting needs rethinking.** Agent workflows chain 10 to 20 sequential calls, so a single 429 can fail a whole task. That pushes providers toward limits based on tokens or cost, spending caps per task, and retry budgets ([Zuplo](https://zuplo.com/learning-center/token-based-rate-limiting-ai-agents)).

Two tensions remain unresolved.

**Consolidation versus least privilege.** Merging create, update and delete into one write tool with a `method` parameter, as GitHub did, mixes destructive and harmless operations and makes per-tool approval coarser. Meanwhile, community guidance for Gemini says each function should "do one thing well" ([gemini_ex guide](https://hexdocs.pm/gemini_ex/function_calling.html)).

**Versioning for model consumers.** Agents re-read tool descriptions on every call, so editing a description changes behaviour. Anthropic stopped a web-search tool from needlessly adding "2025" to queries purely by rewording its description ([Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)). Yet no source defines whether a description edit counts as a breaking change, or how to version an API for LLM consumers.

## The CLI-versus-MCP fight ended in code mode

The sharpest debate of 2025–26 was whether agents need MCP at all. It ran in three phases.

**Phase 1, early 2025: MCP hype.**

**Phase 2, mid-2025 to early 2026: the backlash.** Critics pointed to MCP's token overhead and to coding agents' fluency with shells:

- Armin Ronacher argued that MCP "demands too much context" and that composition happens through inference ([Ronacher](https://lucumr.pocoo.org/2025/7/3/tools/)).
- Mario Zechner replaced browser MCP servers with a README and four Puppeteer scripts. That avoids the 13,700–18,000 tokens such servers load per session ([Zechner](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/); [browse-tool](https://github.com/nino-chavez/browse-tool)).
- Simon Willison called Skills "maybe a bigger deal than MCP" ([Techmeme](https://www.techmeme.com/251017/p14)).
- Eric Holmes's "MCP is dead. Long live the CLI" topped Hacker News in February 2026 ([summary](https://velog.io/@surim014/mcp-is-dead-long-live-the-cli)).
- Perplexity's CTO reportedly said in March 2026 that the company was moving to APIs and CLIs internally ([agent-engineering.dev](https://www.agent-engineering.dev/article/why-perplexity-is-stepping-back-from-the-model-context-protocol-mcp-internally)). The widely repeated "72% context waste" figure is a worst case measured by Apideck, not Perplexity's own number.

**Phase 3, second half of 2026: convergence on code mode,** described below.

The benchmarks are thin and mostly measure cost rather than correctness:

- **Scalekit** ran 75 tests on Claude Sonnet 4. The `gh` CLI succeeded 100% of the time against 72% for GitHub's MCP server, and MCP used 4–32 times more tokens. On the simplest task the CLI used 1,365 tokens and MCP 44,026, mostly schema overhead. Critics note that most MCP failures were timeouts and remote-server problems ([Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use)).
- **Arize** ran a larger 500-trial study on Claude Opus 4.6. Correctness was tightly clustered: MCP 0.834, two Skill variants 0.826 and 0.833, and a bare-model baseline 0.845. On the hardest tier, MCP cost more than six times as much as Skills. Arize concluded that "the question was wrong" ([Arize](https://arize.com/blog/mcp-vs-cli-skills-for-agents-what-our-eval-found-and-which-you-should-use/)).

The defensible reading is that the choice of surface mainly changes cost and latency, not success rates.

The pro-MCP side won the argument about where the overhead comes from. GitHub's Sam Morrow argued that critics confuse "the laziest possible MCP implementation with the protocol itself" ([Sam Morrow](https://sam-morrow.com/blog/progressive-discovery-in-mcp-part-1)). Vendors' own fixes cut the overhead by 50% to 99.9%. By September 2026 Willison's position had softened. For a terminal agent with unrestricted internet access, "there's almost no reason to use MCPs". For tightly controlled agents, though, MCP limits which services are reachable, keeps API keys away from the model and supports audit logging ([Willison](https://simonwillison.net/2026/Sep/20/hn-49779718/)). A CLI, by contrast, "inherits whatever ambient permissions the shell user has" ([palma.ai](https://palma.ai/blog/mcp-vs-cli-not-the-same-thing)), and most SaaS services that business users need have no CLI at all.

The synthesis is **code mode**: the model writes code against an API inside a sandbox, instead of calling tools one at a time.

- **Cloudflare** argued in September 2025 that models have seen "millions of lines of real-world code" but only contrived tool-calling examples ([Cloudflare docs](https://developers.cloudflare.com/agents/api-reference/codemode)). By February 2026 it exposed its entire API through two tools: `search()` over the OpenAPI spec, and `execute()`. Those tools take about 1,000 tokens, versus more than a million for conventional per-endpoint tools ([Cloudflare](https://blog.cloudflare.com/code-mode-mcp/); [InfoQ](https://www.infoq.com/news/2026/04/cloudflare-code-mode-mcp-server/)). In March 2026 code mode became the default for its MCP portals ([Cloudflare changelog](https://developers.cloudflare.com/changelog/post/2026-03-26-mcp-portal-code-mode/)).
- **Anthropic's** "code execution with MCP" post showed one workflow falling from about 150,000 tokens to 2,000 ([Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)). Its programmatic tool calling cut average tokens by 37% on complex research tasks ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use)).
- **Pi 1.0**, the coding agent that had long refused MCP, made the emblematic reversal on 1 October 2026 by adding MCP support through "Codemode" ([The Register](https://www.theregister.com/ai-and-ml/2026/10/02/pi-coding-agent-pulls-a-180-and-adds-mcp-support/5300678)). Ronacher followed with "What is Codemode", revisiting his own scripts-over-MCP advice ([Ronacher](https://lucumr.pocoo.org/2026/10/6/codemode/)).
- **Kin Lane** pushes the logic further. Agents should write deterministic, reviewable integration code once, rather than spend effort "interpreting the same response for the ten-thousandth time" ([API Evangelist](https://apievangelist.com/2026/09/01/agents-should-write-code-to-integrate-not-infer/)).

Which surface to use depends on the context:

| Context | Best-supported surface | Why |
|---|---|---|
| Local coding agent using a well-known tool (`gh`, `git`, `kubectl`) | CLI plus a Skill | Models already know these tools from training; lowest token cost ([Scalekit](https://www.scalekit.com/blog/mcp-vs-cli-use); [Arize](https://arize.com/blog/mcp-vs-cli-skills-for-agents-what-our-eval-found-and-which-you-should-use/)) |
| Large API with hundreds of endpoints | Code mode: search over the OpenAPI spec plus sandboxed execution | About 1,000 tokens for Cloudflare's 2,500-endpoint API ([Cloudflare](https://blog.cloudflare.com/code-mode-mcp/)) |
| Remote SaaS, multi-tenant auth, enterprise audit | Curated remote MCP with OAuth | Keeps credentials away from the model; supports allowlists and audit ([Willison](https://simonwillison.net/2026/Sep/20/hn-49779718/)) |
| Integration that runs repeatedly in production | Deterministic code written by an agent | Reviewable and testable ([API Evangelist](https://apievangelist.com/2026/09/01/agents-should-write-code-to-integrate-not-infer/)) |
| Interactive web app used under the user's session | WebMCP (origin trial only) | No separate OAuth; keeps the UI context ([WebMCP](https://github.com/webmachinelearning/webmcp)) |

## Codegen consolidation and AI gateways redrew the vendor map

### One OpenAPI spec now emits SDKs, CLIs, MCP servers and agent docs

The market for SDK generators consolidated in under a year:

- **Postman** bought liblab in November 2025 and Fern in January 2026 ([Business Wire](https://www.businesswire.com/news/home/20251114198999/en); [Business Wire](https://www.businesswire.com/news/home/20260107174767/en/Postman-Acquires-Fern-to-Help-Businesses-Deliver-World-Class-Developer-Experiences)).
- **Anthropic acquired Stainless on 18 May 2026** ([Anthropic](https://www.anthropic.com/news/anthropic-acquires-stainless)). Stainless generated every official Anthropic SDK and, reportedly, SDKs for OpenAI, Google and Cloudflare ([TechRepublic](https://www.techrepublic.com/de/article/news-anthropic-acquires-stainless-developer-tools/)). The reported price was over $300M ([AI Weekly](https://aiweekly.co/alerts/anthropic-acquires-stainless-sdk-startup-for-300m)). Anthropic said it would wind down all hosted Stainless products, including the SDK generator ([RuntimeWire](https://runtimewire.com/article/anthropic-acquires-stainless-devtools)).

The market answered with open source. On 17 September 2026 Google partnered with Speakeasy to open-source Speakeasy's code generators, citing the abrupt shutdown of the provider it had relied on ([Google Developers Blog](https://developers.googleblog.com/why-client-sdk-generation-belongs-in-the-open/)). Within about two weeks, Cloudflare released **Forge**, an Apache-2.0 pipeline that generates SDKs, CLIs, docs and MCP servers from an OpenAPI spec ([The New Stack](https://thenewstack.io/cloudflare-forge-anthropic-stainless/)).

Across the surviving vendors, the standard output from a single OpenAPI spec is now:

- SDKs and a CLI;
- an MCP server;
- llms.txt and a Markdown version of every docs page;
- a hosted docs-search MCP endpoint.

Fern serves its docs MCP endpoint at `/_mcp/server` ([Fern](https://buildwithfern.com/learn/docs/ai-features/mcp-server.md)) and Mintlify at `/mcp` ([Mintlify](https://www.mintlify.com/docs/ai/model-context-protocol)). Redocly's supports the 2026-07-28 protocol and announces itself through an MCP server card and an A2A agent card ([Redocly](https://redocly.com/blog/ai-features-summer-2026)).

Vendors have also abandoned generating one tool per endpoint. Stainless shipped a code-execution tool plus docs search ([Stainless](https://www.stainless.com/products/mcp)), and Mintlify exposes API endpoints as tools only when the customer opts in ([Mintlify](https://www.mintlify.com/docs/ai/model-context-protocol)). Mintlify's $45M Series B at a $500M valuation in April 2026 shows how much investors now value docs as agent infrastructure ([Mintlify](https://mintlify.com/blog/series-b)).

### Gateways became agent-traffic control and now constrain spec design

Every major API-management vendor now ships some combination of four capabilities:

- exposing REST APIs as MCP tools;
- proxying and governing MCP servers, with OAuth and per-tool access control;
- metering LLM token use;
- increasingly, proxying A2A traffic.

Examples:

- **Kong** Gateway 3.14 (April 2026) added an Agent Gateway for A2A alongside its MCP and LLM plugins ([API Evangelist](https://blogs.apievangelist.com/blogs/kong-2026-04-14-govern-full-ai-data-path-3-14/)).
- **Google Apigee:** the API hub MCP server went GA in July 2026, and Apigee API Products can now match fields inside JSON-RPC payloads to apply quotas per MCP operation ([Apigee release notes](https://docs.cloud.google.com/apigee/docs/release-notes)).
- **Azure API Management** can expose REST APIs as MCP servers, but only as tools; it does not support MCP resources or prompts ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/api-management/mcp-server-overview)).
- **Gravitee** quarantines an MCP tool whenever its schema or scope changes, until an owner re-approves it ([Gravitee](https://www.gravitee.io/blog/gravitee-4.8-agent-mesh)).
- **agentgateway**, an open-source proxy, joined the AAIF in June 2026 ([agentgateway](https://agentgateway.dev/blog/2026-06-04-agentgateway-joins-aaif/)).

Independent AI-gateway startups are being absorbed by security and integration vendors. Palo Alto Networks completed its acquisition of Portkey in May 2026 ([Palo Alto Networks](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents)), and Boomi moved to buy Lunar.dev ([Business Wire](https://www.businesswire.com/news/home/20260513850557/en/Boomi-Announces-Intent-to-Acquire-Lunar.dev-to-Deliver-Governed-Agent-Connectivity-Across-the-Enterprise)).

Gateways now act as de facto style guides. **AWS Bedrock AgentCore Gateway requires an `operationId` on every operation and does not support `oneOf`/`anyOf`** ([AWS docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-core-concepts.md)). Teams whose specs must flow into agent gateways therefore face real pressure toward simple schemas and well-named operations.

Registries follow a layered model. The official MCP Registry is the upstream source, with enterprise sub-registries from GitHub, Docker, Kong, Azure and Apigee beneath it. Registry allowlists are weak controls, though. GitHub's "registry only" policy matches on server names and can be bypassed by editing configuration files ([Beri.net](https://www.beri.net/article/mcp-server-governance-allowlist-registry-gateway-buyers-guide)).

### The design-first toolchain survives and gains an AI-readiness score

AI has not displaced the classic design-first toolchain:

- linting with Spectral rulesets, or the faster, Go-based vacuum ([Speakeasy](https://www.speakeasy.com/blog/why-we-built-our-own-openapi-linter));
- breaking-change detection with oasdiff ([oasdiff](https://github.com/tufin/oasdiff/blob/v1.10.16/BREAKING-CHANGES.md));
- mocking with Microcks, a CNCF Incubating project since May 2026 ([CNCF](https://www.cncf.io/blog/2026/05/07/microcks-becomes-a-cncf-incubating-project/));
- contract testing with Pact.

What has changed is that these tools now ship their own MCP servers and Skills, so coding agents can operate them ([PactFlow](https://pactflow.io/blog/pactflow-mcp-server/)).

A new category scores specs for agent readiness. Jentic's free AI-Readiness Scorecard grades OpenAPI documents on dimensions that include semantic clarity and "AI discoverability". Its premise is that a spec can pass Spectral "and yet your AI agent still fails to use the API reliably" ([Jentic](https://www.jentic.com/blog/agent-check-if-your-apis-are-ai-ready)). No industry-standard ruleset for agent readiness exists yet.

### API-first leaders converged on the same agent playbook

The leading API-first companies now ship strikingly similar agent surfaces:

- **Stripe** runs a remote MCP server and recommends restricted API keys ([Stripe](https://docs.stripe.com/agents/plugin)).
- **Twilio** separates a read-only docs MCP server, which needs no account, from an execution server that is still in alpha ([Twilio](https://www.twilio.com/docs/mcp)).
- **Notion** returns "Notion-flavored Markdown" designed for agents ([Stacklok](https://docs.stacklok.com/toolhive/guides-mcp/notion-remote)).
- **Atlassian's** Rovo MCP server went GA in February 2026, with admin allowlists for AI clients ([Scalekit](https://www.scalekit.com/blog/atlassian-mcp-vs-api)).
- **Salesforce's** hosted MCP servers run every request with the calling user's permissions ([Truto](https://truto.one/blog/best-mcp-server-for-salesforce-hosted-mcp-vs-unified-api-2026/)).

The shared pattern has six parts:

1. remote, OAuth-protected MCP servers rather than local ones;
2. agent permissions capped at the human user's permissions;
3. safe docs search kept separate from credentialed execution;
4. curated toolsets rather than one tool per endpoint;
5. response formats optimised for agents;
6. admin controls such as client allowlists and rate limits.

### Only a quarter of developers design for agents, and no traffic baseline exists

Survey data lags behind vendor activity. Postman's 2025 State of the API report (more than 5,700 respondents) found that ([Business Wire](https://secure.businesswire.com/news/home/20251008162423/en/One-in-Four-Developers-Now-Design-APIs-for-AI-Agents-According-to-Postmans-2025-State-of-the-API-Report); [Postman](https://www.postman.com/state-of-api/2025/)):

- **24.3% of developers design APIs with AI agents in mind**;
- 70% are aware of MCP, but only 10% use it regularly;
- the top security worry, cited by 50.8%, is agents making unauthorised or excessive calls.

Postman's 2026 figures could not be verified.

Gartner's 2026 Hype Cycle for APIs says AI agents are "becoming primary consumers of APIs" ([Gartner](https://www.gartner.com/en/documents/7898077)). A vendor relays a Gartner prediction that by 2028, 80% of organisations will see agents consume the majority of their APIs ([Salt Security](https://content.salt.security/Gartner-How-MCP-and-the-A2A-Protocols-Impact-API-V2.html)).

Hard measurements exist only for web traffic. HUMAN Security recorded 7,851% year-on-year growth in 2025 in traffic from AI agents and agentic browsers ([HUMAN](https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/)). There is still no credible cross-industry figure for agents' share of *API* calls.

## Conclusion

The agent era has not produced a new API design discipline. It is better seen as a stress test that calls in the debts of the old one. The 2010s canon argued for self-description, stateless requests, cache semantics, machine-readable errors, idempotent retries and well-known discovery, and many teams skipped them. Agents fail loudly without them. MCP's own path, from stateful sessions to traffic that a plain round-robin load balancer can handle, shows even the agent-native protocol converging on Fielding's constraints.

The deeper shift is in what is scarce. Human developers paid attention once and remembered what they learned. Models pay for every token of every definition on every call. As a result, the OpenAPI document has become a runtime interface that agents search and read in code mode, and the quality of its descriptions now directly changes product behaviour. Spec writing therefore becomes production work that needs change control, and gateway constraints such as mandatory operationIds and simple schemas become design rules.

The open frontier is codification. No major style guide yet covers tool granularity, token budgets, change control for descriptions, or versioning for LLM consumers, and no book yet teaches them. The effect sizes behind today's guidance come almost entirely from the vendors selling the tools. The teams best placed for late 2026 treat one well-described API as the source for several surfaces: a CLI, a Skill, a curated or code-mode MCP server, and SDKs. Four developments are likely to reset the field within a year:

- OpenAPI's agent-metadata work in version 3.3 and Moonwalk;
- publication of the RateLimit and Idempotency-Key drafts as RFCs;
- MCP's progressive tool discovery and server cards;
- Amundsen's book, the first attempt to turn blog-post consensus into a canon.
