from datetime import datetime
import csv


class Rank:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class Comrade:
    def __init__(self, name, rank, date_of_birth, date_of_join, status, squads):
        self.name = name
        self.rank = rank
        self.date_of_birth = date_of_birth
        self.date_of_join = date_of_join
        self.status = status
        self.squads = squads

    def get_age(self):
        delta = datetime.now() - self.date_of_birth
        return delta.days // 365

    def get_service_length(self):
        delta = datetime.now() - self.date_of_join
        return delta.days // 365
    
    def has_mission(self):
        for squad in self.squads:
            if self in squad.members:
                return True
        return False

    def __str__(self):
        return f"{self.name}, {self.rank}, {self.status}"

class Commander(Comrade):
    def __init__(self, name, rank, date_of_birth, date_of_join, status, squads):
        super().__init__(name, rank, date_of_birth, date_of_join, status, squads)
        self.mission = []

    def has_mission(self):
        return bool(self.mission)
    
    def add_mission(self, mission):
        self.mission.append(mission)

class Mission:
    def __init__(self, name, status, squad):
        self.name = name
        self.status = status
        self.squad = squad
        squad.add_mission(self)
    
class Squad:
    def __init__(self, name, commander, members):
        self.name = name
        self.members = members
        self.commander = commander
        self.mission = []

    def add_member(self, comrade):
        self.members.append(comrade)

    def remove_member(self, comrade):
        self.members.remove(comrade)

    def get_members(self):
        return [str(member) for member in self.members]
    
    def add_mission(self, mission):
        self.mission.append(mission)

    def has_mission(self):
        return bool(self.mission)
    
    def __str__(self):
        return f"{self.name}, commanded by {self.commander.name}, with members: {', '.join([m.name for m in self.members])}"

