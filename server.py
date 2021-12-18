from sanic import Sanic
from sanic import response
import json

from sanic.signals import RESERVED_NAMESPACES

app = Sanic("Search Program")

testPath = 'D:\\programs\\py\\test.txt'
def takeSecond(elem):
    return elem[1]

@app.route("/search")
async def search(request):
    listans = []
    start = int(request.args['start'][0])
    end = int(request.args['end'][0])
    if start < 1880 or start > 2020:
        return response.text({"Error: no start!"})
    if end < 1880 or end > 2020:
        return response.text({"Error: no end!"})
    if end < start:
        return response.text({"Error: time reverse!"})
    with open(testPath,'r') as f:
        list1 = f.readlines()
    for linestring in list1:
        if linestring[0] >= '0' and linestring[0] <='9':
            year,land,ocean = linestring.rstrip().split()
            year,land,ocean = int(year),float(land),float(ocean)
            if year <= end and year >= start:
                listans.append([year,land])
    
    if request.args['cmp'][0] == 'up':
        listans.sort(key = takeSecond,reverse = False)
    else:
        listans.sort(key = takeSecond,reverse = True)
    if request.args['form'][0] == 'JSON':
        JsonAarry = dict()
        for item in listans:
            JsonAarry[item[0]] = item[1]
        return response.json(JsonAarry)
    elif request.args['form'][0] == 'XML':
        XMLAarry = '<Result list>\n'
        for item in listans:
            XMLAarry = XMLAarry + '<year title=%d> <temperature> %s </temperature> </year>\n' % (item[0],str(item[1]))
        XMLAarry = XMLAarry + '</Result list>\n'
        return response.text(XMLAarry)
    else:
        CSVString = 'year,temperature\n'
        for item in listans:
            CSVString = CSVString + str(item[0]) + ',' + str(item[1]) + '\n'
        return response.text(CSVString)



@app.route("/")
async def test(request):    
    return response.json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)

    #http://127.0.0.1:8000/search?start=1900&end=2000&cmp=up&form=CSV