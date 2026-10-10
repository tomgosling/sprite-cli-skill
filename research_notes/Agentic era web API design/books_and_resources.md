# Books, Style Guides and Learning Resources for Web API Design (as of October 2026)

Method note: direct fetches of publisher sites (manning.com, oreilly.com), aip.dev, opensource.zalando.com and substack were blocked by this session's network policy (DNS or proxy 403). Book facts below come from web-search snippets of publisher, library-catalog and retailer pages; the dates should be reliable, but some page counts and ISBNs conflict across sources, and those conflicts are flagged. Style-guide activity was checked live by reading GitHub commit histories (github.com was reachable). "Classic/foundational" = published before about Oct 2021 (older than ~5 years). "Current" = Oct 2021 or later.

## Q1. Most-recommended web API design books today, and which have new editions?

### Takeaway
The only major new edition in the core canon is Arnaud Lauret's *The Design of Web APIs, Second Edition* (Manning, June 2025). No second edition of Geewax's *API Design Patterns* and no third edition of *Continuous API Management* turned up. Most of the canon dates from 2021–2022: Geewax, Higginbotham, Zimmermann et al., Amundsen's Cookbook, Winteringham, Gough et al. These books are close to the 5-year line but are still the current reference set. The 2013–2020 titles (Fielding, Richardson/Amundsen/Ruby, Jin/Sahni/Shevat, Madden, Giroux, Indrasiri/Kuruppu) are classic or foundational.

### Cited Findings

