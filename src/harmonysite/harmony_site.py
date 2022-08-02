import json
import requests

class HarmonySite:
    """
    Access to the HarmonySite API
    
    see https://harmonysite.freshdesk.com/support/solutions/articles/43000590537-api-application-programming-interface

    Methods
    -------
    browse(table, page_number=0, page_size=5)
    """

    def __init__(self, session: requests.Session, api_url: str, username: str, password: str):
        """
        Parameters
        ----------
        session: requests.Session to handle cookies etc
        api_url : str
            This can be found from your harmony site under Admin -> Test the Harmony Site API
        username : str
        password : str
        """
        self._url = api_url
        self._session = session
        self._token = self._get_token(username, password)

    @classmethod
    def build(self, api_url: str, username: str, password: str):
        """
        returns instance of API class with dependencies injected

        Parameters
        ----------
        api_url : str
            This can be found from your harmony site under Admin -> Test the Harmony Site API
        username : str
        password : str
        
        Returns
        -------
        Instantiated API object
        """
        return (requests.Session(), api_url, username, password)

    def _get_token(self, username, password):
        request_data = {
            'output': 'json',
            'endpoint': 'authorise',
            'username': username,
            'password': password,
        }
        return self._result(request_data)['token']

    def _result(self, request_data):
        with self._session.post(url=self._url, data=request_data) as response:
            result_data = json.loads(response.text)
            if result_data['@attributes']['status'] == 'error':
                raise ConnectionRefusedError(result_data['error'])
            del result_data['@attributes']
            return result_data

    def browse(self, table, page_number=0, page_size=5):
        """
        Parameters
        ----------
        table : str
            The HarmonySite table to query
        page_number : int, optional, default 0
        page_size : int, optional, default 5
        
        Returns
        -------
        generator, which yields each table row as a dictionary of values
        """
        start = (page_number * page_size) + 1
        req_data = {
            'output': 'json',
            'raw': 1,
            'endpoint': 'browse',
            'token': self._token,
            'table': table,
            'start': start,
            'n': page_size
            }

        if req_data['start'] == 1:    # workaround for API bug
            del req_data['start']
        
        records = self._result(req_data)['records']
        if records['@attributes']['count'] == '0': return

        key = records['@attributes']['singular'].replace(' ', '_')  # get the correct key name

        #  iterate over records
        for row in records[key]:
            del row['@attributes']  # remove metadata

            # replace empty dicts with None
            for k,v in row.items():
                if type(v) is dict and not(v):
                    row[k] = None
            yield row
