from dataclasses import dataclass
@dataclass
class RunState: status:str="planned"; approved:bool=False
