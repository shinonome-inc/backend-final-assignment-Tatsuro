from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Tweet

CustomUser = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user")
        self.client.force_login(self.user)

    # リクエストを送信
    def test_get_success(self):
        response = self.client.get(reverse("tweets:create"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    # 有効なcontentのデータでリクエストを送信
    def test_post_success(self):
        data = {"content": "First tweet"}
        response = self.client.post(reverse("tweets:create"), data)
        self.assertRedirects(
            response, reverse("accounts:home"), status_code=302, target_status_code=200
        )
        self.assertTrue(Tweet.objects.filter(content=data["content"]).exists())

    # contentがblankの状態でリクエストを送信
    def test_post_failure_with_empty_content(self):
        data = {"content": ""}
        response = self.client.post(reverse("tweets:create"), data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, "form", "content", "This field is required.")
        self.assertFalse(Tweet.objects.filter(content=data["content"]).exists())

    # contentが長すぎるデータでリクエストを送信(140字以上)
    def test_post_failure_with_too_long_content(self):
        data = {"content": "test" * 100}
        response = self.client.post(reverse("tweets:create"), data)
        self.assertEquals(response.status_code, 200),
        self.assertFormError(
            response,
            "form",
            "content",
            "Ensure this value has at most 140 characters (it has 400).",
        )
        self.assertFalse(Tweet.objects.filter(content=data["content"]).exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user")
        self.client.force_login(self.user)
        self.tweet = Tweet.objects.create(user=self.user, content="test")

    # リクエストを送信
    def test_get_success(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")
        self.assertContains(response, self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user", email="test@example.com"
        )
        self.user2 = CustomUser.objects.create_user(
            username="another_user", email="test2@example.com"
        )
        self.tweet = Tweet.objects.create(user=self.user, content="test")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="test")
        self.client.force_login(self.user)

    # リクエストを送信
    def test_post_success(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet.pk})
        )
        self.assertRedirects(
            response, reverse("accounts:home"), status_code=302, target_status_code=200
        )
        self.assertEqual(Tweet.objects.count(), 1)

    # 存在しないtweetに対してリクエストを送信
    def test_post_failure_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 3}))
        self.assertEquals(response.status_code, 404)
        self.assertTrue(Tweet.objects.exists())

    # 別のユーザーが作成したTweetに対してリクエストを送信
    def test_post_failure_with_incorrect_user(self):

        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet2.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.exists())


class TestFavoriteView(TestCase):
    def test_post_success(self):
        pass

    def test_post_failure_with_not_exist_tweet(self):
        pass

    def test_post_failure_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_post_success(self):
        pass

    def test_post_failure_with_not_exist_tweet(self):
        pass

    def test_post_failure_with_unfavorited_tweet(self):
        pass
