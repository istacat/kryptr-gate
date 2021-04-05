from app.models import User, Account, Subordinate


class Admin:
    @staticmethod
    def get_distributors():
        query = User.query.filter(User.role == 'distributor')
        return query

    @staticmethod
    def get_resellers():
        query = User.query.filter(User.role == 'reseller')
        return query

    @staticmethod
    def get_subresellers():
        query = User.query.filter(User.role == 'sub_resseler')
        return query

    @staticmethod
    def get_accounts():
        query = Account.query.all()
        return query


class Distributor:
    @staticmethod
    def get_resellers(distrib_id):
        sub_query = Subordinate.query.filter(Subordinate.chief_id == distrib_id)
        query = []
        for relation in sub_query:
            user = User.query.get(relation.subordinate_id)
            query.append(user)
        return query

    @staticmethod
    def get_sub_resellers(resellers):
        query = []
        for reseller in resellers:
            new_query = Subordinate.query.filter(Subordinate.chief_id == reseller.id)
            for relation in new_query:
                user = User.query.get(relation.subordinate_id)
                query.append(user)
        return query

    @staticmethod
    def get_accounts(distrib_id, resellers, sub_resellers):
        accounts = []
        for account in Account.query.filter(Account.reseller_id == distrib_id):
            accounts.append(account)
        for reseller in resellers:
            for account in Account.query.filter(Account.reseller_id == reseller.id):
                accounts.append(account)
        for sub_reseller in sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts


class Reseller:
    @staticmethod
    def get_sub_resellers(reseller_id):
        sub_query = Subordinate.query.filter(Subordinate.chief_id == reseller_id)
        query = []
        for relation in sub_query:
            user = User.query.get(relation.subordinate_id)
            query.append(user)
        return query

    @staticmethod
    def get_accounts(reseller_id, sub_resellers):
        accounts = []
        for account in Account.query.filter(Account.reseller_id == reseller_id):
            accounts.append(account)
        for sub_reseller in sub_resellers:
            for account in Account.query.filter(Account.reseller_id == sub_reseller.id):
                accounts.append(account)
        return accounts


class SubReseller:
    @staticmethod
    def get_accounts(sub_reseller_id):
        query = Account.query.filter(Account.reseller_id == sub_reseller_id)
        return query
