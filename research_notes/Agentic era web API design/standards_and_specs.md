# Web API Description Formats and HTTP/API Standards: State as of October 2026 (with agent relevance)

Method note: live page fetching (WebFetch, and curl to datatracker.ietf.org, rfc-editor.org, openapis.org, oauth.net and similar) was blocked in this environment. **Primary sources were read directly** for the spec texts hosted on GitHub (OAI OpenAPI/Arazzo/Overlay/Moonwalk, AsyncAPI, GraphQL, the GraphQL Federation/Composite Schemas spec, TypeSpec changelog, llms.txt, the MCP auth spec, IETF aipref and httpapi editor's copies) and json-schema.org. **IETF draft and RFC statuses dated 2025–2026** come from search-engine snapshots of datatracker pages, plus secondary press where noted. **Long-established RFC numbers and dates** (pre-2025) come from canonical RFC metadata as I know it and were not re-fetched; this is flagged where it applies. The web-search budget ran out before I could check Web Bot Auth adopters, schema.org, or a gRPC 2026 release; these are listed as gaps.

---

## 1. OpenAPI Initiative: OpenAPI 3.1.x / 3.2 / 3.3-dev, Moonwalk (4.0), Arazzo, Overlay, and OAI positioning on AI/agents

### Takeaway
OpenAPI **3.2.0 (released 2025-09-19)** is the current OAS feature release. It is fully backward-compatible with 3.1 and adds streaming (SSE/JSONL) via `itemSchema`, the `QUERY` method plus `additionalOperations`, hierarchical tags, `$self`, a `querystring` parameter location, and OAuth device flow / metadata URL. **3.3.0 is in development** (date TBD). **Moonwalk/4.0 has no date**, and the OAI says it may never ship as a 4.0; it now serves as an "ideas engine" and in H1 2026 focused on making OpenAPI "agent-ready". **Arazzo 1.1.0 (2026-05-17)** adds AsyncAPI steps and JSONPath/XPath selectors, and is the OAI's main vehicle for agent workflows, with an MCP/A2A step-type roadmap. **Overlay 1.1.0 (2026-01-14)** adds a `copy` action.

### Cited Findings
**OpenAPI Specification versions (from the spec's own revision history)**
- Revision history in the 3.2.0 spec: **3.2.0 = 2025-09-19**, **3.1.2 = 2025-09-19** (patch), **3.1.1 = 2024-10-24**, 3.1.0 = 2021-02-15, **3.0.4 = 2024-10-24**, 3.0.3 = 2020-02-20 — [OAS 3.2.0 source, Appendix A](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md); rendered at [spec.openapis.org/oas/v3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- New fields confirmed as anchors in the 3.2.0 text:
  - **Document and paths:** `$self` on the OpenAPI Object (`oas-self`); `components.mediaTypes`; Path Item `query` (the **QUERY** method) and `additionalOperations` (for methods beyond the fixed set).
  - **Tags:** `summary`, `parent` (nesting) and `kind` (classification).
  - **Streaming and sequential media:** Media Type `itemSchema`, `itemEncoding` and `prefixEncoding`, with worked text covering `text/event-stream` (SSE), `application/jsonl`, `application/json-seq` and `multipart/mixed`.
  - **Security:** OAuth Flows `deviceAuthorization` (`deviceAuthorizationUrl`); Security Scheme `oauth2MetadataUrl` and `deprecated`.
  - **Other:** Discriminator `defaultMapping`; Example `dataValue` and `serializedValue`; Response `summary`; XML `nodeType` — [OAS 3.2.0 source](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md)
- Secondary summaries agree on the headline list: tags gain `summary`/`parent`/`kind`, QUERY plus `additionalOperations`, streaming via `itemSchema`/`prefixEncoding`, `deviceAuthorization`, `oauth2MetadataUrl`, and deprecatable security schemes. Redocly calls the release "fully backward-compatible. Nothing breaks." — [Redocly blog](https://redocly.com/blog/openapi-3-2); [Nordic APIs](https://nordicapis.com/whats-new-in-openapi-specification-v3-2-0/); [OAI announcement](https://www.openapis.org/?p=4090)
- Tooling uptake: SmartBear announced Swagger support for 3.2.0 — [Swagger blog](https://swagger.io/blog/swagger-launches-support-for-openapi-3-2-0/); Speakeasy maintains an unofficial OpenAPI release-notes page — [Speakeasy](https://www.speakeasy.com/openapi/release-notes)
- **OpenAPI 3.3.0 is in development.** The `v3.3-dev` branch lists "3.3.0 | TBD". Compared with 3.2.0 it currently adds a Path Item-level `security` field and renames the "Criteria for `serializedExample`" heading to "Criteria for `serializedValue`" (fetched 2026-10-10) — [OAS v3.3-dev src/oas.md](https://github.com/OAI/OpenAPI-Specification/blob/v3.3-dev/src/oas.md)

**Moonwalk / OpenAPI 4.0**
- The OAI's post on the 3.2.0 release says the focus is now "more backwards-compatible incremental steps in the 3.x line". It calls Moonwalk an "ideas engine" that "feeds the progress on the main development line", and says "it may come to pass that there is never a v4.0 of OpenAPI". There is "no planned end date to 4.0" — [OAI blog (3.2 release post)](https://www.openapis.org/?p=4090), via search snapshot
- The SIG Moonwalk README still describes its goal as "the next major release… version 4.0". Its first principle reads: "**Semantics**: Semantics provide purpose, whether the consumer is a human or an AI". The README also says "We are not yet at the point of writing a formal specification"; decisions are recorded as ADRs — [OAI/sig-moonwalk](https://github.com/OAI/sig-moonwalk); see also the [Moonwalk 2025 update](https://www.openapis.org/blog/2025/02/05/moonwalk-2025-update)
- The OAI February 2026 newsletter says Moonwalk is treating **LLMs as a new class of API client**. Its H1 2026 focus is what extra metadata would make OpenAPI documents "agent-ready", including **capability discovery and intent signaling** — [OAI Newsletter Feb 2026](https://www.openapis.org/blog/2026/02/10/openapi-initiative-newsletter-february-2026) (via search summary)
- I found no OAI SIG named specifically for "AI" or "MCP". AI/agent work is spread across Moonwalk and Arazzo. The OAI also runs an Industry Standards SIG — [OAI Newsletter Feb 2026](https://www.openapis.org/blog/2026/02/10/openapi-initiative-newsletter-february-2026) (via search summary)

**Arazzo**
- Arazzo revision history: **1.0.0 = 2024-05-29**, **1.0.1 = 2025-01-16** (patch), **1.1.0 = 2026-05-17** (minor release). The README now says "Current Version - 1.1.0" — [Arazzo 1.1.0 source, Appendix A](https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.1.0.md); [Arazzo README](https://github.com/OAI/Arazzo-Specification); rendered at [spec.openapis.org/arazzo/v1.1.0](https://spec.openapis.org/arazzo/v1.1.0)
- What changed from 1.0.1 to 1.1.0 (comparing field anchors in the two texts):
  - **AsyncAPI support:** `sourceDescriptions[].type` may now be `openapi`, `asyncapi` or `arazzo`. New Step fields `channelPath`, `action` (`send`/`receive`) and `correlationId`. A `$message.payload` runtime expression covers receive steps.
  - **Step control:** new Step fields `dependsOn` and `timeout`.
  - **Document identity:** `$self` on the Arazzo document.
  - **Selectors:** a new **Selector Object** and **Expression Type Object** (`jsonpath`, `xpath`, with versioning), usable in outputs and parameter values.
  - **Parameters:** `successParameters` and `failureParameters`; `querystring` parameter values (aligned with OAS 3.2) — [Arazzo 1.1.0](https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.1.0.md) vs [1.0.1](https://github.com/OAI/Arazzo-Specification/blob/main/versions/1.0.1.md)
- Agent positioning in the official README: the listed use cases include "**deterministic API invocation by AI-based LLMs**". The README describes workflows that remove "guesswork for both human and machine consumers" — [Arazzo README](https://github.com/OAI/Arazzo-Specification)
- The OAI June 2026 newsletter reports that the Arazzo roadmap targets **gRPC, GraphQL, SOAP, MCP and A2A step types**. It also notes sessions led by Frank Kilcommins on how "Arazzo and MCP can extend OpenAPI into multi-step, agent-driven interactions" — [OAI Newsletter June 2026](https://www.openapis.org/blog/2026/06/09/openapi-initiative-newsletter-june-2026) (via search summary)
- The OAI highlighted Overlay and Arazzo at DeveloperWeek in February 2026 — [Zuplo, Apr 2026](https://zuplo.com/blog/openapi-arazzo-overlay-specifications-guide) (via search summary)
- Tools listed in the official README:
  - **Jentic:** Arazzo Editor, Arazzo UI, a generator that derives workflows from OpenAPI, a validator, a parser and a resolver.
  - **Others:** Specmatic, Redocly CLI, Spectral, Speakeasy OpenAPI, Itarazzo, and others.
  - **Lag:** the Jentic parser listing still says "Arazzo 1.0.0 and 1.0.1", so 1.1 tooling support is still catching up — [Arazzo README](https://github.com/OAI/Arazzo-Specification)

**Overlay**
- Overlay revision history: **1.0.0 = 2024-10-17**, **1.1.0 = 2026-01-14** — [Overlay 1.1.0 source, Appendix A](https://github.com/OAI/Overlay-Specification/blob/main/versions/1.1.0.md)
- Overlay 1.1.0 actions use an RFC 9535 JSONPath `target` with the modifiers `update`, `remove`, and **`copy`**. `copy` is new in 1.1; it is "a JSONPath expression selecting a single node to copy into the `target` nodes". Listed use cases include translation, environment config, gateway/SLA metadata and traits-like reuse — [Overlay 1.1.0](https://github.com/OAI/Overlay-Specification/blob/main/versions/1.1.0.md); [Overlay README](https://github.com/OAI/Overlay-Specification)
- Overlay tooling: the README lists Bump.sh, Speakeasy, overlays-js, overlay-jvm, apigee-go-gen, openapi-format, oas-patch, IBM oas-overlay-java, Specmatic, BinkyLabs (.NET), Legba and Zuplo — [Overlay README](https://github.com/OAI/Overlay-Specification)

### Inferences
- Overlay is the natural standards-based way to add LLM-oriented hints (for example richer `description`/`summary` text or `x-` agent metadata) to an existing OpenAPI document without forking it. I found no OAI-standardized "LLM hint" vocabulary.
- OAS 3.2's SSE/JSONL `itemSchema` support matters for agents. A streaming endpoint (for example an LLM-style token stream or event feed) can now be described precisely, so a tool generator does not have to treat it as an opaque string.
- Arazzo 1.1 adds AsyncAPI steps and the roadmap adds MCP/A2A step types. Together these make Arazzo the OAI's bid to be the cross-protocol "workflow/recipe" layer above tool protocols.
- Teams waiting for OpenAPI 4.0 should standardize on 3.1/3.2 now. The OAI itself discourages waiting.

### Gaps
- I could not open the OAI blog posts directly; claims from the Feb and Jun 2026 newsletters and the 3.2 post come from search summaries.
- There is no published target date for OAS 3.3.0, and no full list of its planned features beyond what is already on the branch.
- I found no hard adoption metrics for OAS 3.2 versus 3.1 versus 3.0 (for example share of public API descriptions).

---

## 2. Other description formats: AsyncAPI, JSON Schema, TypeSpec, Smithy, GraphQL, gRPC/ConnectRPC, Protobuf

### Takeaway
- **AsyncAPI 3.1.0** shipped 2026-01-31, a minor release whose only new content is a ROS 2 binding.
- **JSON Schema**'s current release is still **2020-12**. A new **IETF `jsonschema` WG** (active 2026-04-30) is aiming for a Proposed Standard RFC, with a milestone of 2027-05.
- **TypeSpec** has been 1.x GA since 2025 (compiler now at 1.17.0); its MCP emitters are still preview.
- **Smithy IDL 2.0** (GA 2022) is still current.
- **GraphQL September 2025** is the first spec edition since Oct 2021. It adds OneOf inputs, schema coordinates, and descriptions on documents "in motivation for AI-consumers". `@defer`/`@stream` are still not in the spec, and the Federation (Composite Schemas) spec is only "Stage 0".
- **ConnectRPC** remains CNCF Sandbox.
- **Protobuf Edition 2026** is in the v36 release-candidate line (2026 Q3 target).

### Cited Findings
**AsyncAPI**
- AsyncAPI Spec **3.1.0** release notes are dated **2026-01-31**: "a minor release, and it doesn't bring any breaking changes". The new content is a **ROS 2** protocol binding. Tooling updated: @asyncapi/specs 6.11.1, parser-js 3.6.0, converter-js 1.7.0, Studio — [AsyncAPI 3.1.0 release notes (source)](https://github.com/asyncapi/website/blob/master/markdown/blog/release-notes-3.1.0.md)
- 3.0.0 dates to December 2023, so 3.1 was the first spec update in about two years — [youngju.dev deep-dive](https://www.youngju.dev/blog/culture/2026-05-14-api-schema-2026-json-schema-openapi-3-1-asyncapi-graphql-grpc-deep-dive) (secondary)
- Topics on the agenda after 3.1: documenting late or out-of-sequence events (latency expectations), AND-logic for multiple security schemes, and aligning `discriminator` with the OAS Discriminator Object — [AsyncAPI 3.1.0 release notes](https://github.com/asyncapi/website/blob/master/markdown/blog/release-notes-3.1.0.md); [AsyncAPI Feb 2026 summary](https://www.asyncapi.com/blog/2026-february-summary)
- The master-branch spec text reads "Version 3.1.0" and lists ROS 2 among protocols — [asyncapi/spec](https://github.com/asyncapi/spec/blob/master/spec/asyncapi.md)

**JSON Schema**
- As of 2026-10-10 json-schema.org says: "**The current version is 2020-12!** The previous version was 2019-09" — [json-schema.org/specification](https://json-schema.org/specification)
- Blog post "JSON Schema and IETF" (Greg Dennis, **2026-07-06**):
  - **History:** all published JSON Schema versions were IETF Internet-Drafts that never became RFCs.
  - **New IETF effort:** Lisa Dusseault started an IETF effort; a WG charter exists, and the initial draft "is little more than an edit of 2020-12", recombining Core, Validation and Hyper-Schema into one document.
  - **Plan:** the TSC will propose post-2020-12 changes on the IETF list and "proceed with our plans to publish what we have" — [JSON Schema blog](https://json-schema.org/blog/posts/ietf-cooperation)
- IETF **jsonschema WG**:
  - **Timeline:** created as Proposed 2026-04-06, charter approved and group active **2026-04-30**.
  - **Leadership:** chair Paul Hoffman, AD Andy Newton.
  - **Milestone:** request publication as a Proposed Standard by **2027-05-31**.
  - **WG draft:** `draft-ietf-jsonschema-json-schema-01` (Dusseault, Wright, Andrews) — [datatracker jsonschema history](https://datatracker.ietf.org/group/jsonschema/history/); [charter](https://datatracker.ietf.org/doc/charter-ietf-jsonschema/) (via search snapshot)
- The community's own "stable" next spec is still a work in progress in the repo: the README describes "the **work in progress** of the next set of JSON Schema IETF Internet Draft documents" — [json-schema-org/json-schema-spec](https://github.com/json-schema-org/json-schema-spec)
- Agent relevance: a JSON Schema case study, "How JSON Schema makes LLM output reliable" (dottxt, 2025-12-16), describes JSON Schema as the contract for structured LLM output — [JSON Schema blog index](https://json-schema.org/blog)

**TypeSpec (Microsoft)**
- The compiler changelog's latest entry is **1.17.0**. The series runs 1.7.x → 1.17.0, so minor releases are roughly monthly — [TypeSpec compiler CHANGELOG](https://github.com/microsoft/typespec/blob/main/packages/compiler/CHANGELOG.md)
- The **1.0 GA** post lists the production-ready set: the compiler, the HTTP and OpenAPI libraries, the VS Code extension, and the OpenAPI 3.0 and JSON Schema emitters. Protocol emitters remain preview — [TypeSpec 1.0 GA](https://typespec.io/blog/typespec-1-0-GA-release/)
- **MCP:** a 2025-05-30 post, "API-first MCP servers with TypeSpec", introduced MCP server emitters. The MCP work is "in Public Preview and implementation may significantly change" — [TypeSpec MCP blog](https://typespec.io/blog/2025-05-30-typespec-mcp/)
- Adoption: Microsoft describes TypeSpec as used "to deliver APIs at a massive scale" (Azure). I found no hard external adoption metrics — [Nordic APIs session](https://nordicapis.com/sessions/apis-at-scale-with-typespec/)

**Smithy (AWS)**
- Smithy IDL **2.0** went GA on **2022-08-19** and remains the current IDL version — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2022/08/smithy-interface-definition-language-idl-2-0-generally-available/)
- **Smithy-Java** client framework reached GA (article dated 2026-04-13) — [Classmethod](https://dev.classmethod.jp/articles/smithy-java-client-framework/)
- InfoQ (Japan) reported in Sept 2025 on AWS open-sourcing its Smithy API models (inferred from the article title/URL; content not read) — [InfoQ JP](https://www.infoq.com/jp/news/2025/09/aws-smithy-api-models-opensource)
- I found no Smithy-specific MCP release — [apis.io Smithy listing](https://apis.io/providers/smithy/) (via search summary)

**GraphQL**
- The **September 2025 Edition** is tagged in the spec repo (heading "_September 2025 Edition_"). Its changelog calls it the first edition since **October2021** and lists these notable changes:
  - **OneOf input objects** ("input unions").
  - **Schema coordinates**.
  - "**Descriptions on documents, in motivation for AI-consumers**" (#1170).
  - Broader deprecation support.
  - Full Unicode support — [GraphQL Sept 2025 changelog](https://github.com/graphql/graphql-spec/blob/main/changelogs/September2025.md); [spec.graphql.org/September2025](https://spec.graphql.org/September2025/)
- **Incremental delivery (`@defer`/`@stream`) is not in the Sept 2025 edition** (zero occurrences of "defer" or "stream" in the edition's top-level file, and per secondary analysis none in the spec text). The Incremental Delivery RFC is still at RFC 2 (Draft), with spec-draft commits as of 2026-07-15. **GraphQL.js v17 went GA 2026-06-15**; its stable `execute()` rejects schemas with `@defer`/`@stream`, and incremental delivery needs a separately named experimental function — [youngju.dev analysis, 2026-07-17](https://www.youngju.dev/blog/2026-07-17-graphql-spec-september-2025-graphql-js-17.en) (secondary; GraphQL.js GA date not verified at source)
- **Federation:** the Composite Schemas WG (announced 2024-05-16) includes Apollo, ChilliCream, Graphile, Hasura, Netflix, The Guild and WunderGraph, and was meeting biweekly through Dec 2026. Its spec repo is now titled "**GraphQL Federation**" and marked "**Stage 0: Preliminary**". The spec was originally created by ChilliCream and covers composition plus query-plan execution — [composite-schemas-spec README/spec](https://github.com/graphql/composite-schemas-spec); [graphql.org federation resources](https://graphql.org/resources/federation/)
- **GraphQL-over-HTTP** spec is at "**Stage 2: Draft**" — [graphql/graphql-over-http](https://github.com/graphql/graphql-over-http)

**gRPC / ConnectRPC / Protobuf**
- **Connect RPC** was accepted into the CNCF at **Sandbox** level on **2024-04-13**. I found no evidence of promotion to Incubating — [CNCF project page](https://www.cncf.io/projects/connect-rpc/); [Buf blog](https://buf.build/blog/connect-rpc-joins-cncf)
- **Protobuf Editions:**
  - **Edition 2024** was announced 2025-06-27.
  - **Edition 2026** was announced **2026-07-13**, with plans to ship in the **36.x** line during **Q3 2026**. Announced changes include tightened defaults (for example `enforce_naming_style` = `STYLE2026`) and enforced schema-size limits (`enforce_proto_limits`) — [protobuf.dev news 2026-07-13](https://protobuf.dev/news/2026-07-13); [protobuf.dev news index](https://protobuf.dev/news/)
  - **v36.0-rc1** is the first protoc accepting Edition 2026. As of 2026-07-16 stable was v35.1; Edition 2026 "adds no new syntax" — [youngju.dev](https://www.youngju.dev/blog/2026-07-16-protobuf-edition-2026-tightening-defaults.en) (secondary); [v36.0-rc1 notes](https://newreleases.io/project/github/protocolbuffers/protobuf/release/v36.0-rc1)

### Inferences
- GraphQL is the only major API spec that explicitly cites AI consumers as motivation for a normative change (document descriptions). OpenAPI's equivalent work (Moonwalk "semantics", "intent signaling") has not yet reached a spec.
- JSON Schema matters more than ever as the lingua franca of LLM tool and function schemas, since MCP, OpenAI and Anthropic tool schemas are JSON Schema subsets. Yet the spec has been frozen at 2020-12 for six years, and the RFC is at least mid-2027 away. Expect continued dialect fragmentation (for example the 3.1/3.2 OAS dialect versus LLM-provider "strict mode" subsets).
- TypeSpec's MCP emitter puts it in the "write once, emit OpenAPI + MCP" camp. Its stability guarantees cover only the OpenAPI and JSON Schema emitters.

### Gaps
- I did not find the exact TypeSpec 1.0 GA date in fetched content (believed to be around May 2025; not verified) or the release date of 1.17.0.
- No gRPC core release or 2026 gRPC spec change was researched (search budget exhausted). gRPC's own CNCF status (Incubating) was not re-verified.
- I could not confirm the Protobuf Edition 2026 GA (v36.0 final) date as of Oct 2026.
- There is no Smithy roadmap or AI-specific Smithy work beyond the above.

---

## 3. IETF HTTP APIs (httpapi) and HTTP WG (httpbis) outputs

### Takeaway
Several API building blocks are now published RFCs: Problem Details (RFC 9457), Structured Fields (RFC 9651), Link-Template (RFC 9652), Deprecation (RFC 9745, Mar 2025), api-catalog (RFC 9727, Jun 2025), and the **QUERY method (RFC 10008, June 2026)**. The two headers most often requested for agent-friendly APIs are **still drafts as of Oct 2026**: **RateLimit** (-11, May 2026, no IESG approval confirmed) and **Idempotency-Key** (-07 Oct 2025; a newer editor's copy is suggested). Resumable Uploads is also still a draft.

### Cited Findings
**Published RFCs (API-relevant)**
- **RFC 10008 — The HTTP QUERY Method** (formerly `draft-ietf-httpbis-safe-method-w-body`): published **June 2026** as Proposed Standard. Authors are Julian Reschke, James M. Snell and Mike Bishop. QUERY carries a body like POST but is **safe, idempotent and cacheable** — [InfoQ, Sep 2026](https://www.infoq.com/news/2026/09/http-query-method/); [vensas.de](https://vensas.de/en/blog/http-query-method-dotnet-10); [datatracker draft page noting RFC 10008](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/); canonical [RFC 10008](https://www.rfc-editor.org/rfc/rfc10008.html). The exact day is unconfirmed (secondary sources only). OAS 3.2 already models QUERY (Path Item `query`) — [OAS 3.2.0](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md)
- **RFC 9745 — The Deprecation HTTP Response Header Field:** **2025-03**, Proposed Standard (httpapi WG). It signals that a resource is or will be deprecated, plus a `deprecation` link relation — [httpapi WG page](https://datatracker.ietf.org/wg/httpapi/); [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html)
- **RFC 9727 — api-catalog: A Well-Known URI and Link Relation to Help Discovery of APIs:** **2025-06**, Proposed Standard (errata exist). It defines `/.well-known/api-catalog` and the `api-catalog` link relation. The catalog format uses the Linkset format (RFC 9264) — [httpapi WG page](https://datatracker.ietf.org/wg/httpapi/); [RFC 9727](https://www.rfc-editor.org/rfc/rfc9727.html) (format details from RFC text as I know it; not re-fetched)
- **RFC 9652 — The Link-Template HTTP Header Field:** **2024-09**, Proposed Standard — [httpapi WG page](https://datatracker.ietf.org/wg/httpapi/)
- Established RFCs, not re-fetched (canonical metadata):
  - **RFC 9457** Problem Details for HTTP APIs (July 2023; obsoletes RFC 7807) — [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)
  - **RFC 9651** Structured Field Values for HTTP (Sept 2024; obsoletes RFC 8941; adds Date and Display String types) — [RFC 9651](https://www.rfc-editor.org/rfc/rfc9651.html)
  - **RFC 8594** Sunset HTTP header (May 2019, Informational) — [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html)
  - **RFC 9264** Linkset (July 2022) — [RFC 9264](https://www.rfc-editor.org/rfc/rfc9264.html)
  - **RFC 9535** JSONPath (Feb 2024; used by Overlay and Arazzo) — [RFC 9535](https://www.rfc-editor.org/rfc/rfc9535.html)

**Drafts (not RFCs) as of Oct 2026**
- **RateLimit header fields** (`draft-ietf-httpapi-ratelimit-headers`):
  - **Version:** latest **-11**, published **2026-05-23**, expires 2026-11-24; intended Standards Track.
  - **Design:** two fields, `RateLimit` and `RateLimit-Policy`, replacing the three `RateLimit-Limit/-Remaining/-Reset` fields of earlier drafts.
  - **Approval status is disputed:** one blog says it has IESG approval pending publication, while another says the IESG has not scheduled it and an early directorate review found it "not ready". The datatracker snapshot showed no IESG approval.
  - Some vendors (reportedly Cloudflare) already emit the draft format — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/); [flowverify blog](https://www.flowverify.co/blog/ietf-ratelimit-header-still-a-draft-2026); editor's copy [ietf-wg-httpapi/ratelimit-headers](https://github.com/ietf-wg-httpapi/ratelimit-headers)
- **Idempotency-Key header** (`draft-ietf-httpapi-idempotency-key-header`):
  - **Version:** last numbered revision found is **-07 (October 2025)**, expiring 2026-04-18. A "latest" editor's copy lists expiry 2026-12-08, which suggests a newer revision exists; this is unconfirmed.
  - **Content:** the value is a Structured Fields String; UUIDs are recommended; keys must not be reused with a different payload. Per secondary guides it maps errors to 400 (missing key), 422 (key reused with a different payload) and 409 (concurrent retry).
  - Widely implemented by payment and API platforms despite having no RFC — [datatracker](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header); [-07](https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html); [greenbytes latest](https://greenbytes.de/tech/specs/draft-ietf-httpapi-idempotency-key-header-latest.html); [editor's copy](https://github.com/ietf-wg-httpapi/idempotency/blob/main/draft-ietf-httpapi-idempotency-key-header.md)
- **Deprecation manifest** (`draft-rmili-httpapi-deprecation-manifest-00`, 2026-06-26): an individual draft (not WG-adopted) for field-level lifecycle signalling — [httpapi WG page](https://datatracker.ietf.org/wg/httpapi/)
- **Resumable Uploads for HTTP** (`draft-ietf-httpbis-resumable-upload`): the editor's copy is dated **2026-08-23**; datatracker shows -12, IESG state "I-D Exists", intended Proposed Standard. It evolved from the tus protocol — [httpwg.org](https://httpwg.org/http-extensions/draft-ietf-httpbis-resumable-upload.html); [datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpbis-resumable-upload/)

### Inferences
- The "agent-readiness" HTTP toolkit can now rely on standards for:
  - error semantics (9457)
  - lifecycle signals (9745 Deprecation + 8594 Sunset)
  - machine discovery of APIs (9727 api-catalog → linkset → OpenAPI/Arazzo docs)
  - complex read-only queries (10008 QUERY)
- Retry-safety (Idempotency-Key) and quota awareness (RateLimit), the two things autonomous agents most need for safe retries and back-off, remain de facto conventions without RFC status. Designers should implement them per the latest drafts and expect minor syntax churn.
- QUERY now has both an RFC and an OAS 3.2 description. Support in frameworks, proxies and CDNs will lag; .NET 10 support is reported by vensas.de.

### Gaps
- I could not verify on datatracker the precise IESG state of the RateLimit draft (approved vs not) or whether a -08 of Idempotency-Key exists.
- I could not confirm the exact publication day of RFC 10008.
- I found no evidence of a Link-Template follow-on or new httpapi RFCs published in late 2025–2026 beyond those listed. The httpapi WG's complete current document list was not retrievable.

---

## 4. Auth standards: OAuth 2.1, BCPs, metadata, DPoP/RAR/Token Exchange, CIMD, Transaction Tokens, GNAP, and agent-specific identity work

### Takeaway
- **OAuth 2.1 is still an Internet-Draft** (-16, 2026-09-02); the WG milestone to send it to the IESG is Dec 2026.
- The building blocks agents actually use are RFCs: RFC 9700 Security BCP, RFC 9728 Protected Resource Metadata, RFC 9449 DPoP, RFC 9396 RAR, RFC 8693 Token Exchange, and the new **RFC 10017** (Browser-Based Apps BCP, Aug 2026).
- **Client ID Metadata Documents** (WG draft, revised Aug 2026) and **Transaction Tokens** (WG draft, revised Aug 2026) are in progress.
- Agent-specific authorization work is a **crowd of individual drafts with no WG adoption**. The IETF held an **agentproto** WG-forming BoF at IETF 126 (2026-07-23).
- The OpenID Foundation's **AIIM Community Group** has published a whitepaper (Oct 2025), a NIST response (Mar 2026), and is running an MCP security interop (Gartner IAM Summit 2026).

### Cited Findings
**OAuth core and BCPs**
- **OAuth 2.1** (`draft-ietf-oauth-v2-1`): the latest is **-16, updated 2026-09-02**; -15 was 2026-03-02. IESG state "I-D Exists"; WG milestone "**Dec 2026** Submit OAuth 2.1 to IESG" — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/); [oauth.net specs](https://oauth.net/specs/) (via search snapshots)
- **RFC 10017 — OAuth 2.0 for Browser-Based Applications** (BCP 212): published **2026-08-24** — [RFC 10017](https://datatracker.ietf.org/doc/html/rfc10017)
- **RFC 10027 — Cross-Device Flows security** is listed on oauth.net as a recent RFC; I found no date — [oauth.net specs](https://oauth.net/specs/)
- oauth.net (snapshot about mid-2026) lists four WG drafts **in the RFC Editor queue**: JWT BCP update (`rfc8725bis`), **Identity Chaining**, **Token Status List**, and `rfc7523bis` (JWT client auth/assertion grants). Queue entry dates run Apr–Aug 2026 — [oauth.net specs](https://oauth.net/specs/); [rfc7523bis](https://datatracker.ietf.org/doc/draft-ietf-oauth-rfc7523bis/)
- An update to the Security BCP is in progress (`draft-ietf-oauth-security-topics-update`) — [datatracker](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-update-01)
- Established RFCs, not re-fetched (canonical metadata):
  - **RFC 9700** Best Current Practice for OAuth 2.0 Security (Jan 2025, BCP 240) — [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
  - **RFC 9728** OAuth 2.0 Protected Resource Metadata (Apr 2025) — [RFC 9728](https://www.rfc-editor.org/rfc/rfc9728.html)
  - **RFC 9449** DPoP (Sept 2023) — [RFC 9449](https://www.rfc-editor.org/rfc/rfc9449.html)
  - **RFC 9396** Rich Authorization Requests (May 2023) — [RFC 9396](https://www.rfc-editor.org/rfc/rfc9396.html)
  - **RFC 8693** Token Exchange (Jan 2020) — [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693.html)
  - **RFC 7591** Dynamic Client Registration (July 2015) — [RFC 7591](https://www.rfc-editor.org/rfc/rfc7591.html)
  - **RFC 8707** Resource Indicators (Feb 2020) — [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html)
  - **RFC 9635** GNAP core (Oct 2024; a separate protocol from OAuth with little mainstream uptake) — [RFC 9635](https://www.rfc-editor.org/rfc/rfc9635.html)

**Client ID Metadata Documents (CIMD)**
- `draft-ietf-oauth-client-id-metadata-document` (Aaron Parecki, Emelia Smith; Standards Track):
  - **Revisions:** -01 (2026-03-02), -02 (2026-07-06), and an editor's copy dated **2026-08-10**.
  - **Mechanism:** the `client_id` is an HTTPS URL that resolves to a JSON client metadata document, and the AS must check that the document's `client_id` exactly matches the URL.
  - **-02 additions:** URL rules (a path is required, query strings discouraged) — [datatracker -02](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-02); [drafts.oauth.net](https://drafts.oauth.net/draft-ietf-oauth-client-id-metadata-document/draft-ietf-oauth-client-id-metadata-document.html)

**Transaction Tokens**
- `draft-ietf-oauth-transaction-tokens`: -11 (2026-07-30), latest editor's copy 2026-08-12. Standards Track; **not an RFC**, with no IESG/RFC Editor status on oauth.net — [datatracker -11](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-transaction-tokens-11); [drafts.oauth.net](https://drafts.oauth.net/oauth-transaction-tokens/draft-ietf-oauth-transaction-tokens.html)
- Individual follow-on: "**Transaction Tokens For Agents**" (`draft-araut-oauth-transaction-tokens-for-agents-02`) — [datatracker](https://datatracker.ietf.org/doc/draft-araut-oauth-transaction-tokens-for-agents/)

**Agent-specific IETF work (all individual drafts unless noted)**
- Examples:
  - `draft-oauth-ai-agents-on-behalf-of-user-02` — [link](https://datatracker.ietf.org/doc/html/draft-oauth-ai-agents-on-behalf-of-user-02)
  - Agent Authorization Profile (AAP) `draft-aap-oauth-profile-00` (Feb 2026) — [link](https://datatracker.ietf.org/doc/html/draft-aap-oauth-profile-00)
  - Attenuating agent tokens `draft-niyikiza-oauth-attenuating-agent-tokens-00` (Mar 2026; tool-level and argument-level constraints) — [link](https://datatracker.ietf.org/doc/html/draft-niyikiza-oauth-attenuating-agent-tokens-00)
  - `draft-mishra-oauth-agent-grants-01` (DAAP) — [link](https://datatracker.ietf.org/doc/html/draft-mishra-oauth-agent-grants-01)
  - `draft-embesozzi-oauth-agent-native-authorization-00` (extends First-Party Apps; FiPA itself is "Waiting for Write-Up") — [link](https://datatracker.ietf.org/doc/html/draft-embesozzi-oauth-agent-native-authorization-00)
  - `draft-song-oauth-ai-agent-authorization-00` — [link](https://www.ietf.org/archive/id/draft-song-oauth-ai-agent-authorization-00.html)
- One analysis characterizes the field as "seven competing proposals, no adopted working group" — [Forkast](https://forkast.news/the-ietf-published-a-draft-for-agent-identity-the-market-already-shipped/) (secondary)
- **AIMS / `draft-klrc-aiagent-auth-03`** (AI Agent Authentication and Authorization, July 2026) was presented at a **WIMSE** (Workload Identity in Multi-System Environments) interim. It is an individual draft — [WIMSE interim 2026-01 agenda](https://datatracker.ietf.org/doc/agenda-interim-2026-wimse-01-wimse-01/) (via search summary)
- **agentproto** (Agent Communication Protocols):
  - **BoF:** WG-forming BoF at **IETF 126 Vienna, 2026-07-23**; chairs Leslie Daigle and Orie Steele, AD Charles Eckel (ART).
  - **Charter:** listed in "External Review"; it would define "protocol building blocks for enabling interoperability for AI Agent applications".
  - **Outcome:** chartering not confirmed in the sources found.
  - **DAWN:** the companion discovery BoF was reportedly **not** chartered — [agentproto about](https://datatracker.ietf.org/wg/agentproto/about/); [minutes](https://datatracker.ietf.org/doc/minutes-126-agentproto-202607230700/); [Forkast on DAWN](https://forkast.news/ietf-defers-dawn-charter-despite-12-drafts-and-broad-industry-support/)

**OpenID Foundation and W3C**
- The OIDF **Artificial Intelligence Identity Management (AIIM) Community Group** is a community group that does **not produce specifications**; it identifies gaps and use cases — [OIDF AIIM CG](https://openid.net/cg/artificial-intelligence-identity-management-community-group/)
  - Whitepaper "**Identity Management for Agentic AI**" (Oct 2025) — [PDF](https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf); [arXiv 2510.25819](https://arxiv.org/pdf/2510.25819); [announcement](https://openid.net/new-whitepaper-tackles-ai-agent-identity-challenges/)
  - **NIST response (Mar 2026)** on AI agent security: the most urgent risks are "failures of trust" — [OIDF](https://openid.net/oidf-responds-to-nist-on-ai-agent-security/)
  - **Interop event:** MCP clients, gateways and servers securing agent flows with open identity standards, at Gartner IAM Summit 2026. Participants commit by 2026-08-10 and must show a successful test by 2026-10-16 — [OIDF CFP](https://openid.net/call-for-participation-demonstrate-mcp-based-ai-agent-security-with-open-identity-standards-2/)
- **W3C "Agent Identity Registry Protocol" Community Group** call for participation (2026-04-24) — [W3C](https://www.w3.org/community/agent-identity/2026/04/24/call-for-participation-in-agent-identity-registry-protocol-community-group/)

### Inferences
- In practice, "OAuth 2.1" for agents means OAuth 2.0 plus RFC 9700. The OAuth 2.1 label is used normatively by MCP even though it is not an RFC.
- The agent-relevant stack is RFC 9728 (resource → AS discovery) + RFC 8414 + CIMD (registration without DCR) + RFC 8707 (audience binding) + optionally DPoP. RAR, Token Exchange and Transaction Tokens handle fine-grained and delegated scopes.
- Standardization of "agent on behalf of user" delegation semantics is at least 2027+, since nothing is WG-adopted yet. API providers should build on Token Exchange (`act` claim), RAR and short-lived tokens rather than any agent-specific draft.

### Gaps
- I could not confirm whether agentproto was chartered after IETF 126, or the live IESG state of OAuth 2.1 -16.
- I found no publication date for RFC 10027 and no RFC numbers for the queued Identity Chaining / Token Status List drafts.
- GNAP follow-on RFCs (for example resource-server connections) were not verified.

---

## 5. Web discovery and AI-crawler-adjacent standards: llms.txt, IETF aipref, robots.txt, Web Bot Auth / RFC 9421, schema.org

### Takeaway
- **llms.txt** is an informal proposal (Jeremy Howard). It was **revised to "v2" in Aug 2026**, adding link-relation discovery and path-scoped files.
- Adoption is around 10% of domains, concentrated in developer documentation. Independent crawl studies show general AI crawlers rarely fetch it, and Google says it doesn't use it.
- **IETF aipref** vocabulary is at **-08 (2026-09-13)**, still without consensus; it missed its Aug 2026 IESG milestone. The attach draft defines a `Content-Usage` header and a robots.txt directive.
- **webbotauth** adopted **`draft-ietf-webbotauth-httpsig-protocol-00` on 2026-09-01**, based on RFC 9421 HTTP Message Signatures. There is no RFC yet.

### Cited Findings
**llms.txt**
- Proposal "The /llms.txt file, **v2**", by Jeremy Howard: originally **2024-09-03**, date-modified **2026-08-10**.
  - **Adoption claims:** "thousands of sites publish an llms.txt file"; documentation platforms (Mintlify) generate them; **Chrome Lighthouse audits for one** as part of "agentic browsing" checks; OpenAI, Anthropic and Gemini publish llms.txt files for their developer docs.
  - **Placement:** the file may sit at the site root **or at any path**, covering pages under that path — [llms-txt index.qmd](https://github.com/AnswerDotAI/llms-txt/blob/main/nbs/index.qmd); [llmstxt.org](https://llmstxt.org/)
- v2 changes (August 2026):
  - **Discovery via standard link relations:** `rel="alternate" type="text/markdown"` points to a page's markdown version, and `rel="describedby"` points to the covering llms.txt, as HTML `<link>` or an HTTP `Link:` header.
  - **Markdown URLs:** both `page.html.md` and `page.md` are allowed.
  - **Scoping:** the most specific path-scoped file applies.
  - **Removed:** `llms_txt2ctx` context-expansion tooling and the mechanical meaning of the `Optional` section.
  - **Consumption model:** agents "view or search the llms.txt… then follow the relevant links" — [llms-txt changes.qmd](https://github.com/AnswerDotAI/llms-txt/blob/main/nbs/changes.qmd)
- Adoption and criticism (secondary, mostly SEO/GEO vendors):
  - **Adoption:** SE Ranking reports **10.13%** adoption across about 300k domains (May 2026); about **8.7%** of the top 1,000 sites (June 2026).
  - **Crawler requests:** Ahrefs reportedly found **97%** of llms.txt files got **zero requests** (137,210 domains, May 2026). Limy.ai counted 408 llms.txt requests in more than 500M bot events.
  - **AI citations:** no significant correlation with AI citations.
  - **Google:** Gary Illyes said in July 2025 that Google does not support it.
  - **Where it is used:** coding agents are the consumer that demonstrably reads these files — [byfaro.ai](https://byfaro.ai/blog/ai-crawlers-ignore-llmstxt-97-of-the-time-so-stop-making-one); [limy.ai](https://limy.ai/blog/llms-txt-in-2026-the-full-guide); [geoly.ai](https://www.geoly.ai/blog/does-llms-txt-work); [1clickreport](https://www.1clickreport.com/blog/llms-txt-evidence-2026). Figures are second-hand; the underlying Ahrefs and SE Ranking studies were not read.

**IETF AI Preferences (aipref) WG**
- `draft-ietf-aipref-vocab` "A Vocabulary For Expressing AI Usage Preferences":
  - **Version:** **-08, 2026-09-13**, expires 2027-03-18, Standards Track.
  - **Consensus:** the draft states that "presence or absence of any particular text does not indicate consensus".
  - **Milestone:** sending to IESG by **Aug 2026** has been missed.
  - **Categories** (editor's copy): **AI Training (`train-ai`)**, **AI Use**, **Search**, plus vocabulary extensions and an exemplary serialization — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/); [WG about](https://datatracker.ietf.org/wg/aipref/about/); [editor's copy](https://github.com/ietf-wg-aipref/drafts/blob/main/draft-ietf-aipref-vocab.md)
- Interims: April 2026 removed "large" from the training-model definition and dropped high-level AI/ML definitions. At June 2026 several issues were still unconverged, and the training and search definitions were "consensus-seeking" — [minutes interim-2026-aipref-01](https://datatracker.ietf.org/doc/minutes-interim-2026-aipref-01-202604141315/); [June 2026 minutes](https://ietfminutes.org/minutes/2026-06-17/aipref.html)
- `draft-ietf-aipref-attach` defines a **`Content-Usage` HTTP header field** (example `Content-Usage: train-ai=n`) and a **Content-Usage directive in robots.txt** (RFC 9309). One third-party tracker said it had lapsed (expired) as of July 2026 — [editor's copy](https://ietf-wg-aipref.github.io/drafts/draft-ietf-aipref-attach.html); [Barkhausen notes on aipref, Content-Usage, RSL](https://www.barkhausen.ai/notes/ai-usage-preference-standards/)
- Related individual draft: `draft-zehta-aipref-exclusions-01` (Informational) — [IETF archive](https://www.ietf.org/archive/id/draft-zehta-aipref-exclusions-01.html)
- Baseline: **RFC 9309** Robots Exclusion Protocol (Sept 2022; canonical metadata, not re-fetched) — [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)

**Web Bot Auth (webbotauth WG) and HTTP Message Signatures**
- **`draft-ietf-webbotauth-httpsig-protocol-00`** "HTTP Message Signatures for automated traffic" (Thibault Meunier, Sandor Major): **adopted as a WG draft 2026-09-01**, replacing the individual draft. It is not an RFC — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/); [nerdleveltech](https://nerdleveltech.com/web-bot-auth-ietf-standard-agent-verification) (secondary)
- Related drafts: architecture `draft-meunier-web-bot-auth-architecture-05` (Informational) and registry / "Signature Agent card" `draft-meunier-webbotauth-registry-01` — [architecture](https://datatracker.ietf.org/doc/html/draft-meunier-web-bot-auth-architecture); [registry](https://datatracker.ietf.org/doc/html/draft-meunier-webbotauth-registry-01)
- The underlying signature standard is **RFC 9421 HTTP Message Signatures** (Feb 2024; canonical metadata, not re-fetched) — [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421.html)

### Inferences
- llms.txt v2 now points at **standard link relations (`describedby`, `alternate`)**. This brings it closer to the IETF-style discovery world (RFC 9727 api-catalog also uses linksets and link relations). An agent-ready site could chain `/.well-known/api-catalog` → OpenAPI/Arazzo, plus `llms.txt` → markdown docs.
- llms.txt is useful for coding agents and doc consumption, not for search visibility. Its value for API providers is in developer documentation.
- AI usage preferences (aipref) and bot authentication (webbotauth) are both stuck at the draft or early-WG stage. Providers wanting verifiable agent identity today must use RFC 9421 signatures per the WG draft and vendor directories, and accept churn.

### Gaps
- Search budget ran out before checking:
  - which vendors (Cloudflare, OpenAI, Visa, Akamai and so on) ship Web Bot Auth or `Signature-Agent` in production;
  - Really Simple Licensing (RSL) and Cloudflare Content Signals status;
  - **schema.org** releases or agent-relevant vocabulary (not researched at all).
- I could not verify the original Ahrefs and SE Ranking llms.txt studies or the Chrome Lighthouse llms.txt audit page beyond the llms.txt v2 document's own citation.

---

## 6. Explicit bridges between API specs and agents (Arazzo for agents, OpenAPI→MCP, x- extensions, MCP's use of IETF auth RFCs)

### Takeaway
The bridges are mostly **tooling conventions, not standards**:
- Many OpenAPI→MCP and Arazzo→MCP generators exist, with incompatible `x-mcp` extensions.
- The OAI's formal answers are Arazzo, with an MCP/A2A step-type roadmap, and Moonwalk's "agent-ready" metadata exploration.
- The clearest standards-level bridge is MCP's authorization spec. It makes **RFC 9728, RFC 8707, OAuth 2.1 and CIMD** load-bearing for every agent-facing HTTP API.

### Cited Findings
- The MCP authorization spec (2025-11-25 revision):
  - **Resource metadata:** MCP servers must expose **RFC 9728 Protected Resource Metadata**, with discovery via `WWW-Authenticate` `resource_metadata` or well-known URIs.
  - **Audience binding:** clients use **RFC 8707** resource indicators.
  - **Registration:** "Authorization servers and MCP clients **SHOULD** support OAuth **Client ID Metadata Documents**", while Dynamic Client Registration (RFC 7591) moved to MAY.
  - It is framed on **OAuth 2.1** — [MCP spec 2025-11-25 authorization (source)](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx); [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization); [Keycloak MCP guide](https://www.keycloak.org/securing-apps/mcp-authz-server)
  - Secondary sources mention a **2026-07-28** MCP revision adding RFC 9207 issuer validation (unverified) — [Keycloak nightly](https://www.keycloak.org/nightly/securing-apps/mcp-authz-server)
- **Arazzo→MCP tools:**
  - **HAPI MCP** exposes each Arazzo `workflowId` as one MCP tool — [mcp-com-ai/hapimcp](https://github.com/mcp-com-ai/hapimcp)
  - **WSO2 arazzo-mcp-generator** generates a Python MCP server (fastmcp + arazzo-runner) — [wso2/arazzo-mcp-generator](https://github.com/wso2/arazzo-mcp-generator/releases)
  - **OrcA** is a VS Code extension that turns OpenAPI/Arazzo into MCP — [VS Marketplace](https://marketplace.visualstudio.com/items?itemName=la-rebelion-labs.orca-mcp)
  - **Jentic** offers Arazzo generator and runner tooling — [Arazzo README](https://github.com/OAI/Arazzo-Specification)
- **OpenAPI→MCP converters** include agentfront `mcp-from-openapi` (with `fromArazzo()` and an `x-mcp` extension family), `openapi-mcp-generator` (where `x-mcp` is an include/exclude flag at root, path and operation level), FastMCP `from_openapi`, Stainless, Speakeasy, AWS AgentCore Gateway, and the LangChain OpenAPI toolkit — [agentfront](https://github.com/agentfront/mcp-from-openapi); [openapi-mcp-generator](https://github.com/harsha-iiiv/openapi-mcp-generator); [Cadenya overview](https://cadenya.com/other-content/openapi-specs-as-agent-tools-and-mcp)
- `x-mcp` naming collision: Redocly's experimental `introspect-mcp` command records an MCP server's capabilities as an `x-mcp` extension *inside* an OpenAPI description. That is a different semantics from the converter flags — [apis.io, 2026-09-25](https://apis.io/2026/09/25/redocly-documents-mcp-servers-in-openapi-and-its-own-agent-door-is-undocumented/)
- TypeSpec offers MCP server emitters (preview) — [TypeSpec MCP blog](https://typespec.io/blog/2025-05-30-typespec-mcp/)
- GraphQL Sept 2025 added descriptions on executable documents "in motivation for AI-consumers" — [GraphQL changelog](https://github.com/graphql/graphql-spec/blob/main/changelogs/September2025.md)
- MCP is governed through the **Agentic AI Foundation** under the Linux Foundation, separate from the OAI — [WorkOS](https://workos.com/blog/everything-your-team-needs-to-know-about-mcp-in-2026) (secondary)

### Inferences
- There is no standard `x-` vocabulary for LLM hints; each converter defines its own (`x-mcp`, `x-speakeasy-*` and others). An OAI-level standard is plausible via Moonwalk's "intent signaling" work or an Overlay-based convention, but none exists as of Oct 2026.
- Arazzo's "workflow = one tool" pattern (HAPI, WSO2) is emerging as the answer to the "too many fine-grained tools" problem when OpenAPI operations are mapped 1:1 to MCP tools.
- Because MCP builds on RFC 9728 and CIMD, ordinary REST APIs that adopt the same metadata can serve both MCP clients and direct-HTTP agents with one auth setup.

### Gaps
- I could not open OAI blog content to check for any official OAI statement endorsing or specifying an OpenAPI→MCP mapping. None was found in search results.
- No adoption numbers exist for Arazzo in production, or for which OpenAPI→MCP converters dominate.
