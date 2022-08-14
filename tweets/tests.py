from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Tweet

CustomUser = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    # リクエストを送信
    def test_success_get(self):
        response = self.client.get(reverse("tweets:create"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    # 有効なcontentのデータでリクエストを送信
    def test_success_post(self):
        data = {"content": "First tweet"}
        response = self.client.post(reverse("tweets:create"), data)
        self.assertRedirects(
            response, reverse("accounts:home"), status_code=302, target_status_code=200
        )
        self.assertTrue(Tweet.objects.filter(content=data["content"]).exists())

    # contentがblankの状態でリクエストを送信
    def test_failure_post_with_empty_content(self):
        data = {"content": ""}
        response = self.client.post(reverse("tweets:create"), data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, "form", "content", "This field is required.")
        self.assertFalse(Tweet.objects.filter(content=data["content"]).exists())

    # contentが長すぎるデータでリクエストを送信(140字以上)
    def test_failure_post_with_too_long_content(self):
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
        self.user = CustomUser.objects.create_user(username="test")
        self.client.force_login(self.user)
        self.tweet = Tweet.objects.create(user=self.user, content="test")

    # リクエストを送信
    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")
        self.assertContains(response, self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="test1", email="test1@example.com"
        )
        self.client.force_login(self.user1)
        self.tweet = Tweet.objects.create(user=self.user1, content="test")

    # リクエストを送信
    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet.pk})
        )
        self.assertRedirects(
            response, reverse("accounts:home"), status_code=302, target_status_code=200
        )
        self.assertEqual(Tweet.objects.count(), 0)

    # 存在しないtweetに対してリクエストを送信
    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 2}))
        self.assertEquals(response.status_code, 404)
        self.assertTrue(Tweet.objects.exists())

    # 別のユーザーが作成したTweetに対してリクエストを送信
    def test_failure_post_with_incorrect_user(self):
        self.user2 = CustomUser.objects.create_user(
            username="test2", email="test2@example.com"
        )
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.exists())


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
