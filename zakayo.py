import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///testingb.db')
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
        citizens = (
            session.query(cls)
            .join(TaxDetails)
            .filter(cls.employer == employer)
            .all()
        )
        for citizen in citizens:
            print(f'Citizen: {citizen.first_name} {citizen.last_name}')
            print(f'Profession: {citizen.profession}')
            print(f'Salary: {citizen.salary}')
            print(f'Business Income: {citizen.business_income}')
            print(f'Total Income: {citizen.total_income}')
            print(f'Taxes to be Paid:')
            for tax_detail in citizen.tax_details:
                print(f'  Paye: {tax_detail.paye}')
                print(f'  Housing Levy: {tax_detail.housing_levy}')
                print(f'  Road Levy: {tax_detail.road_levy}')
                print(f'  Service Fee: {tax_detail.service_fee}')
                print(f'  Business Tax: {tax_detail.business_tax}')
                print(f'  Total Tax: {tax_detail.total_tax}')
            print('---')

    @classmethod
    def pay_tax(cls, citizen_id, personal_tax_paid, business_tax_paid, mpesa_code):
        citizen = session.get(cls, citizen_id)
        if citizen:
            total_tax = sum(tax.total_tax for tax in citizen.tax_details)
            taxes_paid = TaxesPaid(
                citizen=citizen,
                personal_tax_paid=personal_tax_paid,
                business_tax_paid=business_tax_paid,
                total_tax_paid=personal_tax_paid + business_tax_paid,
                taxes_left_to_pay=total_tax - (personal_tax_paid + business_tax_paid),
                mpesa_code=mpesa_code
            )
            session.add(taxes_paid)
            session.commit()
            print("Tax payment recorded successfully.")
        else:
            print("Citizen not found.")


    @classmethod
    def find_citizens_by_name(cls, first_name, last_name):
        citizens = (
            session.query(cls, TaxDetails)
            .join(TaxDetails)
            .filter(cls.first_name == first_name, cls.last_name == last_name)
            .all()
        )
        for citizen, tax_details in citizens:
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

    @classmethod
    def get_total_tax_paid(cls):
        total_tax_paid = 0.0
        taxes_paid = session.query(TaxesPaid).all()
        for tax_paid in taxes_paid:
            total_tax_paid += tax_paid.total_tax_paid
        return total_tax_paid
    
   
    

class TaxDetails(Base):
    __tablename__ = 'tax_details'
    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey('citizens.id'))
    first_name = Column(String)
    last_name = Column(String)
    paye = Column(Float)
    housing_levy = Column(Float)
    road_levy = Column(Float)
    service_fee = Column(Float)
    business_tax = Column(Float)
    total_tax = Column(Float)
    citizen = relationship('Citizen', back_populates='tax_details')

class TaxesPaid(Base):
    __tablename__ = 'taxes_paid'
    id = Column(Integer, primary_key=True)
    citizen_id = Column(Integer, ForeignKey('citizens.id'))
    personal_tax_paid = Column(Float)
    business_tax_paid = Column(Float)
    total_tax_paid = Column(Float)
    taxes_left_to_pay = Column(Float)
    mpesa_code = Column(String)  # Add the mpesa_code attribute
    citizen = relationship('Citizen', back_populates='taxes_paid')



def calculate_tax(total_income):
    # Perform tax calculation based on income
    paye = total_income * 0.3
    housing_levy = total_income * 0.02
    road_levy = total_income * 0.01
    service_fee = total_income * 0.015
    return paye, housing_levy, road_levy, service_fee


def populate_database():
    # Add seed citizens
    seed_citizens = [
        ('John', 'Doe', 'Engineer', 'ABC Inc.', 50000, 10000),
        ('Jane', 'Smith', 'Doctor', 'XYZ Hospital', 80000, 0),
        ('Bethwel', 'Kipruto', 'Software Developer', 'ZAKAYO SOFTWARES', 700000, 900000),
        ('Faith', 'Kilonzi', 'Software Developer', 'KENYA AIRWAYS LTD', 400000, 110000),
        ('Edgar', ' Obare', 'Content Creator', 'Self Employed', 10000, 1000)
    ]

    for citizen_data in seed_citizens:
        first_name, last_name, profession, employer, salary, business_income = citizen_data
        existing_citizen = session.query(Citizen).filter_by(
            first_name=first_name,
            last_name=last_name,
            employer=employer
        ).first()

        if not existing_citizen:
            total_income = salary + business_income
            paye, housing_levy, road_levy, service_fee = calculate_tax(total_income)
            total_tax = paye + housing_levy + road_levy + service_fee + (business_income * 0.35)
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
                first_name=first_name,
                last_name=last_name,
                paye=paye,
                housing_levy=housing_levy,
                road_levy=road_levy,
                service_fee=service_fee,
                business_tax=business_income * 0.35,
                total_tax=total_tax
            )
            session.add(citizen)
            session.add(tax_details)
            session.commit()


