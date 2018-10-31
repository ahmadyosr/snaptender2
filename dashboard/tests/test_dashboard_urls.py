from django.test import TestCase

class PollsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/dashboard/')
        resp1 = self.client.get('/dashboard/upload/')
        resp2 = self.client.get('/dashboard/login/')
        resp3 = self.client.get('/dashboard/snippets/')
        print('tset' )
        self.assertTrue(resp.status_code in (200 , 302))
        self.assertTrue(resp1.status_code in (200 , 302))
        self.assertTrue(resp2.status_code in (200 , 302))
        self.assertTrue(resp3.status_code in (200 , 302))



