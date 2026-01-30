from icalendar import Calendar, Event
import pandas as pd

df = pd.read_csv("final.csv")
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])


def export_to_ical(df, filename="mon_edt.ics"):
    cal = Calendar()
    cal.add("prodid", "-//Mon Projet Parsing EDT//mxm.dk//")
    cal.add("version", "2.0")

    for index, row in df.iterrows():
        event = Event()
        event.add("summary", row["cours"])
        event.add("dtstart", row["start"])
        event.add("dtend", row["end"])
        description = f"Prof(s): {row['prof']}"
        event.add("description", description)
        cal.add_component(event)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())

    print(f"Calendrier exporté avec succès : {filename}")


export_to_ical(df)
