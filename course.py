from urllib import parse

class Course:
    def __init__(self, name: str, href: str, category: str,
                 progress: int | None) -> None:
        self.name = name
        self.href = href
        self.category = category
        self.progress = progress

        parsed_href = parse.parse_qs(parse.urlsplit(self.href).query)
        self.id = int(parsed_href['id'][0])