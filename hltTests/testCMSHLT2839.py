import sys

def accept(event_count, offset, prescale):
  return (((event_count + offset) % prescale) == 0)

n_events = int(sys.argv[1])
n_datasets = int(sys.argv[2])
prescale1 = int(sys.argv[3])
prescale2 = int(sys.argv[4])

class EventResults:
  def __init__(self):
    self.trigger = False
    self.pds = []
    self.finor = False

eventResults = []
for event_i in range(n_events):
  er = EventResults()
  er.trigger = accept(event_i, 0, prescale1)
  finor = False
  for pd_j in range(n_datasets):
    pd_res = er.trigger and accept(event_i, pd_j, prescale2)
    finor = (finor or pd_res)
    er.pds.append(pd_res)
  er.finor = finor
  eventResults.append(er)

def show_tr(ret):
  return '1' if ret else ' '

print(f'n_events = {n_events}')
print(f'n_datasets = {n_datasets}')
print(f'prescale1 = {prescale1}')
print(f'prescale2 = {prescale2}')
print('-'*25)
print('Trigger: '+' '.join([show_tr(foo.trigger) for foo in eventResults]))
for pd_j in range(n_datasets):
  print(f'PD {pd_j}   : '+' '.join([show_tr(foo.pds[pd_j]) for foo in eventResults]))
print('-'*25)
print('PD OR  : '+' '.join([show_tr(foo.finor) for foo in eventResults]))
print('-'*25)
print('Accepted:', sum([int(foo.finor) for foo in eventResults]))
