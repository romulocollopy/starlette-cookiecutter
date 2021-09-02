class ChassisExceptions(Exception):
    pass


class RepositoryExceptions(ChassisExceptions):
    pass


class TableNotDefined(RepositoryExceptions):
    pass
