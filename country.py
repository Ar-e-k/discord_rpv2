import csv
import army


class Country:

    def __init__(self, name, stability, literacy, economy, population, public):
        self.name = name.lower()

        self.army = army.Army()
        armies = {"sol": 100, "cav": 50, "arch": 40, "con": 10, "art": 0, }
        self.army.add_template("Deafult1", armies)
        armies = {"ligh": 30, "heav": 5, "bord": 50}
        self.army.add_template("Deafult2", armies)

        self.public = public
        self.spendings = {
            "total": 0,
            "education_spending": 10000,
            "economy_spending": 0,
            "benefits_spending": 0
        }
        self.spendings["army"] = self.army.return_cost(100)

        self.population = Population("pop", population[0], population[1], population[2], [
                                     "population", "population_tier"])
        self.literacy = Literacy("literacy", literacy[0], literacy[1], literacy[2], [
                                 "literacy", "literacy_tier"])
        self.stability = Stability("stability", stability[0], stability[1], stability[2], [
                                   "stability", "stability_tier"])
        self.economy = Economy("economy", economy[0], economy[1], economy[2], economy[3], economy[4], [
                               "budget", "economy_tier"])

        self.population.update_ratio(
            self.literacy.return_value(),
            self.army.return_man()
        )
        # Getting the basic population proportions

        self.mod = [
            "tax",
            "form",
            "capital",
            "education_spending",
            "economy_spending",
            "benefits_spending",
            "name"
        ]  # All the values user can modify
        self.ad_mod = [
            "population",
            "population_tier",
            "literacy",
            "literacy_tier",
            "stability",
            "stability_tier",
            "budget",
            "economy_tier",
            "trade",
            "culture",
            "area"
        ]  # All the additional values admin can modify

        self.changes = {}  # Constains all the names of vars that can be changed
        for feature in [self.population, self.literacy, self.stability, self.economy]:
            self.changer_dic(feature)
        for feature in list(self.public.keys())+list(self.spendings.keys()):
            self.changes[feature] = self
        self.changes["name"] = self

    def changer_dic(self, feat):  # Creates the changer dictionary
        for i in feat.return_attributes():
            self.changes[i] = feat

    def update(self):
        self.update_spending()

        self.economy.update_modifier(
            self.population.return_pop("rural"),
            self.population.return_pop("artisan"),
            self.spendings["total"],
            self.stability.return_value(),
            self.public["area"]
        )
        self.economy.apply_modifier()
        if self.economy.check_budget():
            mes = self.name+" is out of budget, please contact them to limit spendings or get a loan\nThey currently need " + \
                str(self.economy.return_value())+" more money"
            self.economy.change_value(0)
            return mes

        self.population.update_ratio(
            self.literacy.return_value(),
            self.army.retrun_man()
        )
        self.literacy.update_modifier(
            self.spendings["education_spending"],
            self.population.return_value()
        )
        self.stability.update_modifier(
            self.spendings["benefits_spending"],
            self.population.return_value(),
            self.literacy.return_value(),
            self.economy.return_income()
        )

        for feature in [self.population, self.literacy, self.stability]:
            feature.apply_modifier()

        return "Task succesfull"

    def update_spending(self):
        self.spendings["army"] = self.army.return_cost(self.stability.return_value())
        all = 0
        for money in self.spendings:
            if money != "total":
                all += self.spendings[money]
        self.spendings["total"] = all

    def change(self, category, value, admin=False, add=False):
        if category in self.mod:
            pass
        elif category in self.ad_mod and admin == True:
            pass
        else:
            return "Invalid categoty"
        return self.changes[category].change_self(category, value, add=add)

    def change_self(self, category, value, add=False):
        if category in self.public.keys() and not(add):
            self.public[category] = value
        elif category in self.spendings.keys():
            try:
                value = float(value)
            except ValueError:
                return "Invalid value"
            if add:
                self.spendings[category] += value
            else:
                self.spendings[category] = value
        elif category == "name" and not(add):
            self.name = value
        else:
            return "Invalid category"
        return "Task succesfull"

    def return_priv(self):
        all = {}
        for val in [self.population, self.literacy, self.stability, self.economy]:
            all[val.return_name()] = val.return_round_value()
            all[val.return_name()+" change"] = val.return_modifier()
        all.update(self.public)
        all.update(self.spendings)
        all["tax"] = self.economy.tax
        all["trade"] = self.economy.return_trade()
        return all

    def return_pub(self):
        all = {}
        all.update(self.public)
        return all

    def return_all(self):
        all = {}
        all["Name"] = self.name
        for val in [self.population, self.literacy, self.stability, self.economy]:
            all[val.return_name()] = val.value
            all[val.return_name()+" change"] = val.modifier
            all[val.return_name()+" tier"] = val.tier_info
        all.update(self.public)
        all.update(self.spendings)
        all["tax"] = self.economy.tax
        all["trade"] = self.economy.trade
        return all

    def return_army(self, typ):
        typ = typ.lower()

        return_dic = {
            "cost": self.army.return_cost(self.stability.return_value()),
            "max_cost": self.army.return_max_cost(),
            "man": self.army.return_man()
        }
        if typ in return_dic:
            return return_dic[typ]
        else:
            return self.army.return_all()

    def return_division(self, typ, sub_type, name):
        typ = typ.lower()
        name = name.lower()
        sub_type = sub_type.lower()

        if typ == "division":
            return_dic = {
                "cost": self.army.division(self.army.return_division_cost, name, stability=self.stability.return_value()),
                "man": self.army.division(self.army.return_division_man, name),
                "template": self.army.division(self.army.return_division_template, name),
                "all": self.army.division(self.army.return_division, name)
            }
            if sub_type in return_dic:
                return return_dic[sub_type]
            else:
                return self.army.return_division_names()
        elif typ == "template":
            return_dic = {
                "cost": self.army.template(self.army.return_template_cost, name, stability=self.stability.return_value()),
                "man": self.army.template(self.army.return_template_man, name),
                "all": self.army.template(self.army.return_template, name)
            }
            if sub_type in return_dic:
                return return_dic[sub_type]
            else:
                return self.army.return_template_names()
        else:
            return "Invalid type"

    def change_template(self, typ, name, army, sub_type="none"):
        typ = typ.lower()

        army_list = army.split(" ")
        armies = {
            "sol": 0,
            "arch": 0,
            "cav": 0,
            "art": 0,
            "con": 0,
            "bord": 0,
            "heav": 0,
            "ligh": 0
        }
        rem = []

        for unit in armies.keys():
            try:
                armies[unit] = army_list[army_list.index(unit)+1]
            except ValueError:
                rem.append(unit)

        for i in rem:
            del armies[i]

        if typ == "add":
            return self.army.add_template(name, armies)
        elif typ == "update":

            sub_type = sub_type.lower()

            if sub_type == "add":
                return self.army.template(self.army.update_template_add, name, armies=armies)
            elif sub_type == "redo":
                return self.army.template(self.army.update_template_redefine, name, armies=armies)
            elif sub_type == "delete":
                return self.army.template(self.army.update_template_delete, name, armies=armies)
            else:
                return "Inalid subtype"

    def change_division(self, typ, name, template):
        typ = typ.lower()

        if typ == "add":
            return self.army.add_division(name, template)
        elif typ == "change_template":
            return self.army.division(self.army.change_division_template, name, template_name=template)

    def change_division_detail(self, typ, name, kwargs):
        print(kwargs)


