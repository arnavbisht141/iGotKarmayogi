"""Demo course catalogue for the Official Statistical System learning platform.

Content is written for training demonstrations: facts reflect published frameworks
(SNA 2008, PLFS, IIP, DPDP Act 2023, UN Fundamental Principles), kept at an
introductory level. Instructors are institutional faculty, not named individuals.
"""

NSSTA = "National Statistical Systems Training Academy (NSSTA)"
NSO = "National Statistics Office (NSO), MoSPI"
ISTM = "Institute of Secretariat Training & Management (ISTM)"
MEITY = "Ministry of Electronics & Information Technology (MeitY)"


def lesson(title, points, question, options, answer, explanation, minutes=20):
    return {
        "title": title,
        "points": points,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "minutes": minutes,
    }


COURSES = [
    # ── Statistical ────────────────────────────────────────────────────────────
    {
        "title": "National Accounts Statistics & GDP Compilation",
        "category": "National Accounts",
        "difficulty": "advanced",
        "hours": 7.0,
        "organization": NSO,
        "instructor": "Faculty, National Accounts Division",
        "overview": "Compile GDP the way the National Statistics Office does: the SNA 2008 framework, the production, income and expenditure approaches, GVA at basic prices, base revisions, and the advance and provisional estimate calendar.",
        "skills": [("National Accounts Statistics & GDP Estimation", "Economic Statistics"), ("Supply and Use Tables", "Economic Statistics")],
        "modules": [
            {
                "title": "Module 1: The SNA 2008 Framework",
                "description": "Concepts, accounting identities and the three approaches to measuring GDP.",
                "lessons": [
                    lesson(
                        "Three approaches to measuring GDP",
                        [
                            "GDP can be measured by the production approach (sum of value added), the income approach (compensation of employees, operating surplus, mixed income) and the expenditure approach (final consumption, capital formation, net exports).",
                            "In principle all three approaches give the same total; differences in practice appear as statistical discrepancies.",
                            "India follows the System of National Accounts (SNA) 2008 recommended by the United Nations.",
                        ],
                        "Which approach measures GDP as the sum of final consumption, gross capital formation and net exports?",
                        ["Production approach", "Income approach", "Expenditure approach", "Value added approach"],
                        2,
                        "The expenditure approach sums final uses of output: consumption, investment and net exports.",
                    ),
                    lesson(
                        "GVA at basic prices and GDP",
                        [
                            "Gross Value Added (GVA) at basic prices measures output minus intermediate consumption, valued before product taxes.",
                            "GDP equals GVA at basic prices plus product taxes minus product subsidies.",
                            "Sector-wise GVA shows the contribution of agriculture, industry and services to growth.",
                        ],
                        "How is GDP derived from GVA at basic prices?",
                        [
                            "GVA plus product subsidies minus product taxes",
                            "GVA plus product taxes minus product subsidies",
                            "GVA minus depreciation",
                            "GVA plus net factor income from abroad",
                        ],
                        1,
                        "GDP = GVA at basic prices + product taxes - product subsidies.",
                    ),
                ],
            },
            {
                "title": "Module 2: Estimates, Revisions and Base Years",
                "description": "The release calendar and why base years are revised.",
                "lessons": [
                    lesson(
                        "The GDP release calendar",
                        [
                            "First Advance Estimates of annual GDP are released in early January, before the fiscal year ends.",
                            "Provisional Estimates follow at the end of May, alongside the fourth quarter estimate.",
                            "Estimates are revised as fuller data such as the Annual Survey of Industries becomes available.",
                        ],
                        "When are the Provisional Estimates of annual GDP released?",
                        ["Early January", "End of May", "Mid August", "December"],
                        1,
                        "Provisional Estimates are released at the end of May together with the Q4 estimate.",
                    ),
                    lesson(
                        "Why base years are revised",
                        [
                            "The current national accounts series uses 2011-12 as its base year.",
                            "Base revisions update the structure of the economy, new data sources and methodology.",
                            "Back-series are compiled so that growth rates remain comparable over time.",
                        ],
                        "What is the main reason for revising the base year of national accounts?",
                        [
                            "To make growth rates look higher",
                            "To reflect the changed structure of the economy and new data sources",
                            "To align with the calendar year",
                            "To reduce the number of sectors reported",
                        ],
                        1,
                        "Base revisions capture structural change in the economy and incorporate improved data and methods.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Periodic Labour Force Survey (PLFS): Concepts & Estimation",
        "category": "Sample Surveys",
        "difficulty": "intermediate",
        "hours": 5.5,
        "organization": NSO,
        "instructor": "Faculty, Survey Design & Research Division",
        "overview": "Understand how India measures employment: usual status and current weekly status, the key labour market indicators, and the rotational panel design used for quarterly urban estimates.",
        "skills": [("Labour Force Statistics", "Social Statistics"), ("Sample Survey Design & Sampling Techniques", "Statistical Methodology")],
        "modules": [
            {
                "title": "Module 1: Activity Status Concepts",
                "description": "Reference periods and how a person's activity status is determined.",
                "lessons": [
                    lesson(
                        "Usual status and current weekly status",
                        [
                            "Usual status uses a reference period of 365 days and combines principal status with subsidiary status (ps+ss).",
                            "Current weekly status (CWS) uses a reference period of the 7 days preceding the survey.",
                            "CWS captures short-term changes, which makes it suitable for quarterly estimates.",
                        ],
                        "What is the reference period for current weekly status in PLFS?",
                        ["365 days", "30 days", "7 days", "1 day"],
                        2,
                        "Current weekly status is determined for the 7 days preceding the date of survey.",
                    ),
                    lesson(
                        "Labour market indicators",
                        [
                            "Labour Force Participation Rate (LFPR) is the share of the population that is employed or seeking work.",
                            "Worker Population Ratio (WPR) is the share of the population that is employed.",
                            "Unemployment Rate (UR) is the share of the labour force that is unemployed.",
                        ],
                        "The unemployment rate is calculated as unemployed persons divided by which denominator?",
                        ["Total population", "Labour force", "Working-age population", "Employed persons"],
                        1,
                        "UR = unemployed persons / labour force, where the labour force is employed plus unemployed.",
                    ),
                ],
            },
            {
                "title": "Module 2: Survey Design",
                "description": "The rotational panel and the quarterly bulletin.",
                "lessons": [
                    lesson(
                        "The urban rotational panel",
                        [
                            "In urban areas PLFS follows a rotational panel: each selected household is visited four times, a first visit and three revisits.",
                            "Overlap between quarters improves the precision of estimates of change.",
                            "Rural households are visited once in the annual schedule.",
                        ],
                        "How many times is a selected urban household visited under the PLFS rotational panel?",
                        ["Once", "Twice", "Four times", "Every month for a year"],
                        2,
                        "Urban households receive a first visit followed by three revisits in successive quarters.",
                    ),
                    lesson(
                        "From sample to published estimate",
                        [
                            "Survey weights (multipliers) scale sample observations up to population totals.",
                            "Estimates for small domains carry wide sampling errors and should be interpreted with care.",
                            "Quarterly bulletins report urban indicators in current weekly status.",
                        ],
                        "Why should estimates for very small domains be interpreted cautiously?",
                        [
                            "They are always biased upwards",
                            "Their relative standard errors are large because few sample units fall in them",
                            "They exclude weights",
                            "They use a different questionnaire",
                        ],
                        1,
                        "Few sample observations in a small domain produce large sampling errors.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "SDG Indicators & the National Indicator Framework",
        "category": "Official Statistics",
        "difficulty": "intermediate",
        "hours": 4.5,
        "organization": NSO,
        "instructor": "Faculty, Social Statistics Division",
        "overview": "Monitor the Sustainable Development Goals with official statistics: the global indicator framework, India's National Indicator Framework, indicator metadata and data gaps.",
        "skills": [("SDG Indicator Monitoring", "Social Statistics"), ("Official Statistics Quality Framework (NQAF)", "Data Governance")],
        "modules": [
            {
                "title": "Module 1: Global and National Frameworks",
                "description": "How goals, targets and indicators fit together.",
                "lessons": [
                    lesson(
                        "Goals, targets and indicators",
                        [
                            "The 2030 Agenda has 17 Sustainable Development Goals and 169 targets.",
                            "Progress is tracked through a global indicator framework maintained by the UN Statistical Commission.",
                            "Each indicator has metadata describing its definition, computation method and data sources.",
                        ],
                        "How many Sustainable Development Goals are there in the 2030 Agenda?",
                        ["8", "15", "17", "169"],
                        2,
                        "There are 17 goals, supported by 169 targets.",
                    ),
                    lesson(
                        "India's National Indicator Framework",
                        [
                            "MoSPI developed the National Indicator Framework (NIF) to monitor SDG progress with national data.",
                            "NIF indicators draw on surveys, censuses and administrative records across ministries.",
                            "NIF progress reports give year-on-year trends for each goal.",
                        ],
                        "Which organisation developed India's National Indicator Framework for SDG monitoring?",
                        ["NITI Aayog", "Reserve Bank of India", "MoSPI", "Election Commission"],
                        2,
                        "The NIF was developed by the Ministry of Statistics and Programme Implementation.",
                    ),
                ],
            },
            {
                "title": "Module 2: Data Quality and Gaps",
                "description": "Disaggregation, administrative data and closing indicator gaps.",
                "lessons": [
                    lesson(
                        "Disaggregation: leave no one behind",
                        [
                            "SDG indicators should be disaggregated by sex, age, location, income and disability where relevant.",
                            "Disaggregation often needs larger samples or linked administrative data.",
                            "Aggregates can hide gaps that disaggregated data reveal.",
                        ],
                        "Why do SDG indicators emphasise disaggregation?",
                        [
                            "To reduce the reporting burden",
                            "To reveal inequalities that national averages hide",
                            "To avoid publishing national totals",
                            "To simplify metadata",
                        ],
                        1,
                        "Disaggregated data show which groups are being left behind, which averages conceal.",
                    ),
                    lesson(
                        "Using administrative data",
                        [
                            "Administrative records such as health or education management systems can fill survey gaps.",
                            "Coverage, definitions and timeliness must be assessed before use.",
                            "Documenting these checks in metadata supports trust in the indicator.",
                        ],
                        "What must be assessed before using administrative records for an SDG indicator?",
                        [
                            "Only the file format",
                            "Coverage, definitions and timeliness",
                            "The number of pages in the report",
                            "Nothing, administrative data are always complete",
                        ],
                        1,
                        "Administrative data need checks on coverage, concept alignment and timeliness before statistical use.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Index of Industrial Production (IIP) & Industrial Statistics",
        "category": "Official Statistics",
        "difficulty": "intermediate",
        "hours": 5.0,
        "organization": NSO,
        "instructor": "Faculty, Economic Statistics Division",
        "overview": "Compile and interpret the Index of Industrial Production: base year, sectoral and use-based classifications, weights, and the relationship with the Annual Survey of Industries.",
        "skills": [("Industrial Statistics & IIP", "Economic Statistics")],
        "modules": [
            {
                "title": "Module 1: Structure of the IIP",
                "description": "Classifications, base year and index formula.",
                "lessons": [
                    lesson(
                        "Sectoral and use-based classification",
                        [
                            "The IIP is published for three sectors: mining, manufacturing and electricity.",
                            "The use-based classification groups items into primary, capital, intermediate, infrastructure/construction, consumer durable and consumer non-durable goods.",
                            "The current series uses 2011-12 as its base year and is released monthly.",
                        ],
                        "Which three sectors make up the sectoral IIP?",
                        [
                            "Agriculture, industry and services",
                            "Mining, manufacturing and electricity",
                            "Construction, trade and transport",
                            "Public, private and household",
                        ],
                        1,
                        "The sectoral IIP covers mining, manufacturing and electricity.",
                    ),
                    lesson(
                        "The index formula",
                        [
                            "The IIP is a Laspeyres type fixed-base index.",
                            "Item weights reflect the relative importance of items in the base year.",
                            "A fixed base makes month-to-month comparisons consistent but ages as the economy changes.",
                        ],
                        "What type of index formula does the IIP use?",
                        ["Paasche", "Fisher", "Laspeyres fixed-base", "Chain-linked geometric"],
                        2,
                        "The IIP uses a Laspeyres fixed-base formula with base-year weights.",
                    ),
                ],
            },
            {
                "title": "Module 2: Annual Survey of Industries",
                "description": "Coverage and use of ASI data.",
                "lessons": [
                    lesson(
                        "ASI coverage",
                        [
                            "The Annual Survey of Industries covers factories registered under Sections 2m(i) and 2m(ii) of the Factories Act, 1948.",
                            "It provides detailed data on output, inputs, employment and capital.",
                            "ASI results are used to revise national accounts estimates for the manufacturing sector.",
                        ],
                        "Which units does the Annual Survey of Industries cover?",
                        [
                            "All households in India",
                            "Factories registered under the Factories Act, 1948",
                            "Only public sector undertakings",
                            "Agricultural cooperatives",
                        ],
                        1,
                        "ASI covers factories registered under Sections 2m(i) and 2m(ii) of the Factories Act, 1948.",
                    ),
                    lesson(
                        "Interpreting monthly IIP releases",
                        [
                            "Year-on-year growth compares a month with the same month of the previous year, removing seasonality.",
                            "Quick estimates are revised in later releases as more factories report.",
                            "Base effects can make growth rates swing when the previous year was unusually weak or strong.",
                        ],
                        "Why is year-on-year growth used for monthly IIP rather than month-on-month growth?",
                        [
                            "It removes seasonal patterns by comparing the same month",
                            "It needs fewer data",
                            "It is never revised",
                            "It ignores base effects",
                        ],
                        0,
                        "Comparing the same month across years neutralises seasonal variation.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Agricultural Statistics & Crop Estimation Surveys",
        "category": "Sample Surveys",
        "difficulty": "beginner",
        "hours": 4.0,
        "organization": NSSTA,
        "instructor": "Faculty, Field Operations Division",
        "overview": "Estimate crop area, yield and production with crop cutting experiments, land use classification and the agriculture census.",
        "skills": [("Agricultural Statistics", "Economic Statistics"), ("Sample Survey Design & Sampling Techniques", "Statistical Methodology")],
        "modules": [
            {
                "title": "Module 1: Area and Yield",
                "description": "How production estimates are built.",
                "lessons": [
                    lesson(
                        "Production equals area times yield",
                        [
                            "Crop production is estimated as area under the crop multiplied by average yield.",
                            "Area estimates come from land records and schemes such as the Timely Reporting Scheme.",
                            "Yield is estimated from crop cutting experiments under the General Crop Estimation Surveys.",
                        ],
                        "How is crop production estimated in official agricultural statistics?",
                        [
                            "Area multiplied by yield",
                            "Rainfall multiplied by area",
                            "Market arrivals only",
                            "Fertiliser sales divided by area",
                        ],
                        0,
                        "Production = area under the crop x average yield per unit area.",
                    ),
                    lesson(
                        "Crop cutting experiments",
                        [
                            "In a crop cutting experiment a plot of fixed size is randomly located in a selected field and harvested.",
                            "Random plot location avoids bias from choosing the best or worst part of a field.",
                            "Yields from many experiments are combined with survey weights.",
                        ],
                        "Why is the plot in a crop cutting experiment located randomly within the field?",
                        [
                            "To make harvesting faster",
                            "To avoid selection bias in the yield estimate",
                            "To reduce the plot size",
                            "Because farmers request it",
                        ],
                        1,
                        "Random location prevents the field worker from biasing yield towards unusually good or poor patches.",
                    ),
                ],
            },
            {
                "title": "Module 2: Structural Statistics",
                "description": "Land use and the agriculture census.",
                "lessons": [
                    lesson(
                        "Land use classification",
                        [
                            "Land use statistics classify reporting area into categories such as forests, net area sown and current fallows.",
                            "Consistent classification allows comparisons across states and years.",
                            "Changes in net area sown are an early signal of agricultural stress or expansion.",
                        ],
                        "What is the purpose of a standard land use classification?",
                        [
                            "To set crop prices",
                            "To allow consistent comparison of land use across states and years",
                            "To register land ownership",
                            "To forecast rainfall",
                        ],
                        1,
                        "A common classification makes land use data comparable across regions and time.",
                    ),
                    lesson(
                        "The agriculture census",
                        [
                            "The agriculture census is conducted every five years.",
                            "It collects structural data on the number and area of operational holdings.",
                            "Holding size classes inform policy for small and marginal farmers.",
                        ],
                        "How often is the agriculture census conducted?",
                        ["Every year", "Every three years", "Every five years", "Every ten years"],
                        2,
                        "The agriculture census follows a five-year cycle.",
                    ),
                ],
            },
        ],
    },
    # ── Technical ──────────────────────────────────────────────────────────────
    {
        "title": "SQL for Official Statistics Databases",
        "category": "Programming",
        "difficulty": "beginner",
        "hours": 5.0,
        "organization": NSSTA,
        "instructor": "Faculty, Data Processing Division",
        "overview": "Query unit-level survey and administrative databases confidently: filtering and aggregation, joins across files, window functions and query performance.",
        "skills": [("SQL for Statistical Databases", "Data Science")],
        "modules": [
            {
                "title": "Module 1: Querying Survey Tables",
                "description": "Selecting, filtering and aggregating records.",
                "lessons": [
                    lesson(
                        "Aggregation with GROUP BY",
                        [
                            "GROUP BY collapses rows into groups so aggregates like SUM and COUNT can be computed per group.",
                            "WHERE filters rows before grouping; HAVING filters groups after aggregation.",
                            "Weighted totals are computed as SUM(value * weight), not SUM(value).",
                        ],
                        "Which clause filters groups after aggregation?",
                        ["WHERE", "HAVING", "ORDER BY", "LIMIT"],
                        1,
                        "HAVING applies conditions to aggregated groups; WHERE filters individual rows before grouping.",
                    ),
                    lesson(
                        "Joining household and person files",
                        [
                            "Survey microdata are often split into household-level and person-level files linked by a household identifier.",
                            "An INNER JOIN keeps only matching records; a LEFT JOIN keeps all records from the left table.",
                            "Always check row counts before and after a join to catch duplicate keys.",
                        ],
                        "Which join keeps every household even if no matching person records exist?",
                        [
                            "INNER JOIN with households on the right",
                            "LEFT JOIN with households on the left",
                            "CROSS JOIN",
                            "SELF JOIN",
                        ],
                        1,
                        "A LEFT JOIN preserves all rows from the left table.",
                    ),
                ],
            },
            {
                "title": "Module 2: Analytical SQL",
                "description": "Window functions and performance.",
                "lessons": [
                    lesson(
                        "Window functions",
                        [
                            "Window functions compute values across related rows without collapsing them, for example running totals.",
                            "PARTITION BY defines the groups; ORDER BY defines the order within each group.",
                            "They are useful for ranking districts or computing month-on-month change.",
                        ],
                        "What distinguishes a window function from a GROUP BY aggregate?",
                        [
                            "It returns one row per group",
                            "It computes across related rows while keeping each row",
                            "It only works on text columns",
                            "It cannot use ORDER BY",
                        ],
                        1,
                        "Window functions keep the individual rows while adding calculations over a window of rows.",
                    ),
                    lesson(
                        "Query performance",
                        [
                            "Indexes speed up lookups on columns used in filters and joins.",
                            "Selecting only needed columns reduces data transferred.",
                            "EXPLAIN shows how the database plans to execute a query.",
                        ],
                        "What is the main benefit of an index on a column used in WHERE filters?",
                        [
                            "It compresses the table",
                            "It speeds up finding matching rows",
                            "It encrypts the column",
                            "It removes duplicates",
                        ],
                        1,
                        "Indexes let the database locate matching rows without scanning the whole table.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "R for Survey Data Analysis",
        "category": "Programming",
        "difficulty": "intermediate",
        "hours": 6.0,
        "organization": NSSTA,
        "instructor": "Faculty, Survey Design & Research Division",
        "overview": "Analyse complex survey data correctly in R: design objects with strata, clusters and weights, design-based estimates and variance estimation with replicate weights.",
        "skills": [("Python & R for Public Sector Data Analytics", "Data Science"), ("Sample Survey Design & Sampling Techniques", "Statistical Methodology")],
        "modules": [
            {
                "title": "Module 1: Survey Design Objects",
                "description": "Declaring the sampling design before estimation.",
                "lessons": [
                    lesson(
                        "Declaring a survey design",
                        [
                            "In the R survey package, svydesign() declares cluster identifiers, strata and weights.",
                            "All estimates are then computed from the design object rather than the raw data frame.",
                            "Ignoring clustering and stratification usually understates standard errors.",
                        ],
                        "What happens to standard errors if clustering in a survey design is ignored?",
                        [
                            "They are usually understated",
                            "They are always overstated",
                            "They are unaffected",
                            "They become zero",
                        ],
                        0,
                        "Clustered samples carry less independent information, so ignoring clustering understates variance.",
                    ),
                    lesson(
                        "Design-based estimates",
                        [
                            "svymean() and svytotal() compute weighted means and totals with design-based standard errors.",
                            "svyby() produces estimates for subgroups such as states or sectors.",
                            "Report the standard error or confidence interval with every estimate.",
                        ],
                        "Which function computes a weighted mean with a design-based standard error?",
                        ["mean()", "svymean()", "summary()", "lm()"],
                        1,
                        "svymean() uses the declared design to compute the estimate and its standard error.",
                    ),
                ],
            },
            {
                "title": "Module 2: Variance Estimation",
                "description": "Replicate weights and reporting uncertainty.",
                "lessons": [
                    lesson(
                        "Replicate weights",
                        [
                            "Replicate weight methods such as jackknife and bootstrap estimate variance by re-computing estimates on resampled weights.",
                            "They allow variance estimation for complex statistics without deriving formulas.",
                            "Some published microdata provide replicate weights instead of design variables to protect confidentiality.",
                        ],
                        "Why are replicate weights useful for variance estimation?",
                        [
                            "They remove the need for sampling weights",
                            "They estimate variance for complex statistics by re-computing on resampled weights",
                            "They increase the sample size",
                            "They eliminate non-response",
                        ],
                        1,
                        "Replicate methods approximate the sampling distribution by repeatedly re-estimating with perturbed weights.",
                    ),
                    lesson(
                        "Reporting uncertainty",
                        [
                            "A relative standard error (RSE) above a chosen threshold signals an unreliable estimate.",
                            "Confidence intervals communicate the plausible range of the population value.",
                            "Suppress or flag estimates that fail reliability rules.",
                        ],
                        "What does a high relative standard error indicate about an estimate?",
                        [
                            "It is highly precise",
                            "It is unreliable and should be flagged or suppressed",
                            "It is biased upwards",
                            "It was not weighted",
                        ],
                        1,
                        "A high RSE means the sampling error is large relative to the estimate.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "GIS & Geospatial Analysis for Statistics",
        "category": "Data Science",
        "difficulty": "intermediate",
        "hours": 5.5,
        "organization": NSSTA,
        "instructor": "Faculty, Data Informatics & Innovation Division",
        "overview": "Integrate geography with official statistics: vector and raster data, coordinate reference systems, spatial joins and responsible thematic mapping.",
        "skills": [("GIS & Geospatial Analysis", "Data Science")],
        "modules": [
            {
                "title": "Module 1: Spatial Data Fundamentals",
                "description": "Data models and coordinate systems.",
                "lessons": [
                    lesson(
                        "Vector and raster data",
                        [
                            "Vector data represent features as points, lines and polygons, such as villages, roads and district boundaries.",
                            "Raster data represent continuous surfaces as grids of cells, such as satellite imagery or night-time lights.",
                            "Choosing the right model depends on whether the phenomenon is discrete or continuous.",
                        ],
                        "Which data model is best suited to district boundaries?",
                        ["Raster", "Vector polygons", "Point cloud", "Time series"],
                        1,
                        "Administrative boundaries are discrete features represented as vector polygons.",
                    ),
                    lesson(
                        "Coordinate reference systems",
                        [
                            "A coordinate reference system (CRS) defines how coordinates map to locations on Earth.",
                            "GPS coordinates are commonly in WGS 84 (EPSG:4326).",
                            "Layers must share a CRS before spatial operations, or features will not align.",
                        ],
                        "What must be true before overlaying two spatial layers?",
                        [
                            "They must have the same file size",
                            "They must use the same coordinate reference system",
                            "They must be rasters",
                            "They must have the same colour scheme",
                        ],
                        1,
                        "Layers need a common CRS so that coordinates refer to the same locations.",
                    ),
                ],
            },
            {
                "title": "Module 2: Spatial Analysis and Mapping",
                "description": "Linking survey data to geography and mapping it honestly.",
                "lessons": [
                    lesson(
                        "Spatial joins",
                        [
                            "A spatial join attaches attributes based on location, for example assigning survey points to districts.",
                            "Point-in-polygon joins require clean, non-overlapping boundary polygons.",
                            "Always validate a sample of joined records against known locations.",
                        ],
                        "What does a point-in-polygon spatial join do?",
                        [
                            "Merges two tables on a shared ID column",
                            "Assigns each point the attributes of the polygon it falls within",
                            "Converts polygons to rasters",
                            "Removes points outside the map",
                        ],
                        1,
                        "Each point inherits attributes from the polygon that contains it.",
                    ),
                    lesson(
                        "Responsible choropleth maps",
                        [
                            "Choropleth maps should show rates or ratios, not raw counts, because large areas dominate raw totals.",
                            "Classification method and number of classes change the visual story.",
                            "Include a legend, data source and reference period on every map.",
                        ],
                        "Why should choropleth maps usually show rates rather than raw counts?",
                        [
                            "Rates are easier to compute",
                            "Raw counts mostly reflect population or area size, not intensity",
                            "Counts cannot be mapped",
                            "Rates remove the need for a legend",
                        ],
                        1,
                        "Normalising by population or area reveals intensity instead of size.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Machine Learning for Official Statistics",
        "category": "AI/ML",
        "difficulty": "advanced",
        "hours": 8.0,
        "organization": NSSTA,
        "instructor": "Faculty, Data Informatics & Innovation Division",
        "overview": "Apply machine learning responsibly in statistical production: automated coding to NIC and NCO classifications, validation without leakage, nowcasting with alternative data, and fairness.",
        "skills": [("Machine Learning for Statistics", "Data Science")],
        "modules": [
            {
                "title": "Module 1: Automated Classification",
                "description": "Coding free-text survey responses at scale.",
                "lessons": [
                    lesson(
                        "Coding industry and occupation text",
                        [
                            "Survey respondents describe their work in free text that must be coded to classifications such as NIC (industry) and NCO (occupation).",
                            "Supervised text classifiers trained on previously coded records can suggest codes automatically.",
                            "Low-confidence predictions should be routed to expert coders for review.",
                        ],
                        "How should low-confidence predictions from an automated coding model be handled?",
                        [
                            "Accepted automatically",
                            "Routed to expert coders for review",
                            "Deleted from the dataset",
                            "Assigned a random code",
                        ],
                        1,
                        "A human-in-the-loop review of uncertain cases protects classification quality.",
                    ),
                    lesson(
                        "Validation without leakage",
                        [
                            "Split data into training, validation and test sets before any model fitting.",
                            "Data leakage occurs when information from the test set influences training, inflating accuracy.",
                            "Report performance per class, not only overall accuracy, because rare codes matter.",
                        ],
                        "What is data leakage in model validation?",
                        [
                            "Losing data during a file transfer",
                            "Information from the test set influencing training and inflating measured accuracy",
                            "Using too few features",
                            "Training for too many epochs",
                        ],
                        1,
                        "Leakage makes a model look better than it will perform on genuinely new data.",
                    ),
                ],
            },
            {
                "title": "Module 2: Nowcasting and Responsible AI",
                "description": "Alternative data and fairness.",
                "lessons": [
                    lesson(
                        "Nowcasting with alternative data",
                        [
                            "Nowcasting estimates the current state of an indicator before official data are released.",
                            "Alternative sources such as satellite night-time lights or digital payment volumes can act as timely proxies.",
                            "Nowcasts must be benchmarked against official releases and clearly labelled as experimental.",
                        ],
                        "How should nowcasts built from alternative data be presented?",
                        [
                            "As final official statistics",
                            "As experimental estimates benchmarked against official releases",
                            "Without any description of the method",
                            "Only in internal files",
                        ],
                        1,
                        "Transparency about their experimental nature maintains trust in official statistics.",
                    ),
                    lesson(
                        "Fairness and explainability",
                        [
                            "Models can reproduce biases present in historical training data.",
                            "Check error rates across groups such as regions or sex before deployment.",
                            "Document features, training data and limitations so results can be explained.",
                        ],
                        "What should be checked before deploying a model used in statistical production?",
                        [
                            "Only overall accuracy",
                            "Error rates across relevant groups, plus documented limitations",
                            "The colour of the dashboard",
                            "Nothing, models are neutral",
                        ],
                        1,
                        "Group-wise error analysis and documentation guard against hidden bias.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Cloud Computing & Data Engineering on Government Cloud",
        "category": "Cloud Computing",
        "difficulty": "intermediate",
        "hours": 6.0,
        "organization": MEITY,
        "instructor": "Faculty, National e-Governance Division",
        "overview": "Build reliable statistical data pipelines on government cloud: service models, the MeghRaj initiative, the shared responsibility model, and ETL design.",
        "skills": [("Government Cloud Architecture & MeghRaj Strategy", "Cloud Computing"), ("Data Engineering & ETL Pipelines", "Data Science")],
        "modules": [
            {
                "title": "Module 1: Cloud Foundations",
                "description": "Service models and government cloud policy.",
                "lessons": [
                    lesson(
                        "IaaS, PaaS and SaaS",
                        [
                            "Infrastructure as a Service provides virtual machines and storage; the user manages the operating system and applications.",
                            "Platform as a Service provides a managed runtime; the user manages only the application and data.",
                            "Software as a Service provides a complete application used over the internet.",
                        ],
                        "In which service model does the user manage the operating system?",
                        ["SaaS", "PaaS", "IaaS", "None of them"],
                        2,
                        "With IaaS the provider supplies infrastructure while the user manages the OS and above.",
                    ),
                    lesson(
                        "MeghRaj and the shared responsibility model",
                        [
                            "MeghRaj (GI Cloud) is the Government of India initiative led by MeitY to accelerate cloud adoption.",
                            "Government departments procure services from empanelled cloud service providers.",
                            "Under the shared responsibility model, the provider secures the cloud platform while the department secures its data, identities and configuration.",
                        ],
                        "Under the shared responsibility model, who is responsible for securing a department's data and access permissions?",
                        ["The cloud provider alone", "The department", "No one", "The internet service provider"],
                        1,
                        "Customers remain responsible for their data, identities and configurations.",
                    ),
                ],
            },
            {
                "title": "Module 2: Data Pipelines",
                "description": "Designing ETL for statistical production.",
                "lessons": [
                    lesson(
                        "Extract, transform, load",
                        [
                            "ETL pipelines extract raw data, transform it through validation and derivation, and load it into analysis-ready stores.",
                            "Each step should be automated, logged and repeatable.",
                            "Keep raw data immutable so any transformation can be re-run.",
                        ],
                        "Why should raw input data be kept immutable in a pipeline?",
                        [
                            "To save storage",
                            "So transformations can be audited and re-run from the original data",
                            "Because cloud storage cannot be edited",
                            "To speed up loading",
                        ],
                        1,
                        "Immutable raw data allow reproducible reprocessing and audit.",
                    ),
                    lesson(
                        "Validation checks",
                        [
                            "Automated checks catch missing values, out-of-range codes and duplicate records early.",
                            "Failed checks should stop the pipeline or quarantine records, not pass silently.",
                            "Validation rules belong in version control alongside the pipeline code.",
                        ],
                        "What should happen when a pipeline validation check fails?",
                        [
                            "Nothing, continue loading",
                            "Stop the pipeline or quarantine the failing records",
                            "Delete the entire dataset",
                            "Email the raw file publicly",
                        ],
                        1,
                        "Failures must be surfaced so bad data never reach published outputs.",
                    ),
                ],
            },
        ],
    },
    # ── Digital governance ─────────────────────────────────────────────────────
    {
        "title": "Data Privacy & the DPDP Act, 2023 for Statistical Offices",
        "category": "Data Governance",
        "difficulty": "intermediate",
        "hours": 4.5,
        "organization": MEITY,
        "instructor": "Faculty, Data Governance Programme",
        "overview": "Handle personal data lawfully and release statistics safely: the Digital Personal Data Protection Act, 2023, statutory confidentiality, and statistical disclosure control.",
        "skills": [("Data Privacy Compliance & DPDP Act 2023", "Data Governance"), ("Statistical Disclosure Control", "Data Governance")],
        "modules": [
            {
                "title": "Module 1: The DPDP Act, 2023",
                "description": "Roles, consent and obligations.",
                "lessons": [
                    lesson(
                        "Data Principals and Data Fiduciaries",
                        [
                            "Under the Digital Personal Data Protection Act, 2023, the individual is the Data Principal.",
                            "The entity that determines the purpose and means of processing is the Data Fiduciary.",
                            "Data Fiduciaries must protect personal data with reasonable security safeguards.",
                        ],
                        "Under the DPDP Act, 2023, what is the person to whom the personal data relate called?",
                        ["Data Fiduciary", "Data Processor", "Data Principal", "Consent Manager"],
                        2,
                        "The individual is the Data Principal; the entity deciding purposes is the Data Fiduciary.",
                    ),
                    lesson(
                        "Consent and purpose",
                        [
                            "Consent must be free, specific, informed, unconditional and unambiguous.",
                            "Personal data should be processed only for the purpose for which they were collected.",
                            "The Data Protection Board of India adjudicates non-compliance.",
                        ],
                        "Which body adjudicates non-compliance under the DPDP Act, 2023?",
                        [
                            "The Data Protection Board of India",
                            "CERT-In",
                            "The Election Commission",
                            "The Comptroller and Auditor General",
                        ],
                        0,
                        "The Act establishes the Data Protection Board of India.",
                    ),
                ],
            },
            {
                "title": "Module 2: Confidentiality in Statistical Releases",
                "description": "Protecting respondents in published data.",
                "lessons": [
                    lesson(
                        "Statutory confidentiality",
                        [
                            "The Collection of Statistics Act, 2008 protects information collected for statistical purposes.",
                            "Individual returns must not be disclosed in a form that identifies respondents.",
                            "Confidentiality is a precondition for truthful responses.",
                        ],
                        "Why is respondent confidentiality essential for official statistics?",
                        [
                            "It reduces printing costs",
                            "Respondents give truthful information only when they trust it will not be disclosed",
                            "It is optional",
                            "It speeds up tabulation",
                        ],
                        1,
                        "Trust in confidentiality underpins response rates and data quality.",
                    ),
                    lesson(
                        "Statistical disclosure control",
                        [
                            "Disclosure control techniques include suppressing small cells, coarsening categories and adding noise.",
                            "k-anonymity requires each record to be indistinguishable from at least k-1 others on identifying variables.",
                            "Anonymised microdata still need a disclosure risk assessment before release.",
                        ],
                        "What does k-anonymity require?",
                        [
                            "Every record has a unique identifier",
                            "Each record is indistinguishable from at least k-1 others on identifying variables",
                            "Data are encrypted with k keys",
                            "Only k records are released",
                        ],
                        1,
                        "k-anonymity makes each record blend into a group of at least k records.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Digital Signatures, eSign & PKI in Government Workflows",
        "category": "Digital Governance",
        "difficulty": "beginner",
        "hours": 3.5,
        "organization": MEITY,
        "instructor": "Faculty, National e-Governance Division",
        "overview": "Use digital signatures with confidence: public key infrastructure, the legal basis under the IT Act, 2000, digital signature certificates and Aadhaar-based eSign.",
        "skills": [("Public Key Infrastructure (PKI) & Digital Signatures", "Digital Governance")],
        "modules": [
            {
                "title": "Module 1: How Digital Signatures Work",
                "description": "Keys, hashes and certificates.",
                "lessons": [
                    lesson(
                        "Public and private keys",
                        [
                            "A digital signature is created with the signer's private key and verified with the corresponding public key.",
                            "The document is first hashed; any change to the document changes the hash and breaks the signature.",
                            "The private key must never be shared.",
                        ],
                        "Which key is used to create a digital signature?",
                        ["The verifier's public key", "The signer's private key", "A shared password", "The certificate authority's public key"],
                        1,
                        "Signatures are created with the private key and verified with the public key.",
                    ),
                    lesson(
                        "Certificates and trust",
                        [
                            "A digital signature certificate binds a public key to the identity of its holder.",
                            "Certifying Authorities are licensed by the Controller of Certifying Authorities (CCA).",
                            "The IT Act, 2000 gives legal recognition to electronic signatures.",
                        ],
                        "Who licenses Certifying Authorities in India?",
                        ["CERT-In", "The Controller of Certifying Authorities", "The Reserve Bank of India", "UIDAI"],
                        1,
                        "The CCA licenses and regulates Certifying Authorities under the IT Act, 2000.",
                    ),
                ],
            },
            {
                "title": "Module 2: eSign in Practice",
                "description": "Signing government documents online.",
                "lessons": [
                    lesson(
                        "Aadhaar-based eSign",
                        [
                            "eSign is an online electronic signature service that uses Aadhaar e-KYC to authenticate the signer.",
                            "It removes the need for a physical token holding a digital signature certificate.",
                            "The signed document can be verified by any recipient.",
                        ],
                        "What does eSign use to authenticate the signer?",
                        ["A USB token only", "Aadhaar e-KYC", "A handwritten signature scan", "An email link"],
                        1,
                        "eSign authenticates signers through Aadhaar-based e-KYC.",
                    ),
                    lesson(
                        "Verifying signed documents",
                        [
                            "Verification checks that the document is unchanged and the certificate is valid and not revoked.",
                            "A broken signature indicates tampering or a changed file.",
                            "Keep an audit trail of signing events for accountability.",
                        ],
                        "What does a failed signature verification most likely indicate?",
                        [
                            "The document was modified after signing or the certificate is invalid",
                            "The printer is offline",
                            "The file is too large",
                            "The signer used a strong password",
                        ],
                        0,
                        "Verification fails when content changes or the certificate is not valid.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Cybersecurity Essentials for Government Data Systems",
        "category": "Cybersecurity",
        "difficulty": "beginner",
        "hours": 4.0,
        "organization": "Indian Computer Emergency Response Team (CERT-In)",
        "instructor": "Faculty, Cyber Security Awareness Programme",
        "overview": "Protect statistical systems and data from everyday threats: phishing, access control, backups and incident reporting obligations.",
        "skills": [("Critical Infrastructure Cyber Defense & CERT-In Compliance", "Cybersecurity")],
        "modules": [
            {
                "title": "Module 1: Everyday Threats",
                "description": "Phishing and access control.",
                "lessons": [
                    lesson(
                        "Recognising phishing",
                        [
                            "Phishing messages create urgency and ask you to click links, open attachments or share credentials.",
                            "Check the sender's actual address and hover over links before clicking.",
                            "Report suspicious messages rather than deleting them silently.",
                        ],
                        "What is the safest response to a suspicious email asking you to reset your password urgently?",
                        [
                            "Click the link quickly",
                            "Reply with your password",
                            "Report it and reset the password only through the official portal",
                            "Forward it to colleagues",
                        ],
                        2,
                        "Report the message and use known official channels instead of links in the email.",
                    ),
                    lesson(
                        "Least privilege and multi-factor authentication",
                        [
                            "Least privilege gives each user only the access needed for their role.",
                            "Multi-factor authentication blocks most attacks that rely on stolen passwords.",
                            "Review and remove access promptly when roles change.",
                        ],
                        "What does the principle of least privilege mean?",
                        [
                            "Everyone gets administrator access",
                            "Users get only the access their role requires",
                            "Passwords are never changed",
                            "Only senior officers use computers",
                        ],
                        1,
                        "Limiting access reduces the damage from mistakes and compromised accounts.",
                    ),
                ],
            },
            {
                "title": "Module 2: Resilience and Reporting",
                "description": "Backups and incident response.",
                "lessons": [
                    lesson(
                        "The 3-2-1 backup rule",
                        [
                            "Keep 3 copies of important data, on 2 different types of media, with 1 copy offsite or offline.",
                            "Offline backups protect against ransomware that encrypts connected storage.",
                            "Test restoring from backups regularly.",
                        ],
                        "Why should one backup copy be kept offline or offsite?",
                        [
                            "It is cheaper",
                            "It survives ransomware or disasters that affect connected systems",
                            "It is faster to access",
                            "It is legally required for all files",
                        ],
                        1,
                        "An isolated copy stays safe when connected systems are compromised.",
                    ),
                    lesson(
                        "Reporting cyber incidents",
                        [
                            "CERT-In directions of April 2022 require specified cyber incidents to be reported within 6 hours of noticing them.",
                            "Preserve logs and evidence; do not wipe affected systems before investigation.",
                            "Follow your organisation's incident response plan and escalation contacts.",
                        ],
                        "Within how many hours must specified cyber incidents be reported to CERT-In under its April 2022 directions?",
                        ["6 hours", "24 hours", "72 hours", "7 days"],
                        0,
                        "The CERT-In directions require reporting within 6 hours of noticing the incident.",
                    ),
                ],
            },
        ],
    },
    # ── Behavioural & managerial ───────────────────────────────────────────────
    {
        "title": "Leadership for Statistical Teams",
        "category": "Leadership",
        "difficulty": "intermediate",
        "hours": 4.0,
        "organization": ISTM,
        "instructor": "Faculty, Leadership Development Programme",
        "overview": "Lead survey and analysis teams through complex, deadline-driven work: adapting leadership style, delegation, feedback and building accountability.",
        "skills": [("Team Leadership", "Leadership")],
        "modules": [
            {
                "title": "Module 1: Leadership Styles",
                "description": "Adapting to people and situations.",
                "lessons": [
                    lesson(
                        "Situational leadership",
                        [
                            "Situational leadership adapts the balance of direction and support to each person's competence and commitment.",
                            "A new enumerator may need clear direction; an experienced supervisor benefits from delegation.",
                            "Using one style for everyone leaves some team members over-managed and others unsupported.",
                        ],
                        "According to situational leadership, how should you lead a highly experienced and committed team member?",
                        ["With close step-by-step direction", "By delegating responsibility", "By ignoring them", "With frequent public criticism"],
                        1,
                        "Competent and committed people perform best with delegation.",
                    ),
                    lesson(
                        "Effective delegation",
                        [
                            "Delegate the outcome and the authority, not just the task.",
                            "Agree on checkpoints rather than supervising every step.",
                            "Delegation develops people and frees leaders for decisions only they can take.",
                        ],
                        "What should accompany a delegated task for delegation to work?",
                        ["Only a deadline", "The authority and resources needed to deliver it", "A written warning", "Nothing else"],
                        1,
                        "People need authority and resources proportionate to the responsibility delegated.",
                    ),
                ],
            },
            {
                "title": "Module 2: Feedback and Accountability",
                "description": "Building a high-performing culture.",
                "lessons": [
                    lesson(
                        "Giving useful feedback",
                        [
                            "Useful feedback describes specific behaviour and its impact, not personality.",
                            "Timely feedback is easier to act on than feedback saved for annual appraisals.",
                            "Invite the other person's view to make feedback a conversation.",
                        ],
                        "Which feedback is most useful?",
                        [
                            "You are careless",
                            "The district table had 12 unchecked outliers, which delayed release by two days",
                            "Do better next time",
                            "Everyone thinks your work is poor",
                        ],
                        1,
                        "Specific behaviour and impact make feedback actionable.",
                    ),
                    lesson(
                        "Accountability without blame",
                        [
                            "Clear roles, for example using a RACI chart, show who is responsible, accountable, consulted and informed.",
                            "When errors occur, examine the process first to prevent recurrence.",
                            "Psychological safety encourages early reporting of problems.",
                        ],
                        "In a RACI chart, what does the A stand for?",
                        ["Assisted", "Accountable", "Approved", "Assigned"],
                        1,
                        "RACI stands for Responsible, Accountable, Consulted and Informed.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Communicating Statistics to Policymakers and the Public",
        "category": "Management",
        "difficulty": "beginner",
        "hours": 3.5,
        "organization": NSSTA,
        "instructor": "Faculty, Coordination & Publication Division",
        "overview": "Turn statistical results into clear messages: leading with the key finding, explaining uncertainty, writing press releases and briefing senior decision makers.",
        "skills": [("Statistical Communication", "Leadership")],
        "modules": [
            {
                "title": "Module 1: Clear Messages",
                "description": "Structuring what you say.",
                "lessons": [
                    lesson(
                        "Lead with the key finding",
                        [
                            "Busy decision makers read the first line; state the main finding there.",
                            "Support the headline with two or three pieces of evidence.",
                            "Move technical detail to annexes or metadata.",
                        ],
                        "Where should the main finding appear in a policy brief?",
                        ["In the final annex", "In the first line", "In a footnote", "Only in the tables"],
                        1,
                        "Leading with the conclusion ensures the key message is read.",
                    ),
                    lesson(
                        "Explaining uncertainty",
                        [
                            "Report ranges or margins of error alongside point estimates.",
                            "Explain in plain language what a revision or confidence interval means.",
                            "Avoid overstating small differences that are within sampling error.",
                        ],
                        "How should a change that lies within the margin of error be described?",
                        [
                            "As a significant increase",
                            "As not statistically distinguishable from no change",
                            "As a record high",
                            "It should be hidden",
                        ],
                        1,
                        "Differences within sampling error are not evidence of a real change.",
                    ),
                ],
            },
            {
                "title": "Module 2: Releases and Briefings",
                "description": "Press releases and senior briefings.",
                "lessons": [
                    lesson(
                        "Writing a statistical press release",
                        [
                            "State what was measured, the reference period and the headline number in the opening paragraph.",
                            "Use pre-announced release calendars so all users get data at the same time.",
                            "Link to methodology and metadata for users who need detail.",
                        ],
                        "Why do statistical offices publish pre-announced release calendars?",
                        [
                            "To give selected users early access",
                            "To ensure equal and simultaneous access to data for all users",
                            "To delay releases",
                            "To avoid publishing methodology",
                        ],
                        1,
                        "Advance calendars support impartiality and equal access.",
                    ),
                    lesson(
                        "Briefing senior officials",
                        [
                            "Prepare a one-page note with the finding, why it matters and the options.",
                            "Anticipate likely questions and have the supporting numbers ready.",
                            "Be clear about what the data can and cannot support.",
                        ],
                        "What should a one-page briefing note for a senior official contain?",
                        [
                            "All raw tables",
                            "The finding, why it matters, and the options",
                            "Only the methodology",
                            "A list of staff involved",
                        ],
                        1,
                        "Decision makers need the message, its significance and the choices available.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Project Management for Large-Scale Surveys",
        "category": "Management",
        "difficulty": "intermediate",
        "hours": 5.0,
        "organization": ISTM,
        "instructor": "Faculty, Programme Management Division",
        "overview": "Deliver national surveys on time and on budget: scope and work breakdown structures, scheduling and the critical path, risk registers and monitoring field progress.",
        "skills": [("Project Management", "Leadership")],
        "modules": [
            {
                "title": "Module 1: Planning",
                "description": "Scope, work breakdown and schedule.",
                "lessons": [
                    lesson(
                        "Work breakdown structure",
                        [
                            "A work breakdown structure (WBS) decomposes the project into deliverables and work packages.",
                            "Each work package should have an owner, an estimate and a completion criterion.",
                            "A good WBS covers 100 percent of the scope and nothing outside it.",
                        ],
                        "What is the purpose of a work breakdown structure?",
                        [
                            "To list staff salaries",
                            "To decompose the project scope into manageable deliverables and work packages",
                            "To replace the budget",
                            "To record meeting minutes",
                        ],
                        1,
                        "The WBS breaks the full scope into manageable, assignable pieces.",
                    ),
                    lesson(
                        "The critical path",
                        [
                            "The critical path is the longest sequence of dependent activities; it determines the earliest finish date.",
                            "Any delay to a critical path activity delays the whole project.",
                            "Activities off the critical path have float that absorbs small delays.",
                        ],
                        "What happens if an activity on the critical path is delayed?",
                        [
                            "Nothing changes",
                            "The overall project completion is delayed",
                            "Only that activity's budget changes",
                            "Float increases",
                        ],
                        1,
                        "Critical path activities have zero float, so delays push out the end date.",
                    ),
                ],
            },
            {
                "title": "Module 2: Execution and Control",
                "description": "Risks and field monitoring.",
                "lessons": [
                    lesson(
                        "Managing risk",
                        [
                            "A risk register records each risk's likelihood, impact, owner and response.",
                            "Common survey risks include delayed enumerator recruitment, device failures and non-response.",
                            "Review the register at every progress meeting.",
                        ],
                        "What should a risk register record for each risk?",
                        [
                            "Only the risk title",
                            "Likelihood, impact, owner and planned response",
                            "The names of respondents",
                            "The survey questionnaire",
                        ],
                        1,
                        "Owners and responses turn a list of risks into a management tool.",
                    ),
                    lesson(
                        "Monitoring field progress",
                        [
                            "Track completed units against the plan daily using dashboards from data collection devices.",
                            "Monitor quality indicators such as interview duration and item non-response, not just counts.",
                            "Act early on lagging districts rather than waiting for the end of the round.",
                        ],
                        "Which indicator helps detect poor-quality interviews during fieldwork?",
                        [
                            "Number of vehicles used",
                            "Unusually short interview durations",
                            "Office electricity bills",
                            "Number of meetings held",
                        ],
                        1,
                        "Very short interviews can signal skipped questions or fabricated data.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Ethics, Integrity & Professional Independence in Official Statistics",
        "category": "Public Administration",
        "difficulty": "beginner",
        "hours": 3.0,
        "organization": NSSTA,
        "instructor": "Faculty, Coordination & Publication Division",
        "overview": "Apply the UN Fundamental Principles of Official Statistics in daily work: professional independence, impartiality, confidentiality and handling pressure on results.",
        "skills": [("Administrative Law & Official Procedures", "Civil Service Ethics"), ("Professional Ethics in Statistics", "Civil Service Ethics")],
        "modules": [
            {
                "title": "Module 1: The Fundamental Principles",
                "description": "The international standard for trustworthy statistics.",
                "lessons": [
                    lesson(
                        "UN Fundamental Principles of Official Statistics",
                        [
                            "The United Nations Fundamental Principles of Official Statistics set out 10 principles for trustworthy statistics.",
                            "They were endorsed by the UN General Assembly in 2014.",
                            "They cover relevance, impartiality, professional standards, confidentiality and international cooperation.",
                        ],
                        "How many UN Fundamental Principles of Official Statistics are there?",
                        ["5", "7", "10", "17"],
                        2,
                        "There are 10 Fundamental Principles.",
                    ),
                    lesson(
                        "Professional independence",
                        [
                            "Methods, timing and content of statistical releases should be decided on professional grounds.",
                            "Statistics must be released regardless of whether results are politically welcome.",
                            "Independence is what gives users confidence in the numbers.",
                        ],
                        "On what basis should the timing and content of a statistical release be decided?",
                        [
                            "Political convenience",
                            "Professional and scientific considerations",
                            "Media demand",
                            "The preferences of the largest user",
                        ],
                        1,
                        "Professional independence means decisions rest on statistical grounds alone.",
                    ),
                ],
            },
            {
                "title": "Module 2: Integrity in Practice",
                "description": "Handling pressure and conflicts of interest.",
                "lessons": [
                    lesson(
                        "Responding to pressure on results",
                        [
                            "If asked to alter or delay results without statistical justification, document the request.",
                            "Escalate through the proper channels described in your organisation's code of conduct.",
                            "Explain the methodological basis of the results calmly and transparently.",
                        ],
                        "What is the appropriate response to a request to change results without statistical justification?",
                        [
                            "Comply quietly",
                            "Document the request and escalate through proper channels",
                            "Publish unofficial results online",
                            "Delete the data",
                        ],
                        1,
                        "Documentation and escalation protect both the officer and the integrity of statistics.",
                    ),
                    lesson(
                        "Conflicts of interest",
                        [
                            "A conflict of interest arises when personal interests could influence official duties.",
                            "Declare potential conflicts early and step back from related decisions.",
                            "Pre-release access to market-sensitive data must be tightly restricted.",
                        ],
                        "Why is pre-release access to market-sensitive statistics restricted?",
                        [
                            "To make releases slower",
                            "To prevent anyone gaining unfair advantage before public release",
                            "Because the data are always wrong",
                            "To reduce printing",
                        ],
                        1,
                        "Restricting early access protects fairness and trust.",
                    ),
                ],
            },
        ],
    },
    {
        "title": "Change Management & Decision Making in Public Organisations",
        "category": "Leadership",
        "difficulty": "advanced",
        "hours": 4.5,
        "organization": ISTM,
        "instructor": "Faculty, Leadership Development Programme",
        "overview": "Lead modernisation of statistical systems: structured decision making under uncertainty, stakeholder engagement and managing organisational change.",
        "skills": [("Change Management", "Leadership"), ("Evidence-Based Decision Making", "Leadership")],
        "modules": [
            {
                "title": "Module 1: Decision Making",
                "description": "Making sound decisions with incomplete information.",
                "lessons": [
                    lesson(
                        "Structured decision making",
                        [
                            "Define the decision, the objectives and the options before evaluating evidence.",
                            "Compare options against explicit criteria such as cost, quality and timeliness.",
                            "Record the rationale so the decision can be reviewed later.",
                        ],
                        "What should be defined before evaluating the options in a structured decision?",
                        [
                            "The preferred answer",
                            "The decision, objectives and evaluation criteria",
                            "The press release",
                            "Nothing",
                        ],
                        1,
                        "Clear objectives and criteria keep the evaluation of options fair.",
                    ),
                    lesson(
                        "Cognitive biases",
                        [
                            "Confirmation bias leads people to favour evidence that supports what they already believe.",
                            "Seeking disconfirming evidence and independent review reduces bias.",
                            "Pre-mortems ask what could make a decision fail before it is taken.",
                        ],
                        "What is confirmation bias?",
                        [
                            "Favouring evidence that supports existing beliefs",
                            "Confirming every meeting in writing",
                            "Double-checking calculations",
                            "Asking for a second opinion",
                        ],
                        0,
                        "Confirmation bias is the tendency to seek and favour supporting evidence.",
                    ),
                ],
            },
            {
                "title": "Module 2: Leading Change",
                "description": "Bringing people through modernisation.",
                "lessons": [
                    lesson(
                        "Creating urgency and a vision",
                        [
                            "Kotter's model of change begins by creating a sense of urgency.",
                            "A clear vision explains why the change matters, for example faster and more granular statistics.",
                            "Early visible wins build momentum.",
                        ],
                        "According to Kotter's model, what is the first step in leading change?",
                        ["Celebrating wins", "Creating a sense of urgency", "Anchoring change in culture", "Hiring consultants"],
                        1,
                        "Kotter's eight-step model starts with establishing urgency.",
                    ),
                    lesson(
                        "Engaging stakeholders",
                        [
                            "Map stakeholders by their influence and how much the change affects them.",
                            "Involve field staff early when changing data collection methods.",
                            "Address resistance by listening to concerns, not only by issuing instructions.",
                        ],
                        "What is an effective way to reduce resistance to a new data collection method?",
                        [
                            "Announce it without consultation",
                            "Involve field staff early and listen to their concerns",
                            "Penalise all objections",
                            "Keep it secret until launch",
                        ],
                        1,
                        "Early involvement surfaces practical issues and builds ownership.",
                    ),
                ],
            },
        ],
    },
]


FIRST_NAMES = [
    "Aarav", "Ananya", "Arjun", "Bhavna", "Chirag", "Deepika", "Farhan", "Gayatri", "Harsh",
    "Ishita", "Jyoti", "Karan", "Lakshmi", "Manoj", "Neha", "Omkar", "Pooja", "Rahul",
    "Sanjana", "Tarun", "Uma", "Vikram", "Yamini", "Zoya", "Abhishek", "Divya", "Gaurav",
    "Kavya", "Nikhil", "Ritu", "Siddharth", "Swati", "Varun", "Meera", "Rohan", "Shreya",
]

SURNAMES = [
    "Sharma", "Iyer", "Nair", "Reddy", "Singh", "Das", "Menon", "Patel", "Kulkarni", "Banerjee",
    "Rao", "Joshi", "Mehta", "Chatterjee", "Pillai", "Gupta", "Verma", "Mishra", "Bose", "Naidu",
]

# name, job role, domain affinity (added to base level, 0-5 scale)
DIVISIONS = [
    ("Field Operations Division (FOD), NSO", "Field survey supervision and data collection quality", {"statistical": 0.6, "behavioural": 0.3}),
    ("Survey Design & Research Division (SDRD), NSO", "Survey design and sampling methodology", {"statistical": 0.9, "technical": 0.3}),
    ("Data Processing Division (DPD), NSO", "Survey data processing and validation", {"technical": 0.8, "statistical": 0.3}),
    ("National Accounts Division (NAD), NSO", "National accounts compilation and GDP estimation", {"statistical": 0.8}),
    ("Price Statistics Division (PSD), NSO", "CPI compilation and price data validation", {"statistical": 0.9}),
    ("Economic Statistics Division (ESD), NSO", "Industrial statistics and IIP compilation", {"statistical": 0.7, "technical": 0.2}),
    ("Social Statistics Division (SSD), NSO", "SDG indicators and social statistics", {"statistical": 0.6, "behavioural": 0.2}),
    ("Data Informatics & Innovation Division (DIID), MoSPI", "Data platforms, analytics and dissemination systems", {"technical": 1.0, "digital_governance": 0.6}),
    ("Coordination & Publication Division (CAPD), MoSPI", "Coordination, publications and stakeholder communication", {"behavioural": 0.7, "digital_governance": 0.2}),
    ("National Statistical Systems Training Academy (NSSTA)", "Training design and capacity building", {"behavioural": 0.6, "statistical": 0.3}),
]

# designation, count, years of experience
RANKS = [
    ("Additional Director General", 2, 26),
    ("Deputy Director General", 3, 22),
    ("Director", 5, 17),
    ("Joint Director", 3, 14),
    ("Deputy Director", 6, 10),
    ("Assistant Director", 6, 6),
    ("Senior Statistical Officer", 6, 8),
    ("Junior Statistical Officer", 4, 3),
    ("Statistical Investigator", 1, 2),
]

EDUCATION = [
    "M.Sc. Statistics", "M.A. Economics", "M.Stat., Indian Statistical Institute", "M.Sc. Mathematics",
    "B.Tech. Computer Science", "M.A. Econometrics", "Ph.D. Economics", "M.Sc. Agricultural Statistics",
]

INTERESTS = [
    "Survey methodology, Data quality", "Machine learning, Python", "National accounts, Macroeconomics",
    "GIS, Spatial statistics", "Data privacy, Cybersecurity", "Leadership, Public communication",
    "SDG monitoring, Social statistics", "Cloud data platforms, SQL",
]
