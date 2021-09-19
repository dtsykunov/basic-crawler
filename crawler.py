from urllib.request import urlopen
from urllib.parse import urlparse
from html.parser import HTMLParser

VISITED = {}


# https://stackoverflow.com/a/38020041
def is_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_html(url: str) -> str:
    return urlopen(url).read().decode("utf-8")


def is_subpath(path: str) -> bool:
    return path and path[0] == "/"


class BasicParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = None
        self.subresources = set()

    def feed(self, root, html):
        self.root = root
        super().feed(html)

    def handle_starttag(self, tag, attrs):
        if not attrs:
            return
        for attr, value in attrs:
            if attr == 'href':
                break
        if is_subpath(value):
            value = self.root + value
        if not is_url(value):
            return
        self.subresources.add(value)

    def reset(self):
        super().reset()
        self.root = None
        self.subresources = set()


def print_for_site(root: str, subresources: list[str]):
    print(root, "-", *subresources)


if __name__ == "__main__":
    links = set(["https://jetbrains.com"])
    visited = set()
    parser = BasicParser()
    while links:
        link = links.pop()
        if link in visited:
            continue
        visited.add(link)

        try:
            parser.feed(link, get_html(link))
        except:
            parser.reset()
            continue

        print_for_site(link, parser.subresources)
        links.update(parser.subresources)

        parser.reset()
