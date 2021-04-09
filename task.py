import sys

class Client:
  def __init__(self, surname, name, cash):
    self.surname = surname
    self.name = name
    self.cash = cash

  def __repr__(self):
    visuals = '{} {}\ncash: {} zl'.format(self.surname, self.name, self.cash)
    return visuals

  def input(self, value):
    self.cash += value

  def withdrawal(self, value):
    self.cash -= value

  def transfer(self, value, client_to):
    self.cash -= value
    client_to.cash += value

  def interface(self, command):
    if command == '':
      pass
    elif command == 'i':
      self.input(float(input()))
    elif command == 'w':
      self.withdrawal(float(input()))
    elif command == 'q':
      sys.exit()

class Bank:
  def __init__(self, name):
    self.name = name
    self.clients = []

  def add_client(self, surname, name, cash):
    self.clients.append(Client(surname, name, cash))

  def __repr__(self):
    return '{}'.format(self.name)

  def __str__(self):
    visuals = '{}\n'.format(self.name)
    visuals += 'Number of clients: {}\n'.format(len(self.clients))
    return visuals


if __name__ == '__main__':
  banks = []
  banks.append(Bank('mbank'))
  banks.append(Bank('PKO'))

  print(banks)

  banks[0].add_client('Anna','Nowak',1000)
  banks[0].add_client('Ewa','Nowak',1000)
  banks[1].add_client('Piotr','Kowalski',2000)

  print(banks[0])
  print(banks[1])

  print('\n---------- input/withdrawal ----------\n')
  
  print(banks[0].clients[0])
  banks[0].clients[0].input(100)
  print(banks[0].clients[0])
  banks[0].clients[0].withdrawal(200)
  print(banks[0].clients[0])

  print('\n---------- transfer ----------\n')

  print(banks[1].clients[0])
  print(banks[0].clients[0])

  print()
  banks[1].clients[0].transfer(500,banks[0].clients[0])

  print(banks[1].clients[0])
  print(banks[0].clients[0])

  client = banks[1].clients[0]
  while True:
    client.interface(input())
    print(client)