class Comrade_Information_Management_System:
    def __init__(self):
        self.comrades = []
        self.commanders = []
        self.missions = []
        self.squads = []

    def input_comrade(self):
        print("Comrade:")
        while True:
            name = input("Enter name (or leave blank to exit): ")
            if name == "":
                break
            rank_name = input("Enter rank name: ")
            rank = Rank(rank_name)
            date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
            date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
            status = input("Enter status: ")
            comrade = Comrade(name, rank, date_of_birth, date_of_join, status, self.squads)
            self.comrades.append(comrade)

        with open("comrades.txt", "w", newline = '') as f:
            writer = csv.writer(f)
            for comrade in self.comrades:
                writer.writerow([comrade.name, comrade.rank.name, comrade.date_of_birth, comrade.date_of_join, comrade.status])
   
    def input_commander(self):
        print("Commander:")
        while True:
            name = input("Enter name (or leave blank to exit): ")
            if name == "":
                break
            rank_name = input("Enter rank name: ")
            rank = Rank(rank_name)
            date_of_birth = datetime.strptime(input("Enter date of birth (YYYY-MM-DD): "), "%Y-%m-%d")
            date_of_join = datetime.strptime(input("Enter date of join (YYYY-MM-DD): "), "%Y-%m-%d")
            status = input("Enter status: ")
            commander = Commander(name, rank, date_of_birth, date_of_join, status, [])
            self.commanders.append(commander)

        with open("commanders.txt", "w", newline='') as f:
            writer = csv.writer(f)
            for commander in self.commanders:
                writer.writerow([commander.name, commander.rank.name, commander.date_of_birth, commander.date_of_join, commander.status])

    def input_mission(self):
        print("Mission:")
        num_mission = int(input("Enter number of mission: "))
        for mission in range(num_mission):
            name = input("Enter name: ")
            status = input("Enter status: ")
            squad_name = input("Assign squad for this mission: ")
            squad = next((s for s in self.squads if s.name == squad_name), None)
            if squad:
                mission = Mission(name, status, squad)
                squad.commander.add_mission(mission)
                self.missions.append(mission)
                print("Mission added successfully!")

                with open("missions.txt", "a") as missions_file:
                    missions_file.write(f"{name},{status},{squad_name}\n")

                with open("commander_missions.txt", "a") as cmd_missions_file:
                    cmd_missions_file.write(f"{squad.commander.name},{name}\n")

                for comrade in squad.members:
                    with open("comrade_missions.txt", "a") as c_missions_file:
                        c_missions_file.write(f"{comrade.name},{name}\n")
            else:
                print("Squad not found.")

                
    def input_squad(self):
        print("Squad:")
        num_squad = int(input("Enter number of squad: "))

        squads = []
        for i in range(num_squad):
            squad_name = input(f"Enter squad {i + 1} name: ")
            while True:
                commander_name = input(f"Enter commander who will lead squad {i + 1}: ")
                commander = next((c for c in self.commanders if c.name == commander_name), None)
                if commander:
                    is_assigned = any(squad.commander == commander for squad in self.squads)
                    if is_assigned:
                        print("This commander is already assigned to another squad.")
                    else:
                        break
                else:
                    print("Commander not found.")
        
            squad = Squad(squad_name, commander, [])
            squads.append(squad)
            self.squads.append(squad)
            print(f"Squad {squad_name} created with commander {commander_name}")

        for i, squad in enumerate(squads):
            print(f"Input members to squad {i + 1} ({squad.name}):")
            while True:
                member_name = input("Enter member name (or leave blank to exit):")
                if member_name == "":
                    break
                comrade = next((c for c in self.comrades if c.name == member_name), None)
                if comrade:
                    squad.add_member(comrade)
                    print(f" + {comrade.name}")
                else:
                    print("Comrade not found.")

        print(f"Members added to squad {squad_name} with commander {squad.commander.name}:")
        for member in squad.members:
            print(f" + {member.name}")
    
        print("List squad(s) created:")
        for squad in squads:
                print(f"{squad}")

        with open("squads.txt", "w") as f:
            for squad in self.squads:
                f.write(f"{squad.name},{squad.commander.name},{','.join([m.name for m in squad.members])}\n")

    def list_comrades(self):
        print("Comrades:")
        with open("comrades.txt", "r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                name, rank, date_of_birth, date_of_join, status = row
                print(f"{name}, {rank}, {date_of_birth}, {date_of_join}, {status}")

    def list_commanders(self):
        print("Commanders:")
        with open("commanders.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name, rank, date_of_birth, date_of_join, status = row
                print(f"{name}, {rank}, {date_of_birth}, {date_of_join}, {status}")

    def list_missions(self):
        print("Missions:")
        with open("missions.txt", "r") as file:
            for line in file.readlines():
                name, status, squad_name = line.strip().split(",")
                print(f"{name}, {status}, assigned to {squad_name}")

    def create_squad(self):
        self.input_squad()
        print("Squad created successfully!")

    def commander_without_squad(self):
        print("Commander(s) who is(are) inactive:")
        with open("commanders.txt", "r") as file:
            for line in file.readlines():
                name, rank, date_of_birth, date_of_join, status = line.strip().split(",")
                with open("commander_missions.txt", "r") as missions_file:
                    has_mission = any(name in mission_line for mission_line in missions_file.readlines())
                if not has_mission:
                    print(f"{name}, {rank}, {status}")


    def comrade_without_squad(self):
        print("Comrade(s) who is(are) inactive:")
        with open("comrades.txt", "r") as file:
            for line in file.readlines():
                name, rank, date_of_birth, date_of_join, status = line.strip().split(",")
                with open("comrade_missions.txt", "r") as missions_file:
                    has_mission = any(name in mission_line for mission_line in missions_file.readlines())
                if not has_mission:
                    print(f"{name}, {rank}, {status}")
    
    def run_please(self):
        self.input_comrade()
        self.list_comrades()
        self.input_commander()
        self.list_commanders()
        self.input_squad()
        self.input_mission()
        self.list_missions()
        self.commander_without_squad()
        self.comrade_without_squad()
program = Comrade_Information_Management_System()
program.run_please()