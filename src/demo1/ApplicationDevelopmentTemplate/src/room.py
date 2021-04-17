import baseAPI
class room:
	def __init__(self,l):
		self.label=l
		self.groupName='room'
	def getTypeList(self):
		return baseAPI.getSensorTypes(self.label,self.groupName)
	def getSensorCount(self,sensorType):
		return baseAPI.getSensorCount(self.label,sensorType)
	def getSensorLabel(self,sensorType,index):
		return baseAPI.getSensorLabel(self.label,sensorType,index)
