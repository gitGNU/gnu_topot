from weakref import ref

class InputCell(object):
  def __init__(self, init):
    self._value = init
    self._clients = []
    self.stable = True

  def _setValue(self, value):
    if not (self.stable and self._value == value):
      self._value = value
      for client in self._clients:
        client()._update()

  def _getValue(self):
    return self._value

  value = property(_getValue, _setValue)

  def _register(self, client):
    self._clients.append(ref(client, lambda r: self._clients.remove(r)))

class OutputCell(object):
  def __init__(self, action, *sources):
    self._sources = sources
    for source in sources:
      source._register(self)
    self.action = action

  def _update(self):
    self.action()

class Cell(InputCell, OutputCell):
  def __init__(self, compute, *sources):
    def recompute():
      self.value = compute()
    OutputCell.__init__(self, recompute, *sources)
    InputCell.__init__(self, compute())
