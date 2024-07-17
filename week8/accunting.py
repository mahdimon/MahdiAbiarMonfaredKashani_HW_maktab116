from typing import List, Tuple
import pickle
import argparse
from datetime import datetime
import json
import functools
import logging

logging.basicConfig(
    format="%(asctime)s %(message)s", filename="accunting.log", level=logging.DEBUG
)
logger = logging.getLogger()


def main():

    make_files(
        [("accunts.pkl", "b"), ("saved_expence.json", "t"), ("saved_income.json", "t")]
    )

    parser = argparse.ArgumentParser(
        prog="accounting",
        description="helps you to add transaction info to your account",
    )
    subparsers = parser.add_subparsers(dest="command", title="subcommands")

    parser_new = subparsers.add_parser("new", help="create a new bank account")
    parser_new.add_argument("bank_name", choices=Account.valid_bank_names)
    parser_new.add_argument("card_number", type=valid_card_number)
    parser_new.add_argument("balance", type=valid_balance)
    parser_new.set_defaults(func=new)

    parser_expence = subparsers.add_parser("expence", help="add an expence")
    parser_expence.add_argument("card_number", type=valid_card_number)
    parser_expence.add_argument("amount", type=int, nargs="?", default=None)
    parser_expence.add_argument("title")
    parser_expence.add_argument("-s", "--save", action="store_true")
    parser_expence.set_defaults(func=expence)

    parser_income = subparsers.add_parser("income", help="add an income")
    parser_income.add_argument("card_number", type=valid_card_number)
    parser_income.add_argument("amount", type=int, nargs="?", default=None)
    parser_income.add_argument("title")
    parser_income.add_argument("-s", "--save", action="store_true")
    parser_income.set_defaults(func=income)

    parser_history = subparsers.add_parser(
        "history", help="see privios transactions of an account"
    )
    parser_history.add_argument("card_number", type=valid_card_number)
    parser_history.set_defaults(func=history)

    parser_info = subparsers.add_parser(
        "info", help="see the information about your account"
    )
    parser_info.add_argument("card_number", type=valid_card_number)
    parser_info.set_defaults(func=info)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        parser.error(e)


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


def make_files(iter: List[Tuple[str, str]]):
    for path, mode in iter:
        try:
            f = open(path, "x" + mode)
            if path.endswith("json"):
                json.dump(dict(), f)
        except FileExistsError:
            pass
        else:
            f.close()


@log
def new(args: argparse.Namespace):
    Account(args.bank_name, args.card_number, args.balance)


@log
def expence(args: argparse.Namespace):
    obj = Account.get(args.card_number)
    file_path = "saved_expence.json"
    if args.amount:
        obj.withdraw(args.amount, args.title)
        if args.save:
            with open(file_path, "r+") as f:
                file: dict = json.load(f)
                file[args.title] = args.amount
                f.seek(0)
                f.truncate()
                json.dump(file, f)
    else:
        with open(file_path, "r") as f:
            file: dict = json.load(f)
            try:
                amount = file[args.title]
            except KeyError:
                raise ValueError("this title doesnt exists in saved list") from None
            else:
                obj.withdraw(amount, args.title)
    print(obj._history[-1])


@log
def income(args: argparse.Namespace):
    obj = Account.get(args.card_number)
    file_path = "saved_income.json"
    if args.amount:
        obj.deposite(args.amount, args.title)
        if args.save:
            with open(file_path, "r+") as f:
                file: dict = json.load(f)
                file[args.title] = args.amount
                f.seek(0)
                f.truncate()
                json.dump(file, f)
    else:
        with open(file_path, "r") as f:
            file: dict = json.load(f)
            try:
                amount = file[args.title]
            except KeyError:
                raise ValueError("this title doesnt exists in saved list") from None
            else:
                obj.deposite(amount, args.title)
    print(obj._history[-1])


def history(args: argparse.Namespace):
    obj = Account.get(args.card_number)
    list(map(print, obj._history))


def info(args: argparse.Namespace):
    obj = Account.get(args.card_number)
    print(obj)


def valid_card_number(s: str) -> int:

    if 4 <= len(s) <= 8 and s.isdigit():
        return int(s)
    raise argparse.ArgumentTypeError("input must be 4 to 8 diggit number")


def valid_balance(s: str) -> int:
    if s.isdigit() and int(s) >= 0:
        return int(s)
    else:
        raise argparse.ArgumentTypeError("balance must be positive intiger")


class Account:
    valid_bank_names: List[str] = ["melli", "mellat", "sepah", "resalat", "tejarat"]
    pickel_path = "accunts.pkl"

    def __init__(self, bank_name: str, card_number: int, balance: int) -> None:
        self._bank_name = bank_name
        self._card_number = card_number
        self._balance = balance
        self._history: List[str] = []
        self._update()

    def __str__(self) -> str:
        return f"${self._balance} in {self._card_number} from {self._bank_name} bank"

    @property
    def _bank_name(self) -> str:
        return self.__bank_name

    @_bank_name.setter
    def _bank_name(self, value: str) -> None:
        value = value.lower()
        if value in self.valid_bank_names:
            self.__bank_name = value
        else:
            raise ValueError(f"bank name must be in {self.valid_bank_names}")

    @property
    def _card_number(self) -> int:
        return self.__card_number

    @_card_number.setter
    def _card_number(self, value: int) -> None:
        if not 4 <= len(str(value)) <= 8:
            raise ValueError("card number must have 4 to 8 digits")
        try:
            self.__card_number = int(value)
        except:
            raise ValueError("card number must be integer") from None

    @property
    def _balance(self) -> int:
        return self.__balance

    @_balance.setter
    def _balance(self, value: int) -> None:
        try:
            value = int(value)
        except:
            raise ValueError("card number must be integer") from None
        if value < 0:
            raise ValueError("balance must be a pisitive integer")
        self.__balance = value

    def _update(self) -> None:
        with open(self.pickel_path, "rb+") as f:
            lis = [self]
            while True:
                try:
                    obj: Account = pickle.load(f)
                except EOFError:
                    break
                else:
                    if obj._card_number == self._card_number:
                        continue
                    lis.append(obj)

            f.seek(0)
            f.truncate()
            for i in lis:
                pickle.dump(i, f)

    @classmethod
    def get(cls, card_number: int) -> "Account":
        with open(cls.pickel_path, "rb") as f:
            while True:
                try:
                    obj: Account = pickle.load(f)
                except EOFError:
                    raise ValueError(
                        "you dont have an account with account number that you provided"
                    ) from None
                if obj._card_number == card_number:
                    return obj

    def deposite(self, value: int, title: str) -> None:
        self._balance += value
        self._history.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: ${value} was deposited for {title} new balance is {self._balance}"
        )
        self._update()

    def withdraw(self, value: int, title: str):
        if value > self._balance:
            raise ValueError("your balance is not enough") from None
        else:
            self._balance -= value
            self._history.append(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: ${value} was witdrawed for {title} new balance is {self._balance}"
            )
            self._update()


main()
