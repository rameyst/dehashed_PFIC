import math
import pandas as pd
import requests
from tabulate import tabulate


class Dehashed:
    def __init__(self, dehashed_api, dehashed_email):
        self.url = 'https://api.dehashed.com/search'  # url to query from dehashed.com
        self.api_token = dehashed_api  # api token to authenticate
        self.email = dehashed_email  # email for dehashed account

    def dehashed_query(self, keyword, datestamp):
        response_entries_list = []  # initiliaze list variable to contain all http responses from dehashed api call
        query_results_filename = '{}_Dehashed_Results.csv'.format(str(datestamp).replace(':', ''))

        print('URl: {}\nAPI_Token: {}'.format(self.url, self.api_token))
        query_value = '"{}"'.format(keyword)
        r = requests.get(self.url, params={'query': query_value},
                         auth=(self.email, self.api_token),
                         headers={'Accept': 'application/json'})

        total_records = r.json()['total']

        # Extend the entries response to the list. json()['entries'] returns a dict encapsulated in a list
        # Extend is used to format the response correctly into the list variable
        response_entries_list.extend(r.json()['entries'])

        print('checking total records: {}'.format(total_records))
        print('page_no: 1; {}; {}'.format(r.url, r))

        # logic for pagination. Dehashed returns 5000 rows in 1 request. Check total records returned
        # if greater than 5000, figure out how many pages and enumerate enumerate pages
        if total_records > 5000:
            total_pages = math.ceil(total_records/5000)  # calculate the number of pages. ceil rounds up
            for page_no in range(2, total_pages):  # starts at 2 and ends at total pages
                r = requests.get(self.url, params={'query': query_value, 'page': page_no},
                                 auth=(self.email, self.api_token),
                                 headers={'Accept': 'application/json'})
                print('page_no: {}; {}; {}'.format(page_no, r.url, r))

                # possible bug in returned http response which returns a 502 bad gateway response.
                # logic checks for 200 success to write the data. if not 200, it prints the page_no and exits
                if '200' in r:
                    response_entries_list.extend(r.json()['entries'])
                else:
                    print('page_no: {} skipped because of {}'.format(page_no, r))
                    break  # break out of the loop

        print('query complete')
        # create a pandas dataframe to save the results to csv
        df = pd.DataFrame(response_entries_list)
        df.to_csv(query_results_filename, index=False)
        # create a subset of the results dataframe to print to screen
        df_to_tabulate = df[['email', 'username', 'password', 'obtained_from']]
        print(tabulate(df_to_tabulate, headers='keys'))