def create_tables():
    Base.metadata.create_all(engine)


def main_menu():
    print("Welcome to the Tax Tracking System!")
    print("Please select an option:")
    print("1. Proceed as Citizen")
    print("2. Proceed as Administrator")
    option = input("Enter your choice (1 or 2): ")
    if option == '1':
        citizen_menu()
    elif option == '2':
        administrator_menu()
    else:
        print("Invalid choice. Please try again.")
        main_menu()




def citizen_menu():
    citizen_id = input("Enter your ID: ")
    citizen = Citizen.get_citizen_by_id(citizen_id)
    if citizen:
        print(f'Citizen: {citizen.first_name} {citizen.last_name}')
        print(f'Profession: {citizen.profession}')
        print(f'Salary: {citizen.salary}')
        print(f'Business Income: {citizen.business_income}')
        print(f'Total Income: {citizen.total_income}')
        tax_details = citizen.tax_details
        if tax_details:
            print(f'Taxes to be Paid:')
            for tax_detail in tax_details:
                print(f'  Paye: {tax_detail.paye}')
                print(f'  Housing Levy: {tax_detail.housing_levy}')
                print(f'  Road Levy: {tax_detail.road_levy}')
                print(f'  Service Fee: {tax_detail.service_fee}')
                print(f'  Business Tax: {tax_detail.business_tax}')
                print(f'  Total Tax: {tax_detail.total_tax}')
            taxes_paid = citizen.taxes_paid
            if taxes_paid:
                print("Taxes Paid:")
                for tax_paid in taxes_paid:
                    print(f'  Personal Tax Paid: {tax_paid.personal_tax_paid}')
                    print(f'  Business Tax Paid: {tax_paid.business_tax_paid}')
                    print(f'  Total Tax Paid: {tax_paid.total_tax_paid}')
                    print(f'  Taxes Left to Pay: {tax_paid.taxes_left_to_pay}')
        else:
            print("No tax details found for this citizen.")

        print("Options:")
        print("1. Pay Personal Tax")
        print("2. Pay Business Tax")
        print("0. Go Back")
        option = input("Enter your choice (0-2): ")

        if option == '1':
            personal_tax = float(input("Enter the amount to pay for personal tax: "))
            mpesa_code = input("Input Mpesa Code/bank details to verify payment: ")
            Citizen.pay_tax(citizen_id, personal_tax, 0, mpesa_code)
            print("Personal tax payment successful.")
        elif option == '2':
            business_tax = float(input("Enter the amount to pay for business tax: "))
            mpesa_code = input("Input Mpesa Code/bank details to verify payment: ")
            Citizen.pay_tax(citizen_id, 0, business_tax, mpesa_code)
            print("Business tax payment successful.")
        elif option == '0':
            main_menu()  # Go back to the main menu
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Citizen not found.")
        main_menu()

