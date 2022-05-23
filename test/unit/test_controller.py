import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.controllers.controller import Controller
from src.util.user import UserAuthenticator

class TestControllerAdd:

    @pytest.fixture
    @patch('src.util.user.UserAuthenticator', autospec=True)
    def sut(self, mockUAuth, config):
        mockUser = mock.MagicMock()
        mockUser.get_subscription.return_value = config[0]
        mockUser.get_history.return_value = config[1]

        mockUAuth.return_value = mock.MagicMock()
        mockUAuth.return_value.get_user.return_value = mockUser

        return Controller()

    @pytest.mark.parametrize('config, message', [
        (("new", [[1, 2, 3], [1, 2, 3], [1], [1], [1]]), 'exploit alert'),
        (("new", [[1, 2], [1, 2], [1, 2], [1], [1]]), 'critical exploit alert'),
        (("new", [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1], [1]]), 'no exploit alert'),
        (("trusted", [[1, 2, 3], [1, 2, 3], [1], [1], [1]]), 'no reason for exploit checking'),
        (("trusted", [[1, 2], [1], [1], [1], [1]]), 'no reason for exploit checking'),
        (("trusted", [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1], [1]]), 'no reason for exploit checking'),
    ])
    def test_add_item_to_cart_check_message(self, sut, message, capsys):
        result = sut.add_item_to_cart(uid="123", item={'product': 'pc'})
        assert result
        output = str(capsys.readouterr().out).lower()
        assert message in output


class TestControllerCheckout:
    @patch('src.controllers.controller.UserAuthenticator', autospec=True)
    def test_get_total(self, mockUAuth):
        mockUser = mock.MagicMock()
        mockUser.get_cart.return_value = [{'product': 'p1', 'cost': 2}, {'product': 'p2', 'cost': 5}, {'product': 'p3', 'cost': 3}]

        mockUAuth.return_value = mock.MagicMock()
        mockUAuth.return_value.get_user.return_value = mockUser

        sut = Controller()

        assert sut.get_total(uid="123") == 10

    @pytest.mark.parametrize('config, expected', [
        ((7, "new"), None), ((8, "new"), None), ((9, "new"), "regular"), 
        ((47, "new"), None), ((48, "new"), None), ((49, "new"), "trusted"),
        ((7, "regular"), None), ((8, "regular"), None), ((9, "regular"), None), 
        ((47, "regular"), None), ((48, "regular"), None), ((49, "regular"), "trusted"),
        ((7, "trusted"), None), ((8, "trusted"), None), ((9, "trusted"), None), 
        ((47, "trusted"), None), ((48, "trusted"), None), ((49, "trusted"), None)
    ])
    def test_check_for_upgrade(self, config, expected):
        sut = Controller()
        assert sut.check_for_upgrade(history=[None]*config[0], current=config[1]) == expected

    def test_calculate_discount(self):
        sut = Controller()

        subscription_discount = {
            'new': 0,
            'regular': 5,
            'trusted': 15
        }

        for cartsize in [9, 10, 11]:
            for subscription in subscription_discount.keys():
                for gsale in [0, 10, 30]:
                    discount = sut.calculate_discount(cart=[None]*cartsize, subscription=subscription, gsale=gsale)

                    if gsale == 30:
                        assert discount == 30
                    else:
                        expected = gsale + (5 if cartsize > 9 else 0) + subscription_discount[subscription]
                        assert discount == expected

    @patch('src.controllers.controller.UserAuthenticator', autospec=True)
    def test_checkout(self, mockUAuth):
        mockUser = mock.MagicMock()
        mockUser.get_cart.return_value = [{'product': 'p1', 'cost': 2}, {'product': 'p2', 'cost': 5}, {'product': 'p3', 'cost': 3}]
        mockUser.get_history.return_value = [None]*35
        mockUser.get_subscription.return_value = 'regular'

        mockUAuth.return_value = mock.MagicMock()
        mockUAuth.return_value.get_user.return_value = mockUser

        sut = Controller()

        assert sut.checkout(uid='123') == 8.5