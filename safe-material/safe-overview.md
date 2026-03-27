

# SAFe Lean Portfolio Management (LPM) Reference Document

---

## Table of Contents

1. [SAFe LPM Overview](#safe-lpm-overview)
2. [Key Concepts and Definitions](#key-concepts-and-definitions)
3. [SAFe Framework Overview](#safe-framework-overview)
4. [Five Disciplines of SAFe](#five-disciplines-of-safe)
5. [Horizons](#horizons)
6. [Metrics and Measures](#metrics-and-measures)
7. [Ceremonies and Events](#ceremonies-and-events)
8. [Roles and Responsibilities](#roles-and-responsibilities)
9. [Teams and Structures](#teams-and-structures)
10. [Portfolio Kanban States](#portfolio-kanban-states)
11. [Lean Budget Guardrails](#lean-budget-guardrails)
12. [Epic Lifecycle](#epic-lifecycle)
13. [SAFe Principles](#safe-principles)
14. [CALMR – DevOps Mindset](#calmr--devops-mindset)
15. [Continuous Delivery Pipeline](#continuous-delivery-pipeline)
16. [Enterprise and Enterprise Portfolio Management](#enterprise-and-enterprise-portfolio-management)
17. [Portfolio Canvas](#portfolio-canvas)
18. [Portfolio Vision and Strategy Formulation](#portfolio-vision-and-strategy-formulation)
19. [Strategic Analysis Tools](#strategic-analysis-tools)
20. [Portfolio Roadmap](#portfolio-roadmap)
21. [WSJF and Epic Sequencing](#wsjf-and-epic-sequencing)
22. [SAFe Lean Startup Cycle](#safe-lean-startup-cycle)
23. [Participatory Budgeting](#participatory-budgeting)
24. [Color of Money](#color-of-money)
25. [Lean Business Case](#lean-business-case)
26. [Epic Hypothesis Statement](#epic-hypothesis-statement)
27. [Capacity Allocation](#capacity-allocation)
28. [OKRs in SAFe](#okrs-in-safe)
29. [Flow Accelerators](#flow-accelerators)
30. [Connected Kanban Systems](#connected-kanban-systems)
31. [Pivot Types](#pivot-types)
32. [Epics vs Projects](#epics-vs-projects)
33. [Traditional vs Lean Portfolio Management](#traditional-vs-lean-portfolio-management)
34. [LPM Three Collaborations](#lpm-three-collaborations)
35. [LPM Competencies](#lpm-competencies)
36. [Portfolio Organization Patterns](#portfolio-organization-patterns)
37. [Value Streams](#value-streams)
38. [Value Stream Coordination](#value-stream-coordination)
39. [Agile Portfolio Operations](#agile-portfolio-operations)
40. [Lean Governance](#lean-governance)
41. [Compliance in SAFe](#compliance-in-safe)
42. [Technology Business Management (TBM)](#technology-business-management-tbm)
43. [Agile Software Capitalization](#agile-software-capitalization)
44. [Architectural Runway and Enablers](#architectural-runway-and-enablers)
45. [Portfolio Leadership Behaviors](#portfolio-leadership-behaviors)
46. [Decision-Making Principles](#decision-making-principles)
47. [Common Legacy Impediments](#common-legacy-impediments)
48. [LPM Implementation Roadmap](#lpm-implementation-roadmap)
49. [LPM Kickoff Event](#lpm-kickoff-event)
50. [LPM Participants and Engagement](#lpm-participants-and-engagement)
51. [Change Leadership for LPM](#change-leadership-for-lpm)
52. [Preparing Finance for LPM](#preparing-finance-for-lpm)
53. [Common LPM Implementation Challenges](#common-lpm-implementation-challenges)
54. [LPM Community of Practice](#lpm-community-of-practice)
55. [AI-Enabled Portfolio Management](#ai-enabled-portfolio-management)
56. [Large Solution Integration and Delivery](#large-solution-integration-and-delivery)
57. [Product Development Flow Discipline](#product-development-flow-discipline)
58. [Leadership and Culture](#leadership-and-culture)
59. [Team and Technical Agility](#team-and-technical-agility)
60. [Implementing SAFe](#implementing-safe)
61. [Benefits of SAFe](#benefits-of-safe)
62. [Scrum Process (Team Level)](#scrum-process-team-level)
63. [Assessment Questions](#assessment-questions)

---

## SAFe LPM Overview

Lean Portfolio Management (LPM) is one of the **Seven Core Competencies of Business Agility** and one of the **Five Disciplines** of a Lean-Agile Organization in SAFe. It aligns strategy with execution by applying Lean and systems thinking approaches to:

1. **Strategy and Investment Funding**
2. **Agile Portfolio Operations**
3. **Lean Governance**

LPM is essential to achieving **Business Agility** and **Strategy Agility** — the ability to sense changes in market conditions and implement new strategies quickly and decisively. The LPM function governs each SAFe portfolio and provides three essential collaborations to realize its responsibilities.

A **SAFe portfolio** is a collection of **Development Value Streams**. Each Development Value Stream builds, supports, and maintains **Solutions** — products and services — used by Customers. Solutions are one of the central concepts in SAFe because customers buy whole-product Solutions that deliver desired outcomes.

Traditional portfolio management was not designed for today's fast-paced environment; LPM modernizes portfolio management to achieve the strategic agility required to compete in the "age of software, digital, and AI."

> *"Most strategy dialogues end up with executives talking at cross-purposes because … nobody knows exactly what is meant by vision and strategy, and no two people ever quite agree on which topics belong where."* — Geoffrey Moore, *Escape Velocity*

> *"If you are in high tech, or for that matter in any other sector characterised by recurrent disruption, you can't sit still. You simply have to be a growth company."* — Geoffrey Moore, *Zone to Win*

### Core LPM Principles

- **Finance value streams, not work items** — the portfolio funds value streams rather than individual projects or Epics
- **Centralize allocation of funds; decentralize control over how funds are spent** — aligns with SAFe criteria for centralized decision-making (infrequent, long-lasting, economies of scale)
- **Promote the best possible ideas** through transparent, collaborative funding decisions
- **Balance centralized and decentralized decision-making** using Epic threshold guardrails
- **Distinguish between reserving (allocating) funds and spending (releasing) funds** — LPM works best with this separation

### Three LPM Dimensions

| Dimension | Key Collaborators | Primary Focus | Also Known As / Exam Phrasing |
|---|---|---|---|
| Strategy & Investment Funding | Enterprise Executives, Business Owners, Enterprise Architect | Connect portfolio to Enterprise strategy; maintain Portfolio Vision; establish Lean Budgets and Guardrails; establish portfolio flow; realize Portfolio Vision through Epics | "Strategy and investment funding"; "Connect strategy to execution" |
| Agile Portfolio Operations | VMO/LACE, RTE and SM/TC CoP | Coordinate Value Streams; foster operational excellence; support ART execution | "Portfolio operations"; "Coordinate and support decentralized ART execution" |
| Lean Governance | VMO, Enterprise Architect, Business Owners | Governance policies, compliance, spending oversight, audit, forecasting expenses, measurement | "Lean governance"; "Forecast and budget dynamically; measure portfolio performance; coordinate continuous compliance" |

### Five Key Responsibilities of Strategy & Investment Funding

| # | Responsibility | Also Known As / Exam Phrasing |
|---|---|---|
| 1 | Connect the portfolio to Enterprise strategy | Aligning strategy |
| 2 | Maintain a Portfolio Vision | Vision maintenance |
| 3 | Establish Lean Budgets and Guardrails | Budget guardrails |
| 4 | Establish portfolio flow | Portfolio flow / Kanban flow |
| 5 | Realize Portfolio Vision through Epics | Epic realization |

---

## Key Concepts and Definitions

| Term / Abbreviation | Full Name | Definition | Also Known As / Exam Phrasing |
|---|---|---|---|
| LPM | Lean Portfolio Management | One of the Seven Core Competencies of Business Agility and Five Disciplines of a Lean-Agile Organization; aligns strategy with execution using Lean and systems thinking for strategy & investment funding, Agile portfolio operations, and lean governance | Portfolio governance function; LPM Discipline |
| SAFe Portfolio | SAFe Portfolio | A collection of Development Value Streams that build, support, and maintain Solutions delivered to Customers | Portfolio |
| Development Value Stream | Development Value Stream | The sequence of activities needed to convert a business hypothesis into a technology-enabled Solution that delivers Customer value | Dev Value Stream |
| Operational Value Stream | Operational Value Stream | The sequence of activities needed to deliver a product or service to a Customer (e.g., manufacturing, patient treatment) | OVS |
| ART | Agile Release Train | Cross-functional, long-lived team of Agile teams (50–125 people) that builds, supports, and maintains Solutions within Development Value Streams; contains all people needed to define, deliver, and operate the Solution | Train; team of teams |
| Strategic Themes | Strategic Themes | Differentiating business objectives that connect the portfolio to the Enterprise strategy; drive the future state of the portfolio; provide context for Portfolio Vision and Lean budgeting | Portfolio strategic objectives; often written as OKRs |
| OKR | Objectives and Key Results | Format used to communicate strategic intent; Objectives are inspirational and clear; Key Results are value-based, measurable, and gradable | Strategic Theme format; goal-setting framework |
| Portfolio Canvas | Portfolio Canvas | Adaptation of the Business Model Canvas that describes Development Value Streams and captures essential information about partners, activities, resources, and economics; current and future state canvases define Portfolio Vision | Business Model Canvas (adapted) |
| Portfolio Vision | Portfolio Vision | An aspirational description of the future state of the portfolio; "a postcard from the future"; describes how future Solutions solve larger Customer problems | "Postcard from the future"; portfolio future-state |
| Epic | Epic | A significant initiative that requires a Lean business case and moves through the Portfolio Kanban; used to realize Portfolio Vision; the primary container for large strategic initiatives | Portfolio Epic; Enterprise Epic; strategic initiative |
| Business Epic | Business Epic | An Epic that directly delivers business value to customers or the organization | Customer-facing Epic |
| Enabler Epic | Enabler Epic | An Epic that supports the Architectural Runway, technical infrastructure, or compliance without directly delivering user-facing value | Technical Epic; architectural Epic |
| Enterprise Epic | Enterprise Epic | A cross-portfolio initiative that requires collaboration of multiple portfolios; managed through the Enterprise Portfolio Kanban | Cross-portfolio epic |
| MVP | Minimum Viable Product | The smallest release that delivers enough value to validate a business hypothesis; limits investment risk and allows exploratory discovery | Minimum viable product; testable MVP |
| Lean Business Case | Lean Business Case | Provides just enough detail to establish viability; includes MVP definition, business outcome hypothesis, cost estimates, leading indicators, and deployment impact; replaces traditional detailed business cases | LBC; epic hypothesis statement (related) |
| Epic Hypothesis Statement | Epic Hypothesis Statement | Used to define and elaborate epics; includes the business hypothesis, value statement, leading indicators, and NFRs for the epic | Business hypothesis |
| WSJF | Weighted Shortest Job First | Prioritization framework: Cost of Delay divided by Job Duration (Job Size); used to sequence jobs/epics for maximum benefit | Sequencing/prioritization method; economic sequencing |
| Cost of Delay | Cost of Delay | Economic framework for understanding the cost of not delivering value sooner; composed of User-Business Value + Time Criticality + RR&OE; component of WSJF | CoD |
| RR&OE | Risk Reduction and Opportunity Enablement | A component of Cost of Delay measuring risk reduction or new business opportunity enablement; value of information received | Risk Reduction / Opportunity Enablement |
| WIP | Work in Process | The amount of work currently active in the system; limiting WIP is critical to fast flow | Work in progress |
| CDP | Continuous Delivery Pipeline | The integrated pipeline for continuous value delivery; optimized through CALMR practices | Delivery pipeline |
| CALMR | Culture, Automation, Lean Flow, Measurement, Recovery | SAFe's DevOps mindset guiding ARTs toward continuous value delivery | SAFe DevOps approach (modification of CALMS) |
| PI | Planning Interval / Program Increment | A timebox (typically 8–12 weeks) during which an ART delivers incremental value; includes PI Planning and PI System Demo | Program Increment (legacy term) |
| NFR | Nonfunctional Requirements | System qualities and constraints (performance, security, compliance, reliability, maintainability, scalability, usability) that apply across solutions | System qualities; quality attributes |
| EPM | Enterprise Portfolio Management | Ensures alignment between related portfolios and overall enterprise vision and strategy; coordinates cross-portfolio work | Enterprise portfolio coordination |
| VMO | Value Management Office | Supports Agile portfolio operations, lean governance, facilitation, coaching, reporting, and day-to-day portfolio operations | Also LACE; portfolio operations office |
| LACE | Lean-Agile Center of Excellence | Supports Agile portfolio operations, coaching, transformation, and continuous improvement; small team dedicated to implementing the SAFe Lean-Agile way of working | VMO/LACE; Center of Excellence; CoE |
| KPI | Key Performance Indicator | Quantifiable measures used to evaluate how each value stream and its solutions are performing; ongoing "health" metrics | Performance metrics; solution KPIs |
| MTTR | Mean Time to Recover / Restore | Average time to recover from production incidents; key DevOps and quality metric | Mean Time to Restore |
| CFD | Cumulative Flow Diagram | Visualization tool showing quantity of work in a given state, arrival and departure curves; used to measure flow load | Flow load visualization |
| CoP | Community of Practice | A group of people who share a concern or passion for something they do and learn how to do it better through regular interaction | RTE and SM/TC CoP; LPM CoP |
| SPC | SAFe Practice Consultant | Certified change agent who leads SAFe transformation, facilitates workshops (e.g., Value Stream and ART Identification), and provides coaching | SAFe consultant; SAFe change agent |
| Flow Framework | Flow Framework | Created by Mik Kersten; defines five flow metrics (distribution, velocity, time, load, efficiency) plus business results | Kersten Flow Framework |
| Business Agility | Business Agility | The ability of an organization to sense and respond to market changes quickly; LPM is essential to achieving it | Enterprise agility |
| Strategy Agility | Strategy Agility | The ability to sense changes in market conditions and implement new strategies quickly and decisively | Strategic agility; strategic responsiveness |
| Solution | Solution | A product or service delivered to a Customer; the central concept in SAFe that customers actually buy | Product, service, whole-product solution |
| Portfolio Kanban | Portfolio Kanban | A Kanban system that manages the flow of Epics from funnel to done across defined states with WIP limits; part of a connected Kanban system in SAFe | Portfolio Kanban system; Portfolio Kanban board |
| Portfolio Roadmap | Portfolio Roadmap | A comprehensive view across all Value Streams that integrates lower-level roadmaps and communicates the larger picture to Enterprise stakeholders; uses flexible rolling-wave approach | Strategic roadmap |
| Solution Roadmap | Solution Roadmap | A schedule of events and milestones that communicate forecasted Solution deliverables over a planning horizon | Solution-level roadmap |
| Lean Budgets | Lean Budgets | A funding approach that allocates budgets to Value Streams rather than projects, enabling faster and more flexible investment decisions; includes operating, overhead, and capital expenses | Fund Value Streams, not projects; value stream funding |
| BSI | Baseline Solution Investments | "Run the Business" investments including Features, Capabilities, and Epics below the portfolio Epic threshold; ongoing costs to develop, support, and operate current solutions | Run the Business; current solution costs |
| PSI | Proposed Solution Initiatives | "Grow the Business" investments including ART, Solution, and portfolio Epics above the portfolio Epic threshold; significant new development initiatives | Grow the Business; epic voting cost |
| Capacity Allocation | Capacity Allocation | The recommended split of capacity among new Features, Enablers, technical debt/maintenance across the portfolio or Value Stream; determines how available personnel and resources are distributed | Resource distribution; capacity-driven funding model |
| T-shirt Sizing | T-shirt Size Estimates | A simplified estimation technique (S, M, L, XL, XXL) for estimating Epic cost in early stages, using historical data to establish cost ranges | Approximate estimation |
| Architectural Runway | Architectural Runway | The existing code, components, and technical infrastructure needed to implement near-term Features without excessive redesign; must be continually extended by implementing Enablers | Technical runway; enabler infrastructure |
| Lean Startup Cycle | SAFe Lean Startup Cycle | The process of building, measuring, and learning from MVPs to validate Epic hypotheses before committing to full implementation | Build-Measure-Learn |
| Innovation Accounting | Innovation Accounting | A method for measuring progress of Epics using leading indicators to predict business outcomes | Early outcome metrics |
| Agile Contracts | Agile Contracts | Flexible contracting approaches suited for Agile development where all parties are equally incentivized to collaborate toward the most cost-effective Solution | SAFe Managed-Investment Contract |
| Market Rhythms | Market Rhythms | Recurring market patterns that help identify valuable release windows | Seasonal market patterns |
| Market Milestones | Market Milestones | Known market events (competitor releases, regulatory changes, technology changes) that influence release timing | External market events |
| Epic Threshold | Portfolio Epic Threshold | The criterion (forecasted cost, number of PIs, strategic importance, or combination) that determines whether an Epic requires LPM review and approval through the Portfolio Kanban | Guardrail threshold; epic size threshold |
| Participatory Budgeting | Participatory Budgeting (PB) | A collaborative tool/event used in LPM for allocating the portfolio budget to fund Epics and value streams through forums involving leadership and extended teams | PB; collaborative budgeting; PB forums |
| Color of Money | Color of Money | The categorization or classification of funds based on intended purpose, source restrictions, or regulatory constraints; restricts how specific funds can be used | Funding constraints; earmarked funds; regulatory funding constraints |
| SAFe CoFund | SAFe CoFund | A tool that enables enterprises to facilitate Participatory Budgeting and collaboratively prioritize investments | PB tool |
| Economic Framework | Economic Framework | A set of decision guidelines that align everyone with the portfolio's financial objectives and inform continuous trade-off decisions | Decision guidelines; Principle #1 application |
| Sunk Costs | Sunk Costs | Costs already incurred that should be ignored when making forward-looking investment decisions | Ignore sunk costs principle |
| Classes of Service | Classes of Service | Kanban mechanism enabling high-priority items to flow quickly through the system while managing overall WIP | Priority classes |
| VSM | Value Stream Management | A leadership and technical discipline that enables maximum flow of business value through the end-to-end Solution delivery life cycle; foundation is Lean thinking | End-to-end pipeline visibility |
| TBM | Technology Business Management | A value management framework that provides a standard IT cost accounting system to explain total cost of ownership of Solutions | IT cost transparency framework |
| QMS | Quality Management System | A comprehensive system for managing quality, safety, security, and compliance | Quality system; compliance management system |
| Lean QMS | Lean Quality Management System | A modernized QMS incorporating Lean-Agile principles, building compliance incrementally into regular flow of work | Agile QMS; modernized QMS |
| Solution Intent | Solution Intent | The repository for storing, managing, and communicating the knowledge of current and intended solution behavior; used for V&V and traceability | Specifications and Solution Intent |
| V&V | Verification and Validation | Verification: built the solution right (meets specifications); Validation: built the right solution (meets fitness for use) | Verification and Validation |
| IV&V | Independent Verification and Validation | V&V performed by parties independent of the development team, often required by regulations | Independent V&V |
| DoD | Definition of Done | A checklist of criteria that must be met before a backlog item is considered complete; includes compliance activities where applicable | Done criteria; acceptance criteria |
| Enabler | Enabler | A backlog item type used to identify technical, infrastructure, or compliance work that supports future value delivery | Enabler Story; Enabler Feature; Enabler Capability |
| Feature | Feature | A service or function of a system that fulfills a stakeholder need; managed at the ART level; decomposed from Epics | ART-level backlog item |
| Capability | Capability | A higher-level Solution behavior, typically spanning multiple ARTs; managed at the Solution Train level | Large Solution backlog item |
| Story | Story | A small, valuable increment of functionality that can be completed within a single iteration by an Agile Team | User Story; team backlog item |
| HIPPO | Highest-Paid Person's Opinion | Anti-pattern where decisions are driven by seniority rather than data | Decision anti-pattern |
| DevSecOps | DevSecOps | Integration of development, security, and operations practices enabling Release on Demand | Promotes Release on Demand |
| NPS | Net Promoter Score | A metric measuring customer loyalty and satisfaction | Customer Satisfaction measure |
| AARRR | Pirate Metrics | Acquisition, Activation, Revenue, Retention, Referrals — KPIs for software product Value Streams | Software product KPIs |
| PDCA | Plan-Do-Check-Adjust | Deming's continuous improvement cycle; foundation for iterative and incremental development in SAFe | Deming Cycle; learning cycle |
| Design Thinking | Design Thinking | A customer-centric approach that prioritizes customer experience and problem-solving | Customer-Centric Design |
| IP Iteration | Innovation and Planning Iteration | A dedicated iteration within the PI for exploration, innovation, learning, and planning | Innovation sprint; buffer iteration |
| Solution Train | Solution Train | An organizational construct used to build large, complex solutions that require the coordination of multiple ARTs and suppliers | Large Solution; multi-ART coordination |
| STE | Solution Train Engineer | The servant leader and coach for a Solution Train | Large Solution RTE equivalent |
| Calibration Forum | Calibration Forum | A preliminary PB forum run with stakeholders/leaders to validate Epic cost estimates and benefit descriptions before larger forums | Pre-forum; wisdom of the crowd session |
| Hard Rules | Hard Rules (Constraint Type) | Constraints designed into the PB process that must be strictly enforced during forums | Enforced constraints |
| Soft Rules | Soft Rules (Constraint Type) | Constraints communicated as guidelines with some flexibility during PB forums | Flexible constraints; guideline constraints |
| Pivot | Pivot | A decision to change strategic direction based on validated learning from an MVP; portfolio strategy adjusts accordingly | Strategic pivot; structured course correction |
| Persevere | Persevere | A decision to continue investing in an Epic after the MVP validates the business outcome hypothesis | Continue; go decision |
| Stop | Stop | A decision to discontinue work on an Epic at any point in the Portfolio Kanban when it no longer aligns with portfolio strategy | Kill; no-go; terminate |

---

## SAFe Framework Overview

### SAFe Big Picture Components

| Component | Description | Also Known As / Exam Phrasing |
|---|---|---|
| Portfolio | Top-level organizational construct that aligns strategy to execution; contains value streams, portfolio backlog, and portfolio strategy | SAFe Portfolio |
| Value Streams | Organizational constructs containing all capabilities to deliver value to customers | Products and Solutions |
| Agile Release Train (ART) | Team of Agile teams aligned to a shared mission; 50–125 people | ART; Train |
| Agile Teams | Cross-functional groups of ≤10 people that define, build, test, and deploy value | Scrum teams; Kanban teams |
| Continuous Delivery Pipeline | Infrastructure for continuous exploration, integration, deployment, and release | CDP |
| PI Planning | Cadence-based event aligning all ART teams to shared PI objectives | Big room planning; Planning event |
| System Demo | End-of-iteration/PI demonstration of integrated work | Integrated demo |
| Inspect and Adapt | End-of-PI event for evaluation and improvement | I&A |

---

## Five Disciplines of SAFe

| Discipline | Abbreviation | Focus | Description | Also Known As / Exam Phrasing |
|---|---|---|---|---|
| Leadership and Culture | L&C | Leading change, developing leaders, building generative culture | Describes how leaders create a positive, performance-oriented culture enabling individuals and teams to reach their highest potential | Organizational culture; Lean-Agile leadership |
| Team and Technical Agility | TTA | Cross-functional teams, built-in quality, technical practices | Describes critical skills, roles, and practices for high-performing Agile teams and ARTs to create high-quality products | Agile teams; Technical excellence |
| Product Development Flow | PDF | Value flow, product innovation, customer-centric delivery | Enables organizations to release valuable product increments and respond swiftly to market changes | Product flow; Innovation flow |
| Large Solution Integration and Delivery | LSID | Multi-ART coordination, compliance, complex systems | Applies SAFe principles to developing, evolving, and operating the world's largest systems requiring many value streams and ARTs | Large solution; Solution Train |
| Lean Portfolio Management | LPM | Strategy & investment funding, Agile portfolio operations, governance | Aligns strategy and execution by applying Lean thinking to investment funding and portfolio governance | Portfolio management; Strategy alignment |

---

## Horizons

| Horizon | Name | Focus | Investment Type | Current / Emerging / Future | Example (Hospital Portfolio) | Also Known As / Exam Phrasing |
|---|---|---|---|---|---|---|
| Horizon 0 | Retiring / Decommissioning | Solutions being decommissioned; end-of-life products; sunsetting obsolete systems, platforms, or technologies | Extracting remaining value; decommission costs; cost reduction; resource liberation; data migration | Retiring | Decommissioning legacy patient management system; migrating data to new EHR | Decommission; "extracting" phase; Horizon 0; end-of-life; SAFe extension to McKinsey model |
| Horizon 1 | Investing / Optimize and Extend Core | Current solutions generating revenue and value; core business; maintaining and extending existing products/services | Investing in sustaining and enhancing current solutions; improving performance, profitability, incremental improvements | Current | Electronic Health Record (EHR) system — Patient Services, Clinical Operations, Billing & Administration | Current Solutions; core business investment; "Run the business"; cash-cow investments |
| Horizon 2 | Emerging / Grow Emerging Value | Solutions gaining traction; emerging business opportunities; new markets, expanding product lines | Evaluating and growing new capabilities; scaling up; adding features; expanding reach; medium-term reliable return | Emerging | Remote patient monitoring solution — adding device integrations, improving UI | Emerging Solutions; growth investment; "Grow the business" |
| Horizon 3 | Evaluating / Future Bets | Future solutions being explored; new business models and innovations; disruptive technologies | Evaluating potential; research and experimentation; low-cost MVPs; high-risk/high-reward | Future | AI-powered diagnostic tool for medical imaging — high-risk, high-reward experiment | Future Solutions; exploratory investment; "Transform the business"; R&D investments |

### Horizon Investment Guidance

- Based on **Geoffrey Moore's "Zone to Win"** (Performance, Incubation, Transformation, Productivity zones) and **McKinsey's Three Horizons of Growth** (introduced by Baghai, Coley, and White in *The Alchemy of Growth*, 2000)
- SAFe adds **Horizon 0** for retire/decommission — critical in large organizations to stop spending time and people on old systems
- **Guardrail**: Horizon investment targets define the percentage allocation across H0–H3; may be expressed as ranges (e.g., 12%–20%) during PB forums as soft rules
- A value stream solely focused on H1 may be **under-investing in future innovation**, creating long-term risk
- Portfolio Leadership is accountable for **optimizing the whole** while promoting decentralization
- The investment mix is expressed as percentages across horizons
- The percentage invested in each horizon for a Value Stream may not match the overall portfolio allocation

### Key Horizon Management Principles

- Portfolio Leaders actively manage initiatives across **all four horizons** simultaneously
- **H0** work frees capacity for more valuable work and reduces maintenance/security costs
- **H1** work is mostly managed locally by autonomous ARTs and teams
- **H2** initiatives require Portfolio Leaders to ensure alignment with broader portfolio strategy as solutions scale
- **H3** initiatives are typically worked on by a single ART but have significant enough future financial impact to be a Portfolio Kanban concern
- **H2 and H3** carry higher risk but offer greater potential for innovation — emphasis on hypothesis-driven development and validated learning
- Portfolio Leaders must balance short-term value (H0/H1) with long-term growth (H2/H3) and be prepared to **stop or pivot** initiatives that don't demonstrate value
- If an H2 or H1 Solution has zero new big ideas submitted to the funnel, the portfolio team should investigate the Solution Roadmap; if too many ideas are submitted, it may suggest the need to increase overall funding

> **Key Concept:** Portfolio flow distribution tracks the distribution of funding allocation across investment horizons. This ensures a balanced portfolio with both near- and long-term health.

---

## Metrics and Measures

### Flow Metrics (Flow Framework by Mik Kersten)

| Metric | What It Measures | Applies To | How Measured | Why Important | Also Called / Exam Phrasing |
|---|---|---|---|---|---|
| Flow Distribution | Amount of each type of work in the system over time (features, enablers, defects, risks); also distribution of funding across investment horizons | Teams, ARTs, Solution Trains, Portfolios | Count or size of each type of work item at a point in time; PI boundaries commonly used at ART level and above | Balances current and future velocity; too much feature work leaves no capacity for enablers/tech debt; too much tech debt leaves no capacity for customer value | Work type balance; investment horizon distribution |
| Flow Velocity | Number of backlog items completed in a given timeframe (throughput) | Teams, ARTs, Solution Trains, Portfolios | Count of completed work items (stories, features, capabilities, epics) or total story points per iteration or PI | Higher velocity = higher output and indicator process improvements are applied; stability over time is important; drops highlight problems | Throughput; increased productivity metric |
| Flow Time | Total elapsed time for all steps in a workflow from ideation to production | Teams, ARTs, Solution Trains, Portfolios | Average length of time to complete a particular type of work item; histogram/scatter plot visualization helps identify outliers and percentiles | Shorter flow time = less customer wait time = lower cost of delay | End-to-end lead time; cycle time; epic flow time |
| Flow Load | Number of items currently in the system (WIP) | Teams, ARTs, Solution Trains, Portfolios | Cumulative Flow Diagram (CFD) showing work quantity in each state, arrival curve, and departure curve; flow load = vertical distance between curves | Leading indicator of excess WIP; increasing flow load predicts increased future flow times; more frequent delivery lowers flow load | WIP indicator; active items count |
| Flow Efficiency | Proportion of flow time spent in value-added work activities vs. waiting between steps | Teams, ARTs, Solution Trains, Portfolios | Total active time ÷ flow time, expressed as percentage; requires Value Stream Mapping to identify workflow steps and delays | Typical unoptimized systems have single-digit efficiency; higher efficiency = faster value delivery; identifies bottlenecks | Active time ratio; value-added percentage; process efficiency |
| Flow Predictability | How well teams, ARTs, and Solution Trains plan and meet PI objectives | ARTs, Solution Trains | ART Predictability Measure: actual business value delivered in a PI ÷ planned business value | Low/erratic predictability makes commitments unrealistic; reliable trains operate at 80–100%; highlights technology, planning, or performance problems | ART Predictability Measure; PI predictability; delivery predictability |

### DevOps / CALMR Measurement Categories

| Measurement Category | What It Measures | Example Metrics | Source Framework | Also Called / Exam Phrasing |
|---|---|---|---|---|
| Pipeline Flow | Health and efficiency of the delivery pipeline itself | Flow velocity, flow efficiency, flow time, flow load, flow distribution, end-to-end lead time, deployment frequency | Flow Framework (Kersten); Google DORA | Pipeline performance; CDP health |
| Solution Quality | Adherence to functional, nonfunctional, security, and compliance requirements | Change failure rate, defect rates, automated test coverage, code coverage | Flow Framework (quality metrics); Google DORA | Quality metrics; shift-left quality |
| Solution Value | Business value of work exiting the pipeline | Economic outcomes, customer satisfaction, value vs. forecast, cost, happiness, MTTR | Flow Framework (business results); Google DORA | Business results; value metrics |

### Enterprise Portfolio Performance Metrics

| Metric Area | What It Measures | Examples | Also Called / Exam Phrasing |
|---|---|---|---|
| Strategic Theme Progress | Progress each portfolio makes toward strategic themes and enterprise portfolio strategic themes | OKR key result achievement; quarterly alignment review | Strategic theme KR tracking |
| Value Stream KPIs | How each value stream and its solutions perform | Revenue growth, profit growth, market share, customer satisfaction, employee engagement, product quality, returning customer rate, innovation rate, time to