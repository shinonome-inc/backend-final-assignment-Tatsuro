from django.urls import reverse
from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase

from mysite import settings
from .models import FriendShip

User = get_user_model()


class TestSignUpView(TestCase):
    # SignupViewのテスト

    def test_success_get(self):
        # 'signup'リクエストの送信を検証

        response_get = self.client.get(reverse("accounts:signup"))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "registration/signup.html")

    def test_success_post(self):
        # 有効なemail,username,passwordでリクエストを送信

        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "pass0000",
            "password2": "pass0000",
            "age": "22",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertRedirects(
            response, reverse("accounts:home"), status_code=302, target_status_code=200
        )
        self.assertTrue(User.objects.exists())

    def test_failure_post_with_empty_form(self):
        # 空のデータでリクエストを送信

        data_empty = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
            "age": "",
        }
        response_empty = self.client.post(reverse("accounts:signup"), data_empty)
        self.assertEquals(response_empty.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_empty, "form", "username", "This field is required."
        )
        self.assertFormError(response_empty, "form", "email", "This field is required.")
        self.assertFormError(
            response_empty, "form", "password1", "This field is required."
        )
        self.assertFormError(
            response_empty, "form", "password2", "This field is required."
        )

    def test_failure_post_with_empty_username(self):
        # usernameが空のデータでリクエストを送信

        data_empty_username = {
            "username": "",
            "email": "test@example.com",
            "password1": "pass0000",
            "password2": "pass0000",
            "age": "22",
        }
        response_empty_username = self.client.post(
            reverse("accounts:signup"), data_empty_username
        )
        self.assertEquals(response_empty_username.status_code, 200)
        self.assertFormError(
            response_empty_username, "form", "username", "This field is required."
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_email(self):
        # emailが空のデータでリクエストを送信

        data_empty_email = {
            "username": "test",
            "email": "",
            "password1": "test0000",
            "password2": "test0000",
            "age": "22",
        }
        response_empty_email = self.client.post(
            reverse("accounts:signup"), data_empty_email
        )
        self.assertEquals(response_empty_email.status_code, 200)
        self.assertFormError(
            response_empty_email, "form", "email", "This field is required."
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_password(self):
        # passwordが空のデータでリクエストを送信

        data_empty_password = {
            "username": "test",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
            "age": "22",
        }
        response_empty_password = self.client.post(
            reverse("accounts:signup"), data_empty_password
        )
        self.assertEquals(response_empty_password.status_code, 200)
        self.assertFormError(
            response_empty_password, "form", "password1", "This field is required."
        )
        self.assertFormError(
            response_empty_password, "form", "password2", "This field is required."
        )
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_duplicated_user(self):
        # 既に存在するユーザーのデータでリクエストを送信

        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "pass0000",
            "password2": "pass0000",
            "age": "22",
        }

        data_duplicated = {
            "username": "test",
            "email": "test@example.com",
            "password1": "pass0000",
            "password2": "pass0000",
            "age": "22",
        }
        self.client.post(reverse("accounts:signup"), data)
        response_duplicated = self.client.post(
            reverse("accounts:signup"), data_duplicated
        )
        self.assertEqual(response_duplicated.status_code, 200)
        self.assertFormError(
            response_duplicated,
            "form",
            "username",
            "A user with that username already exists.",
        )

    def test_failure_post_with_invalid_email(self):
        # emailが有効な形式でないデータでリクエストを送信

        data_invalid_email = {
            "username": "test",
            "email": "test",
            "password1": "pass0000",
            "password2": "pass0000",
            "age": "22",
        }
        response_invalid_email = self.client.post(
            reverse("accounts:signup"), data_invalid_email
        )
        self.assertEquals(response_invalid_email.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_invalid_email, "form", "email", "Enter a valid email address."
        )

    def test_failure_post_with_too_short_password(self):
        # passwordが短すぎるデータでリクエストを送信

        data_short_password = {
            "username": "test",
            "email": "test@example.com",
            "password1": "p",
            "password2": "p",
            "age": "22",
        }
        response_short_password = self.client.post(
            reverse("accounts:signup"), data_short_password
        )
        self.assertEquals(response_short_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_short_password,
            "form",
            "password2",
            "This password is too short. It must contain at least 8 characters.",
        )

    def test_failure_post_with_password_similar_to_username(self):
        # ユーザーネームに類似したパスワードでリクエストを送信

        data_password_similar_to_username = {
            "username": "test0000",
            "email": "test@example.com",
            "password1": "test0000",
            "password2": "test0000",
            "age": "22",
        }
        response_password_similar_to_username = self.client.post(
            reverse("accounts:signup"), data_password_similar_to_username
        )
        self.assertEquals(response_password_similar_to_username.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_password_similar_to_username,
            "form",
            "password2",
            "The password is too similar to the username.",
        )

    def test_failure_post_with_only_numbers_password(self):
        # 全て数字のpasswordでリクエストを送信

        data_password_only_numbers = {
            "username": "test",
            "email": "test@example.com",
            "password1": "12345678",
            "password2": "12345678",
            "age": "22",
        }
        response_password_only_numbers = self.client.post(
            reverse("accounts:signup"), data_password_only_numbers
        )
        self.assertEquals(response_password_only_numbers.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_password_only_numbers,
            "form",
            "password2",
            "This password is entirely numeric.",
        )

    def test_failure_post_with_mismatch_password(self):
        # password1とpassword2が異なるデータでリクエストを送信

        data_mismatch_password = {
            "username": "test",
            "email": "test@example.com",
            "password1": "pass0000",
            "password2": "pas1111",
            "age": "22",
        }
        response_mismatch_password = self.client.post(
            reverse("accounts:signup"), data_mismatch_password
        )
        self.assertEquals(response_mismatch_password.status_code, 200)
        self.assertFalse(User.objects.exists())
        self.assertFormError(
            response_mismatch_password,
            "form",
            "password2",
            "The two password fields didn’t match.",
        )


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass0000",
        )
        self.client.force_login(self.user)

    def test_success_get(self):
        # リクエストを送信
        response_get = self.client.get(reverse("accounts:home"))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "home.html")


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass0000",
        )

    def test_success_get(self):
        # リクエストを送信
        response_get = self.client.get(reverse("accounts:login"))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "registration/login.html")

    def test_success_post(self):
        # 有効なusername,passwordのデータでリクエストを送信

        data = {
            "username": "test",
            "password": "pass0000",
        }
        response_post = self.client.post(reverse("accounts:login"), data)
        self.assertRedirects(
            response_post,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        # 存在しないusername, 有効な形式のパスワードを送信

        data_not_exist = {
            "username": "test1",
            "password": "pass0000",
        }
        response_not_exist = self.client.post(reverse("accounts:login"), data_not_exist)
        self.assertEquals(response_not_exist.status_code, 200)
        self.assertFormError(
            response_not_exist,
            "form",
            "",
            "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        # 有効なusername, 空のpasswordのデータでリクエストを送信

        data_empty_password = {
            "username": "test",
            "password": "",
        }
        response_empty_password = self.client.post(
            reverse("accounts:login"), data_empty_password
        )
        self.assertEquals(response_empty_password.status_code, 200)
        self.assertFormError(
            response_empty_password, "form", "password", "This field is required."
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="pass0000",
        )
        self.client.force_login(self.user)

    def test_success_get(self):
        # リクエストを送信
        response_get = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(
            response_get,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="test1@example.com",
            password="pass1111",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="test2@example.com",
            password="pass2222",
        )
        self.client.force_login(self.user1)

    def test_success_post(self):
        # リクエストを送信
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "user2"})
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)

    def test_failure_post_with_not_exist_user(self):
        # 存在しないユーザーに対してリクエストを送信
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "user3"})
        )
        self.assertEquals(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "This user does not exist.")
        self.assertEquals(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_self(self):
        # 自分自身に対してリクエストを送信
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "user1"})
        )
        self.assertEquals(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "You can't follow yourself.")
        self.assertEquals(FriendShip.objects.filter(follower=self.user1).count(), 0)


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="test1@example.com",
            password="pass1111",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="test2@example.com",
            password="pass2222",
        )
        self.client.force_login(self.user1)
        FriendShip.objects.create(following=self.user2, follower=self.user1)

    def test_success_post(self):
        # リクエストを送信
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "user2"}),
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEquals(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_not_exist_tweet(self):
        # 存在しないユーザーに対してリクエストを送信
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "user3"})
        )
        self.assertEquals(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "This user does not exist.")
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)

    def test_failure_post_with_incorrect_user(self):
        # 自分自身にリクエストを送信
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "user1"})
        )
        self.assertEquals(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "This is your account.")
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="test1@example.com",
            password="pass1111",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="test2@example.com",
            password="pass2222",
        )
        self.user3 = User.objects.create_user(
            username="user3",
            email="test3@example.com",
            password="pass3333",
        )
        self.client.force_login(self.user1)
        FriendShip.objects.create(following=self.user2, follower=self.user1)
        FriendShip.objects.create(following=self.user3, follower=self.user1)

    def test_success_get(self):
        # フォローリスト一覧を表示・該当ユーザーのフォロー数を表示
        response = self.client.get(
            reverse("accounts:following_list", kwargs={"username": "user1"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["following_number"],
            FriendShip.objects.filter(follower=self.user1).count(),
        )


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="test1@example.com",
            password="pass1111",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="test2@example.com",
            password="pass2222",
        )
        self.user3 = User.objects.create_user(
            username="user3",
            email="test3@example.com",
            password="pass3333",
        )
        self.client.force_login(self.user1)
        FriendShip.objects.create(following=self.user1, follower=self.user2)
        FriendShip.objects.create(following=self.user1, follower=self.user3)

    def test_success_get(self):
        # フォロワーリスト一覧を表示・該当ユーザーのフォロワー数を表示
        response = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": "user1"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["follower_number"],
            FriendShip.objects.filter(following=self.user1).count(),
        )
