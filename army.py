import csv
import copy


class Army:

    def __init__(self):
        self.templates = {}

        self.templates_divisions = {}

        self.divisions = {}

    # Decorators
    def division(self, func, name, **kwargs):
        if name in self.divisions.keys():
            return func(name=name, **kwargs)
        else:
            return "Invalid division name"

    def template(self, func, name, **kwargs):
        if name in self.templates.keys():
            print(kwargs)
            return func(name=name, **kwargs)
        else:
            return "Invalid template name"
    ####

    # Returning army details
    def return_cost(self, stability):
        all = 0
        for cost in self.divisions.values():
            all += cost.return_cost(stability)
        return all

    def return_max_cost(self):
        all = 0
        for cost in self.divisions.values():
            all += cost.return_max_cost()
        return all

    def return_man(self):
        all = 0
        for man in self.divisions.values():
            all += man.return_man()
        return all

    def return_all(self):
        all = {
            "sol": 0,
            "arch": 0,
            "cav": 0,
            "art": 0,
            "con": 0,
            "bord": 0,
            "heav": 0,
            "ligh": 0
        }
        for division in self.divisions.keys():
            div = self.return_division(division)
            for unit, amount in div["current"].items():
                all[unit] += int(amount)
        return all
    ####

    # Returning division details
    def return_division_names(self):
        return list(self.divisions.keys())

    # @division
    def return_division(self, name):
        return self.divisions[name].return_info()

    # @division
    def return_division_template(self, name):
        return self.templates_divisions[name]

    # @division
    def return_division_cost(self, name, stability):
        return self.divisions[name].return_cost(stability)

    # @division
    def return_division_man(self, name):
        return self.divisions[name].return_man()
    ####

    # Editing division details
    def add_division(self, name, template):
        name = name.lower()
        if not(name in self.divisions.keys()) and template in self.templates.keys():
            self.templates_divisions[name] = template
            self.divisions[name] = Division(
                self.templates[template], self.templates[template].keys())
            return "Division added succesfully"
        elif name in self.divisions.keys():
            return "There is already a division named such"
        else:
            return "No such template"

    # @division
    def remove_division(self, name):
        del self.divisions[name]
        del self.templates_divisions[name]
        return "Division removed successfully"

    # @division
    def change_division_reinforce(self, name, armies):
        return self.divisions[name].reinforce(armies)

    # @division+template
    def change_division_template(self, name, template_name):
        if template_name in self.templates.keys():
            self.templates_divisions[name] = template_name
            return self.divisions[name].change_max(self.templates[template_name])
        else:
            return "No such tempalte"
    ####

    # Returning template details
    def return_template_names(self):
        return list(self.templates.keys())

    # @template
    def return_template(self, name):
        return self.templates[name]

    # @template
    def return_template_cost(self, name, stability):
        return Division(self.templates[name], self.templates[name].keys()).return_cost(stability)

    # @template
    def return_template_man(self, name):
        return Division(self.templates[name], self.templates[name].keys()).return_man()
    ####

    # Editing template details
    def add_template(self, name, armies):
        name = name.lower()
        if name not in self.templates.keys():
            lis = {}
            for unit, num in armies.items():
                if num != 0:
                    lis[unit] = num
            self.templates[name] = lis
        else:
            return "There is already a template named such"
        return "Template added succesfully"

    # @template
    def remove_template(self, name):
        if name in self.templates_divisions.values():
            return "Cannot remove a template in use"
        else:
            del self.templates[name]
            return "Task succesfull"

    # @template
    def update_template_add(self, name, armies):
        for unit, num in armies.items():
            if unit in self.templates[name]:
                self.templates[name][unit] += int(num)
            else:
                self.templates[name][unit] = int(num)
        self.update_divisions(name)
        return "Template expanded successfully"

    # @template
    def update_template_redefine(self, name, armies):
        self.templates[name] = armies
        self.update_divisions(name)
        return "Task successfull"

    # @template
    def update_template_delete(self, name, armies):
        for unit in armies.keys():
            del self.templates[name][unit]
        self.update_divisions(name)
        return "Task successfull"

    def update_divisions(self, temp_name):
        for division, template in self.templates_divisions.items():
            if template == temp_name:
                self.divisions[division].change_max(self.templates[temp_name])


