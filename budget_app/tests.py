from django.test import TestCase
from .forms import TransactionForm

class TransactionFormTest(TestCase):
    
    def test_clean_amount(self):
        form = TransactionForm({'amount': -10, 'transaction_type': 'E', 'description': 'test', 'date': '2022-01-01'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['amount'], ['Сумма должна быть положительной'])

