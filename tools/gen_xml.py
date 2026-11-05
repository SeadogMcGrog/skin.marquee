"""Generate the Marquee-specific XML for skin.marquee.

Writes:
  xml/Includes_Marquee.xml   expressions, variables, tile layouts, fog/snow/leaves, hero
  xml/Home.xml               Netflix-style home screen
  xml/Marquee_SettingsPanels.xml (include with the extra skin-settings grouplists)
  playlists/mq_*.xsp         built-in seasonal smart playlists

Usage: python3 gen_xml.py <skin_dir>
"""
import datetime
import os
import sys
from xml.sax.saxutils import escape

SKIN = sys.argv[1]
XML = os.path.join(SKIN, "xml")

# ----------------------------------------------------------------- seasons
SEASONS = [
    dict(key="newyear", name="New Year's", sid=31731, accent="FFE8C25A", accent2="FFC9D1E0",
         greeting="$VAR[MqNewYearGreetVar]", font="mq_greet_newyear", greet_color="FFF0CE6A",
         tagline="Ringing in the new year"),
    dict(key="mlk", name="Martin Luther King Jr. Day", sid=31735, accent="FF4F7FD9", accent2="FFE8C25A",
         greeting="Martin Luther King Jr. Day", font="mq_greet_formal", greet_color="FFF0D27A",
         tagline="Honoring the dream", day_msg="Honoring Dr. King's dream of equality and justice"),
    dict(key="groundhog", name="Groundhog Day", sid=31810, accent="FFC08A55", accent2="FF9CC4E4",
         greeting="Happy Groundhog Day", font="mq_greet_thanksgiving", greet_color="FFE2B07A",
         kicker="FEBRUARY 2",
         tagline="Six more weeks of winter, or an early spring?", day_msg="It's Groundhog Day. Again."),
    dict(key="valentine", name="Valentine's Day", sid=31729, accent="FFE8457A", accent2="FFF7B6C8",
         greeting="Happy Valentine's Day", font="mq_greet_valentine", greet_color="FFF4709A", greet_top=-6,
         tagline="Love stories for date night"),
    dict(key="presidents", name="Presidents' Day", sid=31736, accent="FF3D5AA8", accent2="FFC8102E",
         greeting="Presidents' Day", font="mq_greet_formal", greet_color="FFF2F2F6",
         tagline="Celebrating Washington's Birthday", day_msg="Happy Presidents' Day: celebrating Washington's Birthday"),
    dict(key="stpatrick", name="St. Patrick's Day", sid=31730, accent="FF2EA84F", accent2="FFF2C14E",
         greeting="Happy St. Patrick's Day", font="mq_greet_stpatrick", greet_color="FF4CC96E",
         tagline="A little luck of the Irish"),
    dict(key="easter", name="Easter", sid=31723, accent="FFC9A0F0", accent2="FF8FD9B6",
         greeting="Happy Easter", font="mq_greet_easter", greet_color="FFF9B4D2", greet_top=-26,
         tagline="Springtime favorites for the whole family"),
    dict(key="mothers", name="Mother's Day", sid=31737, accent="FFE07A9A", accent2="FFC9A0F0",
         greeting="Happy Mother's Day", font="mq_greet_valentine", greet_color="FFF49AB6", greet_top=-6,
         tagline="Favorites for the best mom around", day_msg="Here's to Mom: thank you for everything"),
    dict(key="memorial", name="Memorial Day", sid=31724, accent="FF4A7BD8", accent2="FFD62839",
         greeting="Memorial Day", font="mq_greet_memorial", greet_color="FFF2F2F6",
         tagline="Remembering those who gave all"),
    dict(key="july4", name="Independence Day", sid=31725, accent="FFD62839", accent2="FF4A7BD8",
         greeting="Happy Independence Day", font="mq_greet_july4", greet_color="FFE8414F",
         tagline="Red, white and blue all month long"),
    dict(key="juneteenth", name="Juneteenth", sid=31738, accent="FFD33A3A", accent2="FF2E9E5B",
         greeting="Happy Juneteenth", font="mq_greet_july4", greet_color="FFE8534F",
         tagline="Celebrating freedom", day_msg="Celebrating freedom since June 19, 1865"),
    dict(key="fathers", name="Father's Day", sid=31739, accent="FF4A78B8", accent2="FFC8A060",
         greeting="Happy Father's Day", font="mq_greet_july4", greet_color="FF7FA6E0",
         tagline="Movie night picks for Dad", day_msg="Here's to Dad: kick back and enjoy"),
    dict(key="labor", name="Labor Day", sid=31740, accent="FFF28C28", accent2="FF3A6EA5",
         greeting="Happy Labor Day", font="mq_greet_july4", greet_color="FFF5A04A",
         tagline="The unofficial end of summer", day_msg="Enjoy the long weekend!"),
    dict(key="pirate", name="Talk Like a Pirate Day", sid=31741, accent="FFD4A93C", accent2="FFB8322A",
         greeting="Ahoy, Matey!", font="mq_greet_pirate", greet_color="FFE2B84A", greet_top=22,
         kicker="TALK LIKE A PIRATE DAY",
         tagline="Hoist the colors", day_msg="Arrr! Today be Talk Like a Pirate Day, so talk like one!"),
    dict(key="columbus", name="Columbus Day", sid=31742, accent="FF2C7BB5", accent2="FFE8C25A",
         greeting="Columbus Day", font="mq_greet_formal", greet_color="FFF0D27A",
         tagline="Explorers and the open sea", day_msg="Enjoy the long weekend"),
    dict(key="halloween", name="Halloween", sid=31702, accent="FFFF7518", accent2="FFB57EDC",
         greeting="Happy Halloween", font="mq_greet_halloween", greet_color="FFFF8A2A",
         tagline="Creepy picks for spooky season"),
    dict(key="veterans", name="Veterans Day", sid=31743, accent="FF3D5AA8", accent2="FFD62839",
         greeting="Veterans Day", font="mq_greet_memorial", greet_color="FFF2F2F6",
         tagline="Honoring all who served", day_msg="Thank you to all who served"),
    dict(key="thanksgiving", name="Thanksgiving", sid=31703, accent="FFE39B3B", accent2="FFC0533A",
         greeting="Happy Thanksgiving", font="mq_greet_thanksgiving", greet_color="FFF2B35B",
         tagline="Cozy favorites for the whole family"),
    dict(key="christmas", name="Christmas", sid=31704, accent="FFE23B3B", accent2="FF3DBE6E",
         greeting="Merry Christmas", font="mq_greet_christmas", greet_color="FFF04848",
         tagline="Holiday classics by the fireplace"),
]

DEFAULT_ACCENT = "FFE50914"
SLOTS = 5
CUSTOM = [dict(key="custom%d" % n, name="Your holiday %d" % n, sid=31799 + n, custom=True, accent="FFE50914",
               accent2="FFF2E6C8", greeting="", font="mq_hero", greet_color="FFFFFFFF", tagline="") for n in range(1, 6)]
ALL = CUSTOM + SEASONS
SLOT_SEASONS = ALL + [dict(key="everyday", name="Everyday", sid=31722)]
BY_KEY = {s["key"]: s for s in SLOT_SEASONS}

# holidays on fixed dates: default window (MMDD start, MMDD end) and the day itself
FIXED = {"newyear": ("1226", "0101", (1, 1)), "groundhog": ("0127", "0202", (2, 2)), "valentine": ("0201", "0214", (2, 14)), "stpatrick": ("0301", "0317", (3, 17)),
         "juneteenth": ("0613", "0619", (6, 19)), "july4": ("0701", "0731", (7, 4)), "pirate": ("0913", "0919", (9, 19)),
         "halloween": ("1001", "1031", (10, 31)), "veterans": ("1108", "1111", (11, 11)), "christmas": ("1201", "1225", (12, 25))}
MOVING_DEFAULT_TEXT = {"mlk": "the week before", "presidents": "the week before", "easter": "the 1st of the month",
                       "mothers": "the week before", "memorial": "the week before", "fathers": "the week before",
                       "labor": "the week before", "columbus": "the weekend before", "thanksgiving": "November 1"}
MOVING_END_TEXT = {"easter": "the end of the month"}
BEFORE_OPTS = [(0, 31760), (3, 31761), (7, 31762), (14, 31763), (30, 31764)]   # days before the holiday
AFTER_OPTS = [(0, 31765), (1, 31766), (3, 31767), (7, 31768)]                    # days after
# when windows overlap: your own holidays first, then a holiday's own day, then this order
PRIORITY = ["groundhog", "valentine", "presidents", "stpatrick", "juneteenth", "fathers", "mothers", "memorial", "mlk", "labor", "pirate",
            "columbus", "veterans", "newyear", "easter", "july4", "halloween", "thanksgiving", "christmas"]
FONTS = [("bold", "mq_hero", 31770, 0), ("script", "mq_greet_valentine", 31771, 8), ("rounded", "mq_greet_easter", 31772, -26),
         ("slab", "mq_greet_july4", 31773, 0), ("formal", "mq_greet_formal", 31774, 0), ("spooky", "mq_greet_halloween", 31775, 0),
         ("festive", "mq_greet_christmas", 31776, 0), ("celtic", "mq_greet_stpatrick", 31777, 0), ("pirate", "mq_greet_pirate", 31778, 22),
         ("deco", "mq_greet_newyear", 31779, 0), ("harvest", "mq_greet_thanksgiving", 31780, 22), ("classic", "mq_greet_memorial", 31781, 0)]
FONT_OF = {f[1]: f[0] for f in FONTS}
EFFECTS = [("none", 31782), ("fog", 31783), ("snow", 31784), ("leaves", 31785), ("petals", 31786), ("hearts", 31787),
           ("shamrocks", 31788), ("confetti", 31789), ("fireworks", 31790)]
DEFAULT_FX = {"halloween": "fog", "christmas": "snow", "thanksgiving": "leaves", "easter": "petals", "mothers": "petals",
              "valentine": "hearts", "stpatrick": "shamrocks", "newyear": "confetti", "july4": "fireworks", "juneteenth": "fireworks",
              "groundhog": "snow"}
ANIMS = [("still", 31791), ("rock", 31792), ("bob", 31793), ("pulse", 31794), ("spin", 31795)]
DEFAULT_ANIM = {"halloween": "rock", "groundhog": "bob"}
# skin-settings category item id for each season's rows (5 = Seasons & effects)
SETTINGS_ITEM = {"halloween": 6, "thanksgiving": 7, "christmas": 8, "everyday": 9, "easter": 10, "memorial": 11, "july4": 12,
                 "newyear": 13, "valentine": 14, "stpatrick": 15, "mlk": 16, "presidents": 17, "mothers": 18,
                 "juneteenth": 19, "fathers": 20, "labor": 21, "pirate": 22, "columbus": 23, "veterans": 24, "groundhog": 25}
ROWS_SID = {"newyear": 31734, "valentine": 31732, "stpatrick": 31733, "easter": 31726, "memorial": 31727, "july4": 31728,
            "halloween": 31719, "thanksgiving": 31720, "christmas": 31721, "everyday": 31722, "mlk": 31744,
            "presidents": 31745, "mothers": 31746, "juneteenth": 31747, "fathers": 31748, "labor": 31749,
            "pirate": 31750, "columbus": 31751, "veterans": 31752, "groundhog": 31811}


def thanksgiving(year):
    d = datetime.date(year, 11, 1)
    first_thu = d + datetime.timedelta(days=(3 - d.weekday()) % 7)
    return first_thu + datetime.timedelta(days=21)


TG_YEARS = range(2024, 2061)
YEARS = TG_YEARS


