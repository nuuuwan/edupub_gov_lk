from dataclasses import dataclass


@dataclass
class Lang:
    id: int
    name: str

    @property
    def short_name(self):
        return self.name[:2].lower()

    @staticmethod
    def list() -> list['Lang']:
        return [
            Lang(1, "English"),
            # Lang(2, "Sinhala"),
            # Lang(3, "Tamil"),
        ]

    @staticmethod
    def from_id(id: int) -> 'Lang':
        for x in Lang.list():
            if x.id == id:
                return x
        raise ValueError(f'Invalid id: {id}')
