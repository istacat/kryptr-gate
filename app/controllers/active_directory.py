import ldap

# auth('161.97.148.123', 'Administrator@kryptr.li', 'x3Rfh7K9P86wa')


def auth(address, username, password):
    conn = ldap.initialize("ldap://" + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn.simple_bind_s(username, password)