def easter(year):
    """Western (Gregorian) Easter Sunday."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


def memorial_day(year):
    """Last Monday of May."""
    d = datetime.date(year, 5, 31)
    return d - datetime.timedelta(days=d.weekday())


def md(d):
    return "%02d-%02d" % (d.month, d.day)


def yr(y):
    return "$EXP[mq_y%d]" % y


def nth_weekday(year, month, weekday, n):
    """n-th weekday (Mon=0) of a month."""
    d = datetime.date(year, month, 1)
    d += datetime.timedelta(days=(weekday - d.weekday()) % 7)
    return d + datetime.timedelta(weeks=n - 1)


def holiday_windows(year):
    """(key, first day, last day, the holiday itself) for every season touching this year."""
    D = datetime.date
    td = datetime.timedelta
    w = []
    for y in (year - 1, year, year + 1):
        if y not in range(YEARS.start - 1, YEARS.stop + 1):
            continue
        e = easter(y)
        mlk = nth_weekday(y, 1, 0, 3)
        pres = nth_weekday(y, 2, 0, 3)
        mom = nth_weekday(y, 5, 6, 2)
        dad = nth_weekday(y, 6, 6, 3)
        labor = nth_weekday(y, 9, 0, 1)
        colum = nth_weekday(y, 10, 0, 2)
        mem = memorial_day(y)
        tg = thanksgiving(y)
        w += [
            ("newyear", D(y, 12, 26), D(y + 1, 1, 1), D(y + 1, 1, 1)),
            ("mlk", mlk - td(days=6), mlk, mlk),
            ("groundhog", D(y, 1, 27), D(y, 2, 2), D(y, 2, 2)),
            ("valentine", D(y, 2, 1), D(y, 2, 14), D(y, 2, 14)),
            ("presidents", pres - td(days=6), pres, pres),
            ("stpatrick", D(y, 3, 1), D(y, 3, 17), D(y, 3, 17)),
            ("easter", D(y, e.month, 1), D(y, e.month + 1, 1) - td(days=1), e),
            ("mothers", mom - td(days=6), mom, mom),
            ("memorial", mem - td(days=7), mem, mem),
            ("juneteenth", D(y, 6, 13), D(y, 6, 19), D(y, 6, 19)),
            ("fathers", dad - td(days=6), dad, dad),
            ("july4", D(y, 7, 1), D(y, 7, 31), D(y, 7, 4)),
            ("labor", labor - td(days=7), labor, labor),
            ("pirate", D(y, 9, 13), D(y, 9, 19), D(y, 9, 19)),
            ("columbus", colum - td(days=2), colum, colum),
            ("halloween", D(y, 10, 1), D(y, 10, 31), D(y, 10, 31)),
            ("veterans", D(y, 11, 8), D(y, 11, 11), D(y, 11, 11)),
            ("thanksgiving", D(y, 11, 1), tg, tg),
            ("christmas", D(y, 12, 1), D(y, 12, 25), D(y, 12, 25)),
        ]
    return w


def season_calendar():
    """Pick one season per day: of the windows covering a day, the holiday coming up soonest wins
    (so a one-day holiday briefly takes over a month-long theme, then hands it back)."""
    order = [s["key"] for s in SEASONS]
    cal = {}
    for y in YEARS:
        wins = holiday_windows(y)
        d = datetime.date(y, 1, 1)
        while d.year == y:
            cands = [(k, day) for k, a, b, day in wins if a <= d <= b]
            if cands:
                upcoming = [c for c in cands if c[1] >= d]
                if upcoming:
                    k = min(upcoming, key=lambda c: ((c[1] - d).days, order.index(c[0])))[0]
                else:
                    k = max(cands, key=lambda c: c[1])[0]
                cal[d] = k
            d += datetime.timedelta(days=1)
    return cal


CALENDAR = season_calendar()


def date_runs(key):
    """Contiguous date runs for one season, as (year, first, last) within each calendar year."""
    days = sorted(d for d, k in CALENDAR.items() if k == key)
    runs = []
    for d in days:
        if runs and runs[-1][2] == d - datetime.timedelta(days=1) and runs[-1][0] == d.year:
            runs[-1][2] = d
        else:
            runs.append([d.year, d, d])
    return runs


def hour_is(h):
    """True during hour h (0-23). Compares the displayed time text, which works with 12- and 24-hour clocks
    (System.Time(a,b) windows proved unreliable)."""
    h12 = h % 12 or 12
    return "[String.IsEqual(System.Time(hh),%02d) | [String.IsEqual(System.Time(hh),%d) + String.IsEqual(System.Time(xx),%s)]]" % (
        h, h12, "AM" if h < 12 else "PM")


MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

# -------------------------------------------------------------- expressions
def raw_window(key, year):
    for k, first, last, day in holiday_windows(year):
        if k == key and day.year == year:
            return first, last, day
    return None


def opt_cond(prefix, opts, key):
    """'no option chosen' condition for a SelectBool group."""
    return " + ".join("!Skin.HasSetting(mq_%s_%s_%s)" % (key, prefix, o) for o in opts)


def opt_is(prefix, opts, default, key, value):
    """True when option `value` is selected (or nothing is selected and `value` is the default)."""
    c = "Skin.HasSetting(mq_%s_%s_%s)" % (key, prefix, value)
    if value == default:
        c = "[%s | [%s]]" % (c, opt_cond(prefix, opts, key))
    return c


def mmdd_window(key):
    """Window from two MMDD skin strings (wraps over the new year when start > end)."""
    t, a_, b_ = "System.Date(mmdd)", "Skin.String(mq_%s_start)" % key, "Skin.String(mq_%s_end)" % key
    return ("[Integer.IsGreaterOrEqual(%s,%s) + Integer.IsLessOrEqual(%s,%s)] | [Integer.IsGreater(%s,%s) + "
            "[Integer.IsGreaterOrEqual(%s,%s) | Integer.IsLessOrEqual(%s,%s)]]" % (t, a_, t, b_, a_, b_, t, a_, t, b_))


def moving_window(key):
    td = datetime.timedelta
    ge_default, le_default, ge_opt, le_opt, days = [], [], {n: [] for n, _ in BEFORE_OPTS}, {n: [] for n, _ in AFTER_OPTS}, []
    for y in YEARS:
        w = raw_window(key, y)
        if not w:
            continue
        first, last, day = w
        jan1, dec31 = datetime.date(y, 1, 1), datetime.date(y, 12, 31)
        days.append("[System.Date(%s,%s) + %s]" % (md(day), md(day + td(days=1)), yr(y)))
        ge_default.append("[System.Date(%s) + %s]" % (md(first), yr(y)))
        le_default.append("[System.Date(01-01,%s) + %s]" % (md(last + td(days=1)), yr(y)) if last < dec31 else yr(y))
        for n, _ in BEFORE_OPTS:
            st = max(day - td(days=n), jan1)
            ge_opt[n].append("[System.Date(%s) + %s]" % (md(st), yr(y)))
        for n, _ in AFTER_OPTS:
            en = min(day + td(days=n), dec31)
            le_opt[n].append("[System.Date(01-01,%s) + %s]" % (md(en + td(days=1)), yr(y)) if en < dec31 else yr(y))
    bo = [str(n) for n, _ in BEFORE_OPTS]
    ao = [str(n) for n, _ in AFTER_OPTS]
    ge = "[%s + [%s]]" % (opt_cond("before", bo, key), " | ".join(ge_default))
    for n, _ in BEFORE_OPTS:
        ge += " | [Skin.HasSetting(mq_%s_before_%d) + [%s]]" % (key, n, " | ".join(ge_opt[n]))
    le = "[%s + [%s]]" % (opt_cond("after", ao, key), " | ".join(le_default))
    for n, _ in AFTER_OPTS:
        le += " | [Skin.HasSetting(mq_%s_after_%d) + [%s]]" % (key, n, " | ".join(le_opt[n]))
    return "[%s] + [%s]" % (ge, le), " | ".join(days)


def fx_cond(key, fx):
    return opt_is("fx", [e for e, _ in EFFECTS], DEFAULT_FX.get(key, "none"), key, fx)


def expressions():
    out = []
    e = out.append
    e('<expression name="mq_force_any">%s | Skin.HasSetting(mq_force_off)</expression>'
      % " | ".join("Skin.HasSetting(mq_force_%s)" % s["key"] for s in ALL))
    for y in YEARS:
        e('<expression name="mq_y%d">String.IsEqual(System.Date(yyyy),%d)</expression>' % (y, y))
    # --- your own holidays: name + start + end set, not switched off
    for c in CUSTOM:
        k = c["key"]
        e('<expression name="mq_on_%s">!String.IsEmpty(Skin.String(mq_%s_name)) + !String.IsEmpty(Skin.String(mq_%s_start)) + '
          '!String.IsEmpty(Skin.String(mq_%s_end)) + !Skin.HasSetting(mq_%s_off)</expression>' % (k, k, k, k, k))
        e('<expression name="mq_win_%s">%s</expression>' % (k, mmdd_window(k)))
        e('<expression name="mq_inw_%s">$EXP[mq_on_%s] + $EXP[mq_win_%s]</expression>' % (k, k, k))
    for i, c in enumerate(CUSTOM):
        k = c["key"]
        higher = "".join(" + !$EXP[mq_inw_%s]" % h["key"] for h in CUSTOM[:i])
        e('<expression name="mq_date_%s">$EXP[mq_inw_%s]%s</expression>' % (k, k, higher))
    e('<expression name="mq_custom_any">%s</expression>' % " | ".join("$EXP[mq_inw_%s]" % c["key"] for c in CUSTOM))
    # --- built-in holidays
    for sea in SEASONS:
        k = sea["key"]
        e('<expression name="mq_on_%s">!Skin.HasSetting(mq_%s_off)</expression>' % (k, k))
        if k in FIXED:
            win = mmdd_window(k)
            m, d = FIXED[k][2]
            dd = datetime.date(2001, m, d)
            day = "System.Date(%s,%s)" % (md(dd), md(dd + datetime.timedelta(days=1)))
        else:
            win, day = moving_window(k)
        e('<expression name="mq_win_%s">%s</expression>' % (k, win))
        e('<expression name="mq_day_%s">%s</expression>' % (k, day))
        e('<expression name="mq_inw_%s">$EXP[mq_on_%s] + $EXP[mq_win_%s]</expression>' % (k, k, k))
    e('<expression name="mq_anyday">%s</expression>' % " | ".join("[$EXP[mq_on_%s] + $EXP[mq_day_%s]]" % (s["key"], s["key"]) for s in SEASONS))
    for sea in SEASONS:
        k = sea["key"]
        higher = "".join(" + !$EXP[mq_inw_%s]" % h for h in PRIORITY[:PRIORITY.index(k)])
        e('<expression name="mq_date_%s">$EXP[mq_on_%s] + !$EXP[mq_custom_any] + [$EXP[mq_day_%s] | [$EXP[mq_win_%s] + !$EXP[mq_anyday]%s]]</expression>'
          % (k, k, k, k, higher))
    # New Year's Eve: last minute before midnight, and the first half hour of the new year
    e('<expression name="mq_nye_lastminute">$EXP[mq_newyear] + System.Date(12-31,01-01) + %s + String.IsEqual(System.Time(mm),59)</expression>' % hour_is(23))
    e('<expression name="mq_ny_midnight">$EXP[mq_newyear] + System.Date(01-01,01-02) + %s + Integer.IsLess(System.Time(mm),30)</expression>' % hour_is(0))
    for s_ in ALL:
        k = s_["key"]
        e('<expression name="mq_%s">Skin.HasSetting(mq_force_%s) | [!$EXP[mq_force_any] + $EXP[mq_date_%s]]</expression>' % (k, k, k))
    e('<expression name="mq_season">%s</expression>' % " | ".join("$EXP[mq_%s]" % s_["key"] for s_ in ALL))
    # --- effects: each holiday picks one (Seasons > holiday > Effect)
    for fx, _ in EFFECTS[1:]:
        e('<expression name="mq_fxsel_%s">%s</expression>' % (fx, " | ".join("[$EXP[mq_%s] + %s]" % (s_["key"], fx_cond(s_["key"], fx)) for s_ in ALL)))
    off = "!Skin.HasSetting(mq_effects_off)"
    e('<expression name="mq_fog">%s + $EXP[mq_fxsel_fog]</expression>' % off)
    e('<expression name="mq_snow">%s + $EXP[mq_fxsel_snow]</expression>' % off)
    e('<expression name="mq_leaves">%s + $EXP[mq_fxsel_leaves]</expression>' % off)
    e('<expression name="mq_petals">%s + $EXP[mq_fxsel_petals]</expression>' % off)
    e('<expression name="mq_hearts">%s + $EXP[mq_fxsel_hearts]</expression>' % off)
    e('<expression name="mq_shamrocks">%s + $EXP[mq_fxsel_shamrocks]</expression>' % off)
    e('<expression name="mq_confetti">%s + $EXP[mq_fxsel_confetti] + !$EXP[mq_nye_lastminute]</expression>' % off)
    e('<expression name="mq_fireworks">%s + [$EXP[mq_fxsel_fireworks] | $EXP[mq_ny_midnight]]</expression>' % off)
    e('<expression name="mq_balldrop">%s + $EXP[mq_nye_lastminute]</expression>' % off)
    # --- greeting font and icon animation
    for f in FONTS:
        e('<expression name="mq_font_%s">%s</expression>' % (f[0], " | ".join(
            "[$EXP[mq_%s] + %s]" % (s_["key"], opt_is("font", [x[0] for x in FONTS], FONT_OF[s_["font"]], s_["key"], f[0])) for s_ in ALL)))
    for an, _ in ANIMS[1:]:
        e('<expression name="mq_anim_%s">%s</expression>' % (an, " | ".join(
            "[$EXP[mq_%s] + %s]" % (s_["key"], opt_is("anim", [x[0] for x in ANIMS], DEFAULT_ANIM.get(s_["key"], "still"), s_["key"], an)) for s_ in ALL)))
    e('<expression name="mq_rows_focus">!ControlGroup(9100).HasFocus + !ControlGroup(700).HasFocus</expression>')
    e('<expression name="mq_hero_fanart">$EXP[mq_rows_focus] + [!String.IsEmpty(ListItem.Art(fanart)) | !String.IsEmpty(ListItem.Art(tvshow.fanart)) | '
      '!String.IsEmpty(ListItem.Art(artist.fanart)) | !String.IsEmpty(ListItem.Art(landscape))]</expression>')
    return out


# ---------------------------------------------------------------- variables
def var(name, values, default=None):
    lines = ['<variable name="%s">' % name]
    for cond, val in values:
        lines.append('\t<value condition="%s">%s</value>' % (cond, val))
    if default is not None:
        lines.append('\t<value>%s</value>' % default)
    lines.append('</variable>')
    return "\n".join(lines)


def alpha_hex(a, tint):
    return "%02X%s" % (max(0, min(255, int(round(a * 255)))), tint)


def variables():
    v = []
    def override(setting, default_of, fallback, keys=ALL):
        vals = []
        for s_ in keys:
            k = s_["key"]
            vals.append(("$EXP[mq_%s] + !String.IsEmpty(Skin.String(mq_%s_%s))" % (k, k, setting), "$INFO[Skin.String(mq_%s_%s)]" % (k, setting)))
            d = default_of(s_)
            if d is not None:
                vals.append(("$EXP[mq_%s]" % k, d))
        return vals
    v.append(var("MqAccentVar", override("accent", lambda s_: s_["accent"], None), DEFAULT_ACCENT))
    v.append(var("MqAccent2Var", [("$EXP[mq_%s]" % s_["key"], s_["accent2"]) for s_ in ALL], "FFB3B3B3"))
    v.append(var("MqSeasonIconVar", override("icon", lambda s_: "marquee/icon_%s.png" % ("custom" if s_.get("custom") else s_["key"]), None), ""))
    v.append(var("MqSeasonNameVar", [("$EXP[mq_%s]" % c["key"], "$INFO[Skin.String(mq_%s_name)]" % c["key"]) for c in CUSTOM]
                 + [("$EXP[mq_%s]" % s_["key"], s_["name"]) for s_ in SEASONS], "No season"))
    v.append(var("MqTaglineVar", [("$EXP[mq_%s]" % s_["key"], s_["tagline"]) for s_ in SEASONS],
                 "Pick up where you left off, or find something new"))
    # greeting text / colour / small label above it
    v.append(var("MqGreetVar", override("greeting", lambda s_: "$INFO[Skin.String(mq_%s_name)]" % s_["key"] if s_.get("custom") else s_["greeting"], None),
                 "Tonight's lineup"))
    v.append(var("MqGreetColorVar", override("greetcolor", lambda s_: s_["greet_color"], None), "FFFFFFFF"))
    v.append(var("MqKickerVar", override("kicker", lambda s_: s_.get("kicker"), None), ""))
    # backdrop folders (custom folder from settings, else the built-in folder)
    vals = []
    for s_ in ALL:
        k = s_["key"]
        vals.append(("$EXP[mq_%s] + !String.IsEmpty(Skin.String(mq_bg_%s))" % (k, k), "$INFO[Skin.String(mq_bg_%s)]" % k))
        vals.append(("$EXP[mq_%s]" % k, "special://skin/extras/seasons/%s/" % ("default" if s_.get("custom") else k)))
    vals.append(("!String.IsEmpty(Skin.String(mq_bg_default))", "$INFO[Skin.String(mq_bg_default)]"))
    v.append(var("MqBackdropPathVar", vals, "special://skin/extras/seasons/default/"))

    # countdowns
    cd = []
    for c in CUSTOM:
        k = c["key"]
        cd.append(("$EXP[mq_%s] + !String.IsEmpty(Skin.String(mq_%s_message))" % (k, k), "$INFO[Skin.String(mq_%s_message)]" % k))
        cd.append(("$EXP[mq_%s]" % k, "Celebrating $INFO[Skin.String(mq_%s_name)] today" % k))
    # New Year's Eve: seconds in the last minute, minutes in the last hour, hours before that
    for sec in range(60):
        cd.append(("$EXP[mq_nye_lastminute] + String.IsEqual(System.Time(ss),%02d)" % sec,
                   "%d seconds to midnight!" % (60 - sec) if sec < 59 else "1 second to midnight!"))
    for m in range(59):
        cd.append(("$EXP[mq_newyear] + System.Date(12-31,01-01) + %s + String.IsEqual(System.Time(mm),%02d)" % (hour_is(23), m),
                   "%d minutes until midnight" % (60 - m) if m < 59 else "1 minute until midnight"))
    for h in range(23):
        left = 24 - h
        cd.append(("$EXP[mq_newyear] + System.Date(12-31,01-01) + %s" % hour_is(h),
                   "The ball drops at midnight: %d hours to go" % left))
    cd.append(("$EXP[mq_newyear] + System.Date(01-01,01-02)", "Welcome to $INFO[System.Date(yyyy)]! Happy New Year"))
    for d in range(26, 31):
        cd.append(("$EXP[mq_newyear] + System.Date(12-%02d,12-%02d)" % (d, d + 1), "%d days until the new year" % (32 - d)))
    for d in range(1, 15):
        left = 14 - d
        txt = "Happy Valentine's Day!" if left == 0 else ("Valentine's Day is tomorrow" if left == 1 else "%d days until Valentine's Day" % left)
        if left == 0:
            txt = "Wishing you a day full of love"
        cd.append(("$EXP[mq_valentine] + System.Date(02-%02d,02-%02d)" % (d, d + 1), txt))
    for d in range(1, 18):
        left = 17 - d
        txt = "May the luck of the Irish be with you" if left == 0 else ("St. Patrick's Day is tomorrow" if left == 1 else "%d days until St. Patrick's Day" % left)
        cd.append(("$EXP[mq_stpatrick] + System.Date(03-%02d,03-%02d)" % (d, d + 1), txt))
    for d in range(1, 32):
        left = 31 - d
        txt = "Trick or treat! Tonight is the night" if left == 0 else ("Halloween is tomorrow!" if left == 1 else "%d days until Halloween" % left)
        end = "11-01" if d == 31 else "10-%02d" % (d + 1)
        cd.append(("$EXP[mq_halloween] + System.Date(10-%02d,%s)" % (d, end), txt))
    for y in TG_YEARS:
        t = thanksgiving(y)
        ycond = yr(y)
        cd.append(("$EXP[mq_thanksgiving] + %s + System.Date(11-%02d,11-%02d)" % (ycond, t.day, t.day + 1), "Grab a plate and settle in"))
        cd.append(("$EXP[mq_thanksgiving] + %s + System.Date(11-01,11-%02d)" % (ycond, t.day),
                   "Thanksgiving is Thursday, November %d" % t.day))
    for d in range(1, 26):
        left = 25 - d
        txt = "It's Christmas Day! Enjoy the holiday" if left == 0 else ("It's Christmas Eve!" if left == 1 else "%d days until Christmas" % left)
        cd.append(("$EXP[mq_christmas] + System.Date(12-%02d,12-%02d)" % (d, d + 1), txt))
    for y in YEARS:
        ed = easter(y)
        cd.append(("$EXP[mq_easter] + %s + System.Date(%s,%s)" % (yr(y), md(ed), md(ed + datetime.timedelta(days=1))),
                   "He is risen! Happy Easter"))
        cd.append(("$EXP[mq_easter] + %s + System.Date(%02d-01,%s)" % (yr(y), ed.month, md(ed)),
                   "Easter is Sunday, %s %d" % (MONTHS[ed.month], ed.day)))
        mdd = memorial_day(y)
        cd.append(("$EXP[mq_memorial] + %s + System.Date(%s,%s)" % (yr(y), md(mdd), md(mdd + datetime.timedelta(days=1))),
                   "Honoring all who gave their lives in service"))
        cd.append(("$EXP[mq_memorial] + %s + System.Date(05-01,%s)" % (yr(y), md(mdd)),
                   "Memorial Day is Monday, May %d" % mdd.day))
    cd.append(("$EXP[mq_july4] + System.Date(07-01,07-02)", "3 days until Independence Day"))
    cd.append(("$EXP[mq_july4] + System.Date(07-02,07-03)", "2 days until Independence Day"))
    cd.append(("$EXP[mq_july4] + System.Date(07-03,07-04)", "Independence Day is tomorrow!"))
    cd.append(("$EXP[mq_july4] + System.Date(07-04,07-05)", "Celebrating America's birthday"))
    fixed = {"juneteenth", "pirate", "veterans", "groundhog"}
    for sea in SEASONS:
        k = sea["key"]
        if "day_msg" not in sea:
            continue
        seen = set()
        for y in YEARS:
            for kk, a_, b_, day in holiday_windows(y):
                if kk != k or day.year != y or (k in fixed and "fixed" in seen):
                    continue
                if k in fixed:
                    seen.add("fixed")
                    cd.append(("$EXP[mq_%s] + System.Date(%s,%s)" % (k, md(day), md(day + datetime.timedelta(days=1))), sea["day_msg"]))
                    for n in range(1, 7):
                        dd = day - datetime.timedelta(days=n)
                        txt = "%s is tomorrow" % sea["name"] if n == 1 else "%d days until %s" % (n, sea["name"])
                        cd.append(("$EXP[mq_%s] + System.Date(%s,%s)" % (k, md(dd), md(dd + datetime.timedelta(days=1))), txt))
                else:
                    cd.append(("$EXP[mq_%s] + System.Date(%s,%s) + %s" % (k, md(day), md(day + datetime.timedelta(days=1)), yr(y)),
                               sea["day_msg"]))
                    cd.append(("$EXP[mq_%s] + System.Date(%s,%s) + %s" % (k, md(a_), md(day), yr(y)),
                               "%s is %s, %s %d" % (sea["name"], day.strftime("%A"), MONTHS[day.month], day.day)))
    v.append(var("MqCountdownVar", cd, "$VAR[MqTaglineVar]"))
    v.append(var("MqNewYearGreetVar", [("System.Date(12-31,01-01)", "New Year's Eve")], "Happy New Year"))
    v.append(var("MqBallCountVar", [("String.IsEqual(System.Time(ss),%02d)" % s_, str(60 - s_)) for s_ in range(50, 60)], ""))

    # season-mode / fog labels for settings
    v.append(var("MqSeasonModeLabelVar", [("Skin.HasSetting(mq_force_%s)" % s_["key"], "$LOCALIZE[%d]" % s_["sid"]) for s_ in ALL]
                 + [("Skin.HasSetting(mq_force_off)", "$LOCALIZE[31705]")], "$LOCALIZE[31701]"))
    v.append(var("MqFogModeLabelVar", [("Skin.HasSetting(mq_fog_always)", "$LOCALIZE[31708]"),
                                       ("Skin.HasSetting(mq_fog_off)", "$LOCALIZE[31709]")], "$LOCALIZE[31707]"))
    for n in (1, 2, 3):
        v.append(var("MqAddonRowPath_%d" % n, [("Skin.HasSetting(mq_menuaddon_%d_row) + !String.IsEmpty(Skin.String(mq_menuaddon_%d))" % (n, n),
                                                 "plugin://$INFO[Skin.String(mq_menuaddon_%d)]/" % n)], ""))
    v.append(var("MqFogDensityLabelVar", [("Skin.HasSetting(mq_fog_light)", "$LOCALIZE[31711]"),
                                          ("Skin.HasSetting(mq_fog_heavy)", "$LOCALIZE[31713]")], "$LOCALIZE[31712]"))

    # fog layer colours: per-layer base alpha * density, greenish-grey tint for the graveyard look
    for layer, base in (("Ground", 0.52), ("Bank", 0.34), ("Wisp", 0.42)):
        vals = []
        for dens, mul in (("Skin.HasSetting(mq_fog_light)", 0.55), ("Skin.HasSetting(mq_fog_heavy)", 1.45)):
            vals.append(("$EXP[mq_halloween] + " + dens, alpha_hex(base * mul, "D4E4DA")))
            vals.append((dens, alpha_hex(base * mul, "E6ECF2")))
        vals.append(("$EXP[mq_halloween]", alpha_hex(base, "D4E4DA")))
        v.append(var("MqFog%sVar" % layer, vals, alpha_hex(base, "E6ECF2")))

    # artwork
    v.append(var("MqPosterArtVar", [
        ("!String.IsEmpty(ListItem.Art(poster))", "$INFO[ListItem.Art(poster)]"),
        ("!String.IsEmpty(ListItem.Art(tvshow.poster))", "$INFO[ListItem.Art(tvshow.poster)]"),
        ("!String.IsEmpty(ListItem.Art(thumb))", "$INFO[ListItem.Art(thumb)]"),
    ], "$INFO[ListItem.Icon]"))
    v.append(var("MqLandscapeArtVar", [
        ("String.IsEqual(ListItem.DBType,episode) + !String.IsEmpty(ListItem.Art(thumb))", "$INFO[ListItem.Art(thumb)]"),
        ("!String.IsEmpty(ListItem.Art(landscape))", "$INFO[ListItem.Art(landscape)]"),
        ("!String.IsEmpty(ListItem.Art(tvshow.landscape))", "$INFO[ListItem.Art(tvshow.landscape)]"),
        ("!String.IsEmpty(ListItem.Art(fanart))", "$INFO[ListItem.Art(fanart)]"),
        ("!String.IsEmpty(ListItem.Art(tvshow.fanart))", "$INFO[ListItem.Art(tvshow.fanart)]"),
        ("!String.IsEmpty(ListItem.Art(thumb))", "$INFO[ListItem.Art(thumb)]"),
    ], "$INFO[ListItem.Icon]"))
    v.append(var("MqSquareArtVar", [
        ("!String.IsEmpty(ListItem.Art(thumb))", "$INFO[ListItem.Art(thumb)]"),
    ], "$INFO[ListItem.Icon]"))
    v.append(var("MqTileLabelVar", [
        ("String.IsEqual(ListItem.DBType,episode)",
         "$INFO[ListItem.TVShowTitle][COLOR FF8C8C8C]$INFO[ListItem.Season,  S,]$INFO[ListItem.Episode,E,][/COLOR]"),
        ("!String.IsEmpty(ListItem.Artist) + !String.IsEmpty(ListItem.Album)",
         "$INFO[ListItem.Album][COLOR FF8C8C8C]$INFO[ListItem.Artist,  •  ,][/COLOR]"),
    ], "$INFO[ListItem.Label]"))

    # hero (focused item in the rows)
    v.append(var("MqHeroFanartVar", [
        ("!String.IsEmpty(ListItem.Art(fanart))", "$INFO[ListItem.Art(fanart)]"),
        ("!String.IsEmpty(ListItem.Art(tvshow.fanart))", "$INFO[ListItem.Art(tvshow.fanart)]"),
        ("!String.IsEmpty(ListItem.Art(artist.fanart))", "$INFO[ListItem.Art(artist.fanart)]"),
        ("!String.IsEmpty(ListItem.Art(landscape))", "$INFO[ListItem.Art(landscape)]"),
    ], ""))
    v.append(var("MqHeroLogoVar", [
        ("String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,season)", "$INFO[ListItem.Art(tvshow.clearlogo)]"),
    ], "$INFO[ListItem.Art(clearlogo)]"))
    v.append(var("MqHeroTitleVar", [
        ("String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,season)", "$INFO[ListItem.TVShowTitle]"),
        ("!String.IsEmpty(ListItem.Album)", "$INFO[ListItem.Album]"),
        ("!String.IsEmpty(ListItem.Title)", "$INFO[ListItem.Title]"),
    ], "$INFO[ListItem.Label]"))
    v.append(var("MqHeroMetaVar", [
        ("String.IsEqual(ListItem.DBType,episode)",
         "[B]$INFO[ListItem.Season,S,]$INFO[ListItem.Episode,  E,][/B]$INFO[ListItem.Title,  •  ,]$INFO[ListItem.Duration(mins),  •  , min]"),
        ("!String.IsEmpty(ListItem.Artist)", "$INFO[ListItem.Artist]$INFO[ListItem.Year,  •  ,]$INFO[ListItem.Genre,  •  ,]"),
    ], "$INFO[ListItem.Year]$INFO[ListItem.Duration(mins),  •  , min]$INFO[ListItem.MPAA,  •  ,]$INFO[ListItem.Genre,  •  ,]$INFO[ListItem.Rating,  •  ★ ,]"))
    v.append(var("MqHeroPlotVar", [
        ("!String.IsEmpty(ListItem.Plot)", "$INFO[ListItem.Plot]"),
        ("!String.IsEmpty(ListItem.PlotOutline)", "$INFO[ListItem.PlotOutline]"),
        ("!String.IsEmpty(ListItem.Property(Album_Description))", "$INFO[ListItem.Property(Album_Description)]"),
        ("!String.IsEmpty(ListItem.Property(Artist_Description))", "$INFO[ListItem.Property(Artist_Description)]"),
        ("!String.IsEmpty(ListItem.AddonDescription)", "$INFO[ListItem.AddonDescription]"),
    ], ""))

    # --- holiday settings dialog labels
    td = datetime.timedelta
    for s_ in SLOT_SEASONS:
        k = s_["key"]
        if k == "everyday":
            continue
        nm = "$INFO[Skin.String(mq_%s_name)]" % k if s_.get("custom") else s_["name"]
        status = [("Skin.HasSetting(mq_%s_off)" % k, "Off")]
        if s_.get("custom"):
            status = [("String.IsEmpty(Skin.String(mq_%s_name))" % k, "Not set up")] + status
            v.append(var("MqCustomSlotLabel_%s" % k, [("!String.IsEmpty(Skin.String(mq_%s_name))" % k, nm)], "%s: add a holiday" % s_["name"]))
        status.append(("true", "On"))
        if not (k in FIXED or s_.get("custom")):
            v.append(var("MqBefore_%s" % k, [("Skin.HasSetting(mq_%s_before_%d)" % (k, n), "$LOCALIZE[%d]" % sid) for n, sid in BEFORE_OPTS],
                         "Default (%s)" % MOVING_DEFAULT_TEXT[k]))
            v.append(var("MqAfter_%s" % k, [("Skin.HasSetting(mq_%s_after_%d)" % (k, n), "$LOCALIZE[%d]" % sid) for n, sid in AFTER_OPTS],
                         "Default (%s)" % MOVING_END_TEXT.get(k, "on the day")))
        v.append(var("MqHolidayStatus_%s" % k, status))
        for field, setting, dflt in (("kicker", "mq_%s_kicker" % k, "Default (%s)" % s_["kicker"].title() if s_.get("kicker") else "None"), ("message", "mq_%s_message" % k, "None"),
                                     ("greetcolor", "mq_%s_greetcolor" % k, "Default"), ("accent", "mq_%s_accent" % k, "Default"),
                                     ("icon", "mq_%s_icon" % k, "Default"), ("bg", "mq_bg_%s" % k, "Built-in backdrops")):
            val = "$INFO[Skin.String(%s)]" % setting
            if field in ("greetcolor", "accent"):
                val = "[COLOR %s]\u25CF\u25CF\u25CF[/COLOR]  %s" % (val, val)
            v.append(var("MqVal_%s_%s" % (field, k), [("!String.IsEmpty(Skin.String(%s))" % setting, val)], dflt))
        v.append(var("MqGreetSet_%s" % k, [("!String.IsEmpty(Skin.String(mq_%s_greeting))" % k, "$INFO[Skin.String(mq_%s_greeting)]" % k)],
                     "(uses the holiday name)" if s_.get("custom") else "Default (%s)" % s_["greeting"].replace("$VAR[MqNewYearGreetVar]", "Happy New Year")))
        v.append(var("MqFont_%s" % k, [("Skin.HasSetting(mq_%s_font_%s)" % (k, f[0]), "$LOCALIZE[%d]" % f[2]) for f in FONTS],
                     "Default (%s)" % FONT_OF[s_["font"]]))
        v.append(var("MqFx_%s" % k, [("Skin.HasSetting(mq_%s_fx_%s)" % (k, fx), "$LOCALIZE[%d]" % sid) for fx, sid in EFFECTS],
                     "Default (%s)" % DEFAULT_FX.get(k, "none")))
        v.append(var("MqAnim_%s" % k, [("Skin.HasSetting(mq_%s_anim_%s)" % (k, an), "$LOCALIZE[%d]" % sid) for an, sid in ANIMS],
                     "Default (%s)" % DEFAULT_ANIM.get(k, "still")))
    ae = []
    for s_ in ALL:
        k = s_["key"]
        ae.append(("String.IsEqual(Window(home).Property(mq_edit),%s) + !String.IsEmpty(Skin.String(mq_%s_accent))" % (k, k), "$INFO[Skin.String(mq_%s_accent)]" % k))
        ae.append(("String.IsEqual(Window(home).Property(mq_edit),%s)" % k, s_["accent"]))
    v.append(var("MqAccentEditVar", ae, DEFAULT_ACCENT))
    v.append(var("MqEditTitleVar", [("String.IsEqual(Window(home).Property(mq_edit),%s)" % s_["key"],
                                     "$VAR[MqCustomSlotLabel_%s]" % s_["key"] if s_.get("custom") else ("Everyday rows" if s_["key"] == "everyday" else s_["name"]))
                                    for s_ in SLOT_SEASONS], ""))
    # user slot headers
    for s in SLOT_SEASONS:
        for n in range(1, SLOTS + 1):
            k = "mq_%s_%d" % (s["key"], n)
            v.append(var("MqSlotHeader_%s_%d" % (s["key"], n),
                         [("!String.IsEmpty(Skin.String(%s_label))" % k, "$INFO[Skin.String(%s_label)]" % k)],
                         "%s picks %d" % (s["name"], n)))
            v.append(var("MqSlotSettingLabel_%s_%d" % (s["key"], n),
                         [("!String.IsEmpty(Skin.String(%s_label))" % k, "Row %d: $INFO[Skin.String(%s_label)]" % (n, k)),
                          ("!String.IsEmpty(Skin.String(%s_path))" % k, "Row %d: (untitled)" % n)],
                         "Row %d: (empty)" % n))
            v.append(var("MqSlotStyleLabel_%s_%d" % (s["key"], n),
                         [("Skin.HasSetting(%s_landscape)" % k, "$LOCALIZE[31716]"),
                          ("Skin.HasSetting(%s_square)" % k, "$LOCALIZE[31717]")], "$LOCALIZE[31715]"))
    return v


# ------------------------------------------------------------------ layouts
SLOT = 330      # every row occupies exactly this much height (uniform so the grouplist scroll lands on row boundaries)
ROW_GAP = 20
ROWS_TOP = 400  # rows area = 2 * SLOT + ROW_GAP tall, ending at the bottom of the screen
TILE = {
    # kind: (tile w, tile h, item w, item h)
    "landscape": (320, 180, 344, SLOT - 54),
    "poster": (160, 240, 180, SLOT - 54),
    "square": (200, 200, 224, SLOT - 54),
    "category": (280, 150, 300, SLOT - 54),
}


def tile_body(kind, focused):
    tw, th = TILE[kind][0], TILE[kind][1]
    lines = []
    a = lines.append
    a('<control type="image"><width>%d</width><height>%d</height><texture border="16" colordiffuse="%s">marquee/rounded_fill.png</texture></control>'
      % (tw, th, "FF262626" if kind != "category" else ("$VAR[MqAccentVar]" if focused else "FF262626")))
    if kind == "category":
        a('<control type="label"><left>16</left><width>%d</width><height>%d</height><align>center</align><aligny>center</aligny>'
          '<font>mq_tile_bold</font><textcolor>FFFFFFFF</textcolor><label>$INFO[ListItem.Label]</label>%s</control>'
          % (tw - 32, th, "<scroll>true</scroll>" if focused else ""))
        return lines
    # fallback title (hidden behind artwork when artwork exists)
    a('<control type="textbox"><left>14</left><top>14</top><width>%d</width><height>%d</height><align>center</align><aligny>center</aligny>'
      '<font>mq_tile</font><textcolor>FFB3B3B3</textcolor><label>$INFO[ListItem.Label]</label></control>' % (tw - 28, th - 28))
    art = {"landscape": "MqLandscapeArtVar", "poster": "MqPosterArtVar", "square": "MqSquareArtVar"}[kind]
    aspect = "keep" if kind == "square" else "scale"
    a('<control type="image"><width>%d</width><height>%d</height><aspectratio>%s</aspectratio><fadetime>200</fadetime>'
      '<texture background="true" diffuse="marquee/mask_%s.png">$VAR[%s]</texture></control>' % (tw, th, aspect, kind, art))
    # watched tick
    a('<control type="image"><left>%d</left><top>8</top><width>34</width><height>34</height><texture>OverlayWatched.png</texture>'
      '<visible>Integer.IsGreater(ListItem.PlayCount,0) + !ListItem.IsFolder</visible></control>' % (tw - 42))
    # resume progress (Netflix-style red bar)
    a('<control type="image"><left>12</left><top>%d</top><width>%d</width><height>6</height><texture colordiffuse="66FFFFFF" border="3">marquee/underline.png</texture>'
      '<visible>ListItem.IsResumable</visible></control>' % (th - 16, tw - 24))
    a('<control type="progress"><left>12</left><top>%d</top><width>%d</width><height>6</height><info>ListItem.PercentPlayed</info>'
      '<texturebg></texturebg><lefttexture></lefttexture><righttexture></righttexture><overlaytexture></overlaytexture>'
      '<midtexture colordiffuse="$VAR[MqAccentVar]" border="3">marquee/underline.png</midtexture>'
      '<visible>ListItem.IsResumable</visible></control>' % (th - 16, tw - 24))
    if kind in ("landscape", "square"):
        a('<control type="label"><top>%d</top><width>%d</width><height>40</height><font>mq_tile</font><textcolor>%s</textcolor>'
          '<label>$VAR[MqTileLabelVar]</label>%s</control>' % (th + 10, tw, "FFFFFFFF" if focused else "FFA8A8A8",
                                                                "<scroll>true</scroll>" if focused else ""))
    return lines


def layout_include(kind):
    tw, th, iw, ih = TILE[kind]
    out = ['<include name="MqLayout_%s">' % kind, '<param name="list_id">0</param>', '<definition>']
    out.append('<itemlayout width="%d" height="%d"><control type="group"><left>24</left><top>12</top>' % (iw, ih))
    out += tile_body(kind, False)
    out.append('</control></itemlayout>')
    out.append('<focusedlayout width="%d" height="%d"><control type="group"><left>24</left><top>12</top>' % (iw, ih))
    out.append('<animation effect="zoom" start="100" end="106" center="%d,%d" time="180" tween="sine" easing="out" reversible="true" '
               'condition="Control.HasFocus($PARAM[list_id])">Conditional</animation>' % (tw // 2, th // 2))
    out += tile_body(kind, True)
    out.append('<control type="image"><left>-7</left><top>-7</top><width>%d</width><height>%d</height>'
               '<texture border="20" colordiffuse="$VAR[MqAccentVar]">marquee/focus_ring.png</texture>'
               '<visible>Control.HasFocus($PARAM[list_id])</visible></control>' % (tw + 14, th + 14))
    out.append('</control></focusedlayout>')
    out += ['</definition>', '</include>']
    return out


def row(list_id, kind, header, path, target, visible, sortby="", sortorder="", limit=25, back_to=None):
    """One horizontal row (label + list) wrapped in a group that a vertical grouplist can stack."""
    ih = TILE[kind][3]
    vis = "[Integer.IsGreater(Container(%d).NumItems,0) | Container(%d).IsUpdating]" % (list_id, list_id)
    if visible:
        vis = "%s + %s" % (visible, vis)
    attrs = ' target="%s"' % target
    if sortby:
        attrs += ' sortby="%s"' % sortby
    if sortorder:
        attrs += ' sortorder="%s"' % sortorder
    if limit:
        attrs += ' limit="%d"' % limit
    # Two direct grouplist children (the grouplist runs with usecontrolcoords): the list sits 46px down its slot,
    # and the header label is placed after it with a negative top so it consumes no space but draws above the list.
    lh = ih
    return """<control type="list" id="{lid}">
	<left>56</left><top>54</top><width>1864</width><height>{lh}</height>
	<visible>{vis}</visible>
	<orientation>horizontal</orientation>
	<scrolltime tween="cubic" easing="out">320</scrolltime>
	<preloaditems>2</preloaditems>
	<onleft>noop</onleft>
	<onright>noop</onright>{back}
	<include content="MqLayout_{kind}"><param name="list_id" value="{lid}"/></include>
	<content{attrs}>{path}</content>
