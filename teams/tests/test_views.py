from __future__ import unicode_literals
from unittest import skip, skipIf, skipUnless
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

import teams.tests.test_setup as test
from teams.models import Week

# Team list

class TestTeamListView(TestCase):
    def setUp(self):
        self.user1 = test.create_user('user1', 'password')
        self.user2 = test.create_user('user2', 'password')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_team_list_with_no_teams(self):
        """
        No teams are displayed if the queryset is empty.
        """
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(response.context['team_list'], [])
        self.assertContains(response, 'No teams yet.')

    def test_team_list_with_teams(self):
        """
        Teams are displayed in a table.
        """
        self.client.login(username='user1', password='password')
        test.create_team(user=self.user1)
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(
            response.context['team_list'],
            ['<Team: Northeastern University>'],
        )
        self.assertContains(response, 'Northeastern University')

    def test_multiple_teams(self):
        """
        Teams are displayed in alphabetical order.
        """
        self.client.login(username='user1', password='password')
        test.create_team(user=self.user1)
        test.create_team(user=self.user1, name='University of Kansas')
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(
            response.context['team_list'],
            ['<Team: Northeastern University>', '<Team: University of Kansas>'],
        )

    def test_multiple_users_with_teams(self):
        """
        Only the teams belonging to the logged in user will be displayed.
        """
        self.client.login(username='user1', password='password')
        test.create_team(user=self.user1)
        test.create_team(user=self.user2, name='University of Kansas')
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(
            response.context['team_list'],
            ['<Team: Northeastern University>'],
        )
        self.assertContains(response, 'Northeastern University')
        self.assertNotContains(response, 'University of Kansas')

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(
            response.context['team_list'],
            ['<Team: University of Kansas>'],
        )
        self.assertNotContains(response, 'Northeastern University')
        self.assertContains(response, 'University of Kansas')


# Swimmer list

class TestSwimmerListView(TestCase):
    def setUp(self):
        self.user1 = test.create_user('user1', 'password')
        self.user2 = test.create_user('user2', 'password')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_swimmer_list_with_no_swimmers(self):
        """
        No swimmers are displayed if the queryset is empty.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team.abbr}))
        self.assertQuerysetEqual(response.context['swimmer_list'], [])
        self.assertContains(response, 'Northeastern University')
        self.assertNotContains(response, 'Henry Gridley')

    def test_swimmer_list_with_swimmers(self):
        """
        Swimmers are displayed in a table.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        test.create_swimmer(team=team)
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team.abbr}))
        self.assertQuerysetEqual(
            response.context['swimmer_list'],
            ['<Swimmer: Gridley>'],
        )
        self.assertContains(response, 'Gridley')

    def test_multiple_swimmers(self):
        """
        Swimmer are displayed in alphabetical order.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        test.create_swimmer(team=team)
        test.create_swimmer(team=team, last='Pinkes')
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team.abbr}))
        self.assertQuerysetEqual(
            response.context['swimmer_list'],
            ['<Swimmer: Gridley>', '<Swimmer: Pinkes>'],
        )

    def test_multiple_users_with_swimmers(self):
        """
        Only the swimmers belonging to the logged in user will be displayed.
        """
        self.client.login(username='user1', password='password')
        team1 = test.create_team(user=self.user1)
        test.create_swimmer(team=team1)
        team2 = test.create_team(user=self.user2)
        test.create_swimmer(team=team2, last='Thornton')
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team1.abbr}))
        self.assertQuerysetEqual(
            response.context['swimmer_list'],
            ['<Swimmer: Gridley>'],
        )
        self.assertContains(response, 'Northeastern University')
        self.assertContains(response, 'Gridley')
        self.assertNotContains(response, 'Thornton')


        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team2.abbr}))
        self.assertQuerysetEqual(
            response.context['swimmer_list'],
            ['<Swimmer: Thornton>'],
        )
        self.assertContains(response, 'Northeastern University')
        self.assertContains(response, 'Thornton')
        self.assertNotContains(response, 'Gridley')


# Write practices

class TestWritePracticeView(TestCase):
    def setUp(self):
        self.user1 = test.create_user('user1', 'password')
        self.user2 = test.create_user('user2', 'password')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_write_practice_with_no_sets(self):
        """
        Only panel headings are displayed when no sets have been written.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        team = test.create_team(user=self.user1)
        practice = test.create_practice(team, week)
        response = self.client.get(reverse('teams:practice', kwargs={
                'abbr': team.abbr,
                'p_id': practice.id
            })
        )
        self.assertEqual(response.context['practice'].weekday, 'monday')
        self.assertQuerysetEqual(response.context['set_list'], [])
        self.assertContains(response, 'Create a Set')

    def test_write_practice_with_sets(self):
        """
        Sets are displayed in order with all reps and headings.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        team = test.create_team(user=self.user1)
        practice = test.create_practice(team, week)
        set1 = test.create_set(practice=practice)
        rep1 = test.create_rep(_set=set1)
        set2 = test.create_set(practice, 'sprint', 2, 2)
        rep2 = test.create_rep(set2, 4, 25, 'fly')
        rep3 = test.create_rep(set2, 8, 200, 'back')
        response = self.client.get(reverse('teams:practice', kwargs={
                'abbr': team.abbr,
                'p_id': practice.id
            })
        )
        self.assertEqual(response.context['practice'].weekday, 'monday')
        self.assertQuerysetEqual(
            response.context['set_list'],
            ['<Set: warmup>', '<Set: sprint>'],
            ordered=False,
        )
        self.assertContains(response, 'Create a Set')
        self.assertContains(response, 'Warmup')
        self.assertContains(response, 'Sprint')
        self.assertContains(response, 'free')
        self.assertContains(response, 'fly')
        self.assertContains(response, 'back')

    def test_multiple_users_with_sets(self):
        """
        Only sets belonging to the logged in user will be displayed.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        team1 = test.create_team(user=self.user1)
        team2 = test.create_team(user=self.user2)
        practice1 = test.create_practice(team1, week)
        practice2 = test.create_practice(team2, week)
        set1 = test.create_set(practice=practice1)
        rep1 = test.create_rep(_set=set1)
        set2 = test.create_set(practice2, 'sprint', 2, 2)
        rep2 = test.create_rep(set2, 4, 25, 'fly')
        rep3 = test.create_rep(set2, 8, 200, 'back')
        response = self.client.get(reverse('teams:practice', kwargs={
                'abbr': team1.abbr,
                'p_id': practice1.id
            })
        )
        self.assertQuerysetEqual(
            response.context['set_list'],
            ['<Set: warmup>']
        )

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:practice', kwargs={
                'abbr': team2.abbr,
                'p_id': practice2.id
            })
        )
        self.assertQuerysetEqual(
            response.context['set_list'],
            ['<Set: sprint>']
        )


