import db

FIELDS = db.AnimeDB.fields
ENTRY = """Series: {series}
Last: {last_watched}
Total: {total}
Done: {done}
Type: {type}
Season: {season}
Rating: {rating}
Airing Days: {airing_days}
Ep. Notes: {ep_notes}
Notes: {notes}

"""
SEL_ENTRY = """a - Series: {series}
b - Last: {last_watched}
c - Total: {total}
d - Done: {done}
e - Type: {type}
f - Season: {season}
g - Rating: {rating}
h - Airing Days: {airing_days}
i - Ep. Notes: {ep_notes}
j - Notes: {notes}

"""
PROMPT = ">>> "
