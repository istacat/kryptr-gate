from app.models.account import Account


def ecc_encode(number: int) -> str:
    if not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number < 0:
        raise ValueError("number must be positive")

    def alpha_encode(number):
        ALPHABET, base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", list("AAA")
        len_ab = len(ALPHABET)
        len_base = len(base)
        for i in range(len_base):
            number, idx = divmod(number, len_ab)
            base[i] = ALPHABET[idx]

        base.reverse()
        return "".join(base)

    return alpha_encode(number // 1000) + f"{number % 1000:03}"


def get_accounts(user):
    """Get accounts by roles and subordinates"""
    if user.role.name == "admin" or user.role.name == "support":
        return Account.query.all()
    elif user.role.name == "distributor":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        for reseller in user.resellers:
            for account in Account.query.filter(Account.reseller_id == reseller.id):
                accounts.append(account)
        for sub_reseller in user.sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts
    elif user.role.name == "reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        for sub_reseller in user.sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts
    elif user.role.name == "sub_reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        return accounts
