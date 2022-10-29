from typing import Any, List, Optional, TypeVar, Callable, Type, cast
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class ElementStat:
    label: str
    name: str

    def __init__(self, label: str, name: str) -> None:
        self.label = label
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'ElementStat':
        assert isinstance(obj, dict)
        label = from_str(obj.get("label"))
        name = from_str(obj.get("name"))
        return ElementStat(label, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_str(self.label)
        result["name"] = from_str(self.name)
        return result


class ElementType:
    id: int
    plural_name: str
    plural_name_short: str
    singular_name: str
    singular_name_short: str
    squad_select: int
    squad_min_play: int
    squad_max_play: int
    ui_shirt_specific: bool
    sub_positions_locked: List[int]
    element_count: int

    def __init__(self, id: int, plural_name: str, plural_name_short: str, singular_name: str, singular_name_short: str, squad_select: int, squad_min_play: int, squad_max_play: int, ui_shirt_specific: bool, sub_positions_locked: List[int], element_count: int) -> None:
        self.id = id
        self.plural_name = plural_name
        self.plural_name_short = plural_name_short
        self.singular_name = singular_name
        self.singular_name_short = singular_name_short
        self.squad_select = squad_select
        self.squad_min_play = squad_min_play
        self.squad_max_play = squad_max_play
        self.ui_shirt_specific = ui_shirt_specific
        self.sub_positions_locked = sub_positions_locked
        self.element_count = element_count

    @staticmethod
    def from_dict(obj: Any) -> 'ElementType':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        plural_name = from_str(obj.get("plural_name"))
        plural_name_short = from_str(obj.get("plural_name_short"))
        singular_name = from_str(obj.get("singular_name"))
        singular_name_short = from_str(obj.get("singular_name_short"))
        squad_select = from_int(obj.get("squad_select"))
        squad_min_play = from_int(obj.get("squad_min_play"))
        squad_max_play = from_int(obj.get("squad_max_play"))
        ui_shirt_specific = from_bool(obj.get("ui_shirt_specific"))
        sub_positions_locked = from_list(from_int, obj.get("sub_positions_locked"))
        element_count = from_int(obj.get("element_count"))
        return ElementType(id, plural_name, plural_name_short, singular_name, singular_name_short, squad_select, squad_min_play, squad_max_play, ui_shirt_specific, sub_positions_locked, element_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["plural_name"] = from_str(self.plural_name)
        result["plural_name_short"] = from_str(self.plural_name_short)
        result["singular_name"] = from_str(self.singular_name)
        result["singular_name_short"] = from_str(self.singular_name_short)
        result["squad_select"] = from_int(self.squad_select)
        result["squad_min_play"] = from_int(self.squad_min_play)
        result["squad_max_play"] = from_int(self.squad_max_play)
        result["ui_shirt_specific"] = from_bool(self.ui_shirt_specific)
        result["sub_positions_locked"] = from_list(from_int, self.sub_positions_locked)
        result["element_count"] = from_int(self.element_count)
        return result


class Status(Enum):
    A = "a"
    D = "d"
    I = "i"
    N = "n"
    S = "s"
    U = "u"


class Element:
    chance_of_playing_next_round: Optional[int]
    chance_of_playing_this_round: Optional[int]
    code: int
    cost_change_event: int
    cost_change_event_fall: int
    cost_change_start: int
    cost_change_start_fall: int
    dreamteam_count: int
    element_type: int
    ep_next: str
    ep_this: str
    event_points: int
    first_name: str
    form: str
    id: int
    in_dreamteam: bool
    news: str
    news_added: Optional[datetime]
    now_cost: int
    photo: str
    points_per_game: str
    second_name: str
    selected_by_percent: str
    special: bool
    squad_number: None
    status: Status
    team: int
    team_code: int
    total_points: int
    transfers_in: int
    transfers_in_event: int
    transfers_out: int
    transfers_out_event: int
    value_form: str
    value_season: str
    web_name: str
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int
    influence: str
    creativity: str
    threat: str
    ict_index: str
    influence_rank: int
    influence_rank_type: int
    creativity_rank: int
    creativity_rank_type: int
    threat_rank: int
    threat_rank_type: int
    ict_index_rank: int
    ict_index_rank_type: int
    corners_and_indirect_freekicks_order: Optional[int]
    corners_and_indirect_freekicks_text: str
    direct_freekicks_order: Optional[int]
    direct_freekicks_text: str
    penalties_order: Optional[int]
    penalties_text: str
    now_cost_rank: int
    now_cost_rank_type: int
    form_rank: int
    form_rank_type: int
    points_per_game_rank: int
    points_per_game_rank_type: int
    selected_rank: int
    selected_rank_type: int

    def __init__(self, chance_of_playing_next_round: Optional[int], chance_of_playing_this_round: Optional[int], code: int, cost_change_event: int, cost_change_event_fall: int, cost_change_start: int, cost_change_start_fall: int, dreamteam_count: int, element_type: int, ep_next: str, ep_this: str, event_points: int, first_name: str, form: str, id: int, in_dreamteam: bool, news: str, news_added: Optional[datetime], now_cost: int, photo: str, points_per_game: str, second_name: str, selected_by_percent: str, special: bool, squad_number: None, status: Status, team: int, team_code: int, total_points: int, transfers_in: int, transfers_in_event: int, transfers_out: int, transfers_out_event: int, value_form: str, value_season: str, web_name: str, minutes: int, goals_scored: int, assists: int, clean_sheets: int, goals_conceded: int, own_goals: int, penalties_saved: int, penalties_missed: int, yellow_cards: int, red_cards: int, saves: int, bonus: int, bps: int, influence: str, creativity: str, threat: str, ict_index: str, influence_rank: int, influence_rank_type: int, creativity_rank: int, creativity_rank_type: int, threat_rank: int, threat_rank_type: int, ict_index_rank: int, ict_index_rank_type: int, corners_and_indirect_freekicks_order: Optional[int], corners_and_indirect_freekicks_text: str, direct_freekicks_order: Optional[int], direct_freekicks_text: str, penalties_order: Optional[int], penalties_text: str, now_cost_rank: int, now_cost_rank_type: int, form_rank: int, form_rank_type: int, points_per_game_rank: int, points_per_game_rank_type: int, selected_rank: int, selected_rank_type: int) -> None:
        self.chance_of_playing_next_round = chance_of_playing_next_round
        self.chance_of_playing_this_round = chance_of_playing_this_round
        self.code = code
        self.cost_change_event = cost_change_event
        self.cost_change_event_fall = cost_change_event_fall
        self.cost_change_start = cost_change_start
        self.cost_change_start_fall = cost_change_start_fall
        self.dreamteam_count = dreamteam_count
        self.element_type = element_type
        self.ep_next = ep_next
        self.ep_this = ep_this
        self.event_points = event_points
        self.first_name = first_name
        self.form = form
        self.id = id
        self.in_dreamteam = in_dreamteam
        self.news = news
        self.news_added = news_added
        self.now_cost = now_cost
        self.photo = photo
        self.points_per_game = points_per_game
        self.second_name = second_name
        self.selected_by_percent = selected_by_percent
        self.special = special
        self.squad_number = squad_number
        self.status = status
        self.team = team
        self.team_code = team_code
        self.total_points = total_points
        self.transfers_in = transfers_in
        self.transfers_in_event = transfers_in_event
        self.transfers_out = transfers_out
        self.transfers_out_event = transfers_out_event
        self.value_form = value_form
        self.value_season = value_season
        self.web_name = web_name
        self.minutes = minutes
        self.goals_scored = goals_scored
        self.assists = assists
        self.clean_sheets = clean_sheets
        self.goals_conceded = goals_conceded
        self.own_goals = own_goals
        self.penalties_saved = penalties_saved
        self.penalties_missed = penalties_missed
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.saves = saves
        self.bonus = bonus
        self.bps = bps
        self.influence = influence
        self.creativity = creativity
        self.threat = threat
        self.ict_index = ict_index
        self.influence_rank = influence_rank
        self.influence_rank_type = influence_rank_type
        self.creativity_rank = creativity_rank
        self.creativity_rank_type = creativity_rank_type
        self.threat_rank = threat_rank
        self.threat_rank_type = threat_rank_type
        self.ict_index_rank = ict_index_rank
        self.ict_index_rank_type = ict_index_rank_type
        self.corners_and_indirect_freekicks_order = corners_and_indirect_freekicks_order
        self.corners_and_indirect_freekicks_text = corners_and_indirect_freekicks_text
        self.direct_freekicks_order = direct_freekicks_order
        self.direct_freekicks_text = direct_freekicks_text
        self.penalties_order = penalties_order
        self.penalties_text = penalties_text
        self.now_cost_rank = now_cost_rank
        self.now_cost_rank_type = now_cost_rank_type
        self.form_rank = form_rank
        self.form_rank_type = form_rank_type
        self.points_per_game_rank = points_per_game_rank
        self.points_per_game_rank_type = points_per_game_rank_type
        self.selected_rank = selected_rank
        self.selected_rank_type = selected_rank_type

    @staticmethod
    def from_dict(obj: Any) -> 'Element':
        assert isinstance(obj, dict)
        chance_of_playing_next_round = from_union([from_int, from_none], obj.get("chance_of_playing_next_round"))
        chance_of_playing_this_round = from_union([from_int, from_none], obj.get("chance_of_playing_this_round"))
        code = from_int(obj.get("code"))
        cost_change_event = from_int(obj.get("cost_change_event"))
        cost_change_event_fall = from_int(obj.get("cost_change_event_fall"))
        cost_change_start = from_int(obj.get("cost_change_start"))
        cost_change_start_fall = from_int(obj.get("cost_change_start_fall"))
        dreamteam_count = from_int(obj.get("dreamteam_count"))
        element_type = from_int(obj.get("element_type"))
        ep_next = from_str(obj.get("ep_next"))
        ep_this = from_str(obj.get("ep_this"))
        event_points = from_int(obj.get("event_points"))
        first_name = from_str(obj.get("first_name"))
        form = from_str(obj.get("form"))
        id = from_int(obj.get("id"))
        in_dreamteam = from_bool(obj.get("in_dreamteam"))
        news = from_str(obj.get("news"))
        news_added = from_union([from_none, from_datetime], obj.get("news_added"))
        now_cost = from_int(obj.get("now_cost"))
        photo = from_str(obj.get("photo"))
        points_per_game = from_str(obj.get("points_per_game"))
        second_name = from_str(obj.get("second_name"))
        selected_by_percent = from_str(obj.get("selected_by_percent"))
        special = from_bool(obj.get("special"))
        squad_number = from_none(obj.get("squad_number"))
        status = Status(obj.get("status"))
        team = from_int(obj.get("team"))
        team_code = from_int(obj.get("team_code"))
        total_points = from_int(obj.get("total_points"))
        transfers_in = from_int(obj.get("transfers_in"))
        transfers_in_event = from_int(obj.get("transfers_in_event"))
        transfers_out = from_int(obj.get("transfers_out"))
        transfers_out_event = from_int(obj.get("transfers_out_event"))
        value_form = from_str(obj.get("value_form"))
        value_season = from_str(obj.get("value_season"))
        web_name = from_str(obj.get("web_name"))
        minutes = from_int(obj.get("minutes"))
        goals_scored = from_int(obj.get("goals_scored"))
        assists = from_int(obj.get("assists"))
        clean_sheets = from_int(obj.get("clean_sheets"))
        goals_conceded = from_int(obj.get("goals_conceded"))
        own_goals = from_int(obj.get("own_goals"))
        penalties_saved = from_int(obj.get("penalties_saved"))
        penalties_missed = from_int(obj.get("penalties_missed"))
        yellow_cards = from_int(obj.get("yellow_cards"))
        red_cards = from_int(obj.get("red_cards"))
        saves = from_int(obj.get("saves"))
        bonus = from_int(obj.get("bonus"))
        bps = from_int(obj.get("bps"))
        influence = from_str(obj.get("influence"))
        creativity = from_str(obj.get("creativity"))
        threat = from_str(obj.get("threat"))
        ict_index = from_str(obj.get("ict_index"))
        influence_rank = from_int(obj.get("influence_rank"))
        influence_rank_type = from_int(obj.get("influence_rank_type"))
        creativity_rank = from_int(obj.get("creativity_rank"))
        creativity_rank_type = from_int(obj.get("creativity_rank_type"))
        threat_rank = from_int(obj.get("threat_rank"))
        threat_rank_type = from_int(obj.get("threat_rank_type"))
        ict_index_rank = from_int(obj.get("ict_index_rank"))
        ict_index_rank_type = from_int(obj.get("ict_index_rank_type"))
        corners_and_indirect_freekicks_order = from_union([from_int, from_none], obj.get("corners_and_indirect_freekicks_order"))
        corners_and_indirect_freekicks_text = from_str(obj.get("corners_and_indirect_freekicks_text"))
        direct_freekicks_order = from_union([from_int, from_none], obj.get("direct_freekicks_order"))
        direct_freekicks_text = from_str(obj.get("direct_freekicks_text"))
        penalties_order = from_union([from_int, from_none], obj.get("penalties_order"))
        penalties_text = from_str(obj.get("penalties_text"))
        now_cost_rank = from_int(obj.get("now_cost_rank"))
        now_cost_rank_type = from_int(obj.get("now_cost_rank_type"))
        form_rank = from_int(obj.get("form_rank"))
        form_rank_type = from_int(obj.get("form_rank_type"))
        points_per_game_rank = from_int(obj.get("points_per_game_rank"))
        points_per_game_rank_type = from_int(obj.get("points_per_game_rank_type"))
        selected_rank = from_int(obj.get("selected_rank"))
        selected_rank_type = from_int(obj.get("selected_rank_type"))
        return Element(chance_of_playing_next_round, chance_of_playing_this_round, code, cost_change_event, cost_change_event_fall, cost_change_start, cost_change_start_fall, dreamteam_count, element_type, ep_next, ep_this, event_points, first_name, form, id, in_dreamteam, news, news_added, now_cost, photo, points_per_game, second_name, selected_by_percent, special, squad_number, status, team, team_code, total_points, transfers_in, transfers_in_event, transfers_out, transfers_out_event, value_form, value_season, web_name, minutes, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, bonus, bps, influence, creativity, threat, ict_index, influence_rank, influence_rank_type, creativity_rank, creativity_rank_type, threat_rank, threat_rank_type, ict_index_rank, ict_index_rank_type, corners_and_indirect_freekicks_order, corners_and_indirect_freekicks_text, direct_freekicks_order, direct_freekicks_text, penalties_order, penalties_text, now_cost_rank, now_cost_rank_type, form_rank, form_rank_type, points_per_game_rank, points_per_game_rank_type, selected_rank, selected_rank_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["chance_of_playing_next_round"] = from_union([from_int, from_none], self.chance_of_playing_next_round)
        result["chance_of_playing_this_round"] = from_union([from_int, from_none], self.chance_of_playing_this_round)
        result["code"] = from_int(self.code)
        result["cost_change_event"] = from_int(self.cost_change_event)
        result["cost_change_event_fall"] = from_int(self.cost_change_event_fall)
        result["cost_change_start"] = from_int(self.cost_change_start)
        result["cost_change_start_fall"] = from_int(self.cost_change_start_fall)
        result["dreamteam_count"] = from_int(self.dreamteam_count)
        result["element_type"] = from_int(self.element_type)
        result["ep_next"] = from_str(self.ep_next)
        result["ep_this"] = from_str(self.ep_this)
        result["event_points"] = from_int(self.event_points)
        result["first_name"] = from_str(self.first_name)
        result["form"] = from_str(self.form)
        result["id"] = from_int(self.id)
        result["in_dreamteam"] = from_bool(self.in_dreamteam)
        result["news"] = from_str(self.news)
        result["news_added"] = from_union([from_none, lambda x: x.isoformat()], self.news_added)
        result["now_cost"] = from_int(self.now_cost)
        result["photo"] = from_str(self.photo)
        result["points_per_game"] = from_str(self.points_per_game)
        result["second_name"] = from_str(self.second_name)
        result["selected_by_percent"] = from_str(self.selected_by_percent)
        result["special"] = from_bool(self.special)
        result["squad_number"] = from_none(self.squad_number)
        result["status"] = to_enum(Status, self.status)
        result["team"] = from_int(self.team)
        result["team_code"] = from_int(self.team_code)
        result["total_points"] = from_int(self.total_points)
        result["transfers_in"] = from_int(self.transfers_in)
        result["transfers_in_event"] = from_int(self.transfers_in_event)
        result["transfers_out"] = from_int(self.transfers_out)
        result["transfers_out_event"] = from_int(self.transfers_out_event)
        result["value_form"] = from_str(self.value_form)
        result["value_season"] = from_str(self.value_season)
        result["web_name"] = from_str(self.web_name)
        result["minutes"] = from_int(self.minutes)
        result["goals_scored"] = from_int(self.goals_scored)
        result["assists"] = from_int(self.assists)
        result["clean_sheets"] = from_int(self.clean_sheets)
        result["goals_conceded"] = from_int(self.goals_conceded)
        result["own_goals"] = from_int(self.own_goals)
        result["penalties_saved"] = from_int(self.penalties_saved)
        result["penalties_missed"] = from_int(self.penalties_missed)
        result["yellow_cards"] = from_int(self.yellow_cards)
        result["red_cards"] = from_int(self.red_cards)
        result["saves"] = from_int(self.saves)
        result["bonus"] = from_int(self.bonus)
        result["bps"] = from_int(self.bps)
        result["influence"] = from_str(self.influence)
        result["creativity"] = from_str(self.creativity)
        result["threat"] = from_str(self.threat)
        result["ict_index"] = from_str(self.ict_index)
        result["influence_rank"] = from_int(self.influence_rank)
        result["influence_rank_type"] = from_int(self.influence_rank_type)
        result["creativity_rank"] = from_int(self.creativity_rank)
        result["creativity_rank_type"] = from_int(self.creativity_rank_type)
        result["threat_rank"] = from_int(self.threat_rank)
        result["threat_rank_type"] = from_int(self.threat_rank_type)
        result["ict_index_rank"] = from_int(self.ict_index_rank)
        result["ict_index_rank_type"] = from_int(self.ict_index_rank_type)
        result["corners_and_indirect_freekicks_order"] = from_union([from_int, from_none], self.corners_and_indirect_freekicks_order)
        result["corners_and_indirect_freekicks_text"] = from_str(self.corners_and_indirect_freekicks_text)
        result["direct_freekicks_order"] = from_union([from_int, from_none], self.direct_freekicks_order)
        result["direct_freekicks_text"] = from_str(self.direct_freekicks_text)
        result["penalties_order"] = from_union([from_int, from_none], self.penalties_order)
        result["penalties_text"] = from_str(self.penalties_text)
        result["now_cost_rank"] = from_int(self.now_cost_rank)
        result["now_cost_rank_type"] = from_int(self.now_cost_rank_type)
        result["form_rank"] = from_int(self.form_rank)
        result["form_rank_type"] = from_int(self.form_rank_type)
        result["points_per_game_rank"] = from_int(self.points_per_game_rank)
        result["points_per_game_rank_type"] = from_int(self.points_per_game_rank_type)
        result["selected_rank"] = from_int(self.selected_rank)
        result["selected_rank_type"] = from_int(self.selected_rank_type)
        return result


class ChipName(Enum):
    BBOOST = "bboost"
    FREEHIT = "freehit"
    THE_3_XC = "3xc"
    WILDCARD = "wildcard"


class ChipPlay:
    chip_name: ChipName
    num_played: int

    def __init__(self, chip_name: ChipName, num_played: int) -> None:
        self.chip_name = chip_name
        self.num_played = num_played

    @staticmethod
    def from_dict(obj: Any) -> 'ChipPlay':
        assert isinstance(obj, dict)
        chip_name = ChipName(obj.get("chip_name"))
        num_played = from_int(obj.get("num_played"))
        return ChipPlay(chip_name, num_played)

    def to_dict(self) -> dict:
        result: dict = {}
        result["chip_name"] = to_enum(ChipName, self.chip_name)
        result["num_played"] = from_int(self.num_played)
        return result


class TopElementInfo:
    id: int
    points: int

    def __init__(self, id: int, points: int) -> None:
        self.id = id
        self.points = points

    @staticmethod
    def from_dict(obj: Any) -> 'TopElementInfo':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        points = from_int(obj.get("points"))
        return TopElementInfo(id, points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["points"] = from_int(self.points)
        return result


class Event:
    id: int
    name: str
    deadline_time: datetime
    average_entry_score: int
    finished: bool
    data_checked: bool
    highest_scoring_entry: Optional[int]
    deadline_time_epoch: int
    deadline_time_game_offset: int
    highest_score: Optional[int]
    is_previous: bool
    is_current: bool
    is_next: bool
    cup_leagues_created: bool
    h2_h_ko_matches_created: bool
    chip_plays: List[ChipPlay]
    most_selected: Optional[int]
    most_transferred_in: Optional[int]
    top_element: Optional[int]
    top_element_info: Optional[TopElementInfo]
    transfers_made: int
    most_captained: Optional[int]
    most_vice_captained: Optional[int]

    def __init__(self, id: int, name: str, deadline_time: datetime, average_entry_score: int, finished: bool, data_checked: bool, highest_scoring_entry: Optional[int], deadline_time_epoch: int, deadline_time_game_offset: int, highest_score: Optional[int], is_previous: bool, is_current: bool, is_next: bool, cup_leagues_created: bool, h2_h_ko_matches_created: bool, chip_plays: List[ChipPlay], most_selected: Optional[int], most_transferred_in: Optional[int], top_element: Optional[int], top_element_info: Optional[TopElementInfo], transfers_made: int, most_captained: Optional[int], most_vice_captained: Optional[int]) -> None:
        self.id = id
        self.name = name
        self.deadline_time = deadline_time
        self.average_entry_score = average_entry_score
        self.finished = finished
        self.data_checked = data_checked
        self.highest_scoring_entry = highest_scoring_entry
        self.deadline_time_epoch = deadline_time_epoch
        self.deadline_time_game_offset = deadline_time_game_offset
        self.highest_score = highest_score
        self.is_previous = is_previous
        self.is_current = is_current
        self.is_next = is_next
        self.cup_leagues_created = cup_leagues_created
        self.h2_h_ko_matches_created = h2_h_ko_matches_created
        self.chip_plays = chip_plays
        self.most_selected = most_selected
        self.most_transferred_in = most_transferred_in
        self.top_element = top_element
        self.top_element_info = top_element_info
        self.transfers_made = transfers_made
        self.most_captained = most_captained
        self.most_vice_captained = most_vice_captained

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        deadline_time = from_datetime(obj.get("deadline_time"))
        average_entry_score = from_int(obj.get("average_entry_score"))
        finished = from_bool(obj.get("finished"))
        data_checked = from_bool(obj.get("data_checked"))
        highest_scoring_entry = from_union([from_int, from_none], obj.get("highest_scoring_entry"))
        deadline_time_epoch = from_int(obj.get("deadline_time_epoch"))
        deadline_time_game_offset = from_int(obj.get("deadline_time_game_offset"))
        highest_score = from_union([from_int, from_none], obj.get("highest_score"))
        is_previous = from_bool(obj.get("is_previous"))
        is_current = from_bool(obj.get("is_current"))
        is_next = from_bool(obj.get("is_next"))
        cup_leagues_created = from_bool(obj.get("cup_leagues_created"))
        h2_h_ko_matches_created = from_bool(obj.get("h2h_ko_matches_created"))
        chip_plays = from_list(ChipPlay.from_dict, obj.get("chip_plays"))
        most_selected = from_union([from_int, from_none], obj.get("most_selected"))
        most_transferred_in = from_union([from_int, from_none], obj.get("most_transferred_in"))
        top_element = from_union([from_int, from_none], obj.get("top_element"))
        top_element_info = from_union([TopElementInfo.from_dict, from_none], obj.get("top_element_info"))
        transfers_made = from_int(obj.get("transfers_made"))
        most_captained = from_union([from_int, from_none], obj.get("most_captained"))
        most_vice_captained = from_union([from_int, from_none], obj.get("most_vice_captained"))
        return Event(id, name, deadline_time, average_entry_score, finished, data_checked, highest_scoring_entry, deadline_time_epoch, deadline_time_game_offset, highest_score, is_previous, is_current, is_next, cup_leagues_created, h2_h_ko_matches_created, chip_plays, most_selected, most_transferred_in, top_element, top_element_info, transfers_made, most_captained, most_vice_captained)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["deadline_time"] = self.deadline_time.isoformat()
        result["average_entry_score"] = from_int(self.average_entry_score)
        result["finished"] = from_bool(self.finished)
        result["data_checked"] = from_bool(self.data_checked)
        result["highest_scoring_entry"] = from_union([from_int, from_none], self.highest_scoring_entry)
        result["deadline_time_epoch"] = from_int(self.deadline_time_epoch)
        result["deadline_time_game_offset"] = from_int(self.deadline_time_game_offset)
        result["highest_score"] = from_union([from_int, from_none], self.highest_score)
        result["is_previous"] = from_bool(self.is_previous)
        result["is_current"] = from_bool(self.is_current)
        result["is_next"] = from_bool(self.is_next)
        result["cup_leagues_created"] = from_bool(self.cup_leagues_created)
        result["h2h_ko_matches_created"] = from_bool(self.h2_h_ko_matches_created)
        result["chip_plays"] = from_list(lambda x: to_class(ChipPlay, x), self.chip_plays)
        result["most_selected"] = from_union([from_int, from_none], self.most_selected)
        result["most_transferred_in"] = from_union([from_int, from_none], self.most_transferred_in)
        result["top_element"] = from_union([from_int, from_none], self.top_element)
        result["top_element_info"] = from_union([lambda x: to_class(TopElementInfo, x), from_none], self.top_element_info)
        result["transfers_made"] = from_int(self.transfers_made)
        result["most_captained"] = from_union([from_int, from_none], self.most_captained)
        result["most_vice_captained"] = from_union([from_int, from_none], self.most_vice_captained)
        return result


class GameSettings:
    league_join_private_max: int
    league_join_public_max: int
    league_max_size_public_classic: int
    league_max_size_public_h2_h: int
    league_max_size_private_h2_h: int
    league_max_ko_rounds_private_h2_h: int
    league_prefix_public: str
    league_points_h2_h_win: int
    league_points_h2_h_lose: int
    league_points_h2_h_draw: int
    league_ko_first_instead_of_random: bool
    cup_start_event_id: None
    cup_stop_event_id: None
    cup_qualifying_method: None
    cup_type: None
    squad_squadplay: int
    squad_squadsize: int
    squad_team_limit: int
    squad_total_spend: int
    ui_currency_multiplier: int
    ui_use_special_shirts: bool
    ui_special_shirt_exclusions: List[Any]
    stats_form_days: int
    sys_vice_captain_enabled: bool
    transfers_cap: int
    transfers_sell_on_fee: float
    league_h2_h_tiebreak_stats: List[str]
    timezone: str

    def __init__(self, league_join_private_max: int, league_join_public_max: int, league_max_size_public_classic: int, league_max_size_public_h2_h: int, league_max_size_private_h2_h: int, league_max_ko_rounds_private_h2_h: int, league_prefix_public: str, league_points_h2_h_win: int, league_points_h2_h_lose: int, league_points_h2_h_draw: int, league_ko_first_instead_of_random: bool, cup_start_event_id: None, cup_stop_event_id: None, cup_qualifying_method: None, cup_type: None, squad_squadplay: int, squad_squadsize: int, squad_team_limit: int, squad_total_spend: int, ui_currency_multiplier: int, ui_use_special_shirts: bool, ui_special_shirt_exclusions: List[Any], stats_form_days: int, sys_vice_captain_enabled: bool, transfers_cap: int, transfers_sell_on_fee: float, league_h2_h_tiebreak_stats: List[str], timezone: str) -> None:
        self.league_join_private_max = league_join_private_max
        self.league_join_public_max = league_join_public_max
        self.league_max_size_public_classic = league_max_size_public_classic
        self.league_max_size_public_h2_h = league_max_size_public_h2_h
        self.league_max_size_private_h2_h = league_max_size_private_h2_h
        self.league_max_ko_rounds_private_h2_h = league_max_ko_rounds_private_h2_h
        self.league_prefix_public = league_prefix_public
        self.league_points_h2_h_win = league_points_h2_h_win
        self.league_points_h2_h_lose = league_points_h2_h_lose
        self.league_points_h2_h_draw = league_points_h2_h_draw
        self.league_ko_first_instead_of_random = league_ko_first_instead_of_random
        self.cup_start_event_id = cup_start_event_id
        self.cup_stop_event_id = cup_stop_event_id
        self.cup_qualifying_method = cup_qualifying_method
        self.cup_type = cup_type
        self.squad_squadplay = squad_squadplay
        self.squad_squadsize = squad_squadsize
        self.squad_team_limit = squad_team_limit
        self.squad_total_spend = squad_total_spend
        self.ui_currency_multiplier = ui_currency_multiplier
        self.ui_use_special_shirts = ui_use_special_shirts
        self.ui_special_shirt_exclusions = ui_special_shirt_exclusions
        self.stats_form_days = stats_form_days
        self.sys_vice_captain_enabled = sys_vice_captain_enabled
        self.transfers_cap = transfers_cap
        self.transfers_sell_on_fee = transfers_sell_on_fee
        self.league_h2_h_tiebreak_stats = league_h2_h_tiebreak_stats
        self.timezone = timezone

    @staticmethod
    def from_dict(obj: Any) -> 'GameSettings':
        assert isinstance(obj, dict)
        league_join_private_max = from_int(obj.get("league_join_private_max"))
        league_join_public_max = from_int(obj.get("league_join_public_max"))
        league_max_size_public_classic = from_int(obj.get("league_max_size_public_classic"))
        league_max_size_public_h2_h = from_int(obj.get("league_max_size_public_h2h"))
        league_max_size_private_h2_h = from_int(obj.get("league_max_size_private_h2h"))
        league_max_ko_rounds_private_h2_h = from_int(obj.get("league_max_ko_rounds_private_h2h"))
        league_prefix_public = from_str(obj.get("league_prefix_public"))
        league_points_h2_h_win = from_int(obj.get("league_points_h2h_win"))
        league_points_h2_h_lose = from_int(obj.get("league_points_h2h_lose"))
        league_points_h2_h_draw = from_int(obj.get("league_points_h2h_draw"))
        league_ko_first_instead_of_random = from_bool(obj.get("league_ko_first_instead_of_random"))
        cup_start_event_id = from_none(obj.get("cup_start_event_id"))
        cup_stop_event_id = from_none(obj.get("cup_stop_event_id"))
        cup_qualifying_method = from_none(obj.get("cup_qualifying_method"))
        cup_type = from_none(obj.get("cup_type"))
        squad_squadplay = from_int(obj.get("squad_squadplay"))
        squad_squadsize = from_int(obj.get("squad_squadsize"))
        squad_team_limit = from_int(obj.get("squad_team_limit"))
        squad_total_spend = from_int(obj.get("squad_total_spend"))
        ui_currency_multiplier = from_int(obj.get("ui_currency_multiplier"))
        ui_use_special_shirts = from_bool(obj.get("ui_use_special_shirts"))
        ui_special_shirt_exclusions = from_list(lambda x: x, obj.get("ui_special_shirt_exclusions"))
        stats_form_days = from_int(obj.get("stats_form_days"))
        sys_vice_captain_enabled = from_bool(obj.get("sys_vice_captain_enabled"))
        transfers_cap = from_int(obj.get("transfers_cap"))
        transfers_sell_on_fee = from_float(obj.get("transfers_sell_on_fee"))
        league_h2_h_tiebreak_stats = from_list(from_str, obj.get("league_h2h_tiebreak_stats"))
        timezone = from_str(obj.get("timezone"))
        return GameSettings(league_join_private_max, league_join_public_max, league_max_size_public_classic, league_max_size_public_h2_h, league_max_size_private_h2_h, league_max_ko_rounds_private_h2_h, league_prefix_public, league_points_h2_h_win, league_points_h2_h_lose, league_points_h2_h_draw, league_ko_first_instead_of_random, cup_start_event_id, cup_stop_event_id, cup_qualifying_method, cup_type, squad_squadplay, squad_squadsize, squad_team_limit, squad_total_spend, ui_currency_multiplier, ui_use_special_shirts, ui_special_shirt_exclusions, stats_form_days, sys_vice_captain_enabled, transfers_cap, transfers_sell_on_fee, league_h2_h_tiebreak_stats, timezone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["league_join_private_max"] = from_int(self.league_join_private_max)
        result["league_join_public_max"] = from_int(self.league_join_public_max)
        result["league_max_size_public_classic"] = from_int(self.league_max_size_public_classic)
        result["league_max_size_public_h2h"] = from_int(self.league_max_size_public_h2_h)
        result["league_max_size_private_h2h"] = from_int(self.league_max_size_private_h2_h)
        result["league_max_ko_rounds_private_h2h"] = from_int(self.league_max_ko_rounds_private_h2_h)
        result["league_prefix_public"] = from_str(self.league_prefix_public)
        result["league_points_h2h_win"] = from_int(self.league_points_h2_h_win)
        result["league_points_h2h_lose"] = from_int(self.league_points_h2_h_lose)
        result["league_points_h2h_draw"] = from_int(self.league_points_h2_h_draw)
        result["league_ko_first_instead_of_random"] = from_bool(self.league_ko_first_instead_of_random)
        result["cup_start_event_id"] = from_none(self.cup_start_event_id)
        result["cup_stop_event_id"] = from_none(self.cup_stop_event_id)
        result["cup_qualifying_method"] = from_none(self.cup_qualifying_method)
        result["cup_type"] = from_none(self.cup_type)
        result["squad_squadplay"] = from_int(self.squad_squadplay)
        result["squad_squadsize"] = from_int(self.squad_squadsize)
        result["squad_team_limit"] = from_int(self.squad_team_limit)
        result["squad_total_spend"] = from_int(self.squad_total_spend)
        result["ui_currency_multiplier"] = from_int(self.ui_currency_multiplier)
        result["ui_use_special_shirts"] = from_bool(self.ui_use_special_shirts)
        result["ui_special_shirt_exclusions"] = from_list(lambda x: x, self.ui_special_shirt_exclusions)
        result["stats_form_days"] = from_int(self.stats_form_days)
        result["sys_vice_captain_enabled"] = from_bool(self.sys_vice_captain_enabled)
        result["transfers_cap"] = from_int(self.transfers_cap)
        result["transfers_sell_on_fee"] = to_float(self.transfers_sell_on_fee)
        result["league_h2h_tiebreak_stats"] = from_list(from_str, self.league_h2_h_tiebreak_stats)
        result["timezone"] = from_str(self.timezone)
        return result


class Phase:
    id: int
    name: str
    start_event: int
    stop_event: int

    def __init__(self, id: int, name: str, start_event: int, stop_event: int) -> None:
        self.id = id
        self.name = name
        self.start_event = start_event
        self.stop_event = stop_event

    @staticmethod
    def from_dict(obj: Any) -> 'Phase':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        start_event = from_int(obj.get("start_event"))
        stop_event = from_int(obj.get("stop_event"))
        return Phase(id, name, start_event, stop_event)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["start_event"] = from_int(self.start_event)
        result["stop_event"] = from_int(self.stop_event)
        return result


class Team:
    code: int
    draw: int
    form: None
    id: int
    loss: int
    name: str
    played: int
    points: int
    position: int
    short_name: str
    strength: int
    team_division: None
    unavailable: bool
    win: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int
    pulse_id: int

    def __init__(self, code: int, draw: int, form: None, id: int, loss: int, name: str, played: int, points: int, position: int, short_name: str, strength: int, team_division: None, unavailable: bool, win: int, strength_overall_home: int, strength_overall_away: int, strength_attack_home: int, strength_attack_away: int, strength_defence_home: int, strength_defence_away: int, pulse_id: int) -> None:
        self.code = code
        self.draw = draw
        self.form = form
        self.id = id
        self.loss = loss
        self.name = name
        self.played = played
        self.points = points
        self.position = position
        self.short_name = short_name
        self.strength = strength
        self.team_division = team_division
        self.unavailable = unavailable
        self.win = win
        self.strength_overall_home = strength_overall_home
        self.strength_overall_away = strength_overall_away
        self.strength_attack_home = strength_attack_home
        self.strength_attack_away = strength_attack_away
        self.strength_defence_home = strength_defence_home
        self.strength_defence_away = strength_defence_away
        self.pulse_id = pulse_id

    @staticmethod
    def from_dict(obj: Any) -> 'Team':
        assert isinstance(obj, dict)
        code = from_int(obj.get("code"))
        draw = from_int(obj.get("draw"))
        form = from_none(obj.get("form"))
        id = from_int(obj.get("id"))
        loss = from_int(obj.get("loss"))
        name = from_str(obj.get("name"))
        played = from_int(obj.get("played"))
        points = from_int(obj.get("points"))
        position = from_int(obj.get("position"))
        short_name = from_str(obj.get("short_name"))
        strength = from_int(obj.get("strength"))
        team_division = from_none(obj.get("team_division"))
        unavailable = from_bool(obj.get("unavailable"))
        win = from_int(obj.get("win"))
        strength_overall_home = from_int(obj.get("strength_overall_home"))
        strength_overall_away = from_int(obj.get("strength_overall_away"))
        strength_attack_home = from_int(obj.get("strength_attack_home"))
        strength_attack_away = from_int(obj.get("strength_attack_away"))
        strength_defence_home = from_int(obj.get("strength_defence_home"))
        strength_defence_away = from_int(obj.get("strength_defence_away"))
        pulse_id = from_int(obj.get("pulse_id"))
        return Team(code, draw, form, id, loss, name, played, points, position, short_name, strength, team_division, unavailable, win, strength_overall_home, strength_overall_away, strength_attack_home, strength_attack_away, strength_defence_home, strength_defence_away, pulse_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_int(self.code)
        result["draw"] = from_int(self.draw)
        result["form"] = from_none(self.form)
        result["id"] = from_int(self.id)
        result["loss"] = from_int(self.loss)
        result["name"] = from_str(self.name)
        result["played"] = from_int(self.played)
        result["points"] = from_int(self.points)
        result["position"] = from_int(self.position)
        result["short_name"] = from_str(self.short_name)
        result["strength"] = from_int(self.strength)
        result["team_division"] = from_none(self.team_division)
        result["unavailable"] = from_bool(self.unavailable)
        result["win"] = from_int(self.win)
        result["strength_overall_home"] = from_int(self.strength_overall_home)
        result["strength_overall_away"] = from_int(self.strength_overall_away)
        result["strength_attack_home"] = from_int(self.strength_attack_home)
        result["strength_attack_away"] = from_int(self.strength_attack_away)
        result["strength_defence_home"] = from_int(self.strength_defence_home)
        result["strength_defence_away"] = from_int(self.strength_defence_away)
        result["pulse_id"] = from_int(self.pulse_id)
        return result


class Bootstrap:
    events: List[Event]
    game_settings: GameSettings
    phases: List[Phase]
    teams: List[Team]
    total_players: int
    elements: List[Element]
    element_stats: List[ElementStat]
    element_types: List[ElementType]

    def __init__(self, events: List[Event], game_settings: GameSettings, phases: List[Phase], teams: List[Team], total_players: int, elements: List[Element], element_stats: List[ElementStat], element_types: List[ElementType]) -> None:
        self.events = events
        self.game_settings = game_settings
        self.phases = phases
        self.teams = teams
        self.total_players = total_players
        self.elements = elements
        self.element_stats = element_stats
        self.element_types = element_types

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome8':
        assert isinstance(obj, dict)
        events = from_list(Event.from_dict, obj.get("events"))
        game_settings = GameSettings.from_dict(obj.get("game_settings"))
        phases = from_list(Phase.from_dict, obj.get("phases"))
        teams = from_list(Team.from_dict, obj.get("teams"))
        total_players = from_int(obj.get("total_players"))
        elements = from_list(Element.from_dict, obj.get("elements"))
        element_stats = from_list(ElementStat.from_dict, obj.get("element_stats"))
        element_types = from_list(ElementType.from_dict, obj.get("element_types"))
        return Bootstrap(events, game_settings, phases, teams, total_players, elements, element_stats, element_types)

    def to_dict(self) -> dict:
        result: dict = {}
        result["events"] = from_list(lambda x: to_class(Event, x), self.events)
        result["game_settings"] = to_class(GameSettings, self.game_settings)
        result["phases"] = from_list(lambda x: to_class(Phase, x), self.phases)
        result["teams"] = from_list(lambda x: to_class(Team, x), self.teams)
        result["total_players"] = from_int(self.total_players)
        result["elements"] = from_list(lambda x: to_class(Element, x), self.elements)
        result["element_stats"] = from_list(lambda x: to_class(ElementStat, x), self.element_stats)
        result["element_types"] = from_list(lambda x: to_class(ElementType, x), self.element_types)
        return result


def bootstrap_from_dict(s: Any) -> Bootstrap:
    return Bootstrap.from_dict(s)


def bootstrap_to_dict(x: Bootstrap) -> Any:
    return to_class(Bootstrap, x)
