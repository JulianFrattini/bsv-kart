class User:
    def __init__(self):
        return None

    def get_history(self, n: int=-1):
        raise NotImplementedError("This function is not yet implemented")

    def get_subscription(self):
        raise NotImplementedError("This function is not yet implemented")

    def set_subscription(self, subscription: str):
        raise NotImplementedError("This function is not yet implemented")

    def add_flag(self):
        raise NotImplementedError("This function is not yet implemented")

    def add_item_to_cart(self, item):
        raise NotImplementedError("This function is not yet implemented")

    def remove_item_from_cart(self, item):
        raise NotImplementedError("This function is not yet implemented")

    def get_cart(self):
        raise NotImplementedError("This function is not yet implemented")
    

class UserAuthenticator:
    def __init__(self):
        return None

    def get_user(self, uid: str):
        """Return the user with the given user_id

        returns: 
            user -- user object from the database

        raises:
            Exception -- if the user cannot be found or the database is not connected
        """
        raise NotImplementedError("This function is not yet implemented")