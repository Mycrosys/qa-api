from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Issue


class IssueListViewTests(APITestCase):
    """
    Tests for Issues working correctly
    """
    def setUp(self):
        """
        Setup Class to create test user
        """
        User.objects.create_user(username='tester', password='pass')

    def test_can_list_issues(self):
        """
        Tests if a User can see all listed Issues
        """
        tester = User.objects.get(username='tester')
        Issue.objects.create(owner=tester,
                             title='This is a test',
                             due_date='2022-11-29T20:00:00Z')
        response = self.client.get('/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_issue(self):
        """
        Tests if a logged in User can create an Issue
        """
        self.client.login(username='tester', password='pass')
        response = self.client.post('/issues/',
                                    {'title': 'This is a test',
                                     'due_date': '2022-11-29T20:00:00Z'})
        count = Issue.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_issue(self):
        """
        Tests if a User that is not logged in can create an Issue
        """
        response = self.client.post('/issues/',
                                    {'title': 'This is a test',
                                     'due_date': '2022-11-29T20:00:00Z'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class IssueDetailViewTests(APITestCase):

    def setUp(self):
        """
        Setup Class to create test users
        """
        tester = User.objects.create_user(username='tester', password='pass')
        testertwo = User.objects.create_user(username='testertwo', password='pass')
        Issue.objects.create(owner=tester,
                             title='This is a test',
                             description='Just a test Issue',
                             due_date='2022-11-29T20:00:00Z')
        Issue.objects.create(owner=testertwo,
                             title='This is another test',
                             description='Just another test Issue',
                             due_date='2022-11-29T20:00:00Z')


    def test_can_retrieve_issue_using_valid_id(self):
        """
        Tests if a User can see the Issue Details
        """
        response = self.client.get('/issues/1/')
        self.assertEqual(response.data['title'], 'This is a test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_issue_using_invalid_id(self):
        """
        Tests if a User gets the correct Error when requesting
        the Detail of an Issue that doesn't exist
        """
        response = self.client.get('/issues/12345/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_issue(self):
        """
        Tests if a User can update an Issue he/she created
        """
        self.client.login(username='tester', password='pass')
        response = self.client.put('/issues/1/', {'title': 'a new title',
                                                  'description': 'New Description',
                                                  'due_date': '2022-11-19T20:00:00Z'})
        issue = Issue.objects.filter(pk=1).first()
        self.assertEqual(issue.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_issue(self):
        """
        Tests if a User can not update an Issue he/she didn't create
        """
        self.client.login(username='tester', password='pass')
        response = self.client.put('/issues/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