class Division:

    # Division init
    def __init__(self, temp, lis):  # =["ligh", "heav", "bord"]):

        self.max_force = temp
        self.current_force = copy.copy(self.max_force)

        self.experiance = 0
        self.level = 1

        self.costs = self.load("army_expenses")
        self.costs = self.change_tiers(lis, self.costs)
        self.powers = self.load("army")
        self.powers = self.change_tiers(lis, self.powers)

        self.returner = {
            ""
        }

    def load(self, name):
        with open("tier_info/"+name+".csv") as file:
            values = []
            reader = csv.reader(file)
            for line in reader:
                values.append(line)

        heads = values[0]
        heads = list(map(str.lower, heads))
        values.pop(0)
        prop_values = {}
        for value in values:
            bet_value = []
            for v in value:
                try:
                    bet_value.append(float(v))
                except ValueError:
                    bet_value.append(v)
            prop_value = dict(zip(heads[1:], bet_value[1:]))
            prop_values[value[0].lower()] = prop_value
        return prop_values

    def change_tiers(self, lis, source):
        out = {}
        for good in lis:
            out[good] = source[good]
        return source
    ####

    def update(self, force="current", stability=100):
        self.base_cost_calc(force=force)
        self.base_manpower_calc(force=force)
        self.over_cost_calc(force=force, stability=stability)

    # Calculating division stats
    def base_cost_calc(self, force):
        if force == "current":
            force = self.current_force
        else:
            force = self.max_force
        self.base_cost = 0
        for unit in force.keys():
            self.base_cost += int(force[unit])*self.costs[unit]["maintainance"]

    def base_manpower_calc(self, force):
        if force == "current":
            force = self.current_force
        else:
            force = self.max_force
        self.base_man = 0
        for unit in force.keys():
            self.base_man += int(force[unit])*self.costs[unit]["manpower"]

    def over_cost_calc(self, stability, force):
        if force == "current":
            force = self.current_force
        else:
            force = self.max_force
        self.over_cost = 0
        for unit in force.keys():
            self.over_cost += int(force[unit])*self.costs[unit]["stab_multi"]*(100-stability)
    ####

    # Returning values
    def return_cost(self, stability):
        self.update(stability=stability)
        return self.over_cost+self.base_cost

    def return_max_cost(self):
        self.update(force="max")
        return self.over_cost+self.base_cost

    def return_man(self):
        self.update()
        return self.base_man

    def return_info(self):
        all = {}
        all["max"] = self.max_force
        all["current"] = self.current_force
        return all
    ####

    # Editing the division
    def reinforce(self, units):
        for unit in units.keys():
            self.current_force[unit] += int(units[unit])

        self.fix_overfill()

        return "Division reincorced successfully"

    def change_max(self, new):

        self.max_force = new
        for unit in self.max_force.keys():
            num = int(self.max_force[unit])
            if unit in self.current_force.keys():
                if self.current_force[unit] > num:
                    self.current_force[unit] = num
                else:
                    pass
            else:
                pass

        rem = []
        for unit in self.current_force:
            if not(unit in self.max_force):
                rem.append(unit)
        for i in rem:
            del self.current_force[i]

        self. fix_overfill()

        return "Task succesfull"

    def fix_overfill(self):
        for unit, amount in self.current_force.items():
            if amount > self.max_force[unit]:
                self.current_force[unit] = self.max_force[unit]


if __name__ == "__main__":
    army = Army()

    print(army.add_template("defult1", {"sol": 100, "cav": 20, "arch": 10, "con": 0}))
    # print(army.return_template_names())

    # print(army.template(army.return_template, "defult1"))

    print(army.add_division("div1", "defult1"))
    print(army.add_division("div2", "defult1"))
    # print(army.return_division_names())
    #print(army.division(army.return_division, "div1"))
    #print(army.division(army.return_division_template, "div1"))
    # print(army.division(army.remove_division, "div1"))

    #print(army.template(army.update_template_add, "defult1", sol=10))

    print(army.return_all())
