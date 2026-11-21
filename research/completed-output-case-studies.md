# Completed-Output Inspection — First Case Studies

**Research date:** 17 November 2026  
**Status:** First-pass inspection of public artifacts. This is not a full technical audit.

## Case 1 — Uniswap Foundation / Allium: DEX Analytics Portal

**Funding record:** Uniswap Foundation announced a USD 480,000 grant to Allium on 4 April 2024 for a DEX Analytics Portal.

**Problem stated by funder:** Researchers and developers lacked maintained, standardized, reliable DEX data. Inconsistent schemas made it difficult to compare trade events, MEV extraction and protocol behaviour across venues.

**Planned outputs stated in the grant announcement:**
- At least ten DEX data standards.
- A public DEX Analytics Portal.
- Standardized datasets for research into order flow, virtual liquidity and execution strategies.
- A 21-month, four-phase delivery plan.

**Research significance:** This is a strong example of funding an upstream research enabler. Instead of funding only one analysis, the grant targeted the data infrastructure that could make many future analyses possible.

**What we have verified:** The Foundation's grant announcement, funding amount, stated problem, deliverables and timeline.

**What remains unverified:** Whether all promised standards were delivered on schedule, the current completeness and public accessibility of the portal, and measurable downstream research adoption. Do not describe the planned outputs as completed without separate evidence.

**Primary source:** https://www.uniswapfoundation.org/blog/new-initiative-allium-receives-grant-for-dex-analytics-portal

## Case 2 — Uniswap Foundation / Whetstone: Doppler

**Funding record:** The Uniswap Foundation portfolio lists Doppler, developed by Whetstone, as a research grant project.

**Research artifact inspected:** *Doppler: A liquidity bootstrapping ecosystem* (January 2024 whitepaper).

**Problem addressed:** New token markets face a difficult initial price-discovery and liquidity-bootstrapping problem. Initial prices set too low can create immediate arbitrage losses; prices set too high can suppress trading. Conventional liquidity provision also requires capital and specialised market-making work.

**Proposed mechanism:** A non-custodial Uniswap v4 hook using a Dutch-auction dynamic bonding curve to bootstrap two-sided liquidity and automate initial price discovery.

**Technical artifact inspected:** Public project documentation describes hook lifecycle functions, accounting of token sales and proceeds, and periodic curve rebalancing based on sales relative to a predefined schedule.

**Research significance:** The work combines market design, auction theory, AMM mechanics and smart-contract implementation around one bounded economic problem. It has both a written research artifact and an implementable mechanism.

**What we have verified:** The whitepaper exists and explains the mechanism; the repository documentation exposes key contract behaviours.

**What remains unverified:** Independent empirical evidence that the mechanism consistently improves launch outcomes or reduces extractive MEV relative to specified alternatives. The whitepaper's design rationale is not itself proof of superior outcomes.

**Primary sources:**
- Whitepaper: https://www.doppler.lol/whitepaper.pdf
- Technical documentation: https://github.com/whetstoneresearch/doppler/blob/main/docs/Doppler.md
- Uniswap Foundation grants portfolio: https://www.uniswapfoundation.org/grants

## Case 3 — Ethereum Foundation: Institutional Economic Analysis of Slashing Penalties

**Funding record:** Listed in the EF 2024 Academic Grants Round, associated with Eric Alston and William Lehr.

**Problem described by funder:** Slashing policies across proof-of-stake networks, including governance implications and the diversity of automated procedures. The description emphasises balancing punitive measures with due-process mechanisms.

**Interdisciplinary contribution visible in the project definition:** Institutional economics and governance are applied to a technical protocol-enforcement mechanism.

**Research significance:** This is a useful model for translating a technical mechanism into an institutional/economic research question. The question is not only how slashing executes, but how penalty design, discretion and procedural safeguards shape governance.

**What we have verified:** The award record and its public description.

**What remains unverified:** A completed paper or final deliverable attributable to this grant has not yet been located. Do not claim its findings or impact.

**Primary source:** https://blog.ethereum.org/2025/01/17/academic-grants-recipients

## Case 4 — Ethereum Foundation: Blockspace Derivative Frameworks

**Funding record:** Listed in the EF 2024 Academic Grants Round, associated with Shouqiao Wang at Columbia Business School.

**Problem described by funder:** Transaction-fee volatility and market efficiency in Ethereum blockspace markets.

