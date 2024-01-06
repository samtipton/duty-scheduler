from enum import Enum


class Duty:
    def __init__(self, name: str, key: str, exclusions: [str] = []):
        self.name = name
        self.key = key
        self.exclusions = exclusions


class DutyKey(Enum):
    ALL_DUTIES_THIS_WEEK = "*"
    ALL_DUTIES_THIS_SERVICE = "_"
    FIRST_SONG_LEADER = "first_song_leader"
    FIRST_OPENING_PRAYER = "first_opening_prayer"
    FIRST_LESSON = "first_lesson"
    OPENING_PRAYER = "opening_prayer"
    CLOSING_PRAYER = "closing_prayer"
    SONG_LEADER = "song_leader"
    SCRIPTURE_READING = "scripture_reading"
    TABLE_LEAD_CUP = "table_lead_cup"
    TABLE_AID_CUP = "table_aid_cup"
    TABLE_LEAD_BREAD = "table_lead_bread"
    TABLE_AID_BREAD = "table_aid_bread"
    LESSON = "lesson"
    WEDNESDAY_SONG_LEADER = "wednesday_song_leader"
    WEDNESDAY_OPENING_PRAYER = "wednesday_opening_prayer"
    WEDNESDAY_CLOSING_PRAYER = "wednesday_closing_prayer"
    WEDNESDAY_LESSON = "wednesday_lesson"
    USHER = "usher"
    ALT_USHER = "alt_usher"
    SECURITY = "security"
    SOUND_BOARD_OPERATOR = "song_board_operator"
    LORDS_SUPPER_PREP = "lords_supper_prep"


class Duties(Enum):
    # 9am Duties
    FIRST_SONG_LEADER = Duty(
        "Song Leader", DutyKey.FIRST_SONG_LEADER, [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )
    FIRST_OPENING_PRAYER = Duty(
        "Song Leader", DutyKey.FIRST_OPENING_PRAYER, [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )
    FIRST_LESSON = Duty(
        "Lesson", DutyKey.FIRST_LESSON, [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )

    # 10:30am Duties
    OPENING_PRAYER = Duty(
        "Opening Prayer", DutyKey.OPENING_PRAYER, [DutyKey.CLOSING_PRAYER]
    )
    CLOSING_PRAYER = Duty(
        "Closing Prayer", DutyKey.CLOSING_PRAYER, [DutyKey.OPENING_PRAYER]
    )
    SONG_LEADER = Duty(
        "Song Leader", DutyKey.SONG_LEADER, [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )
    SCRIPTURE_READING = Duty("Scripture Reading", DutyKey.SCRIPTURE_READING)

    TABLE_LEAD_CUP = Duty(
        "Table Lead Cup (N)",
        DutyKey.TABLE_LEAD_CUP,
        [DutyKey.TABLE_AID_CUP, DutyKey.TABLE_AID_BREAD, DutyKey.TABLE_LEAD_BREAD],
    )
    TABLE_AID_CUP = Duty(
        "Table Aid Cup (N)",
        DutyKey.TABLE_AID_CUP,
        [DutyKey.TABLE_LEAD_CUP, DutyKey.TABLE_AID_BREAD, DutyKey.TABLE_LEAD_BREAD],
    )
    TABLE_LEAD_BREAD = Duty(
        "Table Lead Bread (S)",
        DutyKey.TABLE_LEAD_BREAD,
        [DutyKey.TABLE_AID_CUP, DutyKey.TABLE_AID_BREAD, DutyKey.TABLE_LEAD_CUP],
    )
    TABLE_AID_BREAD = Duty(
        "Table Aid Bread (S)",
        DutyKey.TABLE_AID_BREAD,
        [DutyKey.TABLE_AID_CUP, DutyKey.TABLE_LEAD_CUP, DutyKey.TABLE_LEAD_BREAD],
    )

    LESSON = Duty("Lesson", DutyKey.LESSON, [])
    WEDNESDAY_SONG_LEADER = Duty(
        "Song Leader", DutyKey.WEDNESDAY_SONG_LEADER, [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )
    WEDNESDAY_OPENING_PRAYER = Duty(
        "Opening Prayer",
        DutyKey.WEDNESDAY_OPENING_PRAYER,
        [DutyKey.ALL_DUTIES_THIS_SERVICE],
    )
    WEDNESDAY_CLOSING_PRAYER = Duty(
        "Closing Prayer",
        DutyKey.WEDNESDAY_CLOSING_PRAYER,
        [DutyKey.ALL_DUTIES_THIS_SERVICE],
    )
    WEDNESDAY_LESSON = Duty(
        "Lesson", "wednesday_lesson", [DutyKey.ALL_DUTIES_THIS_SERVICE]
    )

    USHER = Duty(
        "Weekly Usher",
        DutyKey.USHER,
        [DutyKey.ALT_USHER, DutyKey.SONG_LEADER, DutyKey.FIRST_SONG_LEADER],
    )
    ALT_USHER = Duty(
        "Weekly Alt Usher",
        DutyKey.ALT_USHER,
        [DutyKey.USHER, DutyKey.SONG_LEADER, DutyKey.FIRST_SONG_LEADER],
    )

    SECURITY = Duty("Security", DutyKey.SECURITY, [DutyKey.ALL_DUTIES_THIS_WEEK])
    SOUND_BOARD_OPERATOR = Duty(
        "Sound Board Operator",
        DutyKey.SOUND_BOARD_OPERATOR,
        [DutyKey.ALL_DUTIES_THIS_WEEK],
    )
    LORDS_SUPPER_PREP = Duty(
        "Monthly Lord's Supper Preparation", DutyKey.LORDS_SUPPER_PREP, []
    )
