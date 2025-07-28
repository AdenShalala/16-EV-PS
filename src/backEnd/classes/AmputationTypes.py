from enum import Enum

class AmputationType(Enum):
    ThroughHip = "Through Hip/Pelvic"
    Transfemoral = "Transfemoral/Above Knee"
    Transtibial = "Transtibial/Below Knee"
    KneeDisarticulation = "Knee Disarticulation/Through Knee"
    AnkleDisarticulation = "Ankle Disarticulation / Above Knee"
    Foot = "Foot or Toe"