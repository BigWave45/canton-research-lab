# Completed-Output Case Study Synthesis

**Research date:** 17 November 2026  
**Scope:** Public artifacts from Uniswap Foundation, Ethereum Foundation, and Stellar Development Foundation research funding.  
**Purpose:** Identify useful research-design patterns for the Canton Community Research Grants. This is a descriptive comparison, not a model of grant selection probability.

## 1. Allium DEX Analytics Portal — research infrastructure as a multiplier

### Funding and original problem
The Uniswap Foundation announced a USD 480,000 grant to Allium in April 2024. The stated problem was the lack of maintained, standardized DEX data. Inconsistent schemas and fragmented data made it harder for researchers to compare protocol activity, order flow, and MEV-related behaviour.

The grant announcement specified at least ten data standards and a public portal, delivered over a 21-month, four-phase commitment.

### Public output inspected
The DEX Analytics portal is publicly accessible and exposes schema descriptions, samples, and methodology. Its Orderflow Explorer models a swap's path from frontend or origin, through aggregators and solvers, to liquidity pools. The methodology combines decoded DEX trades and aggregator trades, applies protocol classifications and priority rules, and uses transaction/event ordering to resolve routing paths.

The documentation includes validation logic for simple AMM, aggregator, meta-aggregator, and intent-based swaps. It also documents limitations, including incomplete frontend metadata and missing protocol coverage.

### Why this is a useful case
The contribution is upstream infrastructure. Standardised data can support multiple downstream studies rather than only one paper. The project also makes methodological choices inspectable.

### Evidence and caveats
- The Foundation's grant announcement documents the funding, problem, planned standards, portal, and timeline.
- The live portal and schema documentation demonstrate that a public research-facing artefact exists.
- A 2025 Allium post describes the Orderflow Explorer and its validation methodology.
- Some query access requires an Allium login; public schema pages and sample rows are not equivalent to unrestricted bulk-data access.
- The portal's terms specify non-commercial use, usage limits, no bulk redistribution, and attribution. These conditions must be checked before using its data in a publication or tool.
- The Uniswap Foundation's own announcement is evidence of the funder's rationale, not an independent impact evaluation.

Sources:
- https://www.uniswapfoundation.org/blog/new-initiative-allium-receives-grant-for-dex-analytics-portal
- https://dexanalytics.org/
- https://dexanalytics.org/schemas/orderflow
- https://www.allium.so/blog/mapping-the-flow-of-dex-swap-execution-alliums-orderflow-explorer-2/
- https://dexanalytics.org/about/terms-of-use

## 2. Doppler — mechanism design connected to implementation

### Research problem
Doppler addresses initial price discovery and liquidity bootstrapping. The project describes the challenge of launching a market with an initial price and sufficient two-sided liquidity, while reducing value leakage and extractive behaviour.

### Public output inspected
The January 2024 whitepaper describes a Dutch-auction dynamic bonding curve used to source initial two-sided liquidity. Public technical documentation describes its Uniswap v4 hook lifecycle, accounting for tokens sold and proceeds, and rebalancing behaviour.

The Uniswap Foundation's September 2025 ecosystem update reported that Doppler powered more than two million hooked pools initialized. This is a funder-reported adoption figure. It should not be interpreted as proof that Doppler outperforms alternatives or that every initialized pool is economically active.

### Why this is a useful case
The work links a defined market-design problem to a formal mechanism and a software implementation. The economic idea can be inspected in the paper and compared with the behaviour encoded in the implementation.

### Evidence and caveats
- Whitepaper and technical documentation are publicly available.
- The funder's ecosystem update provides a reported adoption metric.
- Independent causal evidence of improved launch outcomes, reduced MEV, or superior liquidity efficiency has not been established in this review.

Sources:
- https://www.doppler.lol/
- https://raw.githubusercontent.com/whetstoneresearch/docs/refs/heads/main/whitepapers/doppler/Dutch_auction_Dynamic_Bonding_Curves.pdf
- https://github.com/whetstoneresearch/doppler/blob/main/docs/Doppler.md
- https://www.uniswapfoundation.org/blog/ecosystem-update-sept-2025

## 3. Ethereum Foundation — Automated Penalties and Networked Coordination

### Funding and research question
The Ethereum Foundation's 2024 Academic Grants Round included research by Eric Alston, Bryce Bugge, and William Lehr. The public working paper, *Automated Penalties and Networked Coordination*, identifies the Ethereum Foundation as a funder.

### Public output inspected
The paper examines automated penalties and coordination in networked organisations. Its framing connects organisational and institutional economics with technical systems and automated enforcement.

### Why this is a useful case
It shows how research can use blockchain infrastructure as a setting for a broader economic and institutional question. The contribution is not simply a description of protocol mechanics; it investigates how automation changes coordination and enforcement.

