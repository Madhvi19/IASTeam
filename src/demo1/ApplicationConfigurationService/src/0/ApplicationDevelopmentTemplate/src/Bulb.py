import baseAPI
class Bulb:
	def __init__(self,l):
		self.label=l
	def getcolor(self):
		return baseAPI.get(self.label,'color')
	def getintensity(self):
		return baseAPI.get(self.label,'intensity')
	def changeColor(self,dict):
		baseAPI.applyControl(self.label,'changeColor',dict)
	def changeIntensity(self,dict):
		baseAPI.applyControl(self.label,'changeIntensity',dict)
