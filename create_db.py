import sqlite3

connection = sqlite3.connect("startups.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS funding_rounds (
        id INTEGER PRIMARY KEY,
        startup_name TEXT,
        sector TEXT,
        funding_amount_usd_million REAL,
        round_type TEXT,
        investor TEXT,
        city TEXT,
        year INTEGER,
        valuation_usd_million REAL
    )
""")

data = [
    (1,  "Zepto",         "Quick Commerce",   200.0,  "Series E", "Y Combinator, Nexus",         "Mumbai",    2023, 1400.0),
    (2,  "Zepto",         "Quick Commerce",   665.0,  "Series F", "StepStone, Motilal Oswal",    "Mumbai",    2024, 3600.0),
    (3,  "CRED",          "Fintech",          140.0,  "Series D", "Falcon Edge, DST Global",     "Bangalore", 2021, 2200.0),
    (4,  "CRED",          "Fintech",          251.0,  "Series E", "Tiger Global, Falcon Edge",   "Bangalore", 2022, 6400.0),
    (5,  "Razorpay",      "Fintech",          375.0,  "Series F", "Lone Pine Capital",           "Bangalore", 2021, 7500.0),
    (6,  "Razorpay",      "Fintech",          160.0,  "Series G", "Alkeon Capital",              "Bangalore", 2022, 7500.0),
    (7,  "Meesho",        "E-Commerce",       570.0,  "Series F", "Fidelity, B Capital",         "Bangalore", 2021, 4900.0),
    (8,  "Meesho",        "E-Commerce",       275.0,  "Series G", "Prosus, SoftBank",            "Bangalore", 2023, 3900.0),
    (9,  "PhonePe",       "Fintech",          350.0,  "Series A", "General Atlantic",            "Bangalore", 2023, 12000.0),
    (10, "PhonePe",       "Fintech",          100.0,  "Series B", "Ribbit Capital",              "Bangalore", 2023, 12000.0),
    (11, "Ola Electric",  "EV",               300.0,  "Series C", "Tekne Capital, Alpine",       "Bangalore", 2022, 5000.0),
    (12, "Ola Electric",  "EV",               734.0,  "IPO",      "Public Market",               "Bangalore", 2024, 4000.0),
    (13, "Groww",         "Fintech",          251.0,  "Series D", "Tiger Global, Sequoia",       "Bangalore", 2021, 3000.0),
    (14, "Groww",         "Fintech",          83.0,   "Series E", "ICONIQ Capital",              "Bangalore", 2022, 3000.0),
    (15, "Nykaa",         "Beauty & Fashion", 100.0,  "Pre-IPO",  "Steadview Capital",           "Mumbai",    2021, 7400.0),
    (16, "BharatPe",      "Fintech",          370.0,  "Series E", "Tiger Global, Coatue",        "Delhi",     2021, 2850.0),
    (17, "Lenskart",      "D2C Retail",       220.0,  "Series H", "Temasek, KKR",                "Delhi",     2022, 4500.0),
    (18, "Lenskart",      "D2C Retail",       200.0,  "Series I", "ADIA",                        "Delhi",     2023, 4500.0),
    (19, "Slice",         "Fintech",          220.0,  "Series B", "Tiger Global, Insight",       "Bangalore", 2021, 1500.0),
    (20, "Darwinbox",     "HR Tech",          72.0,   "Series D", "TCV, Salesforce Ventures",    "Hyderabad", 2022, 950.0),
    (21, "Unacademy",     "Edtech",           440.0,  "Series F", "Tiger Global, SoftBank",      "Bangalore", 2021, 3440.0),
    (22, "upGrad",        "Edtech",           210.0,  "Series F", "Temasek, IFC",                "Mumbai",    2022, 2700.0),
    (23, "Oyo",           "Hospitality",      660.0,  "Series J", "Microsoft, Airbnb",           "Delhi",     2021, 9600.0),
    (24, "Swiggy",        "Food Delivery",    700.0,  "Series J", "Invesco, Goldman Sachs",      "Bangalore", 2022, 10700.0),
    (25, "Swiggy",        "Food Delivery",    617.0,  "IPO",      "Public Market",               "Bangalore", 2024, 11300.0),
    (26, "Zetwerk",       "B2B Manufacturing",120.0,  "Series E", "Greenoaks, Lightspeed",       "Bangalore", 2021, 2700.0),
    (27, "Zetwerk",       "B2B Manufacturing",150.0,  "Series F", "Avenir, ADIA",                "Bangalore", 2022, 2700.0),
    (28, "Mamaearth",     "D2C Beauty",       52.0,   "Pre-IPO",  "Sequoia, Sofina",             "Delhi",     2022, 1200.0),
    (29, "InMobi",        "Adtech",           100.0,  "Series A", "SoftBank",                    "Bangalore", 2021, 1000.0),
    (30, "Khatabook",     "SME Fintech",      100.0,  "Series C", "Tiger Global, DST Global",    "Bangalore", 2021, 600.0),
    (31, "Open",          "Neobank",          100.0,  "Series D", "Temasek, Tiger Global",       "Bangalore", 2022, 1000.0),
    (32, "Acko",          "Insurtech",        255.0,  "Series E", "General Atlantic, Amazon",    "Mumbai",    2021, 1100.0),
    (33, "Vedantu",       "Edtech",           100.0,  "Series E", "ABC World Asia",              "Bangalore", 2021, 1000.0),
    (34, "Moj / ShareChat","Social Media",    255.0,  "Series F", "Google, Times Internet",      "Bangalore", 2022, 5000.0),
    (35, "Spinny",        "Used Cars",        283.0,  "Series E", "Tiger Global, Avenir",        "Delhi",     2021, 1800.0),
    (36, "Pristyn Care",  "Healthtech",       100.0,  "Series E", "Sequoia, Tiger Global",       "Delhi",     2022, 1400.0),
    (37, "Healthifyme",   "Healthtech",       75.0,   "Series C", "LeapFrog, Khosla",            "Bangalore", 2021, 500.0),
    (38, "Delhivery",     "Logistics",        277.0,  "Pre-IPO",  "Fidelity, Lee Fixel",         "Delhi",     2021, 3000.0),
    (39, "Park+",         "Mobility",         50.0,   "Series B", "Matrix, Sequoia",             "Delhi",     2022, 300.0),
    (40, "Innovaccer",    "Healthtech",       150.0,  "Series E", "Tiger Global, B Capital",     "Delhi",     2022, 1900.0),
]

cursor.executemany("INSERT OR IGNORE INTO funding_rounds VALUES (?,?,?,?,?,?,?,?,?)", data)
connection.commit()
connection.close()
print("✅ Startup funding database created successfully!")
