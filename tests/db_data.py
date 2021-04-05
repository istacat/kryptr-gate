from app.models import User, Subordinate, Account


def fill_test_data():
    admin = User(
        username='a',
        activated=User.StatusType.active,
        role=User.RoleType.admin
    )
    admin.password = 'a'
    admin.save()

    dist1 = User(
        username='d',
        activated=User.StatusType.active,
        role=User.RoleType.distributor
    )
    dist1.password = 'd'
    dist1.save()

    dist2 = User(
        username='d2',
        activated=User.StatusType.active,
        role=User.RoleType.distributor
    )
    dist2.password = 'd2'
    dist2.save()

    res1 = User(
        username='r',
        activated=User.StatusType.active,
        role=User.RoleType.reseller
    )
    res1.password = 'r'
    res1.save()

    sub1 = Subordinate(
        chief_id=dist1.id,
        subordinate_id=res1.id
    )
    sub1.save()

    subres1 = User(
        username='sr',
        activated=User.StatusType.active,
        role=User.RoleType.sub_reseller
    )
    subres1.password = 'sr'
    subres1.save()

    sub2 = Subordinate(
        chief_id=res1.id,
        subordinate_id=subres1.id
    )
    sub2.save()

    support = User(
        username='s',
        activated=User.StatusType.active,
        role=User.RoleType.support
    )
    support.password = 's'
    support.save()

    acc1 = Account(
        name='acc1',
        ecc_id='GHB123',
        ad_login='acc1',
        ad_password='123',
        email='testing@gmail.com',
        reseller_id=subres1.id
    )
    acc1.save()
