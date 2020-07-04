from django.test import SimpleTestCase
from django.urls import reverse, resolve
from stocks.views import get_most_active, StocksView, get_query_results


class TestUrlsStocks(SimpleTestCase):
    # test for functions
    def test_stocks_active_url(self):
        url = reverse('stocks-active')
        print('stocks-active ->', resolve(url))
        self.assertEquals(resolve(url).func, get_most_active)

    def test_stocks_query_url(self):
        url = reverse('stocks-query')
        print('stocks-query ->', resolve(url))
        self.assertEquals(resolve(url).func, get_query_results)

    # test for classes
    def test_stocks_screen_url(self):
        url = reverse('stocks-screen')
        print('stocks-screen ->', resolve(url))
        self.assertEquals(resolve(url).func.view_class, StocksView)