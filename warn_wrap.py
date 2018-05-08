from abc import ABC, abstractmethod
class warn_wrap(ABC):
    @abstractmethod
    def __init__(self):
        self.warning=[]
        self.tags=[]
    @abstractmethod
    def getCurrWarn(self,filt=''):
        pass
    