</control>
<control type="label" id="{lblid}">
	<left>80</left><top>-{neg}</top><width>1500</width><height>{neg}</height>
	<visible>{vis}</visible>
	<font>mq_row</font><textcolor>FFE5E5E5</textcolor><aligny>top</aligny>
	<label>{header}</label>
</control>""".format(vis=vis, header=escape(header), lid=list_id, lh=lh, neg=SLOT, lblid=list_id * 10 + 1, kind=kind, attrs=attrs, path=escape(path),
                     back=("\n\t<onback>SetFocus(%d)</onback>" % back_to) if back_to else "")


# ------------------------------------------------------------- menu & rows
MENU = [
    # key, label, onclick list, visible
    ("home", "$LOCALIZE[10000]", ["SetFocus(2101)"], ""),
    ("movies", "$LOCALIZE[342]", [
        ("Library.HasContent(movies)", "ActivateWindow(Videos,videodb://movies/titles/,return)"),
        ("!Library.HasContent(movies)", "ActivateWindow(Videos,sources://video/,return)")], "!Skin.HasSetting(HomeMenuNoMovieButton)"),
    ("tvshows", "$LOCALIZE[20343]", [
        ("Library.HasContent(tvshows)", "ActivateWindow(Videos,videodb://tvshows/titles/,return)"),
        ("!Library.HasContent(tvshows)", "ActivateWindow(Videos,sources://video/,return)")], "!Skin.HasSetting(HomeMenuNoTVShowButton)"),
    ("music", "$LOCALIZE[2]", ["ActivateWindow(Music,root,return)"], "!Skin.HasSetting(HomeMenuNoMusicButton)"),
    ("musicvideos", "$LOCALIZE[20389]", ["ActivateWindow(Videos,musicvideos,return)"],
     "!Skin.HasSetting(HomeMenuNoMusicVideoButton) + Library.HasContent(musicvideos)"),
    ("livetv", "$LOCALIZE[19020]", ["ActivateWindow(TVChannels)"], "!Skin.HasSetting(HomeMenuNoTVButton) + System.HasPVRAddon"),
    ("radio", "$LOCALIZE[19021]", ["ActivateWindow(RadioChannels)"], "!Skin.HasSetting(HomeMenuNoRadioButton) + System.HasPVRAddon"),
    ("video", "$LOCALIZE[3]", ["ActivateWindow(Videos,root)"], "!Skin.HasSetting(HomeMenuNoVideosButton)"),
    ("addons", "$LOCALIZE[24001]", ["ActivateWindow(AddonBrowser)"], "!Skin.HasSetting(HomeMenuNoProgramsButton)"),
    ("menuaddon1", "$VAR[MqAddonMenuLabel_1]", ["RunAddon($INFO[Skin.String(mq_menuaddon_1)])"], "!String.IsEmpty(Skin.String(mq_menuaddon_1))"),
    ("menuaddon2", "$VAR[MqAddonMenuLabel_2]", ["RunAddon($INFO[Skin.String(mq_menuaddon_2)])"], "!String.IsEmpty(Skin.String(mq_menuaddon_2))"),
    ("menuaddon3", "$VAR[MqAddonMenuLabel_3]", ["RunAddon($INFO[Skin.String(mq_menuaddon_3)])"], "!String.IsEmpty(Skin.String(mq_menuaddon_3))"),
    ("pictures", "$LOCALIZE[1]", ["ActivateWindow(Pictures)"], "!Skin.HasSetting(HomeMenuNoPicturesButton)"),
    ("games", "$LOCALIZE[15016]", ["ActivateWindow(Games)"], "System.GetBool(gamesgeneral.enable) + !Skin.HasSetting(HomeMenuNoGamesButton)"),
    ("favourites", "$LOCALIZE[10134]", ["ActivateWindow(favouritesbrowser)"], "!Skin.HasSetting(HomeMenuNoFavButton)"),
    ("weather", "$LOCALIZE[8]", [("!String.IsEmpty(Weather.Plugin)", "ActivateWindow(Weather)"),
                                 ("String.IsEmpty(Weather.Plugin)", "ReplaceWindow(servicesettings,weather)")],
     "!Skin.HasSetting(HomeMenuNoWeatherButton)"),
]
MENU_IDS = {m[0]: 9101 + i for i, m in enumerate(MENU)}
ROWS_IDS = {m[0]: 2101 + i for i, m in enumerate(MENU)}

M, T, MU = "Library.HasContent(movies)", "Library.HasContent(tvshows)", "Library.HasContent(music)"
SP = "special://skin/playlists/"
SECTION_ROWS = {
    "home": [
        ("landscape", "$LOCALIZE[31010]", SP + "inprogress_movies.xsp", "videos", M, "", ""),
        ("landscape", "$LOCALIZE[626]", "videodb://inprogresstvshows", "videos", T, "lastplayed", "descending"),
        ("poster", "$LOCALIZE[20386]", SP + "recent_unwatched_movies.xsp", "videos", M, "", ""),
        ("landscape", "$LOCALIZE[20387]", SP + "recent_unwatched_episodes.xsp", "videos", T, "", ""),
        ("poster", "$LOCALIZE[31006]", SP + "random_movies.xsp", "videos", M, "", ""),
        ("poster", "$LOCALIZE[31122]", SP + "unwatched_tvshows.xsp", "videos", T, "", ""),
        ("square", "$LOCALIZE[359]", "musicdb://recentlyaddedalbums/", "music", MU, "", ""),
    ],
    "movies": [
        ("landscape", "$LOCALIZE[31010]", SP + "inprogress_movies.xsp", "videos", M, "", ""),
        ("poster", "$LOCALIZE[20386]", SP + "recent_unwatched_movies.xsp", "videos", M, "", ""),
        ("poster", "$LOCALIZE[31007]", SP + "unwatched_movies.xsp", "videos", M, "", ""),
        ("poster", "$LOCALIZE[31006]", SP + "random_movies.xsp", "videos", M, "", ""),
        ("category", "$LOCALIZE[135]", "videodb://movies/genres/", "videos", M, "", ""),
        ("poster", "$LOCALIZE[31075]", "videodb://movies/sets/", "videos", M, "random", ""),
        ("category", "$LOCALIZE[31148]", "library://video/movies/", "videos", M, "", ""),
    ],
    "tvshows": [
        ("landscape", "$LOCALIZE[626]", "videodb://inprogresstvshows", "videos", T, "lastplayed", "descending"),
        ("landscape", "$LOCALIZE[20387]", SP + "recent_unwatched_episodes.xsp", "videos", T, "", ""),
        ("poster", "$LOCALIZE[31122]", SP + "unwatched_tvshows.xsp", "videos", T, "", ""),
        ("category", "$LOCALIZE[135]", "videodb://tvshows/genres/", "videos", T, "", ""),
        ("category", "$LOCALIZE[20388]", "videodb://tvshows/studios/", "videos", T, "", ""),
        ("category", "$LOCALIZE[31148]", "library://video/tvshows/", "videos", T, "", ""),
    ],
    "music": [
        ("square", "$LOCALIZE[517]", "musicdb://recentlyplayedalbums", "music", MU, "", ""),
        ("square", "$LOCALIZE[359]", "musicdb://recentlyaddedalbums/", "music", MU, "", ""),
        ("square", "$LOCALIZE[31012]", SP + "random_albums.xsp", "music", MU, "", ""),
        ("square", "$LOCALIZE[31013]", SP + "random_artists.xsp", "music", MU, "", ""),
        ("square", "$LOCALIZE[31011]", SP + "mostplayed_albums.xsp", "music", MU, "playcount", "descending"),
        ("category", "$LOCALIZE[135]", "musicdb://genres/", "music", MU, "", ""),
        ("category", "$LOCALIZE[31148]", "library://music/", "music", "", "", ""),
    ],
    "musicvideos": [
        ("landscape", "$LOCALIZE[20390]", "videodb://recentlyaddedmusicvideos/", "videos", "", "", ""),
        ("landscape", "$LOCALIZE[31151]", SP + "unwatched_musicvideos.xsp", "videos", "", "", ""),
        ("landscape", "$LOCALIZE[31006]", SP + "random_musicvideos.xsp", "videos", "", "", ""),
    ],
    "livetv": [
        ("square", "$LOCALIZE[31016]", "pvr://channels/tv/*?view=lastplayed", "tvchannels", "", "lastplayed", "descending"),
        ("landscape", "$LOCALIZE[31015]", "pvr://recordings/tv/active?view=flat", "tvrecordings", "", "date", "descending"),
        ("square", "$LOCALIZE[19173]", "pvr://channels/tv", "tvguide", "", "", ""),
        ("category", "$LOCALIZE[31148]", "pvr://tv/", "tvchannels", "", "", ""),
    ],
    "radio": [
        ("square", "$LOCALIZE[31018]", "pvr://channels/radio/*?view=lastplayed", "radiochannels", "", "lastplayed", "descending"),
        ("square", "$LOCALIZE[19174]", "pvr://channels/radio", "radioguide", "", "", ""),
        ("category", "$LOCALIZE[31148]", "pvr://radio/", "radiochannels", "", "", ""),
    ],
    "video": [
        ("category", "$LOCALIZE[31148]", "library://video/", "videos", "", "", ""),
        ("category", "$LOCALIZE[20094]", "sources://video/", "videos", "", "", ""),
        ("category", "$LOCALIZE[136]", "special://videoplaylists/", "videos", "", "", ""),
    ],
    "addons": [
        ("square", "$LOCALIZE[1037]", "addons://sources/video/", "videos", "", "lastused", "descending"),
        ("square", "$LOCALIZE[1038]", "addons://sources/audio/", "music", "", "lastused", "descending"),
        ("square", "$LOCALIZE[1043]", "addons://sources/executable/", "programs", "", "lastused", "descending"),
        ("square", "$LOCALIZE[1039]", "addons://sources/image/", "pictures", "", "lastused", "descending"),
        ("category", "$LOCALIZE[31148]", "addons://", "addonbrowser", "", "", ""),
    ],
    "pictures": [
        ("category", "$LOCALIZE[20094]", "sources://pictures/", "pictures", "", "", ""),
        ("square", "$LOCALIZE[1039]", "addons://sources/image/", "pictures", "", "", ""),
    ],
    "games": [
        ("square", "$LOCALIZE[35049]", "addons://sources/game/", "games", "", "lastused", "descending"),
    ],
    "favourites": [
        ("square", "$LOCALIZE[10134]", "favourites://", "", "", "", ""),
    ],
    "weather": [],
    "menuaddon1": [("square", "$VAR[MqAddonMenuLabel_1]", "$VAR[MqAddonRowPath_1]", "videos", "Skin.HasSetting(mq_menuaddon_1_row)", "", "")],
    "menuaddon2": [("square", "$VAR[MqAddonMenuLabel_2]", "$VAR[MqAddonRowPath_2]", "videos", "Skin.HasSetting(mq_menuaddon_2_row)", "", "")],
    "menuaddon3": [("square", "$VAR[MqAddonMenuLabel_3]", "$VAR[MqAddonRowPath_3]", "videos", "Skin.HasSetting(mq_menuaddon_3_row)", "", "")],
}

BUILTIN = {
    "groundhog": [
        ("poster", "Groundhog Day", SP + "mq_groundhog_movie.xsp", "videos"),
        ("poster", "Stuck in a Time Loop", SP + "mq_groundhog_loops.xsp", "videos"),
        ("poster", "Bill Murray Favorites", SP + "mq_groundhog_murray.xsp", "videos"),
        ("landscape", "Groundhog Day Episodes", SP + "mq_groundhog_episodes.xsp", "videos"),
    ],
    "halloween": [
        ("poster", "Spooky Season", SP + "mq_halloween_spooky.xsp", "videos"),
        ("poster", "Horror Movies", SP + "mq_halloween_horror.xsp", "videos"),
        ("landscape", "Halloween Episodes", SP + "mq_halloween_episodes.xsp", "videos"),
        ("poster", "Creepy TV", SP + "mq_halloween_tv.xsp", "videos"),
    ],
    "thanksgiving": [
        ("poster", "Thanksgiving Favorites", SP + "mq_thanksgiving_movies.xsp", "videos"),
        ("landscape", "Thanksgiving Episodes", SP + "mq_thanksgiving_episodes.xsp", "videos"),
        ("poster", "Family Movie Night", SP + "mq_thanksgiving_family.xsp", "videos"),
    ],
    "christmas": [
        ("poster", "Christmas Movies", SP + "mq_christmas_movies.xsp", "videos"),
        ("landscape", "Holiday Episodes", SP + "mq_christmas_episodes.xsp", "videos"),
        ("poster", "Family Movie Night", SP + "mq_christmas_family.xsp", "videos"),
    ],
    "mlk": [
        ("poster", "Civil Rights Stories", SP + "mq_mlk_civilrights.xsp", "videos"),
        ("poster", "Documentaries", SP + "mq_mlk_docs.xsp", "videos"),
        ("poster", "Based on True History", SP + "mq_memorial_history.xsp", "videos"),
    ],
    "presidents": [
        ("poster", "Presidents & Politics", SP + "mq_presidents_movies.xsp", "videos"),
        ("poster", "American History", SP + "mq_july4_history.xsp", "videos"),
        ("poster", "Political TV", SP + "mq_presidents_tv.xsp", "videos"),
    ],
    "mothers": [
        ("poster", "Movies for Mom", SP + "mq_mothers_movies.xsp", "videos"),
        ("poster", "Romance & Feel-Good", SP + "mq_valentine_romance.xsp", "videos"),
        ("landscape", "Mother's Day Episodes", SP + "mq_mothers_episodes.xsp", "videos"),
    ],
    "juneteenth": [
        ("poster", "Stories of Freedom", SP + "mq_juneteenth_freedom.xsp", "videos"),
        ("poster", "Civil Rights Stories", SP + "mq_mlk_civilrights.xsp", "videos"),
        ("poster", "Documentaries", SP + "mq_mlk_docs.xsp", "videos"),
    ],
    "fathers": [
        ("poster", "Movies for Dad", SP + "mq_fathers_movies.xsp", "videos"),
        ("poster", "Action Night", SP + "mq_fathers_action.xsp", "videos"),
        ("landscape", "Father's Day Episodes", SP + "mq_fathers_episodes.xsp", "videos"),
        ("poster", "War Movies", SP + "mq_memorial_war.xsp", "videos"),
    ],
    "labor": [
        ("poster", "Summer's Last Hurrah", SP + "mq_labor_summer.xsp", "videos"),
        ("poster", "Working-Class Heroes", SP + "mq_labor_workers.xsp", "videos"),
        ("poster", "Party Comedies", SP + "mq_newyear_comedies.xsp", "videos"),
    ],
    "pirate": [
        ("poster", "Pirate Adventures", SP + "mq_pirate_movies.xsp", "videos"),
        ("landscape", "Pirate Episodes", SP + "mq_pirate_episodes.xsp", "videos"),
        ("poster", "Swashbucklers & Adventure", SP + "mq_pirate_adventure.xsp", "videos"),
    ],
    "columbus": [
        ("poster", "Explorers & the Open Sea", SP + "mq_columbus_sea.xsp", "videos"),
        ("poster", "Swashbucklers & Adventure", SP + "mq_pirate_adventure.xsp", "videos"),
        ("poster", "Based on True History", SP + "mq_memorial_history.xsp", "videos"),
    ],
    "veterans": [
        ("poster", "War Movies", SP + "mq_memorial_war.xsp", "videos"),
        ("poster", "Military & War TV", SP + "mq_memorial_tv.xsp", "videos"),
        ("poster", "Based on True History", SP + "mq_memorial_history.xsp", "videos"),
    ],
    "newyear": [
        ("poster", "New Year's Eve Movies", SP + "mq_newyear_movies.xsp", "videos"),
        ("landscape", "New Year's Episodes", SP + "mq_newyear_episodes.xsp", "videos"),
        ("poster", "Party Comedies", SP + "mq_newyear_comedies.xsp", "videos"),
    ],
    "valentine": [
        ("poster", "Romance Movies", SP + "mq_valentine_romance.xsp", "videos"),
        ("poster", "Romantic Comedies", SP + "mq_valentine_romcoms.xsp", "videos"),
        ("landscape", "Valentine's Episodes", SP + "mq_valentine_episodes.xsp", "videos"),
    ],
    "stpatrick": [
        ("poster", "Luck of the Irish", SP + "mq_stpatrick_irish.xsp", "videos"),
        ("landscape", "St. Patrick's Day Episodes", SP + "mq_stpatrick_episodes.xsp", "videos"),
        ("poster", "Family Movie Night", SP + "mq_easter_family.xsp", "videos"),
    ],
    "easter": [
        ("poster", "Easter Movies", SP + "mq_easter_movies.xsp", "videos"),
        ("poster", "The Story of Jesus", SP + "mq_easter_faith.xsp", "videos"),
        ("landscape", "Easter Episodes", SP + "mq_easter_episodes.xsp", "videos"),
        ("poster", "Family Movie Night", SP + "mq_easter_family.xsp", "videos"),
    ],
    "memorial": [
        ("poster", "War Movies", SP + "mq_memorial_war.xsp", "videos"),
        ("poster", "Military & War TV", SP + "mq_memorial_tv.xsp", "videos"),
        ("poster", "Based on True History", SP + "mq_memorial_history.xsp", "videos"),
    ],
    "july4": [
        ("poster", "Patriotic Picks", SP + "mq_july4_patriotic.xsp", "videos"),
        ("landscape", "Independence Day Episodes", SP + "mq_july4_episodes.xsp", "videos"),
        ("poster", "American History", SP + "mq_july4_history.xsp", "videos"),
        ("poster", "War Movies", SP + "mq_memorial_war.xsp", "videos"),
    ],
}

SEASON_INDEX = {"halloween": 1, "thanksgiving": 2, "christmas": 3, "everyday": 4, "easter": 5, "memorial": 6, "july4": 7,
                "newyear": 8, "valentine": 9, "stpatrick": 10, "mlk": 11, "presidents": 12, "mothers": 13,
                "juneteenth": 14, "fathers": 15, "labor": 16, "pirate": 17, "columbus": 18, "veterans": 19,
                "custom1": 20, "custom2": 21, "custom3": 22, "custom4": 23, "custom5": 24, "groundhog": 25}


def seasonal_rows(back_to):
    out = []
    for s in SLOT_SEASONS:
        k = s["key"]
        si = SEASON_INDEX[k]
        season_cond = "" if k == "everyday" else "$EXP[mq_%s]" % k
        # user rows come first: they are the rows people set up on purpose
        for n in range(1, SLOTS + 1):
            p = "mq_%s_%d" % (k, n)
            path = "$INFO[Skin.String(%s_path)]" % p
            base = "!String.IsEmpty(Skin.String(%s_path))" % p
            if season_cond:
                base = season_cond + " + " + base
            header = "$VAR[MqSlotHeader_%s_%d]" % (k, n)
            out.append(row(30000 + si * 100 + n * 10 + 1, "poster", header, path, "videos",
                           base + " + !Skin.HasSetting(%s_landscape) + !Skin.HasSetting(%s_square)" % (p, p), limit=40, back_to=back_to))
            out.append(row(30000 + si * 100 + n * 10 + 2, "landscape", header, path, "videos",
                           base + " + Skin.HasSetting(%s_landscape)" % p, limit=40, back_to=back_to))
            out.append(row(30000 + si * 100 + n * 10 + 3, "square", header, path, "music",
                           base + " + Skin.HasSetting(%s_square)" % p, limit=40, back_to=back_to))
        for i, (kind, header, path, target) in enumerate(BUILTIN.get(k, [])):
            out.append(row(30000 + si * 100 + 80 + i, kind, header, path, target,
                           season_cond + " + !Skin.HasSetting(mq_no_builtin) + !Skin.HasSetting(mq_%s_nobuiltin)" % k, limit=40, back_to=back_to))
    return out


# --------------------------------------------------------------- effects
def scrolling_layer(tex, w, h, top, count_x, time_ms, reverse, diffuse, bob_px, bob_ms, fade_lo):
    """Horizontal seamless loop of a tileable texture with a gentle vertical 'billow'."""
    start, end = ("-%d,0" % w, "0,0") if reverse else ("0,0", "-%d,0" % w)
    imgs = "\n".join('\t\t\t<control type="image"><left>%d</left><top>0</top><width>%d</width><height>%d</height>'
                     '<texture colordiffuse="$VAR[%s]">marquee/%s</texture></control>' % (i * w, w, h, diffuse, tex)
                     for i in range(count_x))
    return """	<control type="group">
		<top>{top}</top><left>0</left><width>{tw}</width><height>{h}</height>
		<animation effect="slide" start="0,0" end="0,-{bob}" time="{bob_ms}" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		<animation effect="fade" start="100" end="{fade_lo}" time="{fade_ms}" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		<control type="group">
			<animation effect="slide" start="{start}" end="{end}" time="{time}" loop="true" condition="true">Conditional</animation>
{imgs}
		</control>
	</control>""".format(top=top, tw=w * count_x, h=h, bob=bob_px, bob_ms=bob_ms, fade_lo=fade_lo, fade_ms=int(bob_ms * 1.37),
                         start=start, end=end, time=time_ms, imgs=imgs)


def effects_include():
    fog = "\n".join([
        scrolling_layer("fog_ground.png", 2048, 640, 470, 2, 95000, False, "MqFogGroundVar", 26, 9000, 78),
        scrolling_layer("fog_bank.png", 2048, 560, 300, 2, 130000, True, "MqFogBankVar", 34, 12000, 60),
        scrolling_layer("fog_wisp.png", 2048, 360, -110, 2, 160000, False, "MqFogWispVar", 22, 7000, 55),
    ])
    snow = []
    for tex, t, alpha in (("snow_small.png", 26000, "B0FFFFFF"), ("snow_large.png", 15000, "C8FFFFFF")):
        snow.append("""	<control type="group">
		<animation effect="slide" start="-36,0" end="36,0" time="7000" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		<control type="group">
			<animation effect="slide" start="0,0" end="0,1080" time="{t}" loop="true" condition="true">Conditional</animation>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="{a}">marquee/{tex}</texture></control>
			<control type="image"><left>0</left><top>-1080</top><width>1920</width><height>1080</height><texture colordiffuse="{a}">marquee/{tex}</texture></control>
		</control>
	</control>""".format(t=t, a=alpha, tex=tex))
    leaves = """	<control type="group">
		<animation effect="slide" start="0,0" end="1920,1080" time="38000" loop="true" condition="true">Conditional</animation>
		<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="D8FFFFFF">marquee/leaves.png</texture></control>
		<control type="image"><left>-1920</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="D8FFFFFF">marquee/leaves.png</texture></control>
		<control type="image"><left>0</left><top>-1080</top><width>1920</width><height>1080</height><texture colordiffuse="D8FFFFFF">marquee/leaves.png</texture></control>
		<control type="image"><left>-1920</left><top>-1080</top><width>1920</width><height>1080</height><texture colordiffuse="D8FFFFFF">marquee/leaves.png</texture></control>
	</control>"""
    petals = leaves.replace("leaves.png", "petals.png").replace('time="38000"', 'time="56000"').replace("D8FFFFFF", "E0FFFFFF")
    # fireworks: (centre x, centre y, size, colour, start delay ms, pause after burst ms)
    bursts = [(1500, 250, 470, "red", 0, 1900), (1150, 160, 360, "white", 900, 2700), (1770, 470, 390, "blue", 1700, 2300),
              (880, 330, 300, "gold", 2600, 3200), (1340, 520, 430, "blue", 3400, 2100), (1690, 130, 330, "white", 4300, 3000),
              (1050, 560, 340, "red", 5100, 2500), (1250, 330, 280, "gold", 6000, 3400)]
    fw = []
    for cx, cy, size, col, d, pause in bursts:
        b = d + 700  # the rocket climbs for 0.7s, then bursts
        fw.append("""	<control type="image">
		<left>{tl}</left><top>{cy}</top><width>8</width><height>140</height>
		<texture colordiffuse="C0FFFFFF">marquee/trail.png</texture>
		<animation type="Conditional" condition="true" loop="true">
			<effect type="slide" start="0,{rise}" end="0,0" delay="{d}" time="700" tween="quadratic" easing="out"/>
			<effect type="fade" start="0" end="100" delay="{d}" time="80"/>
			<effect type="fade" start="100" end="0" delay="{fo}" time="120"/>
			<effect type="fade" start="100" end="100" delay="{b2}" time="{rest}"/>
		</animation>
	</control>
	<control type="image">
		<left>{l}</left><top>{t}</top><width>{s}</width><height>{s}</height>
		<texture colordiffuse="EEFFFFFF">marquee/burst_{col}.png</texture>
		<animation type="Conditional" condition="true" loop="true">
			<effect type="zoom" start="10" end="100" center="auto" delay="{b}" time="1000" tween="quadratic" easing="out"/>
			<effect type="fade" start="0" end="100" delay="{b}" time="120"/>
			<effect type="fade" start="100" end="0" delay="{bf}" time="1300"/>
			<effect type="slide" start="0,0" end="0,50" delay="{bs}" time="1700" tween="quadratic" easing="in"/>
			<effect type="fade" start="100" end="100" delay="{b2}" time="{pause}"/>
		</animation>
	</control>""".format(tl=cx - 4, cy=cy, rise=1080 - cy, d=d, fo=b - 60, b=b, bf=b + 650, bs=b + 300, b2=b + 2000,
                         rest=pause, pause=pause, l=cx - size // 2, t=cy - size // 2, s=size, col=col))
    fireworks = "\n".join(fw)
    shamrocks = leaves.replace("leaves.png", "shamrocks.png").replace('time="38000"', 'time="46000"').replace("D8FFFFFF", "E6FFFFFF")
    hearts = """	<control type="group">
		<animation effect="slide" start="-30,0" end="30,0" time="6000" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		<control type="group">
			<animation effect="slide" start="0,0" end="0,-1080" time="34000" loop="true" condition="true">Conditional</animation>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="D0FFFFFF">marquee/hearts.png</texture></control>
			<control type="image"><left>0</left><top>1080</top><width>1920</width><height>1080</height><texture colordiffuse="D0FFFFFF">marquee/hearts.png</texture></control>
		</control>
	</control>"""
    confetti = "\n".join("""	<control type="group">
		<animation effect="slide" start="-24,0" end="24,0" time="{sway}" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		<control type="group">
			<animation effect="slide" start="0,0" end="0,1080" time="{t}" loop="true" condition="true">Conditional</animation>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="{a}">marquee/{tex}</texture></control>
			<control type="image"><left>0</left><top>-1080</top><width>1920</width><height>1080</height><texture colordiffuse="{a}">marquee/{tex}</texture></control>
		</control>
	</control>""".format(sway=sw, t=t, a=al, tex=tx) for tx, t, al, sw in (("confetti_small.png", 30000, "B8FFFFFF", 5000),
                                                                         ("confetti_large.png", 19000, "D0FFFFFF", 7000)))
    balldrop = """	<control type="group">
		<left>1380</left><top>110</top>
		<animation effect="fade" start="0" end="100" time="800">Visible</animation>
		<control type="image"><left>116</left><top>40</top><width>8</width><height>700</height><texture colordiffuse="B0C9D1E0" border="3">marquee/underline.png</texture></control>
		<control type="image"><left>40</left><top>740</top><width>160</width><height>24</height><texture colordiffuse="FFE8C25A" border="8">marquee/rounded_fill.png</texture></control>
		<control type="image">
			<left>0</left><top>0</top><width>240</width><height>240</height>
			<texture>marquee/ball.png</texture>
			<visible>$EXP[mq_balldrop] + !Player.HasVideo</visible>
			<animation effect="slide" start="0,0" end="0,520" time="59000" tween="linear">Visible</animation>
			<animation effect="rotate" start="-4" end="4" center="auto" time="1600" tween="sine" easing="inout" pulse="true" condition="true">Conditional</animation>
		</control>
		<control type="label">
			<left>-560</left><top>200</top><width>480</width><height>320</height><align>right</align><aligny>center</aligny>
			<font>mq_bigcount</font><textcolor>FFF0CE6A</textcolor><shadowcolor>C0000000</shadowcolor>
			<label>$VAR[MqBallCountVar]</label>
		</control>
	</control>"""
    midnight = """	<control type="group">
		<visible>!Skin.HasSetting(mq_effects_off) + $EXP[mq_ny_midnight] + !Player.HasVideo</visible>
		<animation effect="zoom" start="40" end="100" center="1410,420" time="900" tween="back" easing="out">Visible</animation>
		<animation effect="fade" start="0" end="100" time="400">Visible</animation>
		<control type="label">
			<left>960</left><top>230</top><width>900</width><height>380</height><align>center</align><aligny>center</aligny>
			<font>mq_bigcount</font><textcolor>FFF0CE6A</textcolor><shadowcolor>C0000000</shadowcolor>
			<label>$INFO[System.Date(yyyy)]</label>
		</control>
	</control>"""
    return """<include name="MqSeasonEffects">
