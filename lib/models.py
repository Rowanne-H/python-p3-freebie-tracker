from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref='company')
    devs = association_proxy('freebies', 'dev', 
                               creator=lambda de: Freebie(dev=de))

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(
            item_name = item_name,
            dev_id = dev.id,
            value = value,
            company_id = self.id
        )
        return freebie
    
    def oldest_company(self):
        oldest_company=session.query(Company).order_by(Company.founding_year).first()
        return oldest_company.founding_year

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref='dev')
    companies = association_proxy('freebies', 'company', 
                               creator=lambda co: Freebie(company=co))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False
        
    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
