""" Module to create fixture events. """

from datetime import datetime, date, timedelta
from functools import wraps

import pytest

from collectives.models import db, ActivityType, EventType, Event, EventTag, EventStatus
from collectives.models import Registration, RegistrationLevels, RegistrationStatus
from collectives.models import Question, QuestionType, QuestionAnswer

from tests.fixtures import payment

# pylint: disable=unused-argument, redefined-outer-name


def inject_fixture(name, identifier):
    """Inject a new event into fixtures.

    :param string name: Fixture name
    :param string identifier: Any string. It will be add to event title"""
    globals()[name] = generate_event(identifier)


def generate_event(identifier):
    """Creates a new fixture event.

    :param string identifier: Any string. It will be add to event title"""

    @wraps(identifier)
    @pytest.fixture
    def event(app, leader_user):
        """:returns: A basic event."""

        now = date.today()

        event = Event()
        event.title = f"New collective {identifier}"
        event.start = now + timedelta(days=10)
        event.end = now + timedelta(days=10)
        event.registration_open_time = now - timedelta(days=5)
        event.registration_close_time = now + timedelta(days=5)
        event.description = """**Lorem ipsum** dolor sit amet, consectetur
        adipiscing elit. Quisque mollis vitae diam at hendrerit.
        _Aenean cursus sem vitae condimentum imperdiet._ Sed nec ligula lectus.
        Vivamus vehicula varius turpis, eget accumsan libero. Integer eleifend
        aliquet leo, in malesuada risus tempus id. Suspendisse pharetra iaculis
        nunc vitae sollicitudin. Donec eu accumsan ipsum. Pellentesque
        habitant morbi tristique senectus et netus et malesuada fames ac
        turpis egestas. Morbi ut urna eget eros pellentesque molestie. Donec
        auctor sapien id erat congue, vel molestie sapien varius. Fusce vitae
        iaculis tellus, nec mollis turpis."""
        event.set_rendered_description(event.description)
        event.num_online_slots = 1

        alpinisme = ActivityType.query.filter_by(name="Alpinisme").first()
        event.activity_types.append(alpinisme)

        event_type = EventType.query.filter_by(name="Collective").first()
        event.event_type = event_type

        event.leaders = [leader_user]
        event.main_leader = leader_user

        db.session.add(event)
        db.session.commit()

        return event

    return event


for i in range(1, 10):
    inject_fixture(f"event{i}", i)
inject_fixture("event", "")

inject_fixture("prototype_past_event", "passé")


@pytest.fixture
def past_event(prototype_past_event):
    """:returns: A past event"""
    now = date.today()
    prototype_past_event.start = now - timedelta(days=10)
    prototype_past_event.end = now - timedelta(days=10)
    prototype_past_event.registration_open_time = now - timedelta(days=25)
    prototype_past_event.registration_close_time = now - timedelta(days=11)

    db.session.add(prototype_past_event)
    db.session.commit()
    return prototype_past_event


inject_fixture("prototype_tagged_event", "passé")


@pytest.fixture
def tagged_event(prototype_tagged_event):
    """:returns: A tagged event as Handicaf."""
    handicaf_tag = EventTag(6)
    prototype_tagged_event.tag_refs.append(handicaf_tag)
    db.session.add(prototype_tagged_event)
    db.session.commit()
    return prototype_tagged_event


inject_fixture("prototype_cancelled_event", "annulé")


@pytest.fixture
def cancelled_event(prototype_cancelled_event):
    """:returns: A cancelled event"""
    prototype_cancelled_event.status = EventStatus.Cancelled
    db.session.add(prototype_cancelled_event)
    db.session.commit()
    return prototype_cancelled_event


inject_fixture("prototype_draft_event", "brouillon")


@pytest.fixture
def draft_event(prototype_draft_event):
    """:returns: An event in draft status"""
    prototype_draft_event.status = EventStatus.Pending
    db.session.add(prototype_draft_event)
    db.session.commit()
    return prototype_draft_event


inject_fixture("prototype_paying_event", "paying")


@pytest.fixture
def paying_event(prototype_paying_event):
    """:returns: An event with associated payment_item and prices"""

    prototype_paying_event.payment_items.append(
        payment.payment_item(prototype_paying_event)
    )
    db.session.add(prototype_paying_event)
    db.session.commit()
    return prototype_paying_event


inject_fixture("prototype_disabled_paying_event", "disabled paying")


@pytest.fixture
def disabled_paying_event(prototype_disabled_paying_event):
    """:returns: An event in draft status"""

    prototype_disabled_paying_event.payment_items.append(
        payment.payment_item(prototype_disabled_paying_event)
    )
    db.session.add(prototype_disabled_paying_event)
    db.session.commit()
    return prototype_disabled_paying_event


inject_fixture("prototype_youth_event", "youth")


@pytest.fixture
def youth_event(prototype_youth_event: Event):
    """:returns: An event in with registration restricted to youths"""

    event_type = EventType.query.filter_by(name="Jeunes").first()
    prototype_youth_event.event_type = event_type

    db.session.add(prototype_youth_event)
    db.session.commit()
    return prototype_youth_event


inject_fixture("prototype_free_paying_event", "disabled paying")


@pytest.fixture
def free_paying_event(prototype_free_paying_event):
    """:returns: An event in draft status"""

    prototype_free_paying_event.payment_items.append(payment.free_payment_item())
    db.session.add(prototype_free_paying_event)
    db.session.commit()
    return prototype_free_paying_event


@pytest.fixture
def event1_with_reg(event1, user1, user2, user3, user4):
    """:returns: The fixture `event1`, with 4 users registered.
    :rtype: :py:class:`collectives.models.event.Event`"""
    for user in [user1, user2, user3, user4]:
        event1.registrations.append(
            Registration(
                user_id=user.id,
                status=RegistrationStatus.Active,
                level=RegistrationLevels.Normal,
                is_self=True,
            )
        )
    return event1


