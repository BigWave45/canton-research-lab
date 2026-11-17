# Comparative Grant-Winner Intelligence — Initial Findings

**Research date:** 17 November 2026  
**Status:** Initial desk-research synthesis; not a completed systematic review  
**Research orientation:** Interdisciplinary, with a quantitative core  
**Intended output:** Research paper supported by reproducible analysis, data, models and visualisations

## 1. Scope and comparability

This review uses public award records from the Ethereum Foundation (EF), Stellar Development Foundation (SDF), Uniswap Foundation, and Canton Foundation. These programmes are not interchangeable:

- EF's 2024 Academic Grants Round is an academic research funding round.
- SDF's Academic Research Grants programme is explicitly academic and has formal principal-investigator and proposal requirements.
- Uniswap Foundation's portfolio includes research, implementation, developer infrastructure, security, governance and ecosystem programmes.
- Canton's Protocol Development Fund is a milestone-based public-goods and technical development fund. It is not the Canton Community Research Grants programme.
- Canton Community Research Grants began in November 2026. There is no prior winner cohort for this specific programme in the launch announcement.

The comparison therefore distinguishes programme type before drawing cross-programme observations. Public grant announcements reveal funded topics and stated project aims; they do not by themselves prove completed quality, impact, or the private reasons for selection.

## 2. Programme-level observations

### Ethereum Foundation — 2024 Academic Grants Round

The EF announced 41 funded projects with a total budget of USD 1,786,137.48. Its published categories included cryptography and zero-knowledge proofs, cybersecurity and privacy, economics and MEV, formal verification, consensus, P2P networking, client engineering, and society/regulation.

Examples that combine disciplines or produce analytical methods:
- **An Institutional Economic Analysis of Slashing Penalties on Proof of Stake Cryptocurrency Networks** — institutional economics applied to protocol governance and slashing policy.
- **Balancing Anonymity and Compliance in Financial and Other Transactions** — privacy-preserving credentials with conditional traceability.
- **Ethereum Blockspace Derivative Frameworks** — market design and financial economics applied to transaction-space price volatility.
- **Blockchain Geometry** — analytical tools for visualising blockchain behaviour in equilibrium, combining economic and computational perspectives.
- **Open-Source Software Development and Community Dynamics** — social-science analysis of open-source ecosystems.
- **Execution and Finality in Ethereum from a Legal Perspective** — transaction execution and settlement considered through EU financial regulation.

The grant announcement provides project descriptions and category budgets. It does not establish that all projects completed their intended deliverables or that the listed characteristics caused selection.

### Stellar Development Foundation — Academic Research Grants

SDF publishes awarded projects by quarter. Its public list includes:
- **Market Microstructure and Incentive Design for Perpetual Decentralized Exchanges** (Q1 2026).
- **Automated Market Maker Design to Optimize Liquidity Providers' Returns** (Q2 2025).
- **Analytical Model for Analyzing Leader-based and DAG-based Protocols** (Q1 2025).
- **The Value Proposition of a Retail CBDC** (Q4 2023).
- **Efficiency of Anonymous and Private Decentralized Payments** (Q4 2023).
- **Efficient Historical (Range) Queries for Stellar** (Q3 2025).

The SDF programme requires a short proposal with a technical body, bibliography, budget, PI biography and institutional PI authorisation. It also states an intention not to patent the research. This is materially different from a community content grant and may exclude applicants who cannot satisfy academic PI requirements.

### Uniswap Foundation — research and adjacent grants

The published portfolio lists:
- **Doppler** — a Uniswap v4 liquidity-bootstrapping hook using a Dutch-auction dynamic bonding curve, designed to reduce extractive MEV.
- **DEX Analytics Portal** — accurate, verified and ergonomic DEX/Uniswap datasets.
- **Optimal Routing in the Presence of Hooks** — research on optimal execution across different hook constructs.
- **Research and Incentive Optimization** — protocol fee analysis and incentive campaign research.
- **UCRP** — a community research programme intended to encourage deeper analysis of Uniswap data.

The portfolio is broader than academic research. It includes both knowledge production and practical infrastructure.

### Canton Foundation — adjacent funding evidence

Canton's Protocol Development Fund is a useful local reference for the ecosystem's stated demand for public goods, but it must not be mislabelled as a Community Research Grant winner list.

Its first report (24 August 2026) stated that 42 projects had been approved, representing 290.0 million CC in commitments, with 62.2 million CC paid or minted against accepted milestones and recurring work at that date. Examples include:
- **Open-Source Validator Indexer (PQS)** — SQL-based validator data access for operations, compliance and audit reporting.
- **Canton Payment Streams** — private payment streams, vesting schedules and batch payouts.
- **ISS-Based BFT** — multi-leader ordering for throughput and fault tolerance.
- **Scalability, Performance, and Robustness** — network capacity and reliability work.
- **Token Standard V2** — privacy, performance and institutional settlement features.
- **x402 Protocol Integration** — Canton settlement support for APIs and AI agents.

The report says Development Fund 2.0 will ask proposals to define the problem, evidence need, explain architectural fit, identify a community champion, state funding/duration, and tie payments to measurable milestones. These are signals about the adjacent technical fund, not published criteria for the Community Research Grants.

## 3. Observable characteristics in the funded-project descriptions

The following are patterns in public descriptions, not causal claims about selection.

### A. Specific mechanisms rather than broad themes
Projects tend to name a mechanism or bounded problem: slashing penalties, liquidity-provider returns, optimal routing, private information retrieval, settlement finality, or historical range queries.

