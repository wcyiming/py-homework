import aiohttp
import asyncio
import json
import math
import pylab
import numpy
import statsmodels.api as smp
lowess = smp.nonparametric.lowess

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    # startYear = input("Enter start year:\n")
    # endYear = input("Enter end year:\n")
    # cmp = input("Enter compare mod(up/down):\n")
    # form = input("Enter form(JSON/XML/CSV):\n")
    startYear=1880
    endYear=2020
    cmp="up"
    form="JSON"
    params = {'start': startYear, 'end': endYear, 'cmp': cmp, 'form': form}
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/search',
                            params=params) as resp:
            expect = 'http://127.0.0.1:8000/search?start=%s&end=%s&cmp=%s&form=%s' % (startYear, endYear, cmp, form)
            assert str(resp.url) == expect
            X=[]
            Y=[]
            if form == 'JSON':
                json1 = await resp.json()
                for key,value in json1.items():
                    X.append(key)
                    Y.append(value)
            elif form == 'XML':
                str2 = await resp.text()
                print(str2.replace("<year title=", "").replace("> <temperature>", "")
                      .replace(" </temperature> </year>",""))
            else:
                str3 = await resp.text()
                print(str3.replace(",", " "))
            X, Y = (list(t) for t in zip(*sorted(zip(X, Y))))
            x = numpy.array(X, dtype='i')
            y = numpy.array(Y, dtype='f')
            yest = lowess(y, x, frac = 10 / 140)
            for i in yest:
                print(int(i[0]),round(i[1],5))
            pylab.clf()
            pylab.plot(x, y, label='origin')
            pylab.plot(x, yest[:,1], label='processed')
            pylab.legend()
            pylab.show()
            

asyncio.run(main())