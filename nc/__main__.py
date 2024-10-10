from click import group, argument, Choice

from assets import targets

from .Clicker import Clicker


@group()
def main():
    pass


@main.command()
def list():
    Clicker().list()


@main.command()
@argument('target', type = Choice(choices = targets, case_sensitive = False))
def farm(target: str):
    Clicker().farm(target)


if __name__ == '__main__':
    main()