@pytest.fixture
def event1_with_reg_waiting_list(event1, user1, user2, user3, user4):
    """:returns: The fixture `event1`, with 4 users registered, and 2 in waiting_list.
    :rtype: :py:class:`collectives.models.event.Event`"""
    event1.num_online_slots = 2
    for user in [(user1, True), (user2, True), (user3, False), (user4, False)]:
        status = RegistrationStatus.Active if user[1] else RegistrationStatus.Waiting
        event1.registrations.append(
            Registration(
                user_id=user[0].id,
                status=status,
                level=RegistrationLevels.Normal,
                is_self=True,
            )
        )
    return event1


@pytest.fixture
def event1_with_questions(event1_with_reg):
    """:returns: An event with user registrations and associated questions"""

    event1_with_reg.questions.append(
        Question(
            title="Question",
            description="",
            choices="A\nB\nC\n",
            question_type=QuestionType.MultipleChoices,
            enabled=True,
            required=True,
        )
    )
    event1_with_reg.questions.append(
        Question(
            title="Autre question",
            description="",
            choices="",
            question_type=QuestionType.Text,
            enabled=True,
            required=True,
        )
    )
    db.session.add(event1_with_reg)
    db.session.commit()
    return event1_with_reg


@pytest.fixture
def event1_with_answers(event1_with_questions):
    """:returns: An event with answered questions"""

    q1 = event1_with_questions.questions[0]
    u1 = event1_with_questions.registrations[0].user
    q1.answers.append(QuestionAnswer(user=u1, value="B"))

    db.session.add(q1)
    db.session.commit()
    return event1_with_questions


inject_fixture("prototype_event_in_less_than_48h", "happens in less than 48 hours")


@pytest.fixture
def event_in_less_than_48h_with_reg(
    prototype_event_in_less_than_48h,
    user_with_no_warning_badge,
    user_with_valid_first_warning_badge,
    user_with_expired_first_warning_badge,
    user_with_valid_second_warning_badge,
    user_with_expired_second_warning_badge,
    user_with_expired_banned_badge,
):  # pylint: disable=too-many-arguments
    """
    Returns an event in less than 48 hours
    with registrations for specified users.
    """

    prototype_event_in_less_than_48h.registration_open_time = (
        datetime.now() - timedelta(hours=10)
    )
    prototype_event_in_less_than_48h.registration_close_time = (
        datetime.now() + timedelta(hours=2)
    )
    prototype_event_in_less_than_48h.start = datetime.now() + timedelta(hours=3)
    prototype_event_in_less_than_48h.end = datetime.now() + timedelta(hours=4)
    prototype_event_in_less_than_48h.num_online_slots = 9

    for user in [
        user_with_no_warning_badge,
        user_with_valid_first_warning_badge,
        user_with_expired_first_warning_badge,
        user_with_valid_second_warning_badge,
        user_with_expired_second_warning_badge,
        user_with_expired_banned_badge,
    ]:
        prototype_event_in_less_than_48h.registrations.append(
            Registration(
                user_id=user.id,
                status=RegistrationStatus.Active,
                level=RegistrationLevels.Normal,
                is_self=True,
            )
        )

    db.session.add(prototype_event_in_less_than_48h)
    db.session.commit()

    return prototype_event_in_less_than_48h


@pytest.fixture
def event_in_less_than_48h(prototype_event_in_less_than_48h):
    """Fixture for an event starting in less than 48 hours."""

    prototype_event_in_less_than_48h.registration_open_time = (
        datetime.now() - timedelta(hours=10)
    )
    prototype_event_in_less_than_48h.registration_close_time = (
        datetime.now() + timedelta(hours=2)
    )
    prototype_event_in_less_than_48h.start = datetime.now() + timedelta(hours=3)
    prototype_event_in_less_than_48h.end = datetime.now() + timedelta(hours=4)

    prototype_event_in_less_than_48h.num_online_slots = 9

    db.session.add(prototype_event_in_less_than_48h)
    db.session.commit()

    return prototype_event_in_less_than_48h


@pytest.fixture
def event_with_no_activity_type_in_less_than_48h_with_reg(
    prototype_event_in_less_than_48h,
    user_with_no_warning_badge,
    user_with_valid_first_warning_badge,
):
    """
    Returns an event in less than 48 hours
    with registrations for specified users.
    """

    prototype_event_in_less_than_48h.registration_open_time = (
        datetime.now() - timedelta(hours=10)
    )
    prototype_event_in_less_than_48h.registration_close_time = (
        datetime.now() + timedelta(hours=2)
    )
    prototype_event_in_less_than_48h.start = datetime.now() + timedelta(hours=3)
    prototype_event_in_less_than_48h.end = datetime.now() + timedelta(hours=4)
    prototype_event_in_less_than_48h.num_online_slots = 9

    prototype_event_in_less_than_48h.num_online_slots = 9
    prototype_event_in_less_than_48h.num_online_slots = 9

    prototype_event_in_less_than_48h.activity_types.clear()

    event_type = EventType.query.filter_by(name="Soirée").first()
    prototype_event_in_less_than_48h.event_type = event_type

    for user in [
        user_with_no_warning_badge,
        user_with_valid_first_warning_badge,
    ]:
        prototype_event_in_less_than_48h.registrations.append(
            Registration(
                user_id=user.id,
                status=RegistrationStatus.Active,
                level=RegistrationLevels.Normal,
                is_self=True,
            )
        )

    db.session.add(prototype_event_in_less_than_48h)
    db.session.commit()

    return prototype_event_in_less_than_48h