<control type="group">
	<description>Graveyard fog - billows over the rows and the top menu</description>
	<visible>$EXP[mq_fog] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1600">WindowOpen</animation>
	<animation effect="fade" start="100" end="0" time="300">WindowClose</animation>
	<animation effect="fade" time="1200">VisibleChange</animation>
{fog}
</control>
<control type="group">
	<description>Christmas snow</description>
	<visible>$EXP[mq_snow] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{snow}
</control>
<control type="group">
	<description>Thanksgiving falling leaves</description>
	<visible>$EXP[mq_leaves] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{leaves}
</control>
<control type="group">
	<description>Easter spring petals</description>
	<visible>$EXP[mq_petals] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{petals}
</control>
<control type="group">
	<description>Independence Day fireworks</description>
	<visible>$EXP[mq_fireworks] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{fireworks}
</control>
<control type="group">
	<description>Valentine's hearts</description>
	<visible>$EXP[mq_hearts] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{hearts}
</control>
<control type="group">
	<description>St. Patrick's shamrocks</description>
	<visible>$EXP[mq_shamrocks] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{shamrocks}
</control>
<control type="group">
	<description>New Year's confetti</description>
	<visible>$EXP[mq_confetti] + !Player.HasVideo</visible>
	<animation effect="fade" start="0" end="100" time="1200">WindowOpen</animation>
	<animation effect="fade" time="800">VisibleChange</animation>
{confetti}
</control>
<control type="group">
	<description>New Year's Eve ball drop (the last 60 seconds before midnight)</description>
	<visible>$EXP[mq_balldrop] + !Player.HasVideo</visible>
{balldrop}
</control>
<control type="group">
	<description>Midnight: the new year in giant gold numbers</description>
	<visible>!Skin.HasSetting(mq_effects_off) + $EXP[mq_ny_midnight] + !Player.HasVideo</visible>
{midnight}
</control>
</include>""".format(fog=fog, snow="\n".join(snow), leaves=leaves, petals=petals, fireworks=fireworks,
                     hearts=hearts, shamrocks=shamrocks, confetti=confetti, balldrop=balldrop, midnight=midnight)


def backdrop_include():
    return """<include name="MqSeasonBackdrop">
	<param name="diffuse">FFFFFFFF</param>
	<definition>
	<control type="multiimage">
		<depth>DepthBackground</depth>
		<left>0</left><top>0</top><width>1920</width><height>1080</height>
		<aspectratio>scale</aspectratio>
		<timeperimage>25000</timeperimage>
		<randomize>true</randomize>
		<fadetime>1500</fadetime>
		<imagepath background="true" colordiffuse="$PARAM[diffuse]">$VAR[MqBackdropPathVar]</imagepath>
	</control>
	</definition>
