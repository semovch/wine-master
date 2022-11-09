import argparse

import datetime

from collections import defaultdict

import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def count_age(age):
    if (age%10==1) and (age != 11) and (age != 111) and (age != 211):
        return f'уже {age} год с вами'
    elif (age%10>1) and (age%10<5) and (age!=12) and (age!=13) and (age!=14):
        return f'уже {age} года с вами'
    else:
        return f'уже {age} лет с вами'

    
def main():
    parser = argparse.ArgumentParser(
        description='путь к файлу'
    )
    parser.add_argument('--path', help='введите путь к файлу', default = 'wine.xlsx')
    args = parser.parse_args()
    path = args.path
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    year_of_foundation = 1920 

    winery_age = datetime.datetime.now().year - year_of_foundation 

    wines = pandas.read_excel('wine.xlsx', keep_default_na=False).to_dict(orient='records')

    all_drinks = defaultdict(list)

    for wine in wines:
        all_drinks[wine['Категория']].append(wine) 

    rendered_page = template.render(
        age_with_you = count_age(winery_age),
        all_drinks = all_drinks
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()  
