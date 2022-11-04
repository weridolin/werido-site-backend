class UserPermission:

    @staticmethod
    def permission_key(user,uuid):
        return f"rbac.{user.id}_{uuid}"