import os
from datetime import datetime
from IPython.parallel import Client

rc = Client(packer="pickle")
dview = rc[:]
print rc.ids


@dview.remote(block=True)
def fetch(year):
    import os
    directory = "/mnt/sgeadmin/{}".format(year)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for f in files:
        fname = f.split("/")
        os.system("cd {0}; wget {1}; unzip {2}".format(directory, f, fname))

r = open("../lib/alchemy/urls.txt", "wb")
r = eval(r.readline())

for year in xrange(2005, 2014):
    print year, datetime.now()
    dview.scatter("files", r[year])
    fetch(year)
