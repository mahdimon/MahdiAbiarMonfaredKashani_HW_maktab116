from typing import ClassVar
class BankAccount:
    _min_balance = 100
    def __init__(self,name,balance):
        try:    
            self._name = name
            self._balance = balance
        except Exception as e:
            print(e)
    
    @property
    def _balance(self):
        return self.__balance
    @_balance.setter
    def _balance(self,value):
        if not isinstance(value,(int,float)):
            raise ValueError(f"balance must be int and higher than {self._min_balance}") 
        assert  value > self.__class__._min_balance , f"balance must be higher than {self._min_balance}"
        self.__balance = value
    @property
    def _name(self):
        return self.__name
    @_name.setter
    def _name(self,value):
        if not isinstance(value,str):
            raise ValueError("name must be str" )
        self.__name = value
    
    def withdraw(self,value):
        try:
            self._balance -= value
        except Exception as e:
            print(e)
        else:
            print(f"${value} was withdrawed from your account your balance is ${self._balance}")
    def deposit(self,value):
        try:
            self._balance += value
        except Exception as e:
            print(e)
        else:
            print(f"${value} was deposited to your account your balance is ${self._balance}")
            
    def transmition(self,other:'BankAccount',value):
        try:
            if not isinstance(other,BankAccount):
                raise ValueError("other must be BankAccount object")
            self._balance -= value
            other._balance += value
        except Exception as e:
            print(e)
        else:
            print(f"${value} was transmited to {other._name} your balance is ${self._balance}")
        

        
a = BankAccount("ali",1000)
b = BankAccount("mohsen",10)
c = BankAccount("ehsan" , 1000)
a.deposit(10)
a.withdraw(10)
a.transmition(c,200)
        
        
        
        
        
           
    