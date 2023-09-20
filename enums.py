import enum


class SubjectArea(enum.Enum):
    """
    Enums of different subject areas, they make the code more readable and string comparisons faster
    """
    ANY = ''
    ECE = "Electrical and Computer Engineering"
    CS = "computer science"
    MATH = "mathematics"


class College(enum.Enum):
    """
        Enums of different colleges, they make the code more readable and string comparisons faster
        """
    SCHOOL_OF_ENGINEERING = "Henry Samueli School of Engineering and Applied Science"
    ANDERSON_BUSINESS_SCHOOL = "Anderson school of business"