# Practice schedule

class TestPracticeScheduleView(TestCase):
    def setUp(self):
        self.user1 = test.create_user('user1', 'password')
        self.user2 = test.create_user('user2', 'password')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_schedule_with_no_practices(self):
        """
        Only panel headings are displayed if the queryset is empty.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        week.populate()
        team = test.create_team(user=self.user1)
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ,'sunday']
        practices = [None for x in range(7)]
        practices = zip(practices, weekdays)
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': week.id,
            })
        )
        self.assertEqual(response.context['practices'], practices)
        self.assertContains(response, 'Monday')
        self.assertContains(response, 'Sunday')
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')

    def test_schedule_with_practices(self):
        """
        Practices are displayed in the correct panel.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        week.populate()
        team = test.create_team(user=self.user1)
        practice1 = test.create_practice(team, week)
        set1 = test.create_set(practice=practice1, order=23)
        practice2 = test.create_practice(team, week, weekday='tuesday')
        set2 = test.create_set(practice=practice2, focus='sprint', repeats=2, order=37)
        set3 = test.create_set(practice=practice2, focus='distance', repeats=3, order=38)
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': week.id,
            })
        )
        self.assertEqual(response.context['practices'][0][0].weekday, 'monday')
        self.assertEqual(response.context['practices'][1][0].weekday, 'tuesday')
        self.assertEqual(response.context['practices'][2][0], None)
        self.assertContains(response, 'Monday')
        self.assertContains(response, 23)
        self.assertContains(response, 37)
        self.assertContains(response, 38)
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')

    def test_multiple_users_with_practices(self):
        """
        Only practices belonging to the logged in user will be displayed.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        week.populate()
        team1 = test.create_team(user=self.user1)
        team2 = test.create_team(user=self.user2)
        practice1 = test.create_practice(team1, week)
        practice2 = test.create_practice(team2, week, weekday='tuesday')
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team1.abbr,
                'w_id': week.id
            })
        )
        self.assertEqual(response.context['practices'][0][0].weekday, 'monday')
        self.assertEqual(response.context['practices'][1][0], None)
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team2.abbr,
                'w_id': week.id
            })
        )
        self.assertEqual(response.context['practices'][0][0], None)
        self.assertEqual(response.context['practices'][1][0].weekday, 'tuesday')
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')

    def test_schedule_with_no_weeks(self):
        """
        Current, previous, and next weeks will be created and populated.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': 0,
            })
        )
        current_week = Week.objects.get(present=True)
        previous_week = current_week.get_week(0)
        next_week = current_week.get_week(1)
        self.assertEqual(current_week.monday, date(2017,7,10))
        self.assertEqual(previous_week.monday, date(2017,7,3))
        self.assertEqual(next_week.monday, date(2017,7,17))

    def test_schedule_with_current_week_only(self):
        """
        Previous and next weeks will be created and populated. Current week will
        be returned from a database query.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        week = test.create_week()
        week.populate()
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': 0,
            })
        )
        current_week = Week.objects.get(present=True)
        previous_week = current_week.get_week(0)
        next_week = current_week.get_week(1)
        self.assertEqual(current_week, week)
        self.assertEqual(previous_week.monday, date(2017,7,3))
        self.assertEqual(next_week.monday, date(2017,7,17))

    def test_schedule_get_next_week(self):
        """
        The next week becomes the 'current' week and another week is created as
        the 'next' week.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        week = test.create_week()
        week.populate()
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': 0,
            })
        )

        current_week = Week.objects.get(present=True)
        next_week = current_week.get_week(1)

        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team.abbr,
                'w_id': next_week.id,
            })
        )
        self.assertEqual(response.context['current_week'], next_week)
        self.assertEqual(response.context['previous_week'], current_week)
        self.assertEqual(response.context['next_week'].monday, date(2017,7,24))


