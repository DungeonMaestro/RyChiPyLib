class CyclicSet:
	__slots__ = ["_obj"]

	def __init__(self, obj):
		self._obj = [o for o in obj]

	def __iter__(self):
		cursor = 0
		while True:
			yield self._obj[cursor]

	def __getitem__(self, item):
		return self._obj[item % len(self._obj)]

	def add(self, item):
		if item not in self._obj:
			self._obj.append(item)

class CyclicSpace:
	def __init__(self, period):
		self._period = period
