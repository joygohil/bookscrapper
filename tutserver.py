#!flask/bin/python
from flask import Flask , jsonify;
from flask import request;
import requests;
import json;
import string;
from bs4 import BeautifulSoup;

app = Flask(__name__)

def getMirrorOneLink(link):
    page = requests.get(link);
    soup = BeautifulSoup(page.content,'html.parser');
    div = soup.find("div",{"class" : "book-info__download"});
    link = div.find("a").get('href');
    return link[9:];
def getMirrorTwoLink(link):
    page = requests.get(link);
    soup = BeautifulSoup(page.content,'html.parser');
    findATag = soup.findAll("a")[1];
    link = findATag.get('href');
    return link;


@app.route('/', methods=['GET','POST'])
def get_tasks():
    search = request.form.get("search").replace(" ", "+");
    print "LOG LINK "+"http://libgen.io/search.php?req="+search+"&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def";
    page = requests.get("http://libgen.io/search.php?req="+search+"&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def");
    soup = BeautifulSoup(page.content,'html.parser');
    outputList = [];
    table = soup.find("table", { "class" : "c" });
    for row in table.findAll("tr"):
        cells = row.findAll("td");
        output = {};
        if cells[6].getText() == "English" and cells[8].getText() == "pdf":
            output['authors'] = cells[1].getText();
            output['title'] = cells[2].getText().rstrip('0123456789, -');
            output['publisher'] = cells[3].getText();
            output['year'] = cells[4].getText();
            output['pages'] = cells[5].getText();
            output['language'] = cells[6].getText();
            output['size'] = cells[7].getText();
            output['mirror1'] = "https://libgen.pw/download/book"+getMirrorOneLink(cells[9].find('a').get('href'));
            #output['mirror2'] = getMirrorTwoLink(cells[10].find('a').get('href'));
            outputList.append(output);
            #t.add_row([authors,title,publisher,year,pages,language,size,mirror1,mirror2]);
    print(json.dumps(outputList));
    #return "Hey!";
    return json.dumps(outputList);

if __name__ == '__main__':
    #app.run(host='192.168.0.7',port=5000,ssl_context=('cert.pem','key.pem'))
    app.run(host='192.168.43.186',port=5000);
