from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker,declarative_base
import click
from tabulate import tabulate
# Create a SQL database (change the connection string as needed)
DATABASE_URL = "sqlite:///student.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    roll_number = Column(Integer, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)  # Add this line
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)

# Create the database tables
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define functions to manage student information

def ADD_STUDENT_INFORMATION():
    print("ADDING STUDENT INFORMATION : \n")
    NAME = input("ENTER STUDENT NAME: ").strip().upper()
    ROLL_NUMBER = int(input("ENTER STUDENT ROLL NUMBER: "))
    AGE = int(input("ENTER STUDENT AGE: "))
    CLASS = input("ENTER STUDENT CLASS: ").strip().upper()
    EMAIL_ID = input("ENTER STUDENT E-MAIL ID: ").strip().upper()
    ADDRESS = input("ENTER STUDENT ADDRESS: ").strip().upper()
    MOBILE_NUMBER = input("ENTER STUDENT MOBILE NUMBER: ").strip()

    student = Student(
        name=NAME,
        roll_number=ROLL_NUMBER,
        age=AGE,
        class_name=CLASS,
        email=EMAIL_ID,
        address=ADDRESS,
        mobile_number=MOBILE_NUMBER
    )

    session.add(student)
    session.commit()
    print("\n")
    print("\t STUDENT INFORMATION ADDED SUCCESSFULLY.")
    print("\n")

def DELETE_STUDENT_INFORMATION():
    print("DELETING STUDENT INFORMATION : \n")
    ROLL_NUMBER = int(input("ENTER STUDENT ROLL NUMBER TO DELETE: "))

    student = session.query(Student).filter_by(roll_number=ROLL_NUMBER).first()
    if student:
        session.delete(student)
        session.commit()
        print("\n")
        print("\t STUDENT INFORMATION DELETED SUCCESSFULLY.")
        print("\n")
    else:
        print("\n")
        print("\t STUDENT WITH ROLL NUMBER {} NOT FOUND.".format(ROLL_NUMBER))
        print("\n")

def UPDATE_STUDENT_INFORMATION():
    print("UPDATE STUDENT INFORMATION : \n")
    ROLL_NUMBER = int(input("ENTER STUDENT ROLL NUMBER TO UPDATE: "))

    student = session.query(Student).filter_by(roll_number=ROLL_NUMBER).first()
    if student:
        print("ENTER NEW STUDENT ATTRIBUTE VALUES:")
        NAME = input("ENTER STUDENT NAME: ").strip().upper()
        AGE = int(input("ENTER STUDENT AGE: "))
        CLASS = input("ENTER STUDENT CLASS: ").strip().upper()
        EMAIL_ID = input("ENTER STUDENT E-MAIL ID: ").strip().upper()
        ADDRESS = input("ENTER STUDENT ADDRESS: ").strip().upper()
        MOBILE_NUMBER = input("ENTER STUDENT MOBILE NUMBER: ").strip()

        student.name = NAME
        student.age = AGE
        student.class_name = CLASS
        student.email = EMAIL_ID
        student.address = ADDRESS
        student.mobile_number = MOBILE_NUMBER

        session.commit()
        print("\n")
        print("\t STUDENT INFORMATION UPDATED SUCCESSFULLY.")
        print("\n")
    else:
        print("\n")
        print("\t STUDENT WITH ROLL NUMBER {} NOT FOUND.".format(ROLL_NUMBER))
        print("\n")

def DISPLAY_STUDENT_INFORMATION():
    print("DISPLAYING STUDENT INFORMATION : \n")

    students = session.query(Student).all()
    if students :
        raw_data = [(student.id, student.name, student.roll_number, student.age, student.class_name, student.email, student.address, student.mobile_number) for student in students]
        print(tabulate(raw_data, headers=["ID", "NAME", "ROLL NUMBER", "AGE", "CLASS", "EMAIL", "ADDRESS", "MOBILE NUMBER"], tablefmt="grid"))
          
    else:
        print("\n")
        print("\t NO STUDENT INFORMATION TO DISPLAY.")
        print("\n")

  
@click.command()
@click.option("--create",is_flag=True, help="Create new student.")
@click.option("--delete",is_flag=True, help="Delete student.")
@click.option("--update",is_flag=True, help="Update student.")
@click.option("--display",is_flag=True, help="Display student.")
def main(create,delete,update,display):
    if create:
        ADD_STUDENT_INFORMATION()
    elif delete:
        DELETE_STUDENT_INFORMATION()
    elif update:
        UPDATE_STUDENT_INFORMATION()
    elif display:
        DISPLAY_STUDENT_INFORMATION()

    else:
         
        print("\n")
        print("\t\t\t\t ' ********** WELCOME TO STUDENT MANAGEMENT SYSTEM ********** ' \n")
        run = True

        while run:
            print("PRESS FROM THE FOLLOWING OPTION : \n")
            print("PRESS 1 : TO ADD STUDENT INFORMATION.")
            print("PRESS 2 : TO DELETE STUDENT INFORMATION.")
            print("PRESS 3 : TO UPDATE STUDENT INFORMATION.")
            print("PRESS 4 : TO DISPLAY STUDENT INFORMATION.")
            print("PRESS 5 : TO EXIT SYSTEM.")

            OPTION = int(input("ENTER YOUR OPTION : "))
            print("\n")
            print(end="\n")

            if OPTION == 1:
                ADD_STUDENT_INFORMATION()
            elif OPTION == 2:
                DELETE_STUDENT_INFORMATION()
            elif OPTION == 3:
                UPDATE_STUDENT_INFORMATION()
            elif OPTION == 4:
                DISPLAY_STUDENT_INFORMATION()
            elif OPTION == 5:
                print("THANK YOU! VISIT AGAIN.")
                run = False
            else:
                print("PLEASE CHOOSE THE CORRECT OPTION FROM THE FOLLOWING.")
                print("\n")

if __name__ == '__main__':

    main()