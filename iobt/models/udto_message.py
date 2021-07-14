import json
from typing import Type
from enum import Enum
import uuid
from datetime import datetime

sourceGUID = f"{uuid.uuid4()}"


class Objective(Enum):
    POINT_OF_INTEREST = 'POINT_OF_INTEREST'
    POSSIBLE_TARGET = 'POSSIBLE_TARGET'
    CONFIRMED_TARGET = 'CONFIRMED_TARGET'

class UDTO_Base:
    sourceGuid: str
    timeStamp: str
    personId: str


    def __init__(self, properties):
        now = datetime.now()
        self.timeStamp = now.isoformat()
        self.sourceGuid = sourceGUID
        self.personId = "PAN1"
        self.override(properties)


    def toJSONString(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDICT(self):
        return self.__dict__

    def override(self, properties = None):
        if (properties is not None):
            for key in properties:
                setattr(self, key, properties[key])    

class UDTO_ChatMessage(UDTO_Base):
    user: str
    message: str

    def __init__(self, properties):
        super().__init__(properties)

class UDTO_Command(UDTO_Base):
    targetGuid: str
    command: str
    args: list

    def __init__(self, properties):
        super().__init__(properties)

class Location(UDTO_Base):
    lat: int
    lng: int
    alt: int

    def __init__(self, properties):
        super().__init__(properties)

class UDTO_Position(Location):
    user: str
    speed: int
    heading: int

    def __init__(self, properties):
        super().__init__(properties)

class UDTO_Objective(Location):
    uniqueGuid: str
    name: str
    type: Objective
    note: str

    def __init__(self, properties):
        self.uniqueGuid = f"{uuid.uuid4()}"
        super().__init__(properties)

class UDTO_Observation(Location):
    uniqueGuid: str
    user: str
    target: str
    isTarget=False
    range: int

    def __init__(self, properties):
        self.uniqueGuid = f"{uuid.uuid4()}"
        super().__init__(properties)