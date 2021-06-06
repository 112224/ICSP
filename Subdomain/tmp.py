from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import traceback
import requests
import os
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

url = 'http://www.mydomain.com/hithere?image=2934'


def sep(url):
    val = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    return val


print(sep(url))


