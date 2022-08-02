import unittest
from unittest import mock
import json

import sys
sys.path.append('..')
from src.harmonysite.harmony_site import HarmonySite

TOKENRESPONSEOK = {
    '@attributes': {'status': None},
    'token': 'dummyToken'
}
TOKENRESPONSEBAD = {
    '@attributes': {'status': 'error'},
    'error': 'failed to get token'
}
BROWSERESPONSEBAD = {
    '@attributes': {'status': 'error'},
    'error': 'unknown browse error'
}

BROWSERESPONSEGOOD= {
    "@attributes":{"status":"okay"},
    "records":{
        "@attributes":{"singular":"photo gallery","plural":"galleries","available":"2","count":"2"},
        "photo_gallery":[
            {"@attributes":{"index":"1"},"id":"1","Name":"n1","Description":{}},
            {"@attributes":{"index":"2"},"id":"2","Name":"n2", "Description":{}}
        ]
    }
}

class TestHarmonySite(unittest.TestCase):

    @property
    def configured_api(self):
        self._set_response(TOKENRESPONSEOK)
        return HarmonySite(self.mockSession, 'http://url', 'user', 'password')

    def setUp(self):
        # __enter__ and __exit__ so "using" works
        self.mockResponse = mock.Mock(__enter__=lambda _: self.mockResponse, __exit__=lambda _1, _2, _3, _4: None)

        self.mockSession = mock.Mock()
        self.mockSession.post.return_value = self.mockResponse

    def _set_response(self, value):
        type(self.mockResponse).text= mock.PropertyMock(return_value=json.dumps(value))

    def test_constructor_does_not_throw_good_token(self):
        self._set_response(TOKENRESPONSEOK)
        try:
            hs = HarmonySite(self.mockSession, 'http://url', 'user', 'password')
        except Exception:
            self.fail()

    def test_constructor_throws_bad_token(self):
        self._set_response(TOKENRESPONSEBAD)
        self.assertRaises(ConnectionRefusedError,lambda: HarmonySite(self.mockSession, 'http://url', 'user', 'password'))

    def test_constructor_sets_token(self):
        self._set_response(TOKENRESPONSEOK)
        hs = HarmonySite(self.mockSession, 'http://url', 'user', 'password')
        self.assertEqual(hs._token, 'dummyToken')

    def test_browse_throws_if_bad_response(self):
        hs = self.configured_api
        self._set_response(BROWSERESPONSEBAD)
        self.assertRaises(ConnectionRefusedError,lambda: hs.browse('table').__next__())

    def test_browse_returns_data(self):
        hs = self.configured_api
        self._set_response(BROWSERESPONSEGOOD)
        rows = [row for row in hs.browse('table')]
        self.assertEqual(len(rows), 2)


if __name__ == '__main__':
    unittest.main()