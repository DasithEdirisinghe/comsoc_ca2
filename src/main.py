import hashlib as h
import pandas as pd
import json





class System:
    staff = ["doctor", "nurse", "lab_assistance"]
    # 1-doctor , 2-nurse , 3-lab_assistance , 4-patient
    privilege_level = {'D': 1,
                       'N': 2,
                       'L': 3,
                       'P': 4}

    def _init_(self):
        staff = self.staff
        privilege_level = self.privilege_level
        self.username = ""
        self.privilege = ""

    def welcome(self):
        print("Welcome to the System\n")
        self.userStatus()

    def userStatus(self):
        status = input("Already Registered to the system? [Yes(y)/No(n)]: ").upper()
        if status == "YES" or status == "Y":
            self.logIn()
        elif status == "NO" or status == "N":
            self.signUp()
        else:
            print("Invalid! Try again")
            self.userStatus()

    def logIn(self):
        print("\nLOGIN\n")
        user_name = input("Username: ")
        password = input("Password: ")

        while not self.validateUser(user_name, password):

            user_name = input("Username: ")
            password = input("Password: ")
        else:
            print("Successfully logged In")
            self.action()

    def signUp(self):
        print("\nREGISTER\n")
        user_name = input("Username: ")
        password = input("Password: ")
        user_type = input("Staff or Patient? [Staff(s)/Patient(p)]: ").upper()
        if user_type == 'STAFF' or user_type == 'S':
            level = input("Enter you profession? [Doctor(D)/Nurse(N)/LabAssistance(L): ").upper()
        else:
            level = user_type
        values = [user_name, h.md5(password.encode("utf-8")).hexdigest(), user_type, self.privilege_level[level]]
        self.writeConfig(values)
        print("Successfully registered.Please login to proceed!\n")
        self.logIn()

    def validateUser(self, user_name, password):
        config = pd.read_csv('../config/configuration.csv')
        for index, con in config.iterrows():
            if con[0] == user_name and con[1] == h.md5(password.encode("utf-8")).hexdigest():
                self.username = user_name
                self.privilege = con[3]
                return True
        else:
            print("Invalid Values, Try Again")
            return False

    def writeConfig(self, values):
        config = pd.read_csv('../config/configuration.csv')
        config.loc[config.shape[0]] = values
        config.to_csv('../config/configuration.csv', index=False)

    def showAll(self):
        f = open('../config/data.json', "r")

        # Reading from file
        data = json.loads(f.read())

        # Iterating through the json
        # list
        for i in data["result"]:
            print(i)

        # Closing file
        f.close()

    def show(self, person_name):

        a_file = open('../config/data.json', "r")
        json_object = json.load(a_file)

        # Iterating through the json
        # list
        for i in json_object["result"]:
            if person_name == i['name']:
                print(f"Details of {person_name}\n")
                print(json_object["result"][i])
            break
        else:
            print("No record found")

        # Closing file
        a_file.close()

    def writeData(self,dic):

        a_file = open('../config/data.json', "r")
        json_object = json.load(a_file)
        a_file.close()
        print(len(json_object["result"]))

        for i in json_object["result"]:
            if i["name"] == dic["name"]:
                for key in i:
                    if dic[key] != "":
                        i[key] = dic[key]
                break

        else:
            json_object["result"].append(dic)

        a_file = open('../config/data.json', "w")
        json.dump(json_object, a_file)
        a_file.close()


    def action(self):
        print(f"Hi {self.username}\n")
        print("What kind of action do you want to do")
        action = input("Enter your action [Read(r)/Write(w)]: ").upper()

        dic = {
            "name": "",
            "age": "",
            "sickness_details": "",
            "drug_prescription": "",
            "lab_test_prescription": "",
            "updated_by": ""

        }

        if action == 'W':
            if self.privilege == 2:
                print("You allowed to change the patients personal data")
                if input("New Patient or Existing Patient? [New(n)/Existing(E)]: ").upper() == "E":
                    person_name = input("patient name :")
                    self.show(person_name)

                if input("Do you want to add/change the personal data? [Y/N]: ").upper() == 'Y':
                    name = input("name: ")
                    age = input("age: ")
                    dic["name"] = name
                    dic["age"] = age
                else:
                    print("Thank you")

            if self.privilege == 3:
                print("You allowed to change the patients Lab Test Data")
                if input("New Patient or Existing Patient? [New(n)/Existing(E)]: ").upper() == "E":
                    person_name = input("person_name :")
                    self.show(person_name)
                if input("Do you want to add/change the lab test data? [Y/N]: ").upper() == 'Y':
                    lab_test_prescription = input("lab test data: ")
                    dic["lab_test_prescription"] = lab_test_prescription
                else:
                    print("Thank you")

            if self.privilege == 1:
                print("You allowed to change the patients all data")
                if input("New Patient or Existing Patient? [New(n)/Existing(E)]: ").upper() == "E":
                    person_name = input("patient name :")
                    self.show(person_name)
                if input("Do you want to add/change the patients data? [Y/N]").upper() == 'Y':
                    name = input("name: ")
                    age = input("age: ")
                    sickness_details = input("sickness details: ")
                    drug_prescription = input("Drug prescription: ")
                    lab_test_prescription = input("lab test data: ")

                    dic["name"] = name
                    dic["age"] = age
                    dic["sickness_details"] = sickness_details
                    dic["drug_prescription"] = drug_prescription
                    dic["lab_test_prescription"] = lab_test_prescription

                else:
                    print("Thank you")

            dic["updated_by"] = self.username
            self.writeData(dic)

        elif action == "R":
            if input("Do you want to see all the patients records? [y/n]: ").upper() == "Y":
                self.showAll()
            else:
                name = input("Enter Patient Name to get details: ")
                self.show(name)


system: System = System()
system.welcome()
