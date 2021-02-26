from app.models import User


def fill_test_data():
    u = User(
        username='a',
        activated=User.StatusType.active,
        role=User.RoleType.admin
    )
    u.password = 'a'
    u.save()

    u = User(
        username='d',
        activated=User.StatusType.active,
        role=User.RoleType.distributor
    )
    u.password = 'd'
    u.save()

    u = User(
        username='r',
        activated=User.StatusType.active,
        role=User.RoleType.reseller
    )
    u.password = 'r'
    u.save()

    u = User(
        username='sr',
        activated=User.StatusType.active,
        role=User.RoleType.sub_reseller
    )
    u.password = 'sr'
    u.save()

    u = User(
        username='s',
        activated=User.StatusType.active,
        role=User.RoleType.support
    )
    u.password = 's'
    u.save()
