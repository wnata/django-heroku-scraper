from django.core.management.base import BaseCommand

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from ...models import Job


class Command(BaseCommand):
    help = "collect jobs"

    # определяем логику команд
    def handle(self, *args, **options):

        # собираем html
        html = urlopen('https://jobs.lever.co/opencare')
        # преобразуем в soup-объект
        soup = BeautifulSoup(html, 'html.parser')

        # собираем все посты
        postings = soup.find_all("div", class_="posting")

        for p in postings:
            url = p.find('a', class_='posting-btn-submit')['href']
            title = p.find('h5').text
            location = p.find('span', class_='sort-by-location').text        # check if url in db
            try:
                # сохраняем в базе данных
                Job.objects.create(
                    url=url,
                    title=title,
                    location=location)
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))

        self.stdout.write('job complete')