class Feature:

    # Initialization functions
    def __init__(self, name, value, tier, all_tiers, names):
        self.name = name
        self.value = value

        self.all_tier_info = self.load_tiers()
        self.tier_info = self.all_tier_info[tier]

        self.modifier = 0
        self.changer = {names[0]: self.change_value, names[1]: self.change_tier}

        self.change_dir = "None"

    def load_tiers(self):
        with open("tier_info/"+self.name+".csv") as file:
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

    def change_tiers(self, lis):
        for tier in self.all_tier_info:
            for bad in lis:
                del self.all_tier_info[tier][bad]

    def get_estimate(self, upper, lower, num, high, low, mid):
        if float(num) < lower:
            return low
        elif float(num) > upper:
            return high
        else:
            return mid
    ############################################################################
    # Functions for user input

    def change_self(self, category, value, add=False):
        if not(add):
            return self.changer[category](value)
        else:
            if self.changer[category] != self.change_tier:
                return self.changer[category](value, add=True)
            else:
                return "Cannot add to this value"

    def change_tier(self, tier):
        if tier in list(self.all_tier_info.keys()):
            self.tier_info = self.all_tier_info[tier]
            return "Task succesfull"
        else:
            return "Invalid Tier/nThis is the list of possible tiers:", list(self.all_tier_info.keys())

    def change_value(self, value, add=False):
        try:
            value = float(value)
        except ValueError:
            return "Invalid value"
        if add:
            self.value += value
        else:
            self.value = value
        return "Task succesfull"
    ############################################################################
    # Functions for update

    def apply_modifier(self):
        self.value += self.modifier
        return "Task succesfull"

    def side_modifier(self):
        if self.modifier > 0:
            self.change_dir = "Positive"
        elif self.modifier < 0:
            self.change_dir = "Negative"
        else:
            self.change_dir = "None"
    # Functions for returning

    def return_value(self):
        return self.value

    def return_round_value(self):
        return self.get_estimate(65, 35, self.value, "High", "Low", "Mid")

    def return_name(self):
        return self.name

    def return_modifier(self):
        return self.change_dir

    def return_attributes(self):
        return list(self.changer.keys())