# Delete models

class TestDeleteModelsViews(TestCase):
    def setUp(self):
        self.user1 = test.create_user('user1', 'password')
        self.user2 = test.create_user('user2', 'password')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_delete_team(self):
        """
        Deletes a team.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        response = self.client.get(reverse(
                'teams:deleteTeam',
                kwargs={'abbr': team.abbr}),
            follow=True)
        self.assertQuerysetEqual(response.context['team_list'], [])

    def test_multiple_users_delete_team(self):
        """
        Deleting a team for one user should not delete it for another.
        """
        self.client.login(username='user1', password='password')
        team1 = test.create_team(user=self.user1)
        team2 = test.create_team(user=self.user2)
        response = self.client.get(reverse(
                'teams:deleteTeam',
                kwargs={'abbr': team1.abbr}),
            follow=True)
        self.assertQuerysetEqual(response.context['team_list'], [])

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:team_list'))
        self.assertQuerysetEqual(
            response.context['team_list'],
            ['<Team: Northeastern University>'],
        )

    def test_delete_swimmer(self):
        """
        Deletes a swimmer.
        """
        self.client.login(username='user1', password='password')
        team = test.create_team(user=self.user1)
        swimmer = test.create_swimmer(team=team)
        response = self.client.get(reverse(
                'teams:deleteSwimmer',
                kwargs={'abbr': team.abbr, 's_id': swimmer.id}),
            follow=True)
        self.assertQuerysetEqual(response.context['swimmer_list'], [])

    def test_multiple_users_delete_swimmer(self):
        """
        Deleting a team for one user should not delete it for another.
        """
        self.client.login(username='user1', password='password')
        team1 = test.create_team(user=self.user1)
        swimmer1 = test.create_swimmer(team=team1)
        team2 = test.create_team(user=self.user2)
        swimmer2 = test.create_swimmer(team=team2)
        response = self.client.get(reverse(
                'teams:deleteSwimmer',
                kwargs={'abbr': team1.abbr, 's_id': swimmer1.id}),
            follow=True)
        self.assertQuerysetEqual(response.context['swimmer_list'], [])

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:swimmer_list', kwargs={'abbr': team2.abbr}))
        self.assertQuerysetEqual(
            response.context['swimmer_list'],
            ['<Swimmer: Gridley>'],
        )

    def test_delete_practice(self):
        """
        Deletes a practice.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        week.populate()
        team = test.create_team(user=self.user1)
        practice = test.create_practice(team=team, week=week)
        response = self.client.get(reverse(
                'teams:deletePractice',
                kwargs={'abbr': team.abbr, 'p_id': practice.id}),
            follow=True)
        self.assertEqual(response.context['practices'][0], (None, 'monday'))
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')

    def test_multiple_users_delete_practice(self):
        """
        Deleting a team for one user should not delete it for another.
        """
        self.client.login(username='user1', password='password')
        week = test.create_week()
        week.populate()
        team1 = test.create_team(user=self.user1)
        practice1 = test.create_practice(team=team1, week=week)
        team2 = test.create_team(user=self.user2)
        practice2 = test.create_practice(team=team2, week=week)
        response = self.client.get(reverse(
                'teams:deletePractice',
                kwargs={'abbr': team1.abbr, 'p_id': practice1.id}),
            follow=True)
        self.assertEqual(response.context['practices'][0], (None, 'monday'))

        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('teams:schedule', kwargs={
                'abbr': team2.abbr,
                'w_id': week.id
            })
        )
        self.assertEqual(response.context['practices'][0][0].weekday, 'monday')
        self.assertContains(response, '7/10')
        self.assertContains(response, '7/16')
