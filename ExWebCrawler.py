from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
try:
    html = urlopen("http://yj1.b96dure93e9.xyz/pw/thread.php?fid=3")
except (HTTPError, URLError) as e:
    print(e)
else:

    bs0bj = BeautifulSoup(html.read(), features="lxml")
    print(bs0bj.h1)
