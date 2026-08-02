import sys

from greeting import greet
from farewell import farewell


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(greet(name))
    print(farewell(name))


if __name__ == "__main__":
    main()