def administrator_menu():
    print("Administrator Menu")
    print("Please select an option:")
    print("1. Get a Citizen by ID")
    print("2. Get Citizens working for a certain employer")
    print("3. Get tax details of all citizens")
    print("4. Get data on all citizens with paid taxes (in descending order of total tax paid)")
    print("5. REGISTER NEW CITIZEN")
    print("6. Total tax paid")
    print("7. Citizens with pending tax settlements")

    print("o.EXIT")
    option = input("Enter your desired service: ")
    if option == '1':
        citizen_id = input("Enter Citizen ID: ")
        citizen = Citizen.get_citizen_by_id(citizen_id)
        if citizen:
            print(f'Citizen: {citizen.first_name} {citizen.last_name}')
            print(f'Profession: {citizen.profession}')
            print(f'Salary: {citizen.salary}')
            print(f'Business Income: {citizen.business_income}')
            print(f'Total Income: {citizen.total_income}')
            tax_details = citizen.tax_details
            if tax_details:
                print(f'Taxes to be Paid:')
                for tax_detail in tax_details:
                    print(f'  Paye: {tax_detail.paye}')
                    print(f'  Housing Levy: {tax_detail.housing_levy}')
                    print(f'  Road Levy: {tax_detail.road_levy}')
                    print(f'  Service Fee: {tax_detail.service_fee}')
                    print(f'  Business Tax: {tax_detail.business_tax}')
                    print(f'  Total Tax: {tax_detail.total_tax}')
            else:
                print("No tax details found for this citizen.")
        else:
            print("Citizen not found.")
    elif option == '2':
        employer = input("Enter Employer Name: ")
        Citizen.find_citizens_by_employer(employer)
    elif option == '3':
        citizens = session.query(Citizen).all()
        for citizen in citizens:
            print(f'Citizen: {citizen.first_name} {citizen.last_name}')
            print(f'Profession: {citizen.profession}')
            print(f'Salary: {citizen.salary}')
            print(f'Business Income: {citizen.business_income}')
            print(f'Total Income: {citizen.total_income}')
            tax_details = citizen.tax_details
            if tax_details:
                print(f'Taxes to be Paid:')
                for tax_detail in tax_details:
                    print(f'  Paye: {tax_detail.paye}')
                    print(f'  Housing Levy: {tax_detail.housing_levy}')
                    print(f'  Road Levy: {tax_detail.road_levy}')
                    print(f'  Service Fee: {tax_detail.service_fee}')
                    print(f'  Business Tax: {tax_detail.business_tax}')
                    print(f'  Total Tax: {tax_detail.total_tax}')

            else:
             print("No tax details found for this citizen.")
            print('---')
    elif option == '4':
        citizens = session.query(Citizen).join(TaxesPaid).order_by(TaxesPaid.total_tax_paid.desc()).all()
        for citizen in citizens:
            print(f'Citizen: {citizen.first_name} {citizen.last_name}')
            print(f'Profession: {citizen.profession}')
            print(f'Salary: {citizen.salary}')
            print(f'Business Income: {citizen.business_income}')
            print(f'Total Income: {citizen.total_income}')
            taxes_paid = citizen.taxes_paid
            if taxes_paid:
                for tax_paid in taxes_paid:
                    print(f'Total Tax Paid: {tax_paid.total_tax_paid}')
            print('----')


    elif option == '5':
        register_new_citizen()

    elif option == '6':
        total_tax_paid = Citizen.get_total_tax_paid()
        print(f'Total Tax Paid: {total_tax_paid}')

    
    elif option == '7':
        unpaid_citizens = session.query(Citizen).\
            join(TaxesPaid).\
            filter(TaxesPaid.taxes_left_to_pay > 0).\
            all()
        
        if unpaid_citizens:
            print("Citizens with pending tax settlements:")
            for citizen in unpaid_citizens:
                print(f'Name: {citizen.first_name} {citizen.last_name}')
                print(f'Taxes Left to Pay: {citizen.taxes_paid[-1].taxes_left_to_pay}')
                print("---")
        else:
            print("No citizens found with pending tax settlements.")
       

    elif option == '0':
        main_menu()
    
    else:
        print("Invalid choice. Please try again.")
    main_menu()

def register_new_citizen():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    profession = input("Enter profession: ")
    employer = input("Enter employer: ")
    salary = float(input("Enter salary: "))
    business_income = float(input("Enter business income: "))

    existing_citizen = session.query(Citizen).filter_by(
        first_name=first_name,
        last_name=last_name, 
        employer=employer
    ).first()

    if existing_citizen:
        print("Citizen already exists.")
    else:
        total_income = salary + business_income
        paye, housing_levy, road_levy, service_fee = calculate_tax(total_income)
        total_tax = paye + housing_levy + road_levy + service_fee + (business_income * 0.35)
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
            first_name=first_name,
            last_name=last_name,
            paye=paye,
            housing_levy=housing_levy,
            road_levy=road_levy,
            service_fee=service_fee,
            business_tax=business_income * 0.35,
            total_tax=total_tax
        )
        session.add(citizen)
        session.add(tax_details)
        session.commit()
        print("New citizen registered successfully.")

    administrator_menu()  # Return to the administrator menu after registering a citizen


if __name__ == '__main__':
    create_tables()
    populate_database()
    main_menu()