class Population(Feature):

    def __init__(self, name, value, tier, all_tiers, names):
        super().__init__("economy", value, tier, all_tiers, names)

        self.name = name
        self.change_tiers(["rural", "artisan", "cost"])

    def modifier(self):
        self.modifier = 0
        self.side_modifier()

    def update_ratio(self, literacy, army):
        self.ratio = {
            "manpower": army,
            "rural": int(self.value*self.tier_info["rpop"]*0.01),
            "artisan": int(self.value*self.tier_info["ipop"]*0.01),
            "young": int(self.value*literacy*0.003),
        }
        all = 0
        for i in self.ratio.values():
            all += i
        self.ratio["unemployed"] = self.value-all

    def return_pop(self, type):
        return self.ratio[type]

    def return_round_value(self):
        return self.return_value()


class Stability(Feature):

    def update_modifier(self, benefits, pop, literacy, income):
        money = 0
        money += benefits/pop
        money += income/pop
        money = (money-20)/200

        new_lit = 1-abs((50-literacy)/50)
        if money > 0:
            self.modifier = money*new_lit
        else:
            try:
                self.modifier = money/new_lit
            except ZeroDivisionError:
                self.modifier = 0
        self.modifier *= 0.01*self.tier_info["modifier"]
        self.side_modifier()


class Literacy(Feature):

    def update_modifier(self, spending, pop):
        spending = spending/pop
        change = -(1-spending)
        self.modifier = change/(10*self.value)
        self.modifier *= 0.01*self.tier_info["modifier"]
        self.side_modifier()


class Economy(Feature):

    def __init__(self, name, value, tier, all_tiers, tax, trade, names):
        super().__init__(name, value, tier, all_tiers, names)

        self.total_income = 0
        self.tax = tax
        self.trade = trade
        self.changer["tax"] = lambda x: self.change_tax(x, True)
        self.changer["trade"] = lambda x: self.change_trade(x, True)
        self.change_tiers(["rpop", "ipop"])

    def change_tax(self, value, tax, add=False):
        try:
            if 0 <= value <= 100:
                if tax:
                    if add:
                        self.tax += value
                    else:
                        self.tax = value
                else:
                    if add:
                        self.trade += value
                    else:
                        self.trade = value
                return "Task succesfull"
            else:
                return "Input a value between between 0 and 100"
        except ValueError:
            return "Invalid value"

    def update_modifier(self, rural, artisan, spending, stability, area):
        self.modifier = 0
        self.modifier += rural*self.tier_info["rural"]*0.01
        self.modifier += artisan*self.tier_info["artisan"]*0.01

        self.total_income = self.modifier

        self.modifier *= self.tax*0.01
        self.modifier *= int(self.trade-1)/20/5+1
        if stability < 50:
            self.modifier *= stability/50

        self.modifier -= spending
        self.modifier -= float(area)*self.tier_info["cost"]

        self.side_modifier()

    def check_budget(self):
        if self.value < 0:
            return True
        else:
            return False

    def side_modifier(self):
        self.change_dir = self.modifier

    def return_trade(self):
        if self.trade > 50:
            return self.get_estimate(80, 60, self.trade, "Monopoly", "Medium", "High")
        else:
            return self.get_estimate(40, 20, self.trade, "Medium", "None", "Low")

    def return_income(self):
        return self.total_income

    def return_round_value(self):
        return self.return_value()


def country_init(name, all, test=False):
    public = {}
    for i in ["form", "capital", "culture", "area"]:
        public[i] = all[i]

    population = [float(all["population"]), all["economy_tier"], [
        "rural1", "rural2", "rural3", "rural4", "ind1", "ind2", "ind3", "ind4", "mix1", "mix2"]]
    stability = [float(all["stability"]), all["stability_mod"], ["tier1", "tier2"]]
    literacy = [float(all["literacy"]), all["literacy_mod"], ["tier1", "tier2"]]
    economy = [float(all["budget"]), all["economy_tier"], ["rural1", "rural2", "rural3", "rural4",
                                                           "ind1", "ind2", "ind3", "ind4", "mix1", "mix2"], float(all["tax_rate"]), float(all["trade"])]
    country_now = Country(name.upper(), stability, literacy, economy, population, public)

    if test:
        print(country_now.change_template("add", "Deafult3", "sol 100 arch 1 cav 1"))
        print(country_now.change_division("add", "div1", "Deafult3"))
        print(country_now.return_division("division", "all", "div1"))
        print(country_now.change_template("update", "Deafult3", "sol 10 arch 1 cav 1", sub_type="add"))
        print(country_now.return_division("division", "all", "div1"))
        # print(country_now.return_priv())
        # print(country_now.update())
        # print(country_now.change("tax", 15.0))
        # print(country_now.return_priv())
        # print(country_now.change("education_spending", 10.0))
        # print(country_now.return_priv())

    return country_now
