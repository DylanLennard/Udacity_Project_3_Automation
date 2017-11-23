# -*- coding: utf-8 -*-

import requests


def get_XML_data(URL, FILENAME):

    # request needs to stream data instead of reading in all at once
    r = requests.get(URL, stream=True)

    try:
        # print the URL to debug in event that error gets thrown
        print("Request URL:", r.url)

        # Throw an error for bad status codes
        r.raise_for_status()

        # use iter_lines to parse each line one by one
        events = r.iter_lines()

        # write each line, line by line, into a write file
        with open(FILENAME, 'w') as f:
            for line in events:
                f.write(line.decode('utf-8'))
                f.write("\n")  # this is necessary to correctly format the file

        # success messages
        print("File write was success!")
        print("If this was a sample test set, open the file")
        print("to make sure data looks complete")

    except Exception as e:
        print(e)

    finally:
        r.close()
