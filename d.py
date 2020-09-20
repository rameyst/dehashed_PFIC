# python 3.8+ script to search dehashed.com and save results to csv file
# pip3 install -r requirements.txt

import datetime as dt
import modules.mods as mods
import argparse


if __name__ == '__main__':
    # Modify the following lines
    dehashed_email = ''
    dehashed_api = ''
    # ###################################

    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', help='keyword to search dehashed.com')
    args = parser.parse_args()

    if args.keyword:
        keyword = args.keyword
        datestamp = dt.datetime.now()
        print(datestamp, keyword)
        d = mods.Dehashed(dehashed_api, dehashed_email)
        d.dehashed_query(keyword, datestamp)


