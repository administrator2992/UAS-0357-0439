from faker import Faker
import random
from profiles import db, News
import sys

def create_fake_news(n):
    faker = Faker()
    leker = Faker()
    for _ in range(n):
        profil = News(title=faker.text(), content=leker.text(), flag=random.randint(0, 2), created_by=3)
        db.session.add(profil)
    db.session.commit()

    print(f'Addes {n} fake news to database')

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of news you want to create as an argument.')
        sys.exit(1)
    create_fake_news(int(sys.argv[1]))