</include>"""


def includes_file():
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<!-- Generated by gen_xml.py for skin.marquee. -->', '<includes>']
    parts += ["\t" + x for x in expressions()]
    parts += variables()
    for k in TILE:
        parts += layout_include(k)
    parts.append(effects_include())
    parts.append(backdrop_include())
    parts.append('</includes>')
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------- Home.xml
def menu_button(key, label, actions, visible):
    bid = MENU_IDS[key]
    rid = ROWS_IDS[key]
    acts = []
    for a in actions:
        if isinstance(a, tuple):
            acts.append('\t\t<onclick condition="%s">%s</onclick>' % a)
        else:
            acts.append('\t\t<onclick>%s</onclick>' % a)
    sel = 'String.IsEqual(Window(home).Property(mq_menu),%s)' % key
    return """	<control type="button" id="{bid}">
		<width>auto</width><height>64</height>
		<textoffsetx>15</textoffsetx>
		<font>mq_menu</font>
		<aligny>center</aligny>
		<textcolor>FFB3B3B3</textcolor><focusedcolor>FFFFFFFF</focusedcolor>
		<label>{label}</label>
		<texturefocus colordiffuse="$VAR[MqAccentVar]" border="24,0,24,0">marquee/menu_focus.png</texturefocus>
		<texturenofocus colordiffuse="$VAR[MqMenuSelDiffuse_{key}]" border="24,0,24,0">marquee/menu_focus.png</texturenofocus>
		<onfocus>SetProperty(mq_menu,{key},home)</onfocus>
		<onfocus>SetProperty(mq_rows_id,{rid},home)</onfocus>
		<ondown>SetFocus({rid})</ondown>
{acts}
		{vis}
	</control>""".format(bid=bid, rid=rid, label=label, key=key, acts="\n".join(acts),
                          vis=("<visible>%s</visible>" % visible) if visible else "")


def home_xml():
    rows_xml = []
    for key, *_ in MENU:
        rid = ROWS_IDS[key]
        bid = MENU_IDS[key]
        items = []
        if key == "home":
            items += seasonal_rows(bid)
        base = 40000 + (rid - 2100) * 100
        for i, (kind, header, path, target, cond, sb, so) in enumerate(SECTION_ROWS[key]):
            items.append(row(base + i, kind, header, path, target, cond, sb, so, back_to=bid))
        if key == "home":
            ev = "!Library.HasContent(movies) + !Library.HasContent(tvshows) + !$EXP[mq_season] + String.IsEmpty(Skin.String(mq_everyday_1_path))"
            items.append("""<control type="textbox" id="2198"><left>80</left><top>10</top><width>1300</width><height>120</height><font>mq_tag</font><textcolor>FFD0D0D0</textcolor>
	<visible>%s</visible>
	<label>Your library is empty. Add a video source and scan it into the library, then this screen fills up with rows of your movies and shows. Seasonal rows can be set up in Skin settings.</label></control>
