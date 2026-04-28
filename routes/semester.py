from datetime import datetime

def main():
    print(getSemester())

def getSemester():
    now = datetime.now()
    year = now.year

    # Fall   : August 18 - December 7
    fall_start = datetime(year, 8, 18)
    fall_end   = datetime(year, 12, 7)

    # Winter : December 8 - January 11
    winter_start = datetime(year, 12, 8)
    winter_end   = datetime(year + 1, 1, 11)
    
    # Spring : January 12 - May 11
    spring_start = datetime(year, 1, 12)
    spring_end   = datetime(year, 5, 11)
    
    # Summer : May 12 - August 17
    summer_start = datetime(year, 5, 12)
    summer_end   = datetime(year, 8, 17)

    if fall_start <= now and now <= fall_end:
        return "Fall"
    elif winter_start <= now and now <= winter_end:
        return "Winter"
    elif spring_start <= now and now <= spring_end:
        return "Spring"
    elif summer_start <= now and now <= summer_end:
        return "Summer"

    # Fall back to spring incase everything fails
    return "Spring"


def getYear():
    now = datetime.now()
    year = now.year
    return year

if __name__ == "__main__":
    main()
