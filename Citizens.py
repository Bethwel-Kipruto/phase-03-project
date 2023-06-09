import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///revenue_system.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Citizen(Base):
    __tablename__ = 'citizens'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    profession = Column(String)
    employer = Column(String)
    salary = Column(Float)
    business_income = Column(Float)
    total_income = Column(Float)
    tax_details = relationship('TaxDetails', back_populates='citizen')
    taxes_paid = relationship('TaxesPaid', back_populates='citizen')

    @classmethod
    def get_citizen_by_id(cls, citizen_id):
        return session.get(cls, citizen_id)
    
    @classmethod
    def find_citizens_by_employer(cls, employer):
        citizens = session.query(cls).filter_by(employer=employer).all()
        for citizen in citizens:
            tax_details = session.query(TaxDetails).filter_by(citizen_id=citizen.id).first()
            if tax_details:
                print(f'Citizen: {citizen.first_name} {citizen.last_name}')
                print(f'Profession: {citizen.profession}')
                print(f'Salary: {citizen.salary}')
                print(f'Business Income: {citizen.business_income}')
                print(f'Total Income: {citizen.total_income}')
                print(f'Taxes to be Paid:')
                print(f'  Paye: {tax_details.paye}')
                print(f'  Housing Levy: {tax_details.housing_levy}')
                print(f'  Road Levy: {tax_details.road_levy}')
                print(f'  Service Fee: {tax_details.service_fee}')
                print(f'  Business Tax: {tax_details.business_tax}')
                print(f'  Total Tax: {tax_details.total_tax}')
                print('---')
            else:
                print(f'No tax details found for Citizen: {citizen.first_name} {citizen.last_name}')


class TaxDetails(Base):
    __tablename__ = 'tax_details'
    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey('citizens.id'))
    citizen = relationship('Citizen', back_populates='tax_details')
    paye = Column(Float)
    housing_levy = Column(Float)
    road_levy = Column(Float)
    service_fee = Column(Float)
    business_tax = Column(Float)
    total_tax = Column(Float)


class TaxesPaid(Base):
    __tablename__ = 'taxes_paid'
    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey('citizens.id'))
    citizen = relationship('Citizen', back_populates='taxes_paid')
    personal_tax_paid = Column(Float)
    business_tax_paid = Column(Float)
    total_tax_paid = Column(Float)


Base.metadata.create_all(engine)


def calculate_tax(total_income):
    if total_income < 100000:
        paye = total_income * 0.35
    else:
        paye = total_income * 0.4
    housing_levy = total_income * 0.035
    road_levy = total_income * 0.02
    service_fee = total_income * 0.02
    return paye, housing_levy, road_levy, service_fee


def add_citizen(first_name, last_name, profession, employer, salary, business_income):
    total_income = salary + business_income
    paye, housing_levy, road_levy, service_fee = calculate_tax(total_income)
    citizen = Citizen(
        first_name=first_name,
        last_name=last_name,
        profession=profession,
        employer=employer,
        salary=salary,
        business_income=business_income,
        total_income=total_income
    )
    tax_details = TaxDetails(
        citizen=citizen,
        paye=paye,
        housing_levy=housing_levy,
        road_levy=road_levy,
        service_fee=service_fee,
        business_tax=business_income * 0.35,
        total_tax=paye + housing_levy + road_levy + service_fee + (business_income * 0.35)
    )
    taxes_paid = TaxesPaid(
        citizen=citizen,
        personal_tax_paid=paye,
        business_tax_paid=business_income * 0.35,
        total_tax_paid=paye + (business_income * 0.35)
    )
    session.add(citizen)
    session.add(tax_details)
    session.add(taxes_paid)

# def pay_tax(citizen_id, personal_tax_paid, business_tax_paid):
#     citizen = session.query(Citizen).get(citizen_id)
#     if citizen:
#         taxes_paid = TaxesPaid(
#             citizen=citizen,
#             personal_tax_paid=personal_tax_paid,
#             business_tax_paid=business_tax_paid,
#             total_tax_paid=personal_tax_paid + business_tax_paid
#         )
#         session.add(taxes_paid)
#         session.commit()
#         print("Tax payment recorded successfully.")
#     else:
#         print("Citizen not found.")


# pay_tax(1, 5000, 2500)  # Paying tax for citizen with ID 1

def populate_database():
    # Add seed citizens
    add_citizen('John', 'Doe', 'Engineer', 'ABC Inc.', 50000, 10000)
    add_citizen('Jane', 'Smith', 'Doctor', 'XYZ Hospital', 80000, 0)

    # Commit the changes
    session.commit()

# # Call the seed function to populate the initial data
# populate_database()


# # Adding users with modified tax payment information
# add_citizen('John', 'Doe', 'Engineer', 'ABC Inc.', 50000, 10000)
# add_citizen('Jane', 'Smith', 'Doctor', 'XYZ Hospital', 80000, 0)

# Print the updated records
for citizen in session.query(Citizen).all():
    if citizen.taxes_paid:
        print(f'{citizen.first_name} {citizen.last_name} - Total Tax Paid: {citizen.taxes_paid[0].total_tax_paid}')
    else:
        print(f'{citizen.first_name} {citizen.last_name} - No tax payment records')

session.commit()

#finding a citizen's details and tax information uisng their ID
citizen = Citizen.get_citizen_by_id(1)
if citizen:
    print(f"Found citizen: {citizen.first_name} {citizen.last_name}")
else:
    print("Citizen not found.")

#Trying to find all employees of a certain organization/employer and their tax details
Citizen.find_citizens_by_employer('ABC Inc.')




