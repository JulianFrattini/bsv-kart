from src.util.user import UserAuthenticator
from src.util.globals import get_global_variable as ggv

class Controller:

    def __init__(self):
        """Initialize a controller with a dependency on the user authenticator, which resolves user IDs and returns the actual user from an external database.
        """
        self.uauth = UserAuthenticator()

    def add_item_to_cart(self, uid: str, item: object):
        """Add the given item to the cart of the user if the user exists. Also, check the purchase history of the user to identify possible exploits according to the rules: if the five most recent purchases contained either two or less items, or if the three of the five most recent purchases contained only one item, raise an exploit alert.

        parameters:
            uid -- unique identifier of the user
            item -- item to be added to the users cart

        returns:
            True -- on success

        raises:
            Exception -- if no user is associated to the given user id
        """

        user = self.uauth.get_user(uid)

        # check for potential exploits
        history = user.get_history(n=5)
        if user.get_subscription() in ['new', 'regular']:
            # find potential exploits:
            singular_purchases = [purchase for purchase in history if len(purchase)== 1]
            if len(singular_purchases) >= 3:
                user.add_flag()
                
                print(f'Exploit alert: The recent purchase history of user {uid} contains several singular purchases.')
            else:
                if all(len(purchase)<=2 for purchase in history):
                    user.add_flag()
                    user.add_flag()

                    print(f'Critical exploit alert: The recent purchase history of user {uid} contains only purchases with 2 or less items.')
                else:
                    print(f'No exploit alert for user {uid}')
        else:
            print(f'User {uid} is trusted; no reason for exploit checking')

        user.add_item_to_cart(item)
        return True

    def remove_item_from_cart(self, uid: str, item: object):
        """Remove an item from the cart of a user.
        
        parameters:
            uid -- unique identifier of the user
            item -- item to be added to the users cart
        """
        user = self.uauth.get_user(uid)
        user.remove_item_from_cart(item)

    def checkout (self, uid: str):
        """Perform a checkout for the user. This includes checking for a subscription upgrade, calculating the total discount, and calculating the final amount the cart requires to pay

        parameters:
            uid -- unique identifier of the user
        
        returns:
            total -- total amount the cart is worth with discount
        """
        total = self.get_total(uid=uid)
        user = self.uauth.get_user(uid)

        # check for a potential subscription upgrade
        upgrade = self.check_for_upgrade(history=user.get_history(n=-1), current=user.get_subscription())
        if upgrade:
            user.set_subscription(upgrade)

        cart = user.get_cart()
        discount = self.calculate_discount(cart=cart, subscription=user.get_subscription(), gsale=ggv('global sale'))

        return total*(100-discount)/100.0

    def get_total(self, uid):
        """Calculate the total amount of money the contents of the cart of a user are worth (exluding discounts)

        parameters:
            uid -- unique identifier of the user
        
        returns:
            total -- total amount the cart is worth without discount        
        """
        user = self.uauth.get_user(uid)
        cart = user.get_cart()

        total = sum(item['cost'] for item in cart)

        return total

    def check_for_upgrade(self, history: list, current: str):
        """Given the purchase history and the current subscription of a user, determine if the subscription can be upgraded with one more purchase.

        parameters:
            history -- list of previous purchases
            current -- current subscription tier

        returns:
            str -- new subscription tier in case an upgrade is possible
            None -- in case no upgrade is possible        
        """
        if len(history) == 9 and current == "new":
            return "regular"
        elif len(history) == 49 and current in ["regular", "new"]:
            return "trusted"
        return None

    def calculate_discount(self, cart: list, subscription: str, gsale: int):
        """Calculate the total discount that applies to a cart of a user with the given subscription as well as the global sale.

        parameters:
            cart -- list of items in the cart
            subscription -- current subscription tier
            gsale -- current global sale

        returns 
            total -- total discount
        """
        if gsale == 30:
            return 30
        
        discount = gsale

        if len(cart) > 9:
            discount += 5

        if subscription == "regular":
            discount += 5
        elif subscription == "trusted":
            discount += 15

        return discount