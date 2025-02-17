class StudyMembershipItemNotFound(Exception):
    message: str

    def __init__(
        self,
        message: str = "StudyMembership Item not found",
    ) -> None:
        self.message = message