<control type="button" id="2199">
	<left>80</left><top>10</top><width>auto</width><height>70</height><textoffsetx>30</textoffsetx><font>mq_tile_bold</font><aligny>center</aligny>
	<visible>%s</visible>
	<label>$LOCALIZE[31110]</label>
	<texturefocus border="16" colordiffuse="$VAR[MqAccentVar]">marquee/rounded_fill.png</texturefocus>
	<texturenofocus border="16" colordiffuse="FF333333">marquee/rounded_fill.png</texturenofocus>
	<onclick>ActivateWindow(videos,files,return)</onclick>
</control>""" % (ev, ev))
        rows_xml.append("""		<control type="grouplist" id="{rid}">
			<left>0</left><top>0</top><right>0</right><bottom>0</bottom>
			<orientation>vertical</orientation>
			<usecontrolcoords>true</usecontrolcoords>
			<itemgap>{gap}</itemgap>
			<scrolltime tween="cubic" easing="out">420</scrolltime>
			<onup>SetFocus({bid})</onup>
			<ondown>noop</ondown>
			<visible>String.IsEqual(Window(home).Property(mq_menu),{key})</visible>
			<animation effect="fade" start="0" end="100" time="260">Visible</animation>
			<animation effect="slide" start="0,30" end="0,0" time="260" tween="cubic" easing="out">Visible</animation>
{items}
		</control>""".format(gap=ROW_GAP, rid=rid, bid=bid, key=key, items="\n".join("\t\t\t" + x.replace("\n", "\n\t\t\t") for x in items)))

    menu = "\n".join(menu_button(*m) for m in MENU)
    # one greeting label per font; the text and colour come from the active holiday (or its overrides)
    greet_labels = "\n".join("""			<control type="label">
				<left>0</left><top>{top}</top><width>1300</width><height>170</height><aligny>bottom</aligny>
				<font>{font}</font><textcolor>FFFFFFFF</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>[COLOR $VAR[MqGreetColorVar]]$VAR[MqGreetVar][/COLOR]</label>
				<visible>$EXP[mq_font_{name}]</visible>
			</control>""".format(top=top, font=font, name=name) for name, font, _, top in FONTS)
    greet_labels += """
			<control type="label">
				<left>4</left><top>20</top><width>1300</width><height>40</height>
				<font>mq_meta</font><textcolor>FFF2E6C8</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>[B][UPPERCASE]$VAR[MqKickerVar][/UPPERCASE][/B]</label>
				<visible>$EXP[mq_season]</visible>
			</control>"""
    inits = "\n".join("\t<onload condition=\"String.IsEmpty(Skin.String(mq_%s_%s))\">Skin.SetString(mq_%s_%s,%s)</onload>" % (k, w, k, w, v_)
                      for k, (st, en, _) in FIXED.items() for w, v_ in (("start", st), ("end", en)))

    return """<?xml version="1.0" encoding="UTF-8"?>
<!-- Marquee home screen. Generated by gen_xml.py - edit the generator, not this file. -->
<window>
	<defaultcontrol always="false">9101</defaultcontrol>
	<backgroundcolor>FF0A0A0A</backgroundcolor>
	<onload condition="String.IsEmpty(Window(home).Property(mq_menu))">SetProperty(mq_menu,home,home)</onload>
{inits}
	<controls>
		<include>DefaultBackground</include>

		<!-- ============ backdrop: seasonal art, replaced by the focused item's fanart ============ -->
		<control type="group">
			<visible>!Player.HasVideo</visible>
			<control type="group">
				<animation effect="fade" start="100" end="12" time="500" condition="$EXP[mq_hero_fanart]">Conditional</animation>
				<include content="MqSeasonBackdrop"><param name="diffuse" value="FFFFFFFF"/></include>
			</control>
			<control type="image">
				<left>520</left><top>0</top><width>1400</width><height>788</height>
				<aspectratio>scale</aspectratio>
				<fadetime>500</fadetime>
				<texture background="true">$VAR[MqHeroFanartVar]</texture>
				<visible>$EXP[mq_hero_fanart]</visible>
				<animation effect="fade" time="400">VisibleChange</animation>
			</control>
			<control type="image">
				<left>520</left><top>0</top><width>420</width><height>788</height>
				<texture>marquee/grad_left.png</texture>
				<visible>$EXP[mq_hero_fanart]</visible>
				<animation effect="fade" time="400">VisibleChange</animation>
			</control>
		</control>
		<control type="image"><left>0</left><top>0</top><width>1200</width><height>1080</height><texture>marquee/grad_left.png</texture></control>
		<control type="image"><left>0</left><top>380</top><width>1920</width><height>700</height><texture>marquee/grad_bottom.png</texture></control>
		<control type="image"><left>0</left><top>0</top><width>1920</width><height>260</height><texture>marquee/grad_top.png</texture></control>

		<control type="group">
		<description>everything above the backdrop fades away while an info dialog is open</description>
		<animation effect="fade" start="100" end="0" time="200" tween="sine" condition="$EXP[infodialog_active]">Conditional</animation>
		<!-- ============ hero: seasonal greeting (menu focused) ============ -->
		<control type="group">
			<left>80</left><top>96</top>
			<visible>!$EXP[mq_rows_focus]</visible>
			<animation effect="fade" time="300">VisibleChange</animation>
			<animation effect="fade" start="0" end="100" time="500">WindowOpen</animation>
{greet}
			<control type="label">
				<left>0</left><top>0</top><width>1300</width><height>170</height><aligny>bottom</aligny>
				<font>mq_hero</font><textcolor>FFFFFFFF</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>Tonight's lineup</label>
				<visible>!$EXP[mq_season]</visible>
			</control>
			<control type="label">
				<left>4</left><top>178</top><width>1300</width><height>50</height>
				<font>mq_tag</font><textcolor>FFE8E8E8</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>$VAR[MqCountdownVar]</label>
			</control>
			<control type="label">
				<left>4</left><top>230</top><width>1300</width><height>40</height>
				<font>mq_meta</font><textcolor>FF9A9A9A</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>$INFO[System.Date]</label>
			</control>
		</control>

		<!-- ============ hero: focused item info (rows focused) ============ -->
		<control type="group">
			<left>80</left><top>104</top>
			<visible>$EXP[mq_rows_focus]</visible>
			<animation effect="fade" time="250">VisibleChange</animation>
			<control type="image">
				<left>0</left><top>0</top><width>560</width><height>136</height>
				<aspectratio align="left" aligny="bottom">keep</aspectratio>
				<fadetime>250</fadetime>
				<texture background="true">$VAR[MqHeroLogoVar]</texture>
			</control>
			<control type="label">
				<left>0</left><top>0</top><width>1100</width><height>140</height><aligny>bottom</aligny>
				<font>mq_hero</font><textcolor>FFFFFFFF</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>$VAR[MqHeroTitleVar]</label>
				<visible>String.IsEmpty(ListItem.Art(clearlogo)) + String.IsEmpty(ListItem.Art(tvshow.clearlogo))</visible>
			</control>
			<control type="label">
				<left>2</left><top>150</top><width>1100</width><height>44</height>
				<font>mq_meta</font><textcolor>FFD8D8D8</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>$VAR[MqHeroMetaVar]</label>
			</control>
			<control type="textbox">
				<left>2</left><top>198</top><width>860</width><height>80</height>
				<font>mq_plot</font><textcolor>FFBDBDBD</textcolor><shadowcolor>A0000000</shadowcolor>
				<label>$VAR[MqHeroPlotVar]</label>
				<autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll>
			</control>
		</control>

		<!-- ============ rows ============ -->
		<control type="group" id="2000">
			<left>0</left><top>{rtop}</top><width>1920</width><height>{rh}</height>
			<animation effect="fade" start="0" end="100" time="400" delay="150">WindowOpen</animation>
			<animation effect="fade" start="100" end="0" time="200">WindowClose</animation>
{rows}
		</control>

		<!-- ============ top bar ============ -->
		<control type="group">
			<animation effect="slide" start="0,-120" end="0,0" time="400" tween="cubic" easing="out">WindowOpen</animation>
			<animation effect="slide" start="0,0" end="0,-120" time="200">WindowClose</animation>
			<control type="image">
				<left>66</left><top>34</top><width>52</width><height>52</height>
				<aspectratio>keep</aspectratio>
				<texture>$VAR[MqSeasonIconVar]</texture>
				<visible>$EXP[mq_season]</visible>
				<animation effect="rotate" start="-6" end="6" center="auto" time="2400" tween="sine" easing="inout" pulse="true" condition="$EXP[mq_anim_rock]">Conditional</animation>
				<animation effect="slide" start="0,-4" end="0,4" time="1400" tween="sine" easing="inout" pulse="true" condition="$EXP[mq_anim_bob]">Conditional</animation>
				<animation effect="zoom" start="92" end="110" center="auto" time="1200" tween="sine" easing="inout" pulse="true" condition="$EXP[mq_anim_pulse]">Conditional</animation>
				<animation effect="rotate" start="0" end="-360" center="auto" time="6000" loop="true" condition="$EXP[mq_anim_spin]">Conditional</animation>
			</control>
			<control type="grouplist" id="9100">
				<left>150</left><top>28</top><width>1316</width><height>64</height>
				<orientation>horizontal</orientation>
				<itemgap>6</itemgap>
				<scrolltime tween="cubic" easing="out">300</scrolltime>
				<onright>700</onright>
				<onleft>700</onleft>
				<onup>noop</onup>
{menu}
			</control>
			<control type="grouplist" id="700">
				<right>220</right><top>30</top><width>220</width><height>60</height>
				<orientation>horizontal</orientation>
				<align>right</align>
				<itemgap>8</itemgap>
				<onleft>9100</onleft>
				<onright>9100</onright>
				<ondown>SetFocus($INFO[Window(home).Property(mq_rows_id)])</ondown>
				<include content="MqIconButton"><param name="id" value="701"/><param name="icon" value="icons/search.png"/><param name="onclick" value="ActivateWindow(1107)"/></include>
				<include content="MqIconButton"><param name="id" value="702"/><param name="icon" value="icons/settings.png"/><param name="onclick" value="ActivateWindow(settings)"/></include>
				<include content="MqIconButton"><param name="id" value="703"/><param name="icon" value="icons/power.png"/><param name="onclick" value="ActivateWindow(shutdownmenu)"/></include>
			</control>
			<control type="label">
				<right>60</right><top>30</top><width>160</width><height>60</height>
				<align>right</align><aligny>center</aligny>
				<font>mq_clock</font><textcolor>FFE8E8E8</textcolor>
				<label>$INFO[System.Time]</label>
			</control>
		</control>

		<!-- ============ seasonal effects (drawn last so they drift over everything) ============ -->
		<include>MqSeasonEffects</include>
		</control>
	</controls>
