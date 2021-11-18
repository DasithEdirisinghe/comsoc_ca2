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
        print("\nWelcome to the System\n")
        self.userStatus()

    def userStatus(self):
        count = 0
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
        count = 0
        while not self.validateUser(user_name, password):
            count += 1
            if count > 2:
                print("Too much attempts. Register to the system")
                self.signUp()
                break
            else:
                user_name = input("Username: ")
                password = input("Password: ")
        else:
            print("\nSuccessfully logged In")
            self.action()

    def signUp(self):
        print("\nREGISTER\n")
        user_name = input("Username: ")
        password = input("Password: ")
        user_type = input("\nStaff or Patient? [Staff(s)/Patient(p)]: ").upper()
        if user_type == 'STAFF' or user_type == 'S':
            level = input("\nEnter you profession? [Doctor(D)/Nurse(N)/LabAssistance(L): ").upper()
        else:
            level = user_type

        values = [user_name, h.md5(password.encode("utf-8")).hexdigest(), user_type, self.privilege_level[level]]
        self.writeConfig(values)
        print("\nSuccessfully registered.Please login to proceed!\n")
        self.logIn()

    def validateUser(self, user_name, password):
        count = 0
        config = pd.read_csv('../config/configuration.csv')
        for index, con in config.iterrows():
            if con[0] == user_name and con[1] == h.md5(password.encode("utf-8")).hexdigest():
                self.username = user_name
                self.privilege = con[3]
                return True
        else:
            print("\nInvalid Values, Try Again")
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

        f = open('../config/data.json', "r")
        # Reading from file
        data = json.loads(f.read())
        # Iterating through the json
        # list
        for i in data["result"]:
            if i['name'] == person_name:
                print(i)
                f.close()
                return True

        else:
            print("No record found")
            f.close()
            return False

    def writeData(self, dic):
        a_file = open('../config/data.json', "r")
        json_object = json.load(a_file)
        a_file.close()

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
        print(f"\nHi {self.username}\n")
        print("What kind of action do you want to do")
        action = input("Enter your action [Read(r)/Write(w)]: ").upper()

        if action == 'W':
            self.write()

        elif action == "R":
            self.read()

    def read(self):
        if self.privilege == 4:
            print(f"{self.username} personal data")
            self.show(self.username)
        else:
            if input("Do you want to see all the patients records? [y/n]: ").upper() == "Y":
                self.showAll()
            else:
                name = input("Enter Patient Name to get details: ")
                self.show(name)
        if input("\nDo you need more actions to made? [Y/N]: ").upper() == "Y":
            RW = input("Read or Write? [R/W]: ").upper()
            if RW == "R":
                self.read()
            elif RW == "W":
                self.write()
        else:
            print("Thank You.")

    def write(self):
        dic = {
            "name": "",
            "age": "",
            "sickness_details": "",
            "drug_prescription": "",
            "lab_test_prescription": "",
            "updated_by": ""

        }
        if self.privilege == 2:
            print("You are allowed to change the patients personal data")
            if input("New Patient or Existing Patient? [New(n)/Existing(E)]: ").upper() == "E":
                person_name = input("patient name :")
                show = self.show(person_name)
                if show:
                    if input("\nDo you want to add/change the personal data? [Y/N]: ").upper() == 'Y':
                        name = input("name: ")
                        age = input("age: ")
                        if name == "":
                            dic["name"] = person_name
                        else:
                            dic["name"] = name
                        dic["age"] = age

                        dic["updated_by"] = self.username
                        self.writeData(dic)
                    else:
                        print("No record updated")
            else:
                if input("\nDo you want to add/change the personal data? [Y/N]: ").upper() == 'Y':
                    name = input("name: ")
                    age = input("age: ")
                    dic["name"] = name
                    dic["age"] = age

                    dic["updated_by"] = self.username
                    self.writeData(dic)
                else:
                    print("No record updated")

        if self.privilege == 3:
            print("\nYou allowed to change the patients Lab Test Data\n")
            person_name = input("person_name :")
            show = self.show(person_name)
            if show:
                if input("Do you want to add/change the lab test data? [Y/N]: ").upper() == 'Y':
                    lab_test_prescription = input("lab test data: ")
                    dic["lab_test_prescription"] = lab_test_prescription
                    dic["name"] = person_name
                    dic["updated_by"] = self.username
                    self.writeData(dic)
                else:
                    print("No record updated")

        if self.privilege == 1:
            print("\nYou allowed to change the patients all data\n")
            if input("New Patient or Existing Patient? [New(n)/Existing(E)]: ").upper() == "E":
                person_name = input("patient name: ")
                show = self.show(person_name)
                if show:
                    if input("Do you want to add/change the patients data? [Y/N]: ").upper() == 'Y':
                        name = input("name: ")
                        age = input("age: ")
                        sickness_details = input("sickness details: ")
                        drug_prescription = input("Drug prescription: ")
                        lab_test_prescription = input("lab test data: ")

                        if name == "":
                            dic["name"] = person_name
                        else:
                            dic["name"] = name
                        dic["age"] = age
                        dic["sickness_details"] = sickness_details
                        dic["drug_prescription"] = drug_prescription
                        dic["lab_test_prescription"] = lab_test_prescription

                        dic["updated_by"] = self.username
                        self.writeData(dic)

                    else:
                        print("No record updated")
            else:
                if input("Do you want to add/change the patients data? [Y/N]: ").upper() == 'Y':
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

                    dic["updated_by"] = self.username
                    self.writeData(dic)

                else:
                    print("No record updated")

        if self.privilege == 4:
            print("Sorry you are not authorized to update the data")

        if input("\nDo you need more actions to made? [Y/N]: ").upper() == "Y":
            RW = input("Read or Write? [R/W]: ").upper()
            if RW == "R":
                self.read()
            elif RW == "W":
                self.write()
        else:
            print("Thank You.")


system: System = System()
system.welcome()
