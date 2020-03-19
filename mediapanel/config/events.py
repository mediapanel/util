"""
Events device configuration.
"""
from datetime import datetime
from typing import List, Tuple

from .section import Config


class Event:
    __slots__ = ["name", "enabled"]

    def __init__(self, event_name: str, enabled=True):
        self.name = event_name
        self.enabled = enabled


class Person:
    """
    A person that can have Events.
    """

    __slots__ = ["name", "events"]

    def __init__(self, person_name: str,
                 events: List[Tuple[Event, datetime]] = None):
        self.name = person_name
        self.events = events if events is not None else []

    def add_event(self, event: Event, date: datetime):
        self.events.append((event, date.date()))

    def remove_event(event: Event, date: datetime = None):
        if date is not None:
            self.events.remove((event, date.date()))
        else:
            self.events = [e for e in self.events if e[0] != event]


class EventList:
    """
    A list of people and events for an event category.
    """

    __slots__ = ["event", "events"]

    def __init__(self, event: Event,
                 events: List[Tuple[Person, datetime]]=None):
        self.event = event
        self.events = events if events is not None else []

    def add_event(self, person: Person, date: datetime):
        self.events.append((person, date.date()))

    def remove_event(person: Person, date: datetime = None):
        if date is not None:
            self.events.remove((person, date.date()))
        else:
            self.events = [e for e in self.events if e[0] != person]


class EventsConfig(Config):
    """
    Information about configured events and people who have events.
    """

    __slots__ = ["events", "people"]

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.events = config["events"]
        self.people = config["people"]


    @staticmethod
    def from_v6_values(data):
        event_categories = {}
        event_lists = {}
        for event in data["EVENTS"]:
            name = event["NAME"]
            event_obj = Event(name, event["STATUS"] == "on")
            event_categories[name] = event_obj
            event_lists[name] = EventList(event_obj)

        people = []
        for person in data["PEOPLE"]:
            person_obj = Person(person["NAME"])
            for event_name, event_dates in person["EVENTS"].items():
                event_obj = event_categories[event_name]
                for date in event_dates:
                    dt = datetime.strptime(date, "%m/%d/%Y")
                    person_obj.add_event(event_obj, dt)
                    event_lists[event_name].add_event(person_obj, dt)
            people.append(person_obj)

        return {
            "events": event_lists,
            "people": people,
        }

    def to_v6_values(self):
        people_list = []
        for person in self.people:
            event_categories = {}
            for event, date in person.events:
                date_str = date.strftime("%m/%d/%Y")
                if event.name not in event_categories:
                    event_categories[event.name] = [date_str]
                else:
                    event_categories[event.name].append(date_str)
            people_list.append({"NAME": person.name,
                                "EVENTS": event_categories})

        return {
            "PEOPLE": people_list,
            "EVENTS": [{"NAME": name,
                        "STATUS": "on" if e.event.enabled else "off"}
                       for name, e in self.events.items()],
        }
