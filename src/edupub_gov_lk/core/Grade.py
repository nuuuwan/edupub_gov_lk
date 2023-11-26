from dataclasses import dataclass


@dataclass
class Grade:
    id: int
    name: str

    @property
    def name_num(self):
        return self.name.split(' ')[1].replace('/', '-')

    @staticmethod
    def list() -> list['Grade']:
        return [
            Grade(1, "Grade 1"),
            Grade(2, "Grade 2"),
            Grade(3, "Grade 3"),
            Grade(4, "Grade 4"),
            Grade(5, "Grade 5"),
            Grade(6, "Grade 6"),
            Grade(7, "Grade 7"),
            Grade(8, "Grade 8"),
            Grade(9, "Grade 9"),
            Grade(10, "Grade 10"),
            Grade(11, "Grade 11"),
            Grade(17, "Grade 12/13"),
        ]

    @staticmethod
    def from_id(id: int) -> 'Grade':
        for grade in Grade.list():
            if grade.id == id:
                return grade
        raise ValueError(f"Invalid grade id: {id}")
