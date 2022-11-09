from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime

import pandas

from collections import defaultdict


def year_with_you(age):
    if (age%10==1) and (age != 11) and (age != 111) and (age != 211):
        return f'уже {age} год с вами'
    elif (age%10>1) and (age%10<5) and (age!=12) and (age!=13) and (age!=14):
        return f'уже {age} года с вами'
    else:
        return f'уже {age} лет с вами'

    
def main():
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

age_of_winery = datetime.datetime.now().year - 1920 

wines = pandas.read_excel('wine3.xlsx', keep_default_na=False).to_dict(orient='records')

all_drinks = defaultdict(list)

for wine in wines:
   all_drinks[wine['Категория']].append(wine) 

rendered_page = template.render(
    age_with_you = year_with_you(age_of_winery),
    all_drinks = all_drinks
)
print(all_drinks)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


if __name__ == '__main__':
    main()  
