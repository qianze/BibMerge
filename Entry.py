class Entry(object):
    def __init__(self, sitekey, entrytype, attributes):
    #required fields
        #Strings
        self.sitekey = sitekey
        self.entrytype = entrytype

        #dictionary (begins as empty)
        self.attributes = {}


    '''
    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if amount > self.balance:
            raise RuntimeError('Amount greater than available balance.')
        self.balance -= amount
        return self.balance'''