</window>
""".format(rows="\n".join(rows_xml), menu=menu, greet=greet_labels, rtop=ROWS_TOP, rh=2 * SLOT + ROW_GAP, inits=inits)


def extra_includes():
    """Menu helper vars + icon button include (appended to Includes_Marquee)."""
    out = []
    for n in (1, 2, 3):
        k = "mq_menuaddon_%d" % n
        out.append(var("MqAddonMenuLabel_%d" % n,
                       [("!String.IsEmpty(Skin.String(%s_label))" % k, "$INFO[Skin.String(%s_label)]" % k)],
                       "$INFO[System.AddonTitle(Skin.String(%s))]" % k))
        out.append(var("MqAddonSettingLabel_%d" % n,
                       [("!String.IsEmpty(Skin.String(%s))" % k, "$VAR[MqAddonMenuLabel_%d]" % n)], "(none)"))
    for key, *_ in MENU:
        out.append(var("MqMenuSelDiffuse_%s" % key,
                       [("String.IsEqual(Window(home).Property(mq_menu),%s)" % key, "70FFFFFF")], "00FFFFFF"))
    out.append("""<include name="MqIconButton">
	<control type="radiobutton" id="$PARAM[id]">
		<width>60</width><height>60</height>
		<label></label>
		<font></font>
		<onclick>$PARAM[onclick]</onclick>
		<texturefocus border="16" colordiffuse="$VAR[MqAccentVar]">marquee/rounded_fill.png</texturefocus>
		<texturenofocus />
		<radioposx>12</radioposx>
		<radioposy>12</radioposy>
		<radiowidth>36</radiowidth>
		<radioheight>36</radioheight>
		<textureradioonfocus>$PARAM[icon]</textureradioonfocus>
		<textureradioonnofocus colordiffuse="FFB3B3B3">$PARAM[icon]</textureradioonnofocus>
		<textureradioofffocus>$PARAM[icon]</textureradioofffocus>
		<textureradiooffnofocus colordiffuse="FFB3B3B3">$PARAM[icon]</textureradiooffnofocus>
	</control>
</include>""")
    return out


# --------------------------------------------------------------- settings
def settings_panels():
    """Skin settings grouplists for categories 5..9 (ids 640, 650...)."""
    def btn(cid, label, onclicks, label2=None, extra=""):
        oc = "\n".join("\t\t<onclick>%s</onclick>" % o for o in onclicks)
        l2 = "\n\t\t<label2>%s</label2>" % label2 if label2 else ""
        return """	<control type="button" id="{cid}">
		<label>{label}</label>{l2}
		<include>DefaultSettingButton</include>
{oc}{extra}
	</control>""".format(cid=cid, label=label, l2=l2, oc=oc, extra=extra)

    def radio(cid, label, setting, inverted=False):
        sel = ("!Skin.HasSetting(%s)" if inverted else "Skin.HasSetting(%s)") % setting
        return """	<control type="radiobutton" id="{cid}">
		<label>{label}</label>
		<include>DefaultSettingButton</include>
		<selected>{sel}</selected>
		<onclick>Skin.ToggleSetting({setting})</onclick>
	</control>""".format(cid=cid, label=label, sel=sel, setting=setting)

    def group(gid, item, children):
        return """<control type="grouplist" id="{gid}">
	<top>133</top>
	<left>0</left>
	<right>0</right>
	<bottom>140</bottom>
	<onleft>9000</onleft>
	<onright>9000</onright>
	<onup>{gid}</onup>
	<ondown>{gid}</ondown>
	<visible>Container(9000).HasFocus({item})</visible>
{children}
</control>""".format(gid=gid, item=item, children="\n".join(children))

    panels = []
    c = []
    cid = 6400
    c.append(btn(cid, "$LOCALIZE[31700]", ["Skin.SelectBool(31700,31701|,%s,31705|mq_force_off)" % ",".join("%d|mq_force_%s" % (s_["sid"], s_["key"]) for s_ in ALL)],
                 "$VAR[MqSeasonModeLabelVar]"))
    c.append(btn(cid + 1, "- Active right now", ["noop"], "$VAR[MqSeasonNameVar]"))
    c.append(radio(cid + 2, "Seasonal effects (fog, snow, fireworks...)", "mq_effects_off", inverted=True))
    c.append(radio(cid + 3, "Show built-in seasonal rows", "mq_no_builtin", inverted=True))
    c.append(radio(cid + 4, "Seasonal backdrop behind other screens", "mq_no_global_backdrop", inverted=True))
    c.append(btn(cid + 5, "No-season backgrounds folder", ["Skin.SetPath(mq_bg_default)"], "$INFO[Skin.String(mq_bg_default)]"))
    c.append(btn(cid + 6, "- Use built-in no-season backgrounds", ["Skin.Reset(mq_bg_default)"],
                 extra="\n\t\t<enable>!String.IsEmpty(Skin.String(mq_bg_default))</enable>"))
    c.append(btn(cid + 7, "[B]Everyday rows[/B] (shown all year)", ["SetProperty(mq_edit,everyday,home)", "ActivateWindow(1190)"], "Edit"))
    i = 10
    c.append(btn(cid + i, "[COLOR FF8C8C8C]HOLIDAYS[/COLOR]", ["noop"])); i += 1
    for s_ in SEASONS:
        c.append(btn(cid + i, s_["name"], ["SetProperty(mq_edit,%s,home)" % s_["key"], "ActivateWindow(1190)"],
                     "$VAR[MqHolidayStatus_%s]" % s_["key"])); i += 1
    c.append(btn(cid + i, "[COLOR FF8C8C8C]YOUR OWN HOLIDAYS[/COLOR]", ["noop"])); i += 1
    for c_ in CUSTOM:
        c.append(btn(cid + i, "$VAR[MqCustomSlotLabel_%s]" % c_["key"], ["SetProperty(mq_edit,%s,home)" % c_["key"], "ActivateWindow(1190)"],
                     "$VAR[MqHolidayStatus_%s]" % c_["key"])); i += 1
    panels.append(group(640, 5, c))

    ma = []
    for n in (1, 2, 3):
        k = "mq_menuaddon_%d" % n
        b = 27900 + n * 10
        ma.append(btn(b, "Add-on menu item %d" % n,
                      ["Skin.SetAddon(%s,xbmc.python.pluginsource,xbmc.python.script)" % k], "$VAR[MqAddonSettingLabel_%d]" % n))
        ma.append(btn(b + 1, "- Menu label", ["Skin.SetString(%s_label)" % k], "$INFO[Skin.String(%s_label)]" % k,
                      extra="\n\t\t<enable>!String.IsEmpty(Skin.String(%s))</enable>" % k))
        ma.append(radio(b + 2, "- Show its contents as a row on the home screen", "%s_row" % k))
        ma.append(btn(b + 3, "- Remove from menu", ["Skin.Reset(%s)" % k, "Skin.Reset(%s_label)" % k, "Skin.Reset(%s_row)" % k],
                      extra="\n\t\t<enable>!String.IsEmpty(Skin.String(%s))</enable>" % k))
    menu_addons = '<include name="MqMenuAddonSettings">\n%s\n</include>\n' % "\n".join(ma)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<includes>\n<include name="MqSettingsPanels">\n%s\n</include>\n%s</includes>\n' % ("\n".join(panels), menu_addons)


def holiday_dialog():
    """Custom_1190_MqHoliday.xml: one settings page per holiday (picked by Window(home).Property(mq_edit))."""
    def btn(cid, label, onclicks, label2=None, extra=""):
        oc = "\n".join("\t\t\t<onclick>%s</onclick>" % o for o in onclicks)
        l2 = "\n\t\t\t<label2>%s</label2>" % label2 if label2 else ""
        return """		<control type="button" id="{cid}">
			<label>{label}</label>{l2}
			<include>DefaultSettingButton</include>
{oc}{extra}
		</control>""".format(cid=cid, label=label, l2=l2, oc=oc, extra=extra)

    def radio(cid, label, sel, onclick):
        return """		<control type="radiobutton" id="{cid}">
			<label>{label}</label>
			<include>DefaultSettingButton</include>
			<selected>{sel}</selected>
			<onclick>{onclick}</onclick>
		</control>""".format(cid=cid, label=label, sel=sel, onclick=onclick)

    def head(cid, text):
        return btn(cid, "[COLOR FF8C8C8C][B]%s[/B][/COLOR]" % text, ["noop"])

    groups = []
    for gi, s_ in enumerate(SLOT_SEASONS):
        k = s_["key"]
        gid = 3000 + gi * 100
        b = [gid * 10]

        def nid():
            b[0] += 1
            return b[0]
        ch = []
        custom = s_.get("custom")
        if k != "everyday":
            if custom:
                ch.append(btn(nid(), "Holiday name", ["Skin.SetString(mq_%s_name)" % k], "$INFO[Skin.String(mq_%s_name)]" % k))
            ch.append(radio(nid(), "Show this holiday", "!Skin.HasSetting(mq_%s_off)" % k, "Skin.ToggleSetting(mq_%s_off)" % k))
            ch.append(head(nid(), "DATES"))
            if k in FIXED or custom:
                ch.append(btn(nid(), "Starts (MMDD, e.g. 1001 = Oct 1)", ["Skin.SetNumeric(mq_%s_start)" % k], "$INFO[Skin.String(mq_%s_start)]" % k))
                ch.append(btn(nid(), "Ends (MMDD, e.g. 1031 = Oct 31)", ["Skin.SetNumeric(mq_%s_end)" % k], "$INFO[Skin.String(mq_%s_end)]" % k))
            else:
                bo = ",".join(["31769|"] + ["%d|mq_%s_before_%d" % (sid, k, n) for n, sid in BEFORE_OPTS])
                ao = ",".join(["31769|"] + ["%d|mq_%s_after_%d" % (sid, k, n) for n, sid in AFTER_OPTS])
                ch.append(btn(nid(), "Starts", ["Skin.SelectBool(31796,%s)" % bo], "$VAR[MqBefore_%s]" % k))
                ch.append(btn(nid(), "Ends", ["Skin.SelectBool(31797,%s)" % ao], "$VAR[MqAfter_%s]" % k))
            ch.append(head(nid(), "LOOK"))
            ch.append(btn(nid(), "Greeting", ["Skin.SetString(mq_%s_greeting)" % k], "$VAR[MqGreetSet_%s]" % k))
            ch.append(btn(nid(), "- Small label above the greeting", ["Skin.SetString(mq_%s_kicker)" % k], "$VAR[MqVal_kicker_%s]" % k))
            if custom:
                ch.append(btn(nid(), "- Line under the greeting", ["Skin.SetString(mq_%s_message)" % k], "$VAR[MqVal_message_%s]" % k))
            ch.append(btn(nid(), "- Greeting font", ["Skin.SelectBool(31798,31769|,%s)" % ",".join("%d|mq_%s_font_%s" % (f[2], k, f[0]) for f in FONTS)],
                          "$VAR[MqFont_%s]" % k))
            ch.append(btn(nid(), "- Greeting colour", ["Skin.SetColor(mq_%s_greetcolor,31799)" % k], "$VAR[MqVal_greetcolor_%s]" % k))
            ch.append(btn(nid(), "Highlight colour", ["Skin.SetColor(mq_%s_accent,31799)" % k], "$VAR[MqVal_accent_%s]" % k))
            ch.append(btn(nid(), "Menu icon", ["Skin.SetImage(mq_%s_icon)" % k], "$VAR[MqVal_icon_%s]" % k))
            ch.append(btn(nid(), "- Icon animation", ["Skin.SelectBool(31808,31769|,%s)" % ",".join("%d|mq_%s_anim_%s" % (sid, k, an) for an, sid in ANIMS)],
                          "$VAR[MqAnim_%s]" % k))
            ch.append(btn(nid(), "Backgrounds folder", ["Skin.SetPath(mq_bg_%s)" % k], "$VAR[MqVal_bg_%s]" % k))
            ch.append(btn(nid(), "Effect", ["Skin.SelectBool(31809,31769|,%s)" % ",".join("%d|mq_%s_fx_%s" % (sid, k, fx) for fx, sid in EFFECTS)],
                          "$VAR[MqFx_%s]" % k))
            ch.append(btn(nid(), "- Fog density (when the effect is fog)",
                          ["Skin.SelectBool(31710,31711|mq_fog_light,31712|,31713|mq_fog_heavy)"], "$VAR[MqFogDensityLabelVar]"))
        ch.append(head(nid(), "ROWS ON THE HOME SCREEN"))
        if k in BUILTIN:
            ch.append(radio(nid(), "Built-in rows for this holiday", "!Skin.HasSetting(mq_%s_nobuiltin)" % k, "Skin.ToggleSetting(mq_%s_nobuiltin)" % k))
        for n in range(1, SLOTS + 1):
            p = "mq_%s_%d" % (k, n)
            ch.append(btn(nid(), "$VAR[MqSlotSettingLabel_%s_%d]" % (k, n), ["Skin.SetString(%s_label)" % p], "Set title"))
            ch.append(btn(nid(), "- Choose a video smart playlist", ["Skin.SetFile(%s_path,.xsp|.m3u,special://videoplaylists/)" % p],
                          "$INFO[Skin.String(%s_path)]" % p))
            ch.append(btn(nid(), "- Choose a music smart playlist", ["Skin.SetFile(%s_path,.xsp|.m3u,special://musicplaylists/)" % p,
                                                                     "Skin.SetBool(%s_square)" % p, "Skin.Reset(%s_landscape)" % p]))
            ch.append(btn(nid(), "- Type a path (plugin://, videodb://, library node...)", ["Skin.SetString(%s_path)" % p]))
            ch.append(btn(nid(), "- $LOCALIZE[31714]", ["Skin.SelectBool(31714,31715|,31716|%s_landscape,31717|%s_square)" % (p, p)],
                          "$VAR[MqSlotStyleLabel_%s_%d]" % (k, n)))
            ch.append(btn(nid(), "- Clear this row", ["Skin.Reset(%s_path)" % p, "Skin.Reset(%s_label)" % p, "Skin.Reset(%s_landscape)" % p,
                                                       "Skin.Reset(%s_square)" % p]))
        if k != "everyday":
            resets = ["Skin.Reset(mq_%s_%s)" % (k, x) for x in ("off", "greeting", "kicker", "greetcolor", "accent", "icon", "nobuiltin")]
            resets += ["Skin.Reset(mq_bg_%s)" % k]
            resets += ["Skin.Reset(mq_%s_font_%s)" % (k, f[0]) for f in FONTS]
            resets += ["Skin.Reset(mq_%s_fx_%s)" % (k, fx) for fx, _ in EFFECTS]
            resets += ["Skin.Reset(mq_%s_anim_%s)" % (k, an) for an, _ in ANIMS]
            if k in FIXED:
                resets += ["Skin.SetString(mq_%s_start,%s)" % (k, FIXED[k][0]), "Skin.SetString(mq_%s_end,%s)" % (k, FIXED[k][1])]
            elif custom:
                resets += ["Skin.Reset(mq_%s_%s)" % (k, x) for x in ("name", "start", "end", "message")]
                for n in range(1, SLOTS + 1):
                    resets += ["Skin.Reset(mq_%s_%d_%s)" % (k, n, x) for x in ("path", "label", "landscape", "square")]
            else:
                resets += ["Skin.Reset(mq_%s_before_%d)" % (k, n) for n, _ in BEFORE_OPTS]
                resets += ["Skin.Reset(mq_%s_after_%d)" % (k, n) for n, _ in AFTER_OPTS]
            ch.append(head(nid(), ""))
            ch.append(btn(nid(), "[COLOR FFE8786B]Delete this holiday[/COLOR]" if custom else "[COLOR FFE8786B]Reset this holiday to its defaults[/COLOR]",
                          resets))
        groups.append("""	<control type="grouplist" id="{gid}">
		<left>40</left><top>120</top><width>1360</width><height>760</height>
		<onup>{gid}</onup><ondown>{gid}</ondown><onleft>noop</onleft><onright>noop</onright>
		<visible>String.IsEqual(Window(home).Property(mq_edit),{key})</visible>
{ch}
	</control>""".format(gid=gid, key=k, ch="\n".join(ch)))
    focus = "\n".join('\t<onload condition="String.IsEqual(Window(home).Property(mq_edit),%s)">SetFocus(%d)</onload>' % (s_["key"], 3000 + gi * 100)
                      for gi, s_ in enumerate(SLOT_SEASONS))
    inits = "\n".join("\t<onload condition=\"String.IsEmpty(Skin.String(mq_%s_%s))\">Skin.SetString(mq_%s_%s,%s)</onload>" % (k, w, k, w, v_)
                      for k, (st, en, _) in FIXED.items() for w, v_ in (("start", st), ("end", en)))
    return """<?xml version="1.0" encoding="UTF-8"?>
