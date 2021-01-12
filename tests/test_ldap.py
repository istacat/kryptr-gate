import ldap3
from config import BaseConfig as config


def test_ldap_search():
    ad_name = 'DC=KRYPTR,DC=li'
    server_win_uri = config.LDAP_SERVER
    search_filter = "(&(objectClass=person)(sAMAccountName=*)(sn=*))"
    win_bind_name = config.LDAP_USER
    win_bind_passwd = config.LDAP_PASS
    attrs = ['*']

    def get_users_win_data(ip, search_base, search_filter, attrs, win_bind_name, win_bind_passwd):
        server = ldap3.Server('ldap://{}'.format(ip))
        with ldap3.Connection(server, user=win_bind_name, password=win_bind_passwd) as conn:
            conn.search(search_base, search_filter, attributes=attrs)
            return(conn.entries)

    ad_data = get_users_win_data(server_win_uri, ad_name, search_filter, attrs, win_bind_name, win_bind_passwd)
    assert ad_data
