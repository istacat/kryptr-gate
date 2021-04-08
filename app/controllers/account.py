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


# def get_resellers(user):
#     """Get resellers by roles and subordinates"""
#     if user.role == "admin":
#         query = User.query.filter(User.role == "reseller")
#         return query
#     elif user.role == "distributor":
#         query = []
#         sub_query = Subordinate.query.filter(Subordinate.chief_id == user.id)
#         for relation in sub_query:
#             user = User.query.get(relation.subordinate_id)
#             if user.role == 'reseller':
#                 query.append(user)
#         return query


# def get_sub_resellers(user):
#     """Get sub_resellers by roles and subordinates"""
#     if user.role == "admin":
#         query = User.query.filter(User.role == "sub_reseller")
#         return query
#     elif user.role == "distributor":
#         query = []
#         new_query = Subordinate.query.filter(Subordinate.chief_id == user.id)
#         for reseller in user.resellers:
#             new_query = Subordinate.query.filter(Subordinate.chief_id == reseller.id)
#             for relation in new_query:
#                 user = User.query.get(relation.subordinate_id)
#                 query.append(user)
#         sub_query = Subordinate.query.filter(Subordinate.chief_id == user.id)
#         for relation in sub_query:
#             user = User.query.get(relation.subordinate_id)
#             if user.role == 'sub_reseller':
#                 query.append(user)
#         return query
#     elif user.role == 'reseller':
#         query = []
#         for sub_reseller in user.sub_resellers:
#             new_query = Subordinate.query.filter(Subordinate.chief_id == sub_reseller.id)
#             for relation in new_query:
#                 user = User.query.get(relation.subordinate_id)
#                 query.append(user)
#         return query


def get_accounts(user):
    """Get accounts by roles and subordinates"""
    if user.role == "admin" or user.role == "support":
        return Account.query.all()
    elif user.role == "distributor":
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
    elif user.role == "reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        for sub_reseller in user.sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts
    elif user.role == "sub_reseller":
        accounts = []
        for account in Account.query.filter(Account.reseller_id == user.id):
            accounts.append(account)
        return accounts
