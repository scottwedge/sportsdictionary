import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from dictionary.models import Sport, SuggestedTerm, Term, Definition, Vote


class SportFactory(DjangoModelFactory):
    class Meta:
        model = Sport

    name = factory.Sequence(lambda n: f'Sport {n}')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'User {n}')
    email = factory.Sequence(lambda n: f'User{n}@sportsdictionary.com')


class TermFactory(DjangoModelFactory):
    class Meta:
        model = Term

    sport = factory.SubFactory(SportFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Sequence(lambda n: f'Term text {n}')


class SuggestedTermFactory(DjangoModelFactory):
    class Meta:
        model = SuggestedTerm

    sport = factory.SubFactory(SportFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Sequence(lambda n: f'Suggested Term text {n}')
    example_usage = factory.Sequence(lambda n: f'Example usage for suggested term {n}')
    review_status = SuggestedTerm.PENDING


class DefinitionFactory(DjangoModelFactory):
    class Meta:
        model = Definition

    term = factory.SubFactory(TermFactory)
    user = factory.SubFactory(UserFactory)
    text = factory.Sequence(lambda n: f'Definition {n}')
    example_usage = factory.Sequence(lambda n: f'Example usage for definition {n}')


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    definition = factory.SubFactory(DefinitionFactory)
    user = factory.SubFactory(UserFactory)
    vote_type = Vote.UPVOTE