**Current (published Oct 2021 – 2026)**
- **Arnaud Lauret, *The Design of Web APIs, Second Edition*** (Manning, **June 2025**, ISBN 9781633438149, foreword by Kin Lane). Manning's product page says 536 pp. Other listings say 576 or 604 (estimate). It is revised and rewritten. It covers requirements gathering, OpenAPI (latest version) plus JSON Schema documentation, streamlining and standardizing design decisions "with rationale and automation", and versioning and breaking changes. Its lessons carry over to other styles: listings name GraphQL in some cases and gRPC in others. Lauret is listed as API Industry Researcher at Postman in some listings and API Governance Lead at Postman in others. Best for: the most current end-to-end, design-first REST/OpenAPI textbook. — [Manning](https://manning.com/books/the-design-of-web-apis-second-edition); [i-programmer](https://www.i-programmer.info/book-watch-archive/18197-the-design-of-web-apis-2nd-ed-manning.html); [Miami Univ. bookstore](https://campusstore.miamioh.edu/design-web-apis-second-edition-arnaud/bk/9781633438149); [Simon & Schuster](https://www.simonandschuster.ca/books/The-Design-of-Web-APIs-Second-Edition/Arnaud-Lauret/9781633438149)
  - No source confirmed whether the 2nd edition has an AI/agent chapter (see Gaps).
  - First edition: Manning, 2019 (classic). — [API Handyman / apistylebook search result](https://apihandyman.io/the-api-stylebook/)
- **Bruno Pedro, *Building an API Product: Design, implement, release, and maintain API products that meet user needs*** (Packt, **January 2024**, 278 pp, ISBN 9781837630448). It covers the whole product lifecycle: API types and protocols, strategy built around personas and jobs-to-be-done, machine-readable definitions, release, usage metrics, docs, versioning and retirement. It is aimed at PMs and developers. The author founded API Changelog. Best for: API-as-product thinking with a design-first slant. — [O'Reilly listing](https://www.oreilly.com/library/view/building-an-api/9781837630448/); [Books-A-Million](https://www.booksamillion.com/p/Building-API-Product/Bruno-Pedro/9781837630448)
- **Mark Winteringham, *Testing Web APIs*** (Manning, **December 2022**, ISBN 9781617299537, examples in Java, forewords by Janet Gregory and Lisa Crispin). It covers risk-based test strategy, contract testing, performance and security testing, and testing in production. Best for: quality and testing strategy for HTTP APIs. — [iMusic listing](https://imusic.mx/books/9781617299537/mark-winteringham-2022-testing-web-apis-paperback-book); [Books-A-Million](https://www.booksamillion.com/p/Testing-Web-APIs/Mark-Winteringham/9781617299537)
- **Olaf Zimmermann, Mirko Stocker, Daniel Lübke, Uwe Zdun, Cesare Pautasso, *Patterns for API Design: Simplifying Integration with Loosely Coupled Message Exchanges*** (Addison-Wesley, Vaughn Vernon Signature Series). The authors' site gives **8 Nov 2022**. Pearson's eText says 26 Dec 2022, © 2023. Print ISBN 9780137670109. The book has 44 patterns, and Chapter 2 presents 29 recurring decisions with options and criteria. The companion site is **microservice-api-patterns.org** (the search did not confirm an "api-patterns.org" domain). Best for: a technology-neutral pattern language for message and endpoint design, and for structuring design decisions. — [Authors' book page](https://microservice-api-patterns.org/book); [Pearson](https://eu.pearson.com/patterns-for-api-design-simplifying-integration-with-loosely-coupled-message-exchanges/9780137669981); [O'Reilly](https://www.oreilly.com/library/view/patterns-for-api/9780137670093)
- **Mike Amundsen, *RESTful Web API Patterns and Practices Cookbook: Connecting and Orchestrating Microservices and Distributed Data*** (O'Reilly, **October 2022**, ~468 pp). The listed ISBNs conflict: 9781098106737 vs 9781098106744. It is a set of recipes for making independently built services interoperate. The appendix gives five principles: discovery, extension, composition, evolution, longevity. Best for: hypermedia and evolvability recipes. Its machine-readable metadata themes are directly relevant to agent consumers. — [O'Reilly](https://oreilly.com/library/view/restful-web-api/9781098106737); [Goodreads](https://www.goodreads.com/en/book/show/63234158-restful-web-api-patterns-and-practices-cookbook)
- **James Gough, Daniel Bryant, Matthew Auburn, *Mastering API Architecture*** (O'Reilly, **October 2022**, 286 pp). It covers API platforms: REST, gateways, service mesh, cloud migration, threat modeling, OAuth2/TLS. Best for: the architect's view of the runtime and platform around APIs. — [O'Reilly](https://www.oreilly.com/library/view/-/9781492090625)
- **Mike Amundsen & Derric Gilling, *API Strategy for Decision Makers*** (O'Reilly report, **July 2022**, 47 pp). It covers product management for APIs, the lifecycle from adoption to monetization and deprecation, portfolio positioning, and observability and analytics. Best for: executives and product owners. — [O'Reilly](https://oreilly.com/library/view/api-strategy-for/9781492096795)
- **James Higginbotham, *Principles of Web API Design: Delivering Value with APIs and Microservices*** (Addison-Wesley, 1st ed., **Dec 8, 2021**, © 2022). Best for: an outcome-driven design process that starts from jobs-to-be-done and domain modeling (ADDR process) before choosing a style. (The ADDR detail comes from general knowledge and was not verified in this session's sources.) — [Pearson](https://pearson.com/store/p/principles-of-web-api-design-delivering-value-with-apis-and-microservices/P200000007278); [O'Reilly](https://www.oreilly.com/library/view/-/9780137355754/)
- **Mehdi Medjaoui, Erik Wilde, Ronnie Mitra, Mike Amundsen, *Continuous API Management, 2nd Edition*** (O'Reilly, **October 2021**, 357 pp; library catalogs give © 2022). It adds maturity models for individual APIs and for multi-API landscapes. **No 3rd edition was found.** The 1st edition was November 2018. Best for: governance, API-as-product lifecycle, and managing API landscapes at scale. — [O'Reilly 2e](https://oreilly.com/library/view/continuous-api-management/9781098103514); [O'Reilly 1e](https://www.oreilly.com/library/view/continuous-api-management/9781492043546)

**Borderline (about 5 years old; still widely cited as current references)**
- **JJ Geewax, *API Design Patterns*** (Manning, **July 2021**, 480 pp, ISBN 9781617295850). It is a catalog of resource-oriented patterns: naming, standard methods, and more. It is closely aligned with Google's AIPs, and the author is a Google engineer. **No second edition found.** Best for: resource-oriented design at large scale, and as the book companion to aip.dev. — [O'Reilly copyright page](https://www.oreilly.com/library/view/api-design-patterns/9781617295850/Text/copyright.xhtml); [Flipkart](https://www.flipkart.com/api-design-patterns/p/itm5cf30ee6902bb)

**Classic / foundational (pre-2021)**
- **Roy T. Fielding, *Architectural Styles and the Design of Network-based Software Architectures*** (PhD dissertation, UC Irvine, **2000**). It defines the REST architectural style. Best for: the primary source on REST constraints. — [UCI landing page](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm); [ProQuest](https://www.proquest.com/docview/304591392)
- **Leonard Richardson, Mike Amundsen, Sam Ruby, *RESTful Web APIs: Services for a Changing World*** (O'Reilly, **September 2013**). It is hypermedia-centric and covers evolvable REST. Best for: a deep REST/hypermedia grounding. — [TUM catalog](https://search.ub.tum.de/vufind/Record/ZDB-30-ORH-047586400)
- **Brenda Jin, Saurabh Sahni, Amir Shevat, *Designing Web APIs: Building APIs That Developers Love*** (O'Reilly, **September 2018**; one listing says Oct 16, 2018). It draws on Slack's practice and covers designing, scaling, marketing and evolving APIs, plus developer experience. Best for: a short, DX-focused primer. — [O'Reilly](https://www.oreilly.com/library/view/api-design-and/9781492026914/); [Bookshop](https://bookshop.org/p/books/designing-web-apis-building-apis-that-developers-love-amir-shevat/e4a06d741fb1ff77)
- **Neil Madden, *API Security in Action*** (Manning, **November 2020**, 576 pp, ISBN 9781617296024, examples in Java). It covers authentication, authorization, OAuth2/OIDC, rate limiting, audit, microservices on Kubernetes, and IoT. Best for: the still-definitive developer-level API security text. — [Tenlong](https://tenlong.com.tw/products/9781617296024); [Simon & Schuster](https://www.simonandschuster.ca/books/API-Security-in-Action/Neil-Madden/9781638356646)
- **Marc-André Giroux, *Production Ready GraphQL*** (self-published ebook, **Mar 23, 2020**, ~180 pp). It is language-agnostic and covers schema design, security, performance, versioning and migration. The author worked on GraphQL APIs at Shopify and GitHub. Best for: GraphQL schema design and operations. — [Author announcement](https://xuorig.medium.com/production-ready-graphql-is-now-available-9987c9422be7); [Goodreads](https://www.goodreads.com/book/show/52719441)
- **Kasun Indrasiri & Danesh Kuruppu, *gRPC: Up and Running*** (O'Reilly, **January 2020**, 202 pp). Examples in Go, Java, Node and Python. Best for: a gRPC/protobuf service-design primer. — [O'Reilly](https://oreilly.com/library/view/grpc-up-and/9781492058328)
- **Mike Amundsen, *Design and Build Great APIs*** (Pragmatic Bookshelf, **2020**), cited in his bio as one of his two most recent books. — [Sessionize bio](https://sessionize.com/mike-amundsen)

**Related spec milestones worth listing as "current reading"**
- **OpenAPI 3.2.0** was announced **Sep 23, 2025**, alongside the 3.1.2 patch. Features include support for the QUERY method and custom methods, and improved multipart/XML handling. OAI newsletters say a planned **v3.3** will bring "greater integration with MCP and AI protocols." — [OpenAPI Initiative blog/newsletters](https://www.openapis.org/blog); [OAI newsletter tag](https://openapis.org/tag/newsletter)
- **Arazzo** (workflow specification) 1.0.0 was released May 2024, 1.0.1 in Jan 2025, and **1.1.0 on May 19, 2026**, adding AsyncAPI support. — [OAI](https://www.openapis.org/tag/ai); [Swagger blog](https://swagger.io/blog/the-arazzo-specification-a-deep-dive/)
- The **GraphQL spec, September 2025 edition**, is the first new edition since October 2021. — [graphql.org](https://graphql.org/blog/2025-09-08-september-edition/)

### Inferences
- The "current core shelf" for a team in late 2026 is: Lauret 2e (2025) for the design process and OpenAPI; Geewax (2021) and Google AIPs for resource-oriented conventions; Zimmermann et al. (2022) for a pattern language and decision records; Higginbotham (2021) for discovery and outcomes; *Continuous API Management* 2e (2021) for governance; Pedro (2024) for product; Madden (2020) for security; Winteringham (2022) for testing. Everything except Lauret 2e and Pedro is 4–5+ years old. That makes Lauret 2e the only design textbook that reflects OpenAPI 3.1+ era tooling.
- GraphQL and gRPC book coverage is stale (2020 titles). The 2025 GraphQL spec edition and OpenAPI 3.2 postdate every book on the list, so official specs and docs are the current sources for those styles.

### Gaps
- I could not fetch manning.com to confirm whether *The Design of Web APIs 2e* includes AI/LLM/agent content. Listings mention only OpenAPI, JSON Schema, GraphQL/gRPC carryover, versioning, and automation of design decisions.
- I did not verify dates for *Designing APIs with Swagger and OpenAPI* (Ponelat & Rosenstock, Manning; an O'Reilly listing exists at ISBN 9781617295102) or for other gRPC books (e.g., *gRPC Microservices in Go*, Manning).
- No 2024–2026 GraphQL design book from a major publisher appeared in searches. I found no reliable evidence either way.
- Phil Sturgeon's *Build APIs You Won't Hate* (2015) and *Surviving Other People's APIs* were not verified in this session.

## Q2. New books (2024–2026) on APIs for AI agents, MCP, agent tool design, "AI-ready APIs"

### Takeaway
As of October 2026 there is **no published book from a major publisher dedicated to designing web APIs for AI agent consumers**. The closest is Mike Amundsen's *AI-Driven API Design* (O'Reilly), which his bios describe as a current book project. I found no publication date and no early-release listing for it. What exists instead falls into three groups:
- MCP implementation books: Packt, O'Reilly, Apress, and Manning agent titles.
- General agent-engineering books that include tool and API chapters.
- Long-form guides from vendors and practitioners. The most cited is Anthropic's "Writing effective tools for agents" (Sept 2025).

### Cited Findings

**API-design-for-agents (closest matches)**
- **Mike Amundsen, *AI-Driven API Design*** (O'Reilly). His Sessionize bio says it is his "current book project", and a later bio says he is "currently writing" it. **No publication or early-release listing was found.** Status: in progress, not published (unverified beyond bios). A related O'Reilly Live course of the same name returned Nov 11, 2025. He also runs an API World workshop, "AI-Driven API Design: Build AI-Ready APIs", which uses AI to extract API vocabulary from user stories, generate OpenAPI, and generate and validate tests. — [Sessionize](https://sessionize.com/mike-amundsen); [Amundsen Substack](https://mamund.substack.com/p/ai-driven-api-design); [API World workshop](https://apiworld.co/workshops/master-workshops-ai-driven-api-design-build-ai-ready-apis/); [WeAreDevelopers bio](https://www.wearedevelopers.com/@mike-amundsen.md)
- **Mike Amundsen, *Preparing your APIs for AI Agents*** (Treblle whitepaper/ebook, free; date not confirmed). It covers designing for machine consumers, "intention over interface", and embedding rich metadata so agents can decide on their own. — [Treblle ebook](https://treblle.com/ebooks/preparing-your-apis-for-ai-agents); [Treblle webinar takeaways](https://blog.treblle.com/ai-api-design-mike-amundsen-webinar-takeways)
- **Anthropic, "Writing effective tools for agents — with agents"** (engineering blog, **Sep 11, 2025**). It is the de facto long-form guide to tool and MCP interface design. It covers prototyping tools, evaluating with agents, choosing which tools to build rather than wrapping every endpoint, namespacing, and returning high-signal, token-efficient responses. — [Anthropic Engineering](https://anthropic.com/engineering/writing-tools-for-agents)
- **AWS ML Blog, "MCP tool design: Practical approaches and tradeoffs"** (date not captured). — [AWS](https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs/)
- The Deep Engineering newsletter #48 has an Erik Wilde interview on agent-ready APIs, MCP adoption, and the OpenAPI standards that matter. In it Wilde argues MCP will not fix a poorly designed API and discusses OpenAPI 3.2. — [Deep Engineering #48](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards); [Building Agent-Ready APIs in Production](https://deepengineering.substack.com/p/building-agent-ready-apis-in-production)

**MCP-specific books (2025–2026)**
- **Kyle Stratis, *AI Agents with MCP: Model Context Protocol for Building Clients, Servers, and End-to-End Agents*** (O'Reilly). O'Reilly shows **Sep 2026** and Amazon lists **Oct 20, 2026**, so the dates conflict. It targets the **2026-07-28 MCP spec** and v2 of the Python MCP SDK. — [O'Reilly](https://www.oreilly.com/library/view/ai-agents-with/9798341639546/); [Amazon](https://www.amazon.com/AI-Agents-MCP-End-End/dp/B0FYCBVGX7)
- **Christoffer Noring, *Learn Model Context Protocol with Python*** (Packt, **Oct 2025**, 304 pp). A related Packt listing, *Getting Started with the Model Context Protocol* (Python + TypeScript), also shows Oct 2025 and appears to be the same or a sibling edition (unclear). — [Packt](https://www.packtpub.com/en-us/product/learn-model-context-protocol-with-python-9781806103225); [Packt (Getting Started)](https://www.packtpub.com/en-us/product/getting-started-with-the-model-context-protocol-9781806103232)
- **Mehul Gupta & Niladri Sen, *Model Context Protocol*** (Packt, **July 2025**). A beginner-to-intermediate book on configuring MCP servers for Gmail, Slack, Excel and similar tools. — [Packt](https://www.packtpub.com/en-us/product/model-context-protocol-9781806112364)
- **Naveen Krishnan, *Model Context Protocol for LLMs*** (Packt, **Feb 28, 2026**). Covers secure, scalable multi-agent systems on MCP. — [Amazon](https://www.amazon.com/Model-Context-Protocol-LLMs-context-aware/dp/1806662272)
- **Gigi Sayfan, *Design Multi-Agent AI Systems Using MCP and A2A*** (Packt, **Feb 27, 2026**). — [Packt](https://www.packtpub.com/en-us/product/design-multi-agent-ai-systems-using-mcp-and-a2a-9781806116461)
- **Srinivasan Sekar, *The MCP Standard: A Developer's Guide to Building Universal AI Tools with the Model Context Protocol*** (Apress, 2026). Covers building MCP servers in TypeScript. — [Springer/Apress](https://link.springer.com/book/10.1007/979-8-8688-2364-0)

**Agent-engineering books with tool/API content**
- **Michael Albada, *Building Applications with AI Agents: Designing and Implementing Multiagent Systems*** (O'Reilly). O'Reilly lists **Sep 2025** (354 pp); a retailer lists Oct 21, 2025. The author's talk distilling the book covers tool use, API selection, and "clear interfaces". — [O'Reilly](https://www.oreilly.com/library/view/building-applications-with/9781098176495/); [AI Engineer talk](https://ai.engineer/talks/building-applications-with-ai-agents)
- **Roberto Infante, *AI Agents and Applications*** (Manning). Published **Feb 2026** per one source; O'Reilly's listing indicates March 2026. Covers LangChain, LangGraph, and MCP. — [Manning](https://www.manning.com/books/ai-agents-and-applications); [O'Reilly](https://www.oreilly.com/library/view/ai-agents-and/9781633436541/)
- **Micheal Lanham, *AI Agents in Action, Second Edition*** (Manning, June 2026 per a secondary roundup). Covers MCP, A2A, and the OpenAI Agents SDK. — [Manning](https://www.manning.com/books/ai-agents-in-action-second-edition); [Computing for Geeks roundup](https://computingforgeeks.com/best-ai-agents-books/)
- **Jia Huang, *Designing AI Agents*** (Manning, **MEAP**, final estimated Spring 2027). — [Manning](https://www.manning.com/books/designing-ai-agents)
- **Nicole Koenigstein, *AI Agents: The Definitive Guide*** (O'Reilly, **Early Release**, dated Sep 2026). It covers integrating agents with tools through sandboxing, **API contracts**, and interface isolation. — [O'Reilly](https://www.oreilly.com/library/view/ai-agents-the/0642572247775/)

**Protocol references (primary sources for agent-facing interfaces)**
- **MCP spec revisions:**
  - **2025-06-18**: removed JSON-RPC batching and added structured tool output, elicitation, and resource links.
  - **2025-11-25**: added OIDC discovery, icons for tools, resources and prompts, URL-mode elicitation, tool calling in sampling, and OAuth Client ID Metadata Documents.
  - **2026-07-28**: makes the protocol **stateless**. It removes the initialize handshake, moves the protocol version and capabilities into per-request metadata, and drops Mcp-Session-Id from Streamable HTTP.
  - Whether 2026-07-28 is final or draft is not confirmed in the snippets. The Stratis book targets it.
  - Sources: [MCP 2025-11-25 changelog](https://modelcontextprotocol.io/specification/2025-11-25/changelog); [MCP 2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog); [third-party version timeline](https://hidekazu-konishi.com/entry/mcp_specification_version_timeline.html)

### Inferences
- The "API design for agents" genre is still mostly blogs, whitepapers, newsletters, and conference talks. Amundsen's O'Reilly book is the most likely first canonical title. Until it ships, the de facto reading is: Anthropic's tool-writing guide, Amundsen's Treblle whitepaper, Wilde's Deep Engineering interviews, and the MCP, OpenAPI 3.2 and Arazzo specs.
- MCP books age fast. The spec changed substantially (stateless redesign) in 2026-07-28, so books pinned to 2025 revisions (Packt 2025 titles) will have outdated transport and session details. Stratis (O'Reilly, Sep/Oct 2026) is the only one confirmed to target the 2026 spec.

### Gaps
- No exact title, publication date, or early-release status confirmed for Amundsen's *AI-Driven API Design*. It could not be found in the O'Reilly catalog via search.
- No Pragmatic Bookshelf or Leanpub title specifically on agent-facing API design surfaced.
- I could not confirm whether Lauret 2e, Pedro, or any style-guide book includes an AI/agent chapter.
- The Treblle whitepaper's publication date was not captured.

## Q3. State-of-the-art corporate/public API style guides; maintenance status 2025–2026; any AI/agent guidance

### Takeaway
Three public guides are clearly active in 2026, with commits in mid to late 2026: **Google AIPs**, **Zalando RESTful API Guidelines**, and **Microsoft REST API Guidelines (vNext: Azure + Graph)**. The Heroku HTTP API Design Guide is effectively frozen, with its last substantive commit in 2021. None of the three active guides' recent commit history shows AI, LLM, agent or MCP guidance. Agent guidance currently lives in vendor blogs and specs, not in the major style guides.

### Cited Findings
- **Google AIPs (aip.dev; repo aip-dev/google.aip.dev):** very active. Commits run through **Oct 7, 2026**. Recent examples:
  - "feat: introduce IBV AIP updates" (Aug 17, 2026)
  - AIP-136 changes allowing complex GET as POST (Jun 10, 2026), with a rationale added by Jon Skeet (Jun 18, 2026)
  - several AIP-203 field-behavior fixes (June 2026)

  None of the 10 most recent commit messages mention AI, agents, or MCP. — [GitHub commits](https://github.com/aip-dev/google.aip.dev/commits/master)
- **Zalando RESTful API Guidelines:** active. Most recent commit **Sep 29, 2026** ("clarify end-to-end semantics of http status codes"). Other 2026 changes:
  - host-name consistency (Jun 2026)
  - interval best practice (May 2026)
  - a changed PATCH recommendation (May 2026)
  - time-local/date-time-local formats (Mar 2026)
  - a changelog update covering rule changes since 2024-06-27 (Mar 2026)

  No AI or agent guidance appears in commit titles. One Mar 3, 2026 commit lists "claude" as co-author on tooling. — [GitHub commits](https://github.com/zalando/restful-api-guidelines/commits/main)
- **Microsoft REST API Guidelines (vNext branch):**
  - The repo has core `Guidelines.md`, `azure/` (Azure REST API Guidelines + Considerations for Service Design), and `graph/` (Microsoft Graph REST API Guidelines + pattern catalog).
  - Recent commits: nullable-enum guidance (May 12, 2026; merged Aug 5, 2026); structural collections (Aug 2025); filter-as-segment (Feb 2025).
  - It is moderately active.
  - A fetch of the repo found no AI, LLM, agent or MCP guidance.

  — [GitHub repo](https://github.com/microsoft/api-guidelines); [commits](https://github.com/microsoft/api-guidelines/commits/vNext)
- **Heroku HTTP API Design Guide (interagent/http-api-design):** last commit **Jan 16, 2024**, a README link fix. Before that, the last commits were in 2021. Classic and frozen. — [GitHub commits](https://github.com/interagent/http-api-design/commits/master)
- **API Stylebook (apistylebook.com, Arnaud Lauret):** a curated index linking topics across public guides. Over time it has covered Atlassian, Cisco, Cloud Foundry, Haufe, Heroku, Microsoft, PayPal, Red Hat, the White House, Zalando and Google. Lauret has said the site "needs some refresh" and is "a real pain to update." Treat it as a historical index. — [apistylebook about](https://apistylebook.com/about/); [API Handyman](https://apihandyman.io/the-api-stylebook/); [API Evangelist 2017](https://www.apievangelist.com/2017/09/26/api-design-industry-guide-api-stylebook/)
- **Stripe:**
  - Stripe has no formal public style guide. Its approach is documented in blog posts and docs.
  - **Date-based rolling versions** with account pinning (Brandur Leach's posts), framed as "safety first" versioning with tens of versions per year.
  - Since **2024-09-30.acacia**, Stripe releases monthly non-breaking versions and twice-yearly named releases that may contain breaking changes. Its docs listed **2026-03-25.dahlia** as current when indexed.
  - The V2 API uses JSON request bodies instead of form encoding.

  — [Stripe blog: API versioning](https://stripe.com/ae/blog/api-versioning); [brandur.org/api-upgrades](https://brandur.org/api-upgrades); [brandur.org/fragments/stripe-v2](https://brandur.org/fragments/stripe-v2); [Stripe versioning docs](https://docs.stripe.com/sdks/versioning?lang=ruby)

### Inferences
- For a 2026 team building a house style guide, Google AIPs (paired with Geewax) and Zalando are the most actively curated public baselines. Microsoft Azure/Graph is the strongest enterprise-scale alternative. Heroku and the older Adidas, PayPal and Atlassian guides are historical reference points.
- Agent and MCP considerations have not yet been codified in the major guides as of their visible 2026 commits. That gap is an opportunity: teams currently need to add their own agent-facing rules (tool granularity, error semantics, descriptions) on top of these guides.

### Gaps
- I could not open aip.dev or Zalando's rendered site (blocked). The AI/agent check covered only the latest ~10 commit titles per repo, not full content, so an older or embedded AI-related rule could exist. "IBV AIP updates" (Aug 2026) was not expanded. Its meaning is unknown.
- GitHub, Adidas, PayPal and Atlassian guide maintenance status was not checked (GitHub API access to those repos was blocked in this session).

## Q4. Ongoing publications, newsletters, blogs, podcasts, communities, conferences (2025–2026 activity and agent pivot)

### Takeaway
The API community has largely pivoted to "agentic" framing. Nordic APIs (2026 Summit theme "Evolving APIs for the Agentic Era"), apidays 2026 (agent-oriented OAI tracks), Kin Lane (now co-founder of Naftiko), Erik Wilde (now at Jentic), and Mike Amundsen (AI-Driven API Design) are all active and agent-focused. The API Intersection podcast ended in Jan 2024. The APIs You Won't Hate podcast had episodes in 2025, but its 2026 activity is unconfirmed.

### Cited Findings
- **Nordic APIs:**
  - Active blog with agent-focused pieces, including "How AI Agents Are Changing API Architecture" (Oct 1, 2026) and "How Identity Guides Agentic AI Use of APIs" (Jan 2026).
  - **Nordic APIs Summit 2026**: Stockholm, **Oct 13–14, 2026**, plus an API Security Unconference on Oct 12, themed "Evolving APIs for the Agentic Era".
  - Free eBooks such as *The API Lifecycle*, *Securing the API Stronghold*, and *Developing the API Mindset*. No agent-specific eBook was found.

  — [Nordic APIs](https://nordicapis.com/); [Exploring the Role of APIs in Agentic AI](https://nordicapis.com/exploring-the-role-of-apis-in-agentic-ai/); [Identity article](https://nordicapis.com/how-identity-guides-agentic-ai-use-of-apis/); [Panel: Designing for the Agentic Experience](https://nordicapis.com/sessions/panel-discussion-designing-for-the-agentic-experience/)
- **Kin Lane (API Evangelist):**
  - apievangelist.com has a 2026 index, and its self-description now includes "agents."
  - He is co-founder of **Naftiko**.
  - In a May 2026 New Stack interview, he argued that API governance, OpenAPI and portals decide which enterprises can handle agents.
  - In Jan 2026 (New Stack), he urged designing around business capabilities rather than resources.
  - In a July 2026 Nordic APIs interview, he said many AI-tooling problems "boil down to API design problems."
  - He is on the panel at the Nordic APIs Summit 2026.

  — [Nordic APIs interview](https://nordicapis.com/kin-lane-on-ai-and-the-future-of-apis/); [The New Stack: MCP/API governance readiness](https://thenewstack.io/mcp-api-governance-readiness/); [The New Stack: map your API landscape](https://thenewstack.io/map-your-api-landscape-to-prevent-agentic-ai-disaster/); [API Evangelist](https://apievangelist.com/llms-home.md)
- **Erik Wilde:**
  - Runs the **Getting APIs to Work** YouTube channel and Substack.
  - Left INNOQ in Sept 2025 and is now **Head of Enterprise Strategy at Jentic**, focused on making API landscapes usable by agents.
  - Interviews: Deep Engineering #48 (agent-ready APIs; MCP won't fix a bad API; OpenAPI 3.2), WunderGraph "The Good Thing" (Feb 2, 2026: "many enterprise APIs are not AI ready"), and heise/iX (codify agentic discoveries into deterministic workflows).

  — [Substack](https://substack.com/@gettingapistowork); [Jentic announcement](https://agilebrandguide.com/jentic-welcomes-api-pioneer-erik-wilde-as-head-of-enterprise-strategy/); [Deep Engineering](https://deepengineering.substack.com/p/agent-ready-apis-mcp-adoption-openapi-standards); [WunderGraph podcast](https://wundergraph.com/the-good-thing/32-erik-wilde); [heise](https://heise.de/-10777659)
- **Mike Amundsen:** runs a Substack (mamund.substack.com), O'Reilly Live courses, an API World workshop, and a World Congress 2026 NA session (Sep 23, 2026). His recent focus is "AI-augmented API design." — [Sessionize](https://sessionize.com/mike-amundsen); [Substack](https://mamund.substack.com/p/ai-driven-api-design); [WeAreDevelopers](https://www.wearedevelopers.com/@mike-amundsen.md)
- **APIs You Won't Hate (Phil Sturgeon, Mike Bifulco):** a book-turned-community with a podcast. A dated episode on code-first vs design-first appeared Jul 1, 2025. A listing shows an Apr 2, 2026 episode, but its details are unconfirmed. No 2026 Sturgeon blog posts were found. — [About](https://apisyouwonthate.com/about/); [Podcast tag](https://apisyouwonthate.com/tag/podcast/); [Castfox episode](https://www.castfox.net/podcast/apis-you-wont-hate-691096/episode/generating-api-specs-can-be-painful-with-joel-clermont-from-mastering-laravel-470628)
- **API Intersection podcast (Stoplight):** **ended Jan 4, 2024** ("final episode") because of the Stoplight–SmartBear merger. It ran 50+ episodes, hosted by Jason Harmon. — [Muck Rack listing](https://muckrack.com/podcast/api-intersection/); [Stoplight 50 episodes](https://blog.stoplight.io/2-years-of-api-intersection-celebrating-50-episodes-of-your-fav-api-podcast)
- **apidays 2026:** Singapore (Apr 14–15), New York (May 13–14, with an OAI track on how OpenAPI supports AI agents), and India (Aug 19–20, "NextGen APIs for both humans and agents"). — [OAI: apidays Singapore 2026](https://www.openapis.org/events/apidays-singapore-2026); [OAI: apidays India 2026](https://www.openapis.org/?p=4453); [OAI events](https://www.openapis.org/?p=4432)
- **API World 2026** (apiworld.co) hosts Amundsen's "AI-Driven API Design: Build AI-Ready APIs" master workshop. The page title suggests a Sept 1, 2026 date, but the exact event dates were not confirmed. — [API World](https://apiworld.co/?p=7505); [workshop](https://apiworld.co/workshops/master-workshops-ai-driven-api-design-build-ai-ready-apis/)
- **OpenAPI Initiative blog/newsletter:** active, with an "ai" tag. It covers OpenAPI 3.2, Arazzo 1.1, and the planned v3.3 MCP integration. — [OAI blog](https://www.openapis.org/blog); [OAI AI tag](https://www.openapis.org/tag/ai)

### Inferences
- The thought leaders who defined the 2010s API canon (Lane, Wilde, Amundsen) have all reframed their work around agent consumers. Their 2025–2026 output is talks, newsletters and interviews rather than books. Following their Substacks and YouTube is the most current way to track agent-era API design thinking.
- Corporate moves (Wilde to Jentic, Lane to Naftiko) suggest a new class of "API-to-agent" vendors is forming around API discovery, governance and agent-readiness.

### Gaps
- Not verified in this session: Arnaud Lauret's API Handyman blog activity in 2025–2026 (no recent agent-related posts surfaced), the Postman blog's agent pivot, and "The API Changelog" (Bruno Pedro's newsletter/brand) current activity.
- Exact 2026 dates and agenda for API World were not confirmed.

## Q5. Free online courses/resources

### Takeaway
The notable free agent/MCP courses are the DeepLearning.AI × Anthropic short course, Anthropic Academy's MCP courses, and the Hugging Face MCP Course (built with Anthropic). For classic API skills, Postman's Academy (API Fundamentals Student Expert) is the best-known free path. It is more about API consumption and testing than design.

### Cited Findings
- **DeepLearning.AI, "MCP: Build Rich-Context AI Apps with Anthropic"** (instructor Elie Schoppik, ~2 hrs). Covers MCP architecture, building servers and clients, and remote deployment. It is free during the platform beta, with a paid certificate. — [DeepLearning.AI](https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic); [Class Central](https://www.classcentral.com/course/independent-mcp-build-rich-context-ai-apps-with-anthropic-565506)
- **Hugging Face MCP Course:** free, built in partnership with Anthropic, and goes from beginner to building MCP apps. — [Hugging Face](https://huggingface.co/learn/mcp-course/en/unit0/introduction)
- **Anthropic Academy, "Introduction to Model Context Protocol"** (free; per a third-party review, Anthropic Academy offers 18 free courses with certificates). — [buildmvpfast review](https://www.buildmvpfast.com/blog/anthropic-free-ai-courses-certificates-claude-2026); [Class Central MCP course roundup 2026](https://www.classcentral.com/report/best-mcp-courses/)
- **Postman Academy, API Fundamentals Student Expert:** hands-on REST and Postman basics leading to a certification badge. Its pricing and design content were not confirmed from official pages. — [DEV article](https://dev.to/adityaiiitr2062/postman-student-expert-certification-a-stepping-stone-to-api-mastery-1bg0)
- **Free long-form reading that functions as a course:**
  - the Fielding dissertation (2000) — [UCI](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
  - Google AIPs — [repo](https://github.com/aip-dev/google.aip.dev)
  - Microsoft Azure/Graph guidelines — [repo](https://github.com/microsoft/api-guidelines)
  - Zalando guidelines — [repo](https://github.com/zalando/restful-api-guidelines)
  - Nordic APIs free eBooks — [Nordic APIs](https://nordicapis.com/ebooks/the-api-economy/)
  - Anthropic's tool-writing guide — [Anthropic](https://anthropic.com/engineering/writing-tools-for-agents)

### Inferences
- No free *API design* course (as distinct from MCP-building or API-testing courses) stood out as canonical in 2025–2026. For design specifically, the free canon is the style guides themselves plus Fielding.
- MCP courses created in 2025 likely predate the 2026-07-28 stateless revision, so their transport and session content may be dated.

### Gaps
- I did not verify: Google Cloud's API design guide (cloud.google.com/apis/design) as a separate resource; specific notable Udemy, Coursera or LinkedIn Learning API design courses; and whether DeepLearning.AI's "free for a limited time" still applies in Oct 2026.
