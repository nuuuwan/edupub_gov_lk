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
        for lang in Lang.list():
            if lang.id == id:
                return lang
        raise ValueError(f"Invalid lang id: {id}")
