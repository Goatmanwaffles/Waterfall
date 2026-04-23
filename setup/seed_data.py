
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
grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", ""]
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

usernames = ["Admin", "Instructor", "Student"]
passwords = ["abc"]
roles = ["Administrator", "Instructor", "Student"]
accounts = [
    {"username": "admin",      "password": "abc",      "role": "Administrator"},
    {"username": "instructor", "password": "abc", "role": "Instructor"},
    {"username": "student",    "password": "abc",    "role": "Student"},
    {"username": "iNelson",    "password": "abc",    "role": "Student"},
    {"username": "sMorales",    "password": "abc",    "role": "Student"},
    {"username": "cMiller",    "password": "abc",    "role": "Student"},
    {"username": "bHoward",    "password": "abc",    "role": "Student"},
    {"username": "mWard",    "password": "abc",    "role": "Student"},
    {"username": "jParker",    "password": "abc",    "role": "Student"},
    {"username": "aWilliams",    "password": "abc",    "role": "Student"},
    {"username": "mRamirez",    "password": "abc",    "role": "Student"},
    {"username": "sSenol",    "password": "abc",    "role": "Student"},
    {"username": "zMendoze",    "password": "abc",    "role": "Student"},
    {"username": "eJones",    "password": "abc",    "role": "Student"},
    {"username": "lWood",    "password": "abc",    "role": "Student"},
    {"username": "eJames",    "password": "abc",    "role": "Student"},
    {"username": "eBrooks",    "password": "abc",    "role": "Student"},
    {"username": "lPark",       "password": "abc", "role": "Instructor"},
    {"username": "qTremblay",   "password": "abc", "role": "Instructor"},
    {"username": "jZimmer",     "password": "abc", "role": "Instructor"},
    {"username": "xBauer",      "password": "abc", "role": "Instructor"},
    {"username": "gMehta",      "password": "abc", "role": "Instructor"},
    {"username": "tEllis",      "password": "abc", "role": "Instructor"},
    {"username": "gYildiz",     "password": "abc", "role": "Instructor"},
    {"username": "aCortez",     "password": "abc", "role": "Instructor"},
    {"username": "oDaher",      "password": "abc", "role": "Instructor"},
    {"username": "nAndersson",  "password": "abc", "role": "Instructor"},

]

advisors = [
    {"first_name": "Edward",   "last_name": "Fields",       "department_ID": 1},
    {"first_name": "Donna",    "last_name": "Hancock",      "department_ID": 2},
    {"first_name": "Rebecca",  "last_name": "Cho",          "department_ID": 3},
    {"first_name": "Tommy",    "last_name": "Dawson",       "department_ID": 4},
    {"first_name": "Jennifer", "last_name": "Glover",       "department_ID": 5},
    {"first_name": "Timothy",  "last_name": "Beasley",      "department_ID": 6},
    {"first_name": "Katherine","last_name": "Christensen",  "department_ID": 7},
    {"first_name": "Patricia", "last_name": "Decker",       "department_ID": 8},
    {"first_name": "Craig",    "last_name": "Drake",        "department_ID": 9},
    {"first_name": "Nicholas", "last_name": "Bowers",       "department_ID": 10},
    {"first_name": "Stephanie","last_name": "Downey",       "department_ID": 11},
    {"first_name": "Amy",      "last_name": "Grimes",       "department_ID": 12},
    {"first_name": "Michelle", "last_name": "Ackerman",     "department_ID": 13},
    {"first_name": "Linda",    "last_name": "Fields",       "department_ID": 14},
]

students = [
    {"first_name": "Isaac",    "last_name": "Nelson",   "department_ID": 1,  "total_cred": 192, "advisor_ID": 1,  "account_ID": 4},
    {"first_name": "Samuel",   "last_name": "Morales",  "department_ID": 2,  "total_cred": 66,  "advisor_ID": 2,  "account_ID": 5},
    {"first_name": "Camila",   "last_name": "Miller",   "department_ID": 3,  "total_cred": 186, "advisor_ID": 3,  "account_ID": 6},
    {"first_name": "Brooklyn", "last_name": "Howard",   "department_ID": 4,  "total_cred": 100, "advisor_ID": 4,  "account_ID": 7},
    {"first_name": "Mila",     "last_name": "Ward",     "department_ID": 5,  "total_cred": 153, "advisor_ID": 5,  "account_ID": 8},
    {"first_name": "Joseph",   "last_name": "Parker",   "department_ID": 6,  "total_cred": 11,  "advisor_ID": 6,  "account_ID": 9},
    {"first_name": "Andrew",   "last_name": "Williams", "department_ID": 7,  "total_cred": 26,  "advisor_ID": 7,  "account_ID": 10},
    {"first_name": "Mila",     "last_name": "Ramirez",  "department_ID": 8,  "total_cred": 24,  "advisor_ID": 8,  "account_ID": 11},
    {"first_name": "Scarlett", "last_name": "Senol",    "department_ID": 9,  "total_cred": 30,  "advisor_ID": 9,  "account_ID": 12},
    {"first_name": "Zoe",      "last_name": "Mendoza",  "department_ID": 10, "total_cred": 201, "advisor_ID": 10, "account_ID": 13},
    {"first_name": "Elijah",   "last_name": "Jones",    "department_ID": 11, "total_cred": 147, "advisor_ID": 11, "account_ID": 14},
    {"first_name": "Liam",     "last_name": "Wood",     "department_ID": 12, "total_cred": 131, "advisor_ID": 12, "account_ID": 15},
    {"first_name": "Elijah",   "last_name": "James",    "department_ID": 13, "total_cred": 93,  "advisor_ID": 13, "account_ID": 16},
    {"first_name": "Evelyn",   "last_name": "Brooks",   "department_ID": 14, "total_cred": 184, "advisor_ID": 14, "account_ID": 17},
]

instructors = [
    {"first_name": "Lena",    "last_name": "Park",       "department_ID": 1,  "salary": 294534.29, "account_ID": 18},
    {"first_name": "Quincy",  "last_name": "Tremblay",   "department_ID": 2,  "salary": 663261.66, "account_ID": 19},
    {"first_name": "Javed",   "last_name": "Zimmer",     "department_ID": 3,  "salary": 802874.80, "account_ID": 20},
    {"first_name": "Xavier",  "last_name": "Bauer",      "department_ID": 4,  "salary": 469090.46, "account_ID": 21},
    {"first_name": "Gustavo", "last_name": "Mehta",      "department_ID": 5,  "salary": 434262.43, "account_ID": 22},
    {"first_name": "Tariq",   "last_name": "Ellis",      "department_ID": 6,  "salary": 465903.46, "account_ID": 23},
    {"first_name": "Gustavo", "last_name": "Yildiz",     "department_ID": 7,  "salary": 201988.20, "account_ID": 24},
    {"first_name": "Alan",    "last_name": "Cortez",     "department_ID": 8,  "salary": 446818.44, "account_ID": 25},
    {"first_name": "Oksana",  "last_name": "Daher",      "department_ID": 9,  "salary": 559553.55, "account_ID": 26},
    {"first_name": "Nadia",   "last_name": "Andersson",  "department_ID": 10, "salary": 993400.99, "account_ID": 27},
]



account_index = 0
count = 0