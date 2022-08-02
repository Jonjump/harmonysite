# Harmony Site

[HarmonySite](https://www.harmonysite.com/) provides management AND a website for your choir, orchestra etc.

This package simplifies use of the 
[Harmony Site API](https://harmonysite.freshdesk.com/support/solutions/articles/43000590537-api-application-programming-interface),
from python.  It was originally built for [London Welsh Rugby Club Choir](https://www.lwrcc.uk).  If you have access to a harmony site and the appropriate permissions, you can get started (and check you have the basics working);
all the information on how to do that is [here](https://harmonysite.freshdesk.com/support/solutions/articles/43000590537-api-application-programming-interface).

# Setup
DO NOT use your ordinary credentials for access!  Get a specific login set up.
- This needs to be done by a website admin.
- Note that at present, I find it easier to create a new login than duplicate an existing one.
- It's OK to select "Not Specified" for "member"; members and logins are separate things.
- Use "Data Administration Access" - and specifiy ONLY the tables you need.
- Obviously, set a good password.  Use least 16 characters, and a random password generator.

# Notes
- The API is, at present, read only.
- A nice way to make use of the API is using [Google's Colab](https://colab.research.google.com/?utm_source=scs-index).
That way you don't have to install anything locally, and you can keep notebooks in a google drive.
- you can [book the world-famous London Welsh Rugby Club Choir for your event](https://www.lwrcc.uk/dbpage.php?pg=bookings) 
or come along and [join us](https://www.lwrcc.uk/dbpage.php?pg=membership).

# Where to get it
The source code is currently hosted on GitHub at: https://github.com/jonjump/harmonysite

Binary installers for the latest released version is available at the Python Package Index (PyPI).

`pip install pandas`

# Getting Started
```
from harmonysite import HarmonySite

hs = HarmonySite.build("<your api url>", "<username>", "<password>")
for record in hs.browse("a table name"):
    print (record)
```


# With Pandas
You may well wish to use pandas to access the API - this provides a nice way of performing operations on data tables, 
and works very well, particularly with colab.  In order to avoid this small package pulling in a large dependency, 
panda code is not included, but a very simple way to do it is this ...
```
from harmonysite import HarmonySite
import pandas as pd


hs = HarmonySite.build("<your api url>", "<username>", "<password>")
def dataframe(table_name):
    df = pd.DataFrame.from_records(
         hs.browse(table_name, page=0, page_size=9999999),
         index=idColumn
    )
    if filterColumns:
        return df.filter(filterColumns)
    return df

data = dataframe('<your table name>')
``` 

# Don't Forget
Support the [London Welsh Rugby Club Choir](https://lwrcc.uk)
