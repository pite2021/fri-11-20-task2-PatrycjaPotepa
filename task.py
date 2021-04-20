import sys
import logging
import multiprocessing as mp
from dataclasses import dataclass

class Client:
  def __init__(self, name, surname, cash, credit=0, bank=None):
    self.bank = bank
    self.surname = surname
    self.name = name
    self.cash = cash
    self.credit = credit
    self.cards = []
    self.command_dict = {}
    self.command_dict['i'] = self.command_i
    self.command_dict['w'] = self.command_w
    self.command_dict['q'] = self.command_q

  @property
  def name(self):
    name = self._name[0].upper() + self._name[1:].lower()
    return name

  @name.setter
  def name(self, name):
    if any(c.isdigit() for c in name):
      raise ValueError('Number in name.')
    self._name = name

  def __repr__(self):
    visuals = '\n{} {}\ncash:\t{} zl\ncredit:\t{} zl'.format(self.surname, self.name, self.cash, self.credit)
    return visuals

  def input(self, value):
    self.cash += value

  def withdrawal(self, value):
    self.cash -= value

  def take_credit(self, value):
    self.credit += value
    self.cash += value

  def pay_credit(self, value):
    self.credit -= value
    self.cash -= value

  def transfer(self, value, client_to):
    self.cash -= value
    client_to.cash += value

  def change_bank(self, bank):
    bank.add_client(self.surname, self.name, self.cash)
    self.bank.delete_client(self)

  def delete_account(self):
    self.bank.delete_client(self)
    self.bank = None

  def add_card(self, cash=0, currency='PLN', fee=5):
    card = Card(cash,currency, fee)
    self.cards.append(card)

  def interface(self, command):
    if command in self.command_dict:
      self.command_dict[command]()

  def command_i(self):
    try:
      val = float(input())
      self.input(val)
    except:
      pass

  def command_w(self):
    try:
      val = float(input())
      self.withdrawal(val)
    except:
      pass

  def command_q(self):
    sys.exit()


class Bank:
  def __init__(self, name):
    self.name = name
    self.clients = []

  @classmethod
  def from_list(cls, name, clients):
    bank = cls(name)
    for client in clients:
      client.bank = bank
    bank.clients = clients
    return bank

  @staticmethod
  def total_money(banks):
    money = 0
    for bank in banks:
      money += bank.money()
    return money

  def add_client(self, surname, name, cash):
    self.clients.append(Client(surname, name, cash, bank=self))

  def delete_client(self, client):
    self.clients.remove(client)

  def __repr__(self):
    return '{}'.format(self.name)

  def __str__(self):
    visuals = '{}\n'.format(self.name)
    visuals += 'Number of clients: {}\n'.format(len(self.clients))
    return visuals

  def money(self):
    money = 0
    for client in self.clients:
      money += client.cash
    return money


@dataclass
class Card:
  cash: float
  currency: str
  fee: float

  def input(self, value):
    self.cash += value

  def withdrawal(self, value):
    self.cash -= value 


def gen():
    while True:
      yield input()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  banks = []
  banks.append(Bank('mbank'))
  banks.append(Bank('PKO'))

  logging.info(banks)

  banks[0].add_client('Anna','Nowak',1000.)
  banks[0].add_client('EWA','Nowak',1000.)
  banks[1].add_client('piotr','Kowalski',2000.)

  clients=[Client('TomasZ','Pawlik',3500.)]
  bank = Bank.from_list('ING', clients)
  banks.append(bank)

  logging.info(banks[0])
  logging.info(banks[1])
  logging.info(banks[2].clients[0].bank)

  logging.info('\n---------- Multiprocessing ----------\n')

  def fun(bank):
    return bank.money()

  with mp.Pool(mp.cpu_count()) as p:
    results = p.map(fun, banks)

  logging.info(results)

  logging.info('\n---------- Static ----------\n')

  total_money = Bank.total_money(banks)
  logging.info(total_money)

  logging.info('\n---------- Dataclass ----------\n')

  banks[0].clients[0].add_card()
  banks[0].clients[0].add_card(currency='EUR')
  banks[0].clients[0].add_card(fee=0)
  banks[0].clients[0].cards[0].input(500.)
  banks[0].clients[0].cards[0].withdrawal(100.)
  for card in banks[0].clients[0].cards:
    logging.info(card)

  logging.info('\n---------- input/withdrawal ----------\n')
  
  logging.info(banks[0].clients[0])
  banks[0].clients[0].input(100.)
  logging.info(banks[0].clients[0])
  banks[0].clients[0].withdrawal(200.)
  logging.info(banks[0].clients[0])

  logging.info('\n---------- credit ----------\n')
  
  logging.info(banks[0].clients[0])
  banks[0].clients[0].take_credit(5000.)
  logging.info(banks[0].clients[0])
  banks[0].clients[0].pay_credit(5000.)
  logging.info(banks[0].clients[0])

  logging.info('\n---------- transfer ----------\n')

  logging.info(banks[1].clients[0])
  logging.info(banks[0].clients[0])

  logging.info('\n')
  banks[1].clients[0].transfer(500.,banks[0].clients[0])

  logging.info(banks[1].clients[0])
  logging.info(banks[0].clients[0])

  logging.info('\n---------- change bank ----------\n')
  logging.info(banks[0])
  logging.info(banks[1])
  banks[0].clients[0].change_bank(banks[1])
  logging.info(banks[0])
  logging.info(banks[1])

  logging.info('\n---------- delete account ----------\n')
  logging.info(banks[1])
  banks[1].clients[0].delete_account()
  logging.info(banks[1])

  logging.info('\n---------- Command Line Interface ----------\n')

  client = banks[1].clients[0]
  for command in gen():
    client.interface(command)
    logging.info(client)