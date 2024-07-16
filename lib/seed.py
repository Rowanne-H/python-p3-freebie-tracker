#!/usr/bin/env python3
from faker import Faker
import random 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def create_companies():
    companies = []
    for i in range(10):
        company = Company(
            name = fake.unique.company(),
            founding_year = random.randint(1986, 2024)
        )
        companies.append(company) 
            
    session.add_all(companies)
    session.commit()
    return companies
        
    
def create_devs():
    devs = []
    for i in range(10):
        dev = Dev(
          name = fake.unique.name()  
        )
        devs.append(dev)

    session.add_all(devs)
    session.commit()
    return devs

def create_freebies():
    freebies = []
    for i in range(50):
        freebie = Freebie(
            item_name = fake.unique.name(),
            value = random.randint(1, 100)
        ) 
        freebies.append(freebie)
    session.add_all(freebies)
    session.commit()
    return freebies

def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

def relate_one_to_many(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = random.choice(companies)
        freebie.dev = random.choice(devs)

    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies

if __name__ == '__main__':
    delete_records()
    companies  = create_companies()
    devs = create_devs()
    freebies = create_freebies()
    companies, devs, freebies = relate_one_to_many(companies, devs, freebies)