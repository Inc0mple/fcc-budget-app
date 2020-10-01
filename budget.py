import math
class Category:
    
    def __init__(self,name):
        self.ledger = []
        self.name = name

    def __str__(self):
        lineLength = 30
        lines = []
        output = ""
        total = 0
        for record in self.ledger:
            total += record['amount']
        lines.append(f"{'*'*math.ceil((lineLength-len(self.name))/2)}{self.name}{'*'*math.floor((lineLength-len(self.name))/2)}")
        for record in self.ledger:
            amountString = f"{record['amount']:.2f}"
            lines.append(f"{record['description'][0:23]}{' '*(lineLength-len(record['description'][0:23] + amountString[0:7]))}{record['amount']:.2f}")
        for line in lines:
            output += (line + "\n")
        output += (f"Total: {total:.2f}")
        return output

    def check_funds(self,amount):
        total = 0
        for record in self.ledger:
            total += record['amount']
        return (True if total >= amount else False)
    
    def deposit(self,amount,description = ""):
        self.ledger.append({"amount":amount,"description":description})

    def withdraw(self,amount,description = ""):
        self.ledger.append({"amount":-amount,"description":description}) if self.check_funds(amount) == True else None
        return (True if self.check_funds(amount) else False)

    def transfer(self,amount,other_category):
        if self.check_funds(amount):
            self.withdraw(amount,f"Transfer to {other_category.name}")
            other_category.deposit(amount,f"Transfer from {self.name}")
            return True
        else:
            return False
        

    def get_balance(self):
        total = 0
        for record in self.ledger:
            total += record['amount']
        return total

    
def create_spend_chart(categories):
    totalSpendings = 0
    spendingsDict = {}
    maxCatChar = 0
    for cat in categories:
        spendings = 0
        for record in cat.ledger:
            if record['amount'] < 0:
                spendings -= record['amount']
        totalSpendings += spendings
        spendingsDict[cat.name] = spendings
    spendPercent = {}
    for item in spendingsDict:
        if len(item) > maxCatChar: maxCatChar = len(item)
        spendPercent[item] = int((spendingsDict[item]/totalSpendings)*100//10*10)
    catNum = len(spendingsDict)
    lines = ["Percentage spent by category"]
    for i in range(0,11):
        rowVal = 100 - i*10
        out = f"{' '*(3-len(str(rowVal)))}{rowVal}|"
        for item in spendPercent:
            if spendPercent[item] >= rowVal:
                out += " o "
            else:
                out += "   "
        out += " "    
        lines.append(out)
    lines.append(f"    {'---'*catNum}-")
    for i in range(maxCatChar):
        out = "     "
        for item in spendingsDict:
            out += (item[i] + "  ") if len(item) > i else ("   ")
        lines.append(out)
    
    return "\n".join(lines)