<!-- Holiday settings page. Generated by gen_xml.py. -->
<window type="dialog" id="1190">
{inits}
{focus}
	<include>Animation_DialogPopupOpenClose</include>
	<depth>DepthDialog+</depth>
	<controls>
		<control type="image"><left>-100</left><top>-100</top><width>2120</width><height>1280</height><texture colordiffuse="C0000000">colors/black.png</texture></control>
		<control type="group">
			<centerleft>50%</centerleft><centertop>50%</centertop><width>1440</width><height>920</height>
			<control type="image"><left>0</left><top>0</top><width>1440</width><height>920</height><texture colordiffuse="FF1A1A1A" border="16">marquee/rounded_fill.png</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1440</width><height>90</height><texture colordiffuse="$VAR[MqAccentEditVar]" border="16">marquee/rounded_fill.png</texture></control>
			<control type="label"><left>40</left><top>0</top><width>1200</width><height>90</height><aligny>center</aligny><font>font32_title</font>
				<label>$VAR[MqEditTitleVar]</label></control>
			<control type="label"><right>40</right><top>0</top><width>300</width><height>90</height><align>right</align><aligny>center</aligny><font>font12</font>
				<textcolor>FFE0E0E0</textcolor><label>Back to close</label></control>
{groups}
		</control>
	</controls>
</window>
""".format(inits=inits, focus=focus, groups="\n".join(groups))


# --------------------------------------------------------------- playlists
def xsp(ptype, name, rules, order="random", limit=60, match="one"):
    r = []
    for field, op, values in rules:
        vals = "".join("<value>%s</value>" % escape(v) for v in values)
        r.append('    <rule field="%s" operator="%s">%s</rule>' % (field, op, vals))
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<smartplaylist type="{t}">
    <name>{n}</name>
    <match>{m}</match>
{r}
    <limit>{l}</limit>
    <order direction="ascending">{o}</order>
</smartplaylist>
""".format(t=ptype, n=escape(name), m=match, r="\n".join(r), l=limit, o=order)


PLAYLISTS = {
    "mq_halloween_spooky.xsp": xsp("movies", "Spooky Season", [
        ("tag", "is", ["halloween", "Halloween"]),
        ("title", "contains", ["Halloween", "Hocus Pocus", "Trick 'r Treat", "Pumpkin", "Haunted", "Ghost", "Witch", "Vampire", "Zombie", "Monster"]),
        ("plot", "contains", ["Halloween"]),
    ]),
    "mq_halloween_horror.xsp": xsp("movies", "Horror Movies", [("genre", "is", ["Horror"])]),
    "mq_halloween_tv.xsp": xsp("tvshows", "Creepy TV", [("genre", "is", ["Horror", "Sci-Fi & Fantasy"])], limit=40),
    "mq_halloween_episodes.xsp": xsp("episodes", "Halloween Episodes", [
        ("title", "contains", ["Halloween", "Treehouse of Horror", "Trick or Treat", "Haunted"]),
        ("plot", "contains", ["Halloween"]),
    ], limit=60),
    "mq_thanksgiving_movies.xsp": xsp("movies", "Thanksgiving Favorites", [
        ("tag", "is", ["thanksgiving", "Thanksgiving"]),
        ("title", "contains", ["Thanksgiving", "Turkey", "Planes, Trains"]),
        ("plot", "contains", ["Thanksgiving"]),
    ]),
    "mq_thanksgiving_episodes.xsp": xsp("episodes", "Thanksgiving Episodes", [
        ("title", "contains", ["Thanksgiving", "Turkey", "Pilgrim"]),
        ("plot", "contains", ["Thanksgiving"]),
    ]),
    "mq_thanksgiving_family.xsp": xsp("movies", "Family Movie Night", [("genre", "is", ["Family", "Animation"])], limit=40),
    "mq_christmas_movies.xsp": xsp("movies", "Christmas Movies", [
        ("tag", "is", ["christmas", "Christmas", "xmas"]),
        ("title", "contains", ["Christmas", "Xmas", "Santa", "Grinch", "Elf", "Home Alone", "Polar Express", "Noel", "Holiday", "Scrooge", "Krampus"]),
        ("plot", "contains", ["Christmas", "Santa Claus"]),
    ]),
    "mq_christmas_episodes.xsp": xsp("episodes", "Holiday Episodes", [
        ("title", "contains", ["Christmas", "Xmas", "Santa", "Holiday", "Noel", "Mistletoe"]),
        ("plot", "contains", ["Christmas"]),
    ]),
    "mq_christmas_family.xsp": xsp("movies", "Family Movie Night", [("genre", "is", ["Family", "Animation"])], limit=40),
    "mq_mlk_civilrights.xsp": xsp("movies", "Civil Rights Stories", [
        ("tag", "is", ["civil rights", "Civil Rights", "black history", "Black History", "mlk"]),
        ("title", "contains", ["Selma", "Martin Luther King", "Hidden Figures", "Harriet", "Malcolm X", "The Help",
                               "Mississippi Burning", "Glory Road", "Remember the Titans", "Just Mercy"]),
        ("plot", "contains", ["civil rights", "Civil Rights", "Martin Luther King", "segregation"]),
    ]),
    "mq_mlk_docs.xsp": xsp("movies", "Documentaries", [("genre", "is", ["Documentary"])], limit=40),
    "mq_presidents_movies.xsp": xsp("movies", "Presidents & Politics", [
        ("tag", "is", ["president", "presidents", "politics", "Politics"]),
        ("title", "contains", ["President", "White House", "Lincoln", "Washington", "Kennedy", "JFK", "Nixon",
                               "Air Force One", "Truman", "Jefferson", "Mr. Smith Goes"]),
        ("plot", "contains", ["President of the United States", "the White House"]),
    ]),
    "mq_presidents_tv.xsp": xsp("tvshows", "Political TV", [("genre", "is", ["War & Politics", "Politics"])], limit=40),
    "mq_mothers_movies.xsp": xsp("movies", "Movies for Mom", [
        ("tag", "is", ["mom", "mothers day", "Mother's Day", "mother"]),
        ("title", "contains", ["Mother", "Mamma Mia", "Mommy", "Steel Magnolias", "Little Women"]),
        ("plot", "contains", ["Mother's Day"]),
    ]),
    "mq_mothers_episodes.xsp": xsp("episodes", "Mother's Day Episodes", [
        ("title", "contains", ["Mother's Day", "Mother"]),
        ("plot", "contains", ["Mother's Day"]),
    ]),
    "mq_juneteenth_freedom.xsp": xsp("movies", "Stories of Freedom", [
        ("tag", "is", ["juneteenth", "Juneteenth", "black history", "Black History", "freedom"]),
        ("title", "contains", ["Juneteenth", "Harriet", "12 Years a Slave", "Freedom", "Emancipation", "Amistad", "Glory",
                               "Roots"]),
        ("plot", "contains", ["Juneteenth", "slavery", "emancipation", "Underground Railroad"]),
    ]),
    "mq_fathers_movies.xsp": xsp("movies", "Movies for Dad", [
        ("tag", "is", ["dad", "fathers day", "Father's Day", "father"]),
        ("title", "contains", ["Father", "Daddy", "Big Fish", "Field of Dreams"]),
        ("plot", "contains", ["Father's Day"]),
    ]),
    "mq_fathers_action.xsp": xsp("movies", "Action Night", [("genre", "is", ["Action"])], limit=40),
    "mq_fathers_episodes.xsp": xsp("episodes", "Father's Day Episodes", [
        ("title", "contains", ["Father's Day", "Father"]),
        ("plot", "contains", ["Father's Day"]),
    ]),
    "mq_labor_summer.xsp": xsp("movies", "Summer's Last Hurrah", [
        ("tag", "is", ["summer", "Summer", "labor day", "Labor Day"]),
        ("title", "contains", ["Summer", "Beach", "Vacation", "Road Trip", "Barbecue", "Camp Nowhere", "Wet Hot"]),
        ("plot", "contains", ["Labor Day", "summer vacation"]),
    ]),
    "mq_labor_workers.xsp": xsp("movies", "Working-Class Heroes", [
        ("tag", "is", ["union", "workers", "blue collar", "labor"]),
        ("title", "contains", ["Norma Rae", "Factory", "Working Girl", "9 to 5", "Office Space", "Matewan",
                               "On the Waterfront", "Erin Brockovich", "Silkwood", "Kinky Boots"]),
        ("plot", "contains", ["labor union", "workers", "factory"]),
    ]),
    "mq_groundhog_movie.xsp": xsp("movies", "Groundhog Day", [
        ("title", "contains", ["Groundhog Day"]),
        ("tag", "is", ["groundhog", "Groundhog", "groundhog day"]),
    ]),
    "mq_groundhog_loops.xsp": xsp("movies", "Stuck in a Time Loop", [
        ("tag", "is", ["time loop", "Time Loop", "groundhog"]),
        ("title", "contains", ["Groundhog Day", "Palm Springs", "Happy Death Day", "Edge of Tomorrow", "Source Code",
                               "Before I Fall", "Map of Tiny Perfect Things", "Boss Level", "Naked", "12:01", "Triangle",
                               "Run Lola Run", "About Time", "Repeaters"]),
        ("plot", "contains", ["time loop", "same day over", "relive the same day", "reliving the same day"]),
    ]),
    "mq_groundhog_murray.xsp": xsp("movies", "Bill Murray Favorites", [("actor", "is", ["Bill Murray"])], limit=40),
    "mq_groundhog_episodes.xsp": xsp("episodes", "Groundhog Day Episodes", [
        ("title", "contains", ["Groundhog", "Time Loop", "Same Day", "Repeat", "Deja Vu", "Again and Again"]),
        ("plot", "contains", ["Groundhog Day", "time loop", "same day over"]),
    ]),
    "mq_pirate_movies.xsp": xsp("movies", "Pirate Adventures", [
        ("tag", "is", ["pirate", "Pirate", "pirates", "Pirates"]),
        ("title", "contains", ["Pirate", "Treasure", "Buccaneer", "Captain Blood", "Hook", "Sinbad", "Black Sails", "Peter Pan",
                               "Goonies", "Cutthroat Island", "Swashbuckler", "Blackbeard", "Captain Hook"]),
        ("plot", "contains", ["pirate", "pirates"]),
    ]),
    "mq_pirate_episodes.xsp": xsp("episodes", "Pirate Episodes", [
        ("title", "contains", ["Pirate", "Treasure", "Talk Like a Pirate", "Ahoy", "Buccaneer"]),
        ("plot", "contains", ["pirate"]),
    ]),
    "mq_pirate_adventure.xsp": xsp("movies", "Swashbucklers & Adventure", [("genre", "is", ["Adventure"])], limit=40),
    "mq_columbus_sea.xsp": xsp("movies", "Explorers & the Open Sea", [
        ("tag", "is", ["explorer", "exploration", "ocean", "sea", "sailing"]),
        ("title", "contains", ["Columbus", "1492", "Explorer", "Voyage", "Ocean", "Expedition", "Shipwreck",
                               "Master and Commander", "Mutiny", "Kon-Tiki", "Endurance", "Moana"]),
        ("plot", "contains", ["voyage", "explorer", "expedition", "the New World"]),
    ]),
    "mq_newyear_movies.xsp": xsp("movies", "New Year's Eve Movies", [
        ("tag", "is", ["new year", "New Year", "new years eve", "New Year's Eve"]),
        ("title", "contains", ["New Year", "Midnight", "Countdown", "Auld Lang Syne"]),
        ("plot", "contains", ["New Year's Eve", "New Year's Day"]),
    ]),
    "mq_newyear_episodes.xsp": xsp("episodes", "New Year's Episodes", [
        ("title", "contains", ["New Year", "Countdown", "Midnight", "Resolution"]),
        ("plot", "contains", ["New Year's Eve", "New Year's"]),
    ]),
    "mq_newyear_comedies.xsp": xsp("movies", "Party Comedies", [("genre", "is", ["Comedy"])], limit=40),
    "mq_valentine_romance.xsp": xsp("movies", "Romance Movies", [
        ("genre", "is", ["Romance"]),
        ("tag", "is", ["valentine", "Valentine", "romance", "date night"]),
    ]),
    "mq_valentine_romcoms.xsp": xsp("movies", "Romantic Comedies", [
        ("genre", "is", ["Romance"]),
        ("genre", "is", ["Comedy"]),
    ], match="all"),
    "mq_valentine_episodes.xsp": xsp("episodes", "Valentine's Episodes", [
        ("title", "contains", ["Valentine", "Cupid", "Be Mine", "Love Day"]),
        ("plot", "contains", ["Valentine"]),
    ]),
    "mq_stpatrick_irish.xsp": xsp("movies", "Luck of the Irish", [
        ("tag", "is", ["irish", "Irish", "st patricks day", "St. Patrick's Day", "ireland", "Ireland"]),
        ("title", "contains", ["Irish", "Ireland", "Dublin", "Leprechaun", "Shamrock", "Celtic", "Luck of the", "Banshees"]),
        ("plot", "contains", ["Ireland", "St. Patrick"]),
    ]),
    "mq_stpatrick_episodes.xsp": xsp("episodes", "St. Patrick's Day Episodes", [
        ("title", "contains", ["St. Patrick", "Leprechaun", "Irish", "Shamrock", "Pot of Gold"]),
        ("plot", "contains", ["St. Patrick"]),
    ]),
    "mq_easter_movies.xsp": xsp("movies", "Easter Movies", [
        ("tag", "is", ["easter", "Easter"]),
        ("title", "contains", ["Easter", "Bunny", "Peter Rabbit", "Peter Cottontail"]),
        ("plot", "contains", ["Easter"]),
    ]),
    "mq_easter_faith.xsp": xsp("movies", "The Story of Jesus", [
        ("tag", "is", ["faith", "Faith", "christian", "Christian", "bible", "Bible"]),
        ("title", "contains", ["Jesus", "Passion of the Christ", "The Passion", "Risen", "Resurrection", "King of Kings", "Son of God",
                               "Ben-Hur", "Ten Commandments", "Prince of Egypt", "Greatest Story Ever Told", "The Chosen"]),
        ("plot", "contains", ["Jesus"]),
    ]),
    "mq_easter_episodes.xsp": xsp("episodes", "Easter Episodes", [
        ("title", "contains", ["Easter", "Bunny", "Egg Hunt"]),
        ("plot", "contains", ["Easter"]),
    ]),
    "mq_easter_family.xsp": xsp("movies", "Family Movie Night", [("genre", "is", ["Family", "Animation"])], limit=40),
    "mq_memorial_war.xsp": xsp("movies", "War Movies", [
        ("genre", "is", ["War"]),
        ("tag", "is", ["military", "Military", "memorial day", "Memorial Day", "war", "War"]),
    ]),
    "mq_memorial_tv.xsp": xsp("tvshows", "Military & War TV", [
        ("genre", "is", ["War", "War & Politics", "Military"]),
    ], limit=40),
    "mq_memorial_history.xsp": xsp("movies", "Based on True History", [
        ("genre", "is", ["History"]),
    ], limit=40),
    "mq_july4_patriotic.xsp": xsp("movies", "Patriotic Picks", [
        ("tag", "is", ["patriotic", "Patriotic", "4th of july", "4th of July", "fourth of july", "independence day", "Independence Day"]),
        ("title", "contains", ["America", "Independence", "Patriot", "Liberty", "Freedom", "Yankee Doodle", "1776", "Lincoln",
                               "Glory", "Fourth of July", "4th of July", "Uncle Sam", "Star-Spangled", "Old Glory"]),
        ("plot", "contains", ["Fourth of July", "4th of July", "Independence Day", "Founding Fathers"]),
    ]),
    "mq_july4_episodes.xsp": xsp("episodes", "Independence Day Episodes", [
        ("title", "contains", ["Fourth of July", "4th of July", "Independence Day", "July 4", "Fireworks", "Firecracker"]),
        ("plot", "contains", ["Fourth of July", "4th of July", "fireworks"]),
    ]),
    "mq_july4_history.xsp": xsp("movies", "American History", [
        ("genre", "is", ["History", "Western"]),
    ], limit=40),
}


def main():
    inc = includes_file().replace("</includes>\n", "\n".join(extra_includes()) + "\n</includes>\n")
    open(os.path.join(XML, "Includes_Marquee.xml"), "w").write(inc)
    open(os.path.join(XML, "Home.xml"), "w").write(home_xml())
    open(os.path.join(XML, "Includes_MarqueeSettings.xml"), "w").write(settings_panels())
    open(os.path.join(XML, "Custom_1190_MqHoliday.xml"), "w").write(holiday_dialog())
    for name, body in PLAYLISTS.items():
        open(os.path.join(SKIN, "playlists", name), "w").write(body)
    print("xml generated")


main()