### Evidence and caveats
- The EF award record identifies the project.
- The SSRN working paper identifies EF funding.
- The paper is a working paper; its claims and status should be represented accordingly.
- This paper should not be conflated with every separate project whose title mentions slashing or penalties.

Sources:
- https://blog.ethereum.org/2025/01/17/academic-grants-recipients
- https://papers.ssrn.com/sol3/Delivery.cfm/5147805.pdf?abstractid=5147805&mirid=1

## 4. Ethereum Foundation — Blockspace Derivative Frameworks

### Funding and research question
The EF 2024 Academic Grants Round lists Shouqiao Wang of Columbia Business School for *Ethereum Blockspace Derivative Frameworks*. The announced research concerns transaction-fee volatility and market efficiency in Ethereum blockspace markets.

### Output status
The award description is verified. A completed paper or public model attributable to this grant was not located in this pass.

### Why this is a useful case
The research question translates a technical resource—blockspace—into a financial-market problem involving price volatility, derivatives, and market efficiency. It is a clear example of an interdisciplinary question with a quantitative-finance core.

### Caveat
Do not attribute findings to this project until its actual output is located.

Source:
- https://blog.ethereum.org/2025/01/17/academic-grants-recipients

## 5. Stellar Development Foundation — AMM Design to Optimise LP Returns

### Funding and research question
The SDF quarterly grant register lists Zachary Feinstein and Maxim Bichuch for research on AMM design and liquidity-provider returns.

A University at Buffalo research record identifies the project as active from 1 September 2025 through 31 August 2027, with USD 37,500 in SDF funding.

### Output status
The project period is still active as of 17 November 2026. The absence of a completed public paper at this point is not evidence of non-delivery.

### Why this is a useful case
It defines a measurable financial objective—liquidity-provider returns—and connects it to AMM mechanism design. A rigorous study could require explicit assumptions about volatility, fees, inventory risk, adverse selection, and liquidity allocation.

### Caveat
The actual model, data, assumptions, and findings have not yet been inspected. The award title alone is not enough to infer the method.

Sources:
- https://research.stellar.org/research-grants/grantees
- https://researchconnect.buffalo.edu/en/projects/automated-market-maker-design-to-optimize-liquidity-providers-ret-2/

## 6. Stellar Development Foundation — Market Microstructure and Incentive Design for Perpetual DEXs

### Funding and research question
The SDF grant register lists Ruizhe Jia of Stanford University for *Market Microstructure and Incentive Design for Perpetual Decentralized Exchanges* in Q1 2026.

### Output status
The award record is verified. A completed public paper or dataset was not located in this pass.

### Why this is a useful case
The research question joins market microstructure, participant incentives, liquidity provision, and protocol design. It is a strong example of an interdisciplinary research question whose quantitative core is financial-market behaviour.

### Caveat
Do not claim findings or impact without the actual output.

Source:
- https://research.stellar.org/research-grants/grantees

## 7. Cross-case synthesis

The inspected cases suggest several useful research-design characteristics:

1. **A concrete friction is identified.** Examples include fragmented data, poor initial price discovery, automated enforcement, blockspace price volatility, and LP return optimisation.
2. **The method is matched to the friction.** Data standardisation, auction design, institutional economics, derivatives frameworks, and optimisation are not interchangeable; each is selected for a specific problem.
3. **The disciplines meet around one research question.** Interdisciplinary research is integrated rather than presented as unrelated sections.
4. **The output is inspectable.** Strong public artefacts expose a paper, model, methodology, code, dataset, or technical documentation.
5. **Limitations are documented.** The Allium orderflow methodology is explicit about attribution and coverage gaps.
6. **Impact claims require their own evidence.** A live tool, an initialized pool count, or a funder's update is useful evidence, but does not by itself establish causal economic benefit.

These are observations about publicly documented projects, not proof of why the funders selected them.

## 8. Implications for Canton research

The strongest pattern for our work is:

**Institutional or market problem → precise research question → appropriate quantitative method → Canton-specific technical analysis → reproducible output → clear educational explanation.**

Potential hybrid outputs include:
- a quantitative model of a financial workflow;
- a documented dataset and measurement methodology;
- a reproducible comparison of settlement or collateral processes;
- an empirical study of observable network activity, with strict limits on what public data can establish;
- a framework connecting privacy architecture to institutional control and operational requirements.

Before selecting a Canton topic, we need to establish which relevant data is actually accessible, what can be measured, and what the existing literature already covers.

## 9. Next work

1. Locate the full public output for the EF blockspace derivatives project, if available.
2. Locate the SDF perpetual-DEX project output, if available.
3. Inspect the EF-funded privacy/compliance and blockchain-geometry projects separately.
4. Build a Canton data inventory: source, access method, fields, time coverage, granularity, restrictions, and reproducibility.
5. Map existing Canton papers and technical documentation to avoid duplicating published work.
6. Only then generate and rank original Canton research hypotheses.