### B. A method is visible in the project definition
Descriptions point to a model, cryptographic construction, verification method, dataset, analytical framework, or implementation. The reader can usually infer what work will be done, rather than seeing only a general ambition.

### C. Interdisciplinary work joins disciplines around one question
Examples include:
- economics + protocol governance (slashing);
- privacy engineering + compliance (anonymous credentials with traceability);
- market microstructure + mechanism design (perpetual DEXs and AMMs);
- computer science + economics (blockchain equilibrium visualisation);
- distributed systems + legal analysis (execution and finality).

The useful unit is the integrated research question, not a list of unrelated disciplines.

### D. Some funded research leaves reusable infrastructure
The Uniswap DEX Analytics Portal and Canton's validator indexer illustrate how structured data access can support many downstream researchers and operators. A dataset or tool can have value beyond its original report.

### E. Outputs and impact need separate verification
A funded announcement records intent and award. A completed paper, released dataset, maintained tool, adoption record, or citation trail is stronger evidence of delivery and downstream utility. We must inspect these before treating any case as a demonstrated success.

## 4. What this implies for our Canton research design

For a distinctive hybrid study, the paper should not merely describe Canton or reproduce its own claims. It should answer one bounded question with an inspectable method and a tangible research artifact.

A strong research package could combine:
1. a clearly framed institutional-finance or market-structure problem;
2. a quantitative model or empirical analysis;
3. a technical explanation of the Canton mechanism relevant to that problem;
4. transparent data provenance and reproducible calculations;
5. a visual or dataset that helps other readers reuse the analysis.

The research question must be selected only after reviewing existing Canton literature and confirming data availability. We should not assume private Canton transaction data is publicly observable.

## 5. Initial comparative matrix

| Programme / case | Programme type | Main discipline(s) | Stated method or output | What is publicly evidenced |
|---|---|---|---|---|
| EF 2024 Academic Round | Academic grants | Multiple | 41 funded projects across eight categories | Award announcement, categories, project descriptions and budgets |
| EF: Slashing Penalties | Academic research | Institutional economics, governance | Comparative institutional economic analysis | Award description |
| EF: Anonymity and Compliance | Academic research | Cryptography, privacy, compliance | Privacy-preserving blueprint / credentials | Award description |
| EF: Blockspace Derivatives | Academic research | Financial economics, market design | Derivative-market framework | Award description |
| EF: Blockchain Geometry | Academic research | Economics, computation | Analytical visualisation tools | Award description |
| SDF: Perpetual DEX Microstructure | Academic research | Market microstructure, mechanism design | Market/incentive design research | Award listing |
| SDF: AMM LP Returns | Academic research | Financial economics, optimisation | AMM design to optimise LP returns | Award listing |
| SDF: Leader/DAG Analytical Model | Academic research | Distributed systems, modelling | Analytical protocol model | Award listing |
| Uniswap: Doppler | Research / applied protocol design | Mechanism design, DeFi, engineering | Dutch-auction dynamic bonding curve | Grant portfolio description |
| Uniswap: DEX Analytics Portal | Research infrastructure | Data engineering, market analytics | Verified DEX datasets and portal | Grant portfolio description |
| Uniswap: Optimal Routing with Hooks | Research | Algorithms, execution, market design | Optimal execution research | Grant portfolio description |
| Canton: Validator Indexer (PQS) | Technical public-goods fund | Data systems, operations, compliance | SQL-based validator data access | Fund report, approved and paid amounts |
| Canton: Payment Streams | Technical public-goods fund | Payments, privacy, software engineering | Private streams, vesting, batch payouts | Fund report, approved and paid amounts |
| Canton: ISS-Based BFT | Technical public-goods fund | Distributed systems | Multi-leader ordering | Fund report, approved and paid amounts |

## 6. Limits of this review

- This is a purposive sample, not a statistically representative sample of all grants.
- Award announcements are not equivalent to completed outputs.
- Public descriptions are often short and omit detailed methods.
- Programme mandates and applicant eligibility differ substantially.
- We cannot infer selection causality from the characteristics of funded projects alone.
- We have not yet independently audited the technical or empirical results of the named projects.
- Canton Community Research Grants has no established prior winner cohort in the launch announcement.

## 7. Next research tasks

1. Retrieve and inspect completed outputs for the EF cases above, especially slashing economics, blockspace derivatives, blockchain geometry and anonymity/compliance.
2. Retrieve the Doppler implementation and technical explanation; inspect the DEX Analytics Portal data model and availability.
3. Locate papers or working papers from the SDF market microstructure and AMM projects.
4. Verify the formal Canton Community Research Grants terms and applicant eligibility.
5. Map existing Canton research on privacy, synchronisation, settlement, collateral, token standards and network economics.
6. Inventory publicly accessible Canton datasets and identify what cannot be observed.
7. Build a source-backed hypothesis register only after the literature and data inventory.

## 8. Primary sources

- Ethereum Foundation, 2024 Academic Grants Round Recipients (17 Jan 2025): https://blog.ethereum.org/2025/01/17/academic-grants-recipients
- Stellar Development Foundation, Awarded Research Grants by Quarter: https://research.stellar.org/research-grants/grantees
- Stellar Development Foundation, Academic Research Grants and application requirements: https://research.stellar.org/research-grants
- Uniswap Foundation, Grants portfolio: https://www.uniswapfoundation.org/grants
- Canton Foundation, Protocol Development Fund: The First Report (24 Aug 2026): https://canton.foundation/protocol-development-fund-the-first-report/
- Canton Network, Introducing the Canton Community Research Grants (4 Nov 2026): https://www.canton.network/blog/introducing-the-canton-community-research-grants
