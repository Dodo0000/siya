from django.db import models

# Create your models here.

def getCurrency(value):
    return "Rs.{:,}".format(value)



class DrCr(models.Model):
    '''
    Class for either Debit
    or credit
    '''
    particulars = models.CharField(max_length=500)
    amount = models.FloatField()

    def getAmount(self):
        return self.amount

    def getParticulars(self):
        if self.particulars != "None" or self.particulars == None:
            return self.particulars
        else:
            return "N/A"


class Debit(DrCr):
    def __str__(self):
        return "Debit : {}".format(self.getParticulars)


class Credit(DrCr):
    def __str__(self):
        return "Credit : {}".format(self.getParticulars)


class OneDaysEntry(models.Model):
    '''
    All The Entries made in he journal
    for that one day
    '''
    date = models.DateField(unique=True)
    debits = models.ManyToManyField(Debit,default=None)
    credits = models.ManyToManyField(Credit, default=None)

    def getDate(self):
        return self.date

    def getTotalCredit(self):
        return sum([_.amount for _ in self.credits.all()])

    def getTotalDebit(self):
        return sum([_.amount for _ in self.debits.all()])

    def getTotalCreditCur(self):
        return getCurrency(self.getTotalCredit())

    def getTotalDebitCur(self):
        return getCurrency(self.getTotalDebit())

    def totalBalanceMatchBool(self):
        total_debit = self.getTotalDebit()
        total_credit = self.getTotalCredit()
        return total_debit == total_credit

    def getDifferenceInBalance(self):
        balance = self.getTotalDebit() - self.getTotalCredit()
        if balance >= 0:
            sign = "+"
        else:
            sign = "-"
        return "{0}{1}".format(sign, balance)
    def __str__(self):
        return str(self.date)
