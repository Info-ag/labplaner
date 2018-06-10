"""
Dear Python,

I would like to find the best dates for a number of events. You can get
those events from the db (from app import db). Could you please compare
the dates of those events and check if there are any conflicts and if
possible, resolve those conflicts. Just set the date variable of the
events accordingly.

Thanks

jnsd
"""

from itertools import islice

from app import db

from models.event import Event
from models.date import Date
from models.user import User


"""
--------------
Definitions:
--------------

event_i := Event i
z_i     := Date of event i
z_max_i := Date of event i with the most users available
n       := Intersection of z_n and z_m
"""


def do_your_work():
    events = Event.query.all()
    while True:
        best_dates = []
        for event_i in events:
            if len(event_i.dates) > 0:
                z_max_i = best_date_for_event(event_i)
                best_dates.append(z_max_i)
                # set the date so we do not have to do it later
                event_i.date = z_max_i.day

        conflict, pos = has_conflicts(best_dates)
        if not conflict:
            break

        print(f"Conflict: {conflict}")

        # damn
        # this is where the work begins...
        # event_i.date is now invalid!
        z_max_n: Date = best_dates[pos[0]]
        z_max_m: Date = best_dates[pos[1]]

        users = []
        for user_n in z_max_n.users:
            for user_m in z_max_m.users:
                if user_n is user_m and user_n not in users:
                    print(user_n)
                    users.append(user_n)

        if len(users) > 1:
            u_remove = list(chunks(users, int(len(users)/2)))
            for u_n in list(u_remove[0]):
                z_max_n.users.remove(u_n)
            for u_m in list(u_remove[1]):
                z_max_m.users.remove(u_m)
        elif len(users) != 0: 
            z_max_n.users.remove(users[0])
        else:
            break


    db.session.commit()


def best_date_for_event(event: Event):
    """
    Get the best date for an event.
    :param event: Any event object. It has to contain a list of dates
    :return: The date object with the most users
    """
    return max(event.dates,
               # compare length of users
               key=lambda d: len(
                   # filter all users that participate at this event
                   list(filter(lambda u: event.ag in u.ags, d.users))
               ))


def has_conflicts(dates):
    """
    Verifies whether there are any conflicts in a set of dates.
    This function compares each and every date to the others and compares
    the users of such dates. If they share any user, a conflict is reported.
    :param dates: A list of dates with users
    :return: True if any event shares a user with another event.
    """
    # TODO optimize. Some are still checked twice
    for z_max_n in dates:
        for z_max_m in dates:
            if z_max_m is z_max_n:
                # skip if dates are the same anyway
                continue

            z_max_n: Date
            z_max_m: Date
            # update the result
            if not set(z_max_n.users).isdisjoint(z_max_m.users):
                return True, (dates.index(z_max_n), dates.index(z_max_m))

    return True, (0, 0)


def chunks(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())





def alg(ev1, ev2):
    """
    :param ev1 is an event_id
    :param ev2 is an event_id
    """
    ev1_user_count = []
    users_dates = db.session.query(UserDates).filter_by(event_id=ev1).all()
    for user_date in users_dates:
        if user_date.date_id in ev1_user_count:
            ev1_user_count[user_date.date_id] += 1
        else:
            ev1_user_count[user_date.date_id] = 1

    
def best_date_for_event(event_id):
     """
     :param event_id specific id for an event
     """
     dic = {}
     users_dates = db.session.query(UserDates).filter_by(event_id=event_id).all()
     for user_date in users_dates:
         if user_date.date_id in dic:
             dic[user_date.date_id] += 1
         else:
             dic[user_date.date_id] = 1

    return max(dic)
    