**Interdisciplinary contribution visible in the project definition:** Financial derivatives and market design are applied to blockchain transaction capacity.

**Research significance:** This illustrates a bounded financial-economics question connected to a specific technical resource. It offers a useful pattern for research that formalises a market problem rather than simply describing an ecosystem.

**What we have verified:** The award record and its public description.

**What remains unverified:** A completed paper, model, dataset or final deliverable attributable to this grant has not yet been located.

**Primary source:** https://blog.ethereum.org/2025/01/17/academic-grants-recipients

## Case 5 — Stellar Development Foundation: AMM Design to Optimise LP Returns

**Funding record:** Listed in SDF's Q2 2025 awarded research grants, associated with Zachary Feinstein and Maxim Bichuch.

**Research question indicated by title:** How AMM design can be optimised for liquidity-provider returns.

**Interdisciplinary contribution visible in the project definition:** Quantitative finance, optimisation and automated market design.

**Research significance:** A specific measurable objective (LP returns) is more researchable than a broad theme such as "improving DeFi liquidity." A complete study could compare designs under explicit assumptions about volatility, fees, inventory risk and adverse selection.

**What we have verified:** The official award listing.

**What remains unverified:** The completed paper and its assumptions, model, empirical data and findings have not yet been inspected.

**Primary source:** https://research.stellar.org/research-grants/grantees

## Case 6 — Stellar Development Foundation: Market Microstructure and Incentive Design for Perpetual DEXs

**Funding record:** Listed in SDF's Q1 2026 awarded research grants, associated with Ruizhe Jia at Stanford University.

**Research question indicated by title:** Market microstructure and incentive design in perpetual decentralized exchanges.

**Research significance:** The topic joins market structure, trader incentives, liquidity provision and protocol mechanism design. It is a useful comparator for research where market outcomes depend on both participant behaviour and technical rules.

**What we have verified:** The official award listing.

**What remains unverified:** Completed output, model, dataset and findings have not yet been located.

**Primary source:** https://research.stellar.org/research-grants/grantees

## Cross-case observations

These are descriptive observations about public project definitions and artifacts, not proven causes of funding decisions.

1. **A concrete economic or technical friction is named.** Examples include inconsistent DEX data, initial liquidity formation, slashing procedures, fee volatility and LP returns.
2. **The research method is connected to the problem.** Examples include standardized schemas, auction curves, institutional-economic analysis, derivatives frameworks and optimisation.
3. **Interdisciplinary work is integrated.** Disciplines are combined because the research question crosses their boundaries.
4. **Some projects create reusable artifacts.** Data standards, portals, code and mechanisms can serve users beyond the original research team.
5. **Funding announcements and completed work must be separated.** We have inspected actual artifacts for Doppler and the Allium grant description, but several other cases remain at award-announcement level.

## Implications for Canton

A promising Canton research project should identify a specific institutional or market-process problem where Canton architecture is relevant, then investigate it with a method that can be independently inspected.

Potential forms of contribution include:
- a quantitative model of a financial process;
- an empirical dataset or measurement framework;
- a comparative analysis of settlement or collateral workflows;
- a reproducible methodology for interpreting observable network activity;
- an explanatory model linking privacy architecture to institutional control and operational requirements.

We should not assume that Canton transaction-level data is public or that network-level metrics reveal economic activity. The data inventory must precede topic selection.

## Next inspection tasks

1. Retrieve the full EF grant page and locate links or researcher pages for the slashing and blockspace projects.
2. Search for the Blockchain Geometry and anonymity/compliance project outputs.
3. Find the full SDF AMM and perpetual-DEX papers, if publicly available.
4. Verify current Allium portal functionality and accessible schemas; distinguish public documentation from paid data access.
5. Search for independent empirical evaluations of Doppler rather than relying only on its design documents.
6. Add a completion-status and evidence-strength field to the master project register.


## Follow-up verification — SDF AMM grant status

A University at Buffalo research-project record identifies **Automated Market Maker Design to Optimize Liquidity Providers' Returns** as an active project, with an effective period of 1 September 2025 to 31 August 2027 and USD 37,500 in funding from the Stellar Development Foundation. As of this research date (17 November 2026), it is still within the recorded project period. Therefore, the absence of a completed public paper should not be interpreted as a failure to deliver; the project may still be underway.

Source: https://researchconnect.buffalo.edu/en/projects/automated-market-maker-design-to-optimize-liquidity-providers-ret-2/
