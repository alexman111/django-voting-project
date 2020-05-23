import pytest
from django.contrib.auth.models import User
from voting.models import Profile, Candidate, Comments

@pytest.fixture
def user_factory(db):
    def create_user(username = 'TestUser', password = 'TestPassword', email = 'test@mail.ru'):
        if User.objects.filter(username=username).exists():
            return User.objects.filter(username=username).first()
        else:
            user = User.objects.create(username=username, password=password, email=email)
            return user

    return create_user


@pytest.fixture
def candidate_factory(db):
    def create_candidate(name = 'name', surname = 'surname'):
        if Candidate.objects.filter(surname = surname).exists():
            return Candidate.objects.filter(surname = surname).first()
        else:
            candidate = Candidate.objects.create(name = name, surname= surname)
            return candidate

    return create_candidate


def test_user_data(db, user_factory):
    user = user_factory(username = 'testUser', password = '123456', email = 'test@mail.ru')
    assert user.username == 'testUser' and user.password == '123456' and user.email == 'test@mail.ru'


def test_user_permissions(db, user_factory):
    user = user_factory(username='testUser', password='123456', email='test@mail.ru')
    assert user.is_superuser == False


@pytest.fixture
def profile_factory(db, user_factory):
    def create_profile(voted=False):
        user = user_factory()
        user.profile.is_voted = voted
        user.save()

        return user.profile

    return create_profile


@pytest.fixture
def comment_factory(db):
    def create_comment(user = None, candidate = None, text = 'some_comment'):
        if Comments.objects.filter(text = text).exists():
            return Comments.objects.filter(text = text and candidate == candidate).first()
        else:
            return Comments.objects.create(author = user, text = text, candidate = candidate)

    return create_comment


def test_voting(db, profile_factory):
    profile = profile_factory()
    profile.vote()
    assert profile.is_voted == True


def test_candidate_str(db, candidate_factory):
    candidate = candidate_factory(name = 'test', surname = 'test123')
    assert str(candidate) == 'test test123'


def test_candidate_not_negative_votes(db, candidate_factory):
    candidate = candidate_factory(name='test', surname='test123')
    assert candidate.votes >= 0


def test_candidate_inc_votes(db,candidate_factory):
    candidate = candidate_factory(name='test', surname='test123')
    candidate.inc_votes()
    assert candidate.votes == 1


def test_candidate_not_inc_votes(db,candidate_factory):
    candidate = candidate_factory(name='test', surname='test123')
    candidate1 = candidate_factory(name='test1', surname='test1')

    candidate.inc_votes()
    assert not candidate1.votes == 1


def test_candidates_equal(db,candidate_factory):
    candidate = candidate_factory(name='test', surname='test123')
    candidate1 = candidate_factory(name='test1', surname='test123')

    assert candidate1 == candidate


def test_candidates_not_equal(db,candidate_factory):
    candidate = candidate_factory(name='test', surname='test123')
    candidate1 = candidate_factory(name='test', surname='test12')

    assert not candidate1 == candidate


def test_comment_user(db, comment_factory, user_factory, candidate_factory):
    user = user_factory()
    candidate = candidate_factory()
    comment = comment_factory(user = user, candidate=candidate, text='some text')
    assert comment.author.is_anonymous == False


def test_comment_str(db, comment_factory, user_factory, candidate_factory):
    user = user_factory()
    candidate = candidate_factory()
    comment = comment_factory(user = user, candidate=candidate, text='some text')
    assert str(comment) == comment.text


def test_comment_text(db, comment_factory, user_factory, candidate_factory):
    user = user_factory()
    candidate = candidate_factory()
    comment = comment_factory(user = user, candidate=candidate, text='some text')

    assert comment.text == 'some text'






