# FP&A Executive Planning & Performance Model
This project is a corporate-style FP&A workflow built end-to-end on synthetic data — from raw budget-vs-actual records through a validated data pipeline, monthly P&L, department variance analysis, driver-based forecasting, scenario planning, headcount and cash modeling, an illustrative DCF, and an executive PDF report.
The model uses a fully synthetic dataset so it can be shared publicly without exposing confidential company information.

**[ View the full Executive Report (PDF)](outputs/FPA_Executive_Report.pdf)** &nbsp;|&nbsp; **[ Explore the Excel Model](excel/FPnA_Corporate_Planning_Model.xlsx)**

## Why this project

Leadership needs a repeatable monthly process to know whether the business is tracking to plan and where corrective action is required. This project builds that process: validate the data, produce a P&L, compare actuals to budget, flag material variances, identify drivers, forecast forward, stress-test with scenarios, and translate all of it into owned management actions.

## Business Questions Answered
- Are revenue, gross margin, OpEx, operating profit, and cash tracking to plan?
- Which departments and accounts are driving material variance?
- Which unfavorable variances require management escalation?
- How should the forecast change when revenue growth, COGS, payroll, software, or travel assumptions move?
- What is the FY2026 base, upside, and downside outlook?
- Is planned headcount financially supportable?
- Does the business maintain adequate liquidity?
- Can every executive KPI be traced to a documented definition and source?

## End-to-End FP&A Workflow
**Source Data → Validation → Monthly P&L → KPI Scorecard → Variance Analysis → Management Commentary → Forecast Bridge → Rolling Forecast → Scenario & Sensitivity Analysis → Headcount Plan → Cash Forecast → Executive Dashboard → Governance & Controls**

## Main Excel Deliverable
`excel/FPnA_Corporate_Planning_Model.xlsx`

## Core KPIs
- Revenue
- Gross Profit
- Gross Margin %
- Total OpEx
- Operating Profit
- Operating Margin %
- Budget vs Actual Variance $
- Budget vs Actual Variance %
- Department OpEx Variance %
- Material Variance Status
- FY2026 Forecast Revenue
- FY2026 Forecast Operating Profit
- Headcount / Payroll
- Free Cash Flow
- Ending Cash
- Liquidity Status

## Methodology

**Data grain:** one row per `Month × Department × Account` (420 rows, 12 months × 5 departments × 7 accounts).

**Validation rules** all enforced before anything is published:
- No duplicate grain combinations; no null Month/Department/Account
- Budget and Actual are numeric; Variance and Variance % are recalculated, never hand-entered
- All 12 fiscal months present for every department/account
- Only approved departments and accounts appear
- Revenue, COGS, and required OpEx categories present every month
- Dashboard totals reconcile to the Excel P&L

**Monthly close cadence** the project mirrors:
load & validate actuals → refresh P&L & rank variances → update forecast & assumptions → draft commentary & assign actions → publish & archive.

## Technical Stack
### Excel
Financial modeling, P&L reporting, assumptions, forecast logic, scenario planning, variance analysis, DCF, controls, and executive reporting.

### SQL
Corporate-style reporting schema plus KPI, variance, rolling-trend, and management reporting queries.

### Power BI / DAX
A deployment-ready BI handoff pack includes DAX measures, a date table, data-model specification, executive dashboard page blueprint, corporate theme, refresh checklist, and reconciliation process.

### Python
Validation and management-analysis scripts demonstrate how finance data could be checked and prepared before recurring reporting.

## Corporate Controls Demonstrated
- Source-to-model reconciliation
- Completeness checks
- Duplicate/null validation
- Material variance review
- Forecast assumption change log
- Dashboard-to-model tie-out
- Version control
- Access-review concept
- Monthly archive process

## Why This Project Is Job-Ready
This project demonstrates more than spreadsheet mechanics. It shows the full FP&A thought process:
1. Validate financial data.
2. Translate actuals into a structured P&L.
3. Explain plan vs actual performance.
4. Identify financial drivers and management risks.
5. Update the forward outlook.
6. Evaluate scenarios and sensitivities.
7. Link headcount and operating assumptions to the forecast.
8. Monitor liquidity.
9. Communicate actions to business partners and leadership.
10. Maintain traceability, controls, and version discipline.

## About this project

Built as a portfolio piece to demonstrate an end-to-end FP&A workflow — from raw data through executive decision support — the way a real finance function would run it monthly.

