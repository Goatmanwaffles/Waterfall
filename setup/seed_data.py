
# Uses count to iterates through lists
count = 0

# Seed data generator for testing
student_first_names = [
    "Logan", "Andrew", "Caleb", "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia",
    "Mason", "Isabella", "Lucas", "Mia", "Oliver", "Charlotte", "Elijah", "Amelia", "James", "Harper",
    "Benjamin", "Evelyn", "Jacob", "Abigail", "Michael", "Emily", "William", "Elizabeth", "Alexander", "Mila",
    "Daniel", "Ella", "Matthew", "Avery", "Henry", "Sofia", "Jackson", "Camila", "Sebastian", "Aria",
    "David", "Scarlett", "Joseph", "Victoria", "Samuel", "Madison", "Carter", "Luna", "Owen", "Grace",
    "Wyatt", "Chloe", "John", "Penelope", "Jack", "Layla", "Luke", "Riley", "Jayden", "Zoey",
    "Dylan", "Nora", "Grayson", "Lily", "Levi", "Eleanor", "Isaac", "Hannah", "Gabriel", "Lillian",
    "Julian", "Addison", "Mateo", "Aubrey", "Anthony", "Ellie", "Jaxon", "Stella", "Lincoln", "Natalie",
    "Joshua", "Zoe", "Christopher", "Leah", "Theodore", "Hazel", "Ezra", "Violet", "Thomas", "Aurora",
    "Charles", "Savannah", "Christian", "Audrey", "Aaron", "Brooklyn", "Eli", "Bella", "Connor", "Claire"
]
student_last_names = [
    "Senol", "Roddy", "Stanberry", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres",
    "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz",
    "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez",
    "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim",
    "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray",
    "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long"
]
instructor_first_names = [
    "Javed", "Giovanni", "Mikhail", "Alan", "Barbara", "Chen", "Diana", "Ernest", "Fatima", "George",
    "Helena", "Ivan", "Julia", "Kenji", "Laura", "Marcus", "Nadia", "Omar", "Priya", "Quincy",
    "Rachel", "Stefan", "Tanya", "Umar", "Vera", "Wesley", "Xavier", "Yara", "Zhang", "Arun",
    "Beatrice", "Carlos", "Dmitri", "Elena", "Farid", "Greta", "Hiroshi", "Ingrid", "Jamal", "Karen",
    "Leonid", "Miguel", "Nikolai", "Orla", "Pavel", "Qiang", "Rosa", "Sergei", "Tomas", "Uma",
    "Viktor", "Wendy", "Yusuf", "Zara", "Abdul", "Bianca", "Catalina", "Dennis", "Edith", "Felipe",
    "Gertrude", "Hans", "Isabel", "Jurgen", "Klaus", "Lena", "Magnus", "Nina", "Otto", "Paula",
    "Ravi", "Svetlana", "Tariq", "Ursula", "Vlad", "Wei", "Xiomara", "Yolanda", "Zhen", "Ahmed",
    "Brigitte", "Cyrus", "Dario", "Eduardo", "Francesca", "Gustavo", "Haruki", "Imani", "Jorge", "Kofi",
    "Lars", "Mei", "Nasser", "Oksana", "Pedro", "Renata", "Soren", "Thiago", "Ulrich", "Vivian"
]
instructor_last_names = [
    "Kahn", "Phares", "Nesterenko", "Ahmed", "Becker", "Chowdhury", "Delgado", "Ellis", "Fischer", "Goldberg",
    "Hayashi", "Iqbal", "Jansen", "Koval", "Larsen", "Mehta", "Novak", "OBrien", "Peters", "Quinn",
    "Rossi", "Schmidt", "Tanaka", "Uchida", "Volkov", "Weber", "Xu", "Yamamoto", "Zimmer", "Abbas",
    "Bianchi", "Cortez", "Dubois", "Engel", "Ferrari", "Gupta", "Holmberg", "Ito", "Jung", "Kovacs",
    "Lambert", "Mueller", "Nakamura", "Ortega", "Petrov", "Quintero", "Reza", "Silva", "Takahashi", "Usman",
    "Vargas", "Wallace", "Xiong", "Yildiz", "Zhukov", "Aslan", "Bauer", "Costa", "Daher", "Esposito",
    "Fontaine", "Gallo", "Haddad", "Ishikawa", "Jakobsen", "Kowalski", "Leclerc", "Malik", "Nilsson", "Ozawa",
    "Palmer", "Rahman", "Saito", "Tremblay", "Ueno", "Villanueva", "Wagner", "Yoon", "Zaidi", "Andersson",
    "Bonomi", "Chan", "Dumont", "Eriksson", "Fiore", "Gagnon", "Hansen", "Ivanov", "Jensen", "Kirby",
    "Lindgren", "Marino", "Nakagawa", "Obregon", "Park", "Romero", "Santos", "Toma", "Urbano", "Vega"
]
dept_names = [
    "CS", "BIO", "MATH", "CHEM", "NURS", "PHYS", "ENGL", "FRNC", "JAPN", "BOTN",
    "HIST", "PSYC", "SOCI", "ANTH", "ECON", "POLS", "PHIL", "RELG", "ARTS", "MUSC",
    "THTR", "DANC", "FILM", "ARCH", "BUSN", "ACCT", "MKTG", "FINE", "MGMT", "HRMT",
    "EDUC", "LAWS", "MEDI", "DENT", "PHAR", "VETS", "ENGR", "MECH", "ELEC", "CIVL",
    "INDS", "AERO", "CHEN", "BMED", "ENVS", "GEOL", "ASTR", "OCEA", "METR", "NEUR",
    "GENE", "BIOC", "MICR", "PATH", "ANAT", "PHYL", "KINS", "NUTR", "SPCH", "COMM",
    "JRNL", "ITAL", "SPAN", "GERM", "RUSS", "ARAB", "CHNS", "KORN", "HEBR", "LATN",
    "GREK", "PORT", "STAT", "ACTS", "OPER", "MATS", "NUCL", "PETR", "MARN", "MING",
    "ROBT", "DATA", "CYBR", "NETW", "GAME", "DSGN", "PHOT", "LITR", "WRIT", "LING",
    "GEND", "URBN", "PUBL", "SOCW", "CRIM", "INTL", "ASIA", "LATS", "AFRI", "EURS"
]
buildings = [
    "Smith", "MSB", "DI", "White", "Carnegie", "Hoover", "Roosevelt", "Lincoln", "Jefferson", "Hamilton",
    "Franklin", "Madison", "Adams", "Monroe", "Jackson", "Wilson", "Kennedy", "Eisenhower", "Truman", "Harrison",
    "Tyler", "Polk", "Taylor", "Fillmore", "Pierce", "Buchanan", "Grant", "Hayes", "Garfield", "Arthur",
    "Cleveland", "McKinley", "Taft", "Harding", "Coolidge", "Hayden", "Bailey", "Clarke", "Morrison", "Pemberton",
    "Rockefeller", "Vanderbilt", "Stanford", "Harvard", "Yale", "Princeton", "Columbia", "Dartmouth", "Cornell", "Brown",
    "Edison", "Tesla", "Einstein", "Newton", "Darwin", "Curie", "Galileo", "Kepler", "Copernicus", "Pascal",
    "Turing", "Lovelace", "Babbage", "Knuth", "Dijkstra", "Ritchie", "Wozniak", "Hopper", "Shannon", "Gates",
    "North", "South", "East", "West", "Central", "Main", "Lakeside", "Riverside", "Hillcrest", "Oakwood",
    "Pinegrove", "Maplewood", "Cedar", "Birch", "Willow", "Elm", "Ashford", "Brookside", "Highland", "Meadow",
    "Sunnydale", "Fairview", "Westfield", "Eastgate", "Northstar", "Southpoint", "Summit", "Ridgeway", "Valley", "Crescent"
]
semesters = ["Fall", "Winter", "Spring", "Summer"]
grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
advisor_first_names = [
    "Joseph", "Thomas", "Tommy", "Craig", "Leah", "TJ", "Margaret", "Patricia", "Jennifer", "Linda",
    "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley",
    "Kimberly", "Donna", "Emily", "Michelle", "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca",
    "Sharon", "Laura", "Cynthia", "Kathleen", "Helen", "Amy", "Shirley", "Angela", "Anna", "Ruth",
    "Brenda", "Pamela", "Nicole", "Katherine", "Virginia", "Catherine", "Christine", "Samantha", "Debra", "Janet",
    "Richard", "Charles", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Kenneth",
    "Andrew", "Edward", "Brian", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary",
    "Nicholas", "Eric", "Stephen", "Jonathan", "Larry", "Justin", "Scott", "Brandon", "Frank", "Benjamin",
    "Gregory", "Raymond", "Samuel", "Patrick", "Alexander", "Jack", "Dennis", "Jerry", "Tyler", "Aaron",
    "Henry", "Douglas", "Peter", "Jose", "Adam", "Zachary", "Walter", "Kyle", "Harold", "Carl"
]
advisor_last_names = [
    "Raklovits", "Redy", "Morneweck", "Smith", "Johnson", "So", "Abbott", "Ackerman", "Albright", "Armstrong",
    "Atkinson", "Barrett", "Beasley", "Benson", "Black", "Blackwell", "Blake", "Booker", "Bowers", "Bradley",
    "Branson", "Briggs", "Burke", "Burton", "Byrd", "Caldwell", "Cannon", "Carr", "Cervantes", "Chambers",
    "Chang", "Cho", "Christensen", "Clayton", "Coleman", "Cortez", "Crawford", "Dalton", "Daniels", "Davidson",
    "Dawson", "Decker", "Dempsey", "Diaz", "Dixon", "Donovan", "Downey", "Drake", "Dudley", "Duncan",
    "Eaton", "Ellison", "Emerson", "Everett", "Farmer", "Fields", "Finley", "Fitzgerald", "Fleming", "Fox",
    "Frost", "Galloway", "Gibson", "Gilbert", "Glover", "Goodman", "Goodwin", "Graves", "Griffin", "Grimes",
    "Hancock", "Harmon", "Harvey", "Hendrix", "Hodge", "Holt", "Hopkins", "Horton", "Hunter", "Jefferson",
    "Kane", "Keller", "Kent", "Kirk", "Lamb", "Lane", "Langley", "Lawson", "Levine", "Lowry",
    "Lynch", "MacDonald", "Marshall", "Mayer", "McCarthy", "McGuire", "Nash", "Norris", "Orr", "Owens"
]
course_titles = [
    "CS1", "CS2", "CS3", "Intro to Databases", "Discrete Structures", "CS4", "Elementary Japanese 1", "Elementary Japanese 2", "Calculus I", "Calculus II", "Calculus III", "Linear Algebra", "Differential Equations", "Real Analysis", "Complex Analysis", "Abstract Algebra", "Number Theory", "Topology", "Statistics I", "Statistics II",
    "Probability Theory", "Data Structures", "Algorithms", "Operating Systems", "Computer Networks", "Computer Architecture", "Software Engineering", "Machine Learning", "Artificial Intelligence", "Compilers",
    "Cybersecurity", "Web Development", "Mobile App Development", "Cloud Computing", "Distributed Systems", "Graph Theory", "General Biology", "Cell Biology", "Molecular Biology", "Genetics",
    "Microbiology", "Ecology", "Evolution", "Human Anatomy", "Human Physiology", "General Chemistry", "Organic Chemistry", "Physical Chemistry", "Biochemistry", "Analytical Chemistry",
    "Classical Mechanics", "Electromagnetism", "Thermodynamics", "Quantum Mechanics", "Astrophysics", "Optics", "Nuclear Physics", "Composition I", "Composition II", "Creative Writing",
    "American Literature", "British Literature", "World Literature", "Shakespeare", "Poetry Workshop", "Technical Writing", "Elementary French 1", "Elementary French 2", "Intermediate French", "Elementary Spanish 1",
    "Elementary Spanish 2", "Intermediate Spanish", "Elementary German", "World History", "US History", "European History", "Ancient History", "Medieval History", "Modern History", "Introduction to Psychology",
    "Cognitive Psychology", "Social Psychology", "Developmental Psychology", "Intro to Sociology", "Cultural Anthropology", "Microeconomics", "Macroeconomics", "Econometrics", "International Economics", "Intro to Philosophy",
    "Ethics", "Logic", "Political Theory", "American Government", "Comparative Politics", "Intro to Music Theory", "Art History", "Film Studies", "Intro to Nursing", "Pharmacology"
]
days = ["M", "T", "W", "H", "F"]
usernames = [
    "Drew2000", "Caleb999", "aroddy", "coolGuy77", "dropKick2000", "OrangeMan", "DrMario", "Link", "Ganondworf", "SuperCool",
    "PixelWizard", "ShadowHunter", "NinjaCoder", "CyberFox", "NeonKnight", "DigitalDragon", "QuantumLeap", "ByteMaster", "CodeSamurai", "NovaStar",
    "ZeroHero", "MatrixMind", "SilverBullet", "GoldenEagle", "IronFist", "ThunderBolt", "LightningLord", "FrostBite", "FireFury", "StormBreaker",
    "SteelTitan", "SkyWalker", "MoonRider", "SunChaser", "StarGazer", "CometTrail", "GalaxyExplorer", "NebulaSeeker", "VoidWanderer", "AstroNaut",
    "AlphaOmega", "BetaTester", "GammaRay", "DeltaForce", "EpsilonEdge", "ZetaZone", "SigmaSolo", "OmegaPrime", "PhiPhoenix", "ChiChamp",
    "MegaMan", "UltraViolet", "HyperDrive", "TurboBoost", "RocketRacer", "SpeedDemon", "BlazingFast", "SwiftStrike", "RapidRush", "QuickSilver",
    "SlickShot", "SharpShooter", "EagleEye", "HawkEye", "OwlNight", "FalconWing", "RavenBlack", "CrowCaller", "SnakeEyes", "TigerClaw",
    "LionHeart", "BearHug", "WolfPack", "FoxTrot", "DeerDash", "RabbitRun", "TurtleShell", "DolphinDive", "SharkBite", "WhaleSong",
    "OctoTenta", "CrabCrawl", "LobsterLock", "JellyJolt", "SeaStar", "CoralReef", "KelpKing", "TideTurner", "WaveRider", "DeepDiver",
    "IceBreaker", "SnowFlake", "FrostGiant", "GlacierGuard", "TundraTrack", "BlizzardBlast", "AvalancheArt", "HailHammer", "MistMaker", "FogFinder"
]
passwords = [
    "DrewPass99", "CalebCalebCaleb", "123892138", "Coolest!", "Drop73Drop12!", "FavoriteColor", "RealDoctor3626", "Linkus", "GannonGannon88", "TrulyCool2003",
    "Password123!", "SecureP@ss", "MyK3ySt0ne", "TigerLily88", "BlueSky2024", "RedRose99", "GreenField", "YellowBird", "PurpleRain", "OrangePeel",
    "PinkPanther", "BlackCat13", "WhiteSnow", "GrayWolf42", "SilverSpoon", "GoldenGate", "IronMan88", "SteelBlade", "CopperCoin", "BronzeMedal",
    "DiamondEye", "RubyRed", "SapphireSea", "EmeraldIsle", "PearlWhite", "JadeDragon", "AmberGlow", "OnyxBlack", "OpalShimmer", "TopazTan",
    "CrystalClear", "GlassHouse", "MetalMouth", "StoneCold", "WoodPecker", "PaperPlane", "PlasticMan", "RubberBand", "LeatherBound", "SilkRoad",
    "CottonCandy", "WoolSweater", "DenimJeans", "VelvetTouch", "SatinSheets", "CanvasArt", "FleeceBlanket", "LinenShirt", "NylonRope", "PolyesterMix",
    "Summit9000", "Valley5678", "Ocean1234", "Mountain567", "RiverFlow12", "LakeSide34", "BeachDay89", "ForestGreen7", "DesertHeat6", "ArcticCold5",
    "Pineapple99", "BananaSplit7", "AppleCore42", "GrapeVine66", "LemonZest33", "LimeGreen44", "CherryPop55", "StrawBerry1", "BlueBerry2", "RaspberryJam",
    "PeachFuzz77", "PlumCrazy88", "MangoTango99", "KiwiGold12", "PapayaSun34", "CoconutMilk5", "PizzaSlice22", "BurgerTime33", "SushiRoll44", "TacoTuesday5",
    "PastaFagioli", "RiceBowl99", "SoupDuJour22", "SaladBowl42", "BreadBasket3", "CakeDay1111", "PieChart22", "CookieJar33", "IceCream44", "CandyLand55"
]
roles = ["Administrator", "Instructor", "Student"]
count = 0