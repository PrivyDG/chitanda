from snowball import cmdgroup


@cmdgroup.command()
def migrate():
    """Upgrade the database to the latest migration."""
    pass
