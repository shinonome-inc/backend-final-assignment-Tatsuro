from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()

class TestSignUpView(TestCase):
      # SignupViewのテスト

    def test_success_get(self):
       # 'signup'リクエストの送信を検証 
        
        response_get = self.client.get(reverse('accounts:signup'))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'registration/signup.html')

    def test_success_post(self):
       # 有効なemail,username,passwordでリクエストを送信
        
        data = {
             'username' : 'test',
             'email' : 'test@example.com',
             'password1' : 'pass0000',
             'password2' : 'pass0000',
             'age' : '22',
             }
        response = self.client.post(reverse('accounts:signup'), data) 
        self.assertRedirects(response, reverse('welcome:home'), status_code=302, target_status_code=200)
        self.assertTrue(CustomUser.objects.exists())
        
    def test_failure_post_with_empty_form(self):
       # 空のデータでリクエストを送信

        data_empty = {
            'username' : '',
            'email' : '',
            'password1': '',
            'password2': '',
            'age' : '',
            }
        response_empty = self.client.post(reverse('accounts:signup'), data_empty)
        self.assertEquals(response_empty.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_empty, 'form', 'username', 'This field is required.')
        self.assertFormError(response_empty, 'form', 'email', 'This field is required.')
        self.assertFormError(response_empty, 'form', 'password1', 'This field is required.')
        self.assertFormError(response_empty, 'form', 'password2', 'This field is required.')
       
    def test_failure_post_with_empty_username(self):
        # usernameが空のデータでリクエストを送信
        
        data_empty_username = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'pass0000',
            'password2': 'pass0000',
            'age' : '22',
        }
        response_empty_username = self.client.post(reverse('accounts:signup'), data_empty_username)
        self.assertEquals(response_empty_username.status_code, 200)
        self.assertFormError(response_empty_username, 'form', 'username', 'This field is required.')
        self.assertFalse(CustomUser.objects.exists())

    def test_failure_post_with_empty_email(self):
        # emailが空のデータでリクエストを送信

        data_empty_email = {
             'username':'test',
             'email':'',
             'password1':'test0000',
             'password2':'test0000',
             'age' : '22',
         }
        response_empty_email = self.client.post(reverse('accounts:signup'), data_empty_email)
        self.assertEquals(response_empty_email.status_code,200)
        self.assertFormError(response_empty_email, 'form', 'email', 'This field is required.')
        self.assertFalse(CustomUser.objects.exists())
   
    def test_failure_post_with_empty_password(self):
        # passwordが空のデータでリクエストを送信

        data_empty_password = {
             'username':'test',
             'email':'test@example.com',
             'password1':'',
             'password2':'',
             'age' : '22',
         }
        response_empty_password = self.client.post(reverse('accounts:signup'), data_empty_password)
        self.assertEquals(response_empty_password.status_code, 200)
        self.assertFormError(response_empty_password, 'form', 'password1', 'This field is required.')
        self.assertFormError(response_empty_password, 'form', 'password2', 'This field is required.')
        self.assertFalse(CustomUser.objects.exists())
        
    def test_failure_post_with_duplicated_user(self):
        # 既に存在するユーザーのデータでリクエストを送信
        
        data = {
             'username':'test',
             'email':'test@example.com',
             'password1':'pass0000',
             'password2':'pass0000',
             'age' : '22',
         }
        
        data_duplicated = {
             'username':'test',
             'email':'test@example.com',
             'password1':'pass0000',
             'password2':'pass0000',
             'age' : '22',
        }
        self.client.post(reverse('accounts:signup'), data)
        response_duplicated = self.client.post(reverse('accounts:signup'), data_duplicated)
        self.assertEqual(response_duplicated.status_code, 200)
        self.assertFormError(response_duplicated, 'form', 'username', 'A user with that username already exists.')

    def test_failure_post_with_invalid_email(self):
        # emailが有効な形式でないデータでリクエストを送信

        data_invalid_email = {
             'username':'test',
             'email':'test',
             'password1':'pass0000',
             'password2':'pass0000',
             'age' : '22',
         }
        response_invalid_email = self.client.post(reverse('accounts:signup'), data_invalid_email)
        self.assertEquals(response_invalid_email.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_invalid_email, 'form', 'email', 'Enter a valid email address.')

    def test_failure_post_with_too_short_password(self):
        # passwordが短すぎるデータでリクエストを送信

        data_short_password = {
             'username':'test',
             'email':'test@example.com',
             'password1':'p',
             'password2':'p',
             'age' : '22',
         }
        response_short_password = self.client.post(reverse('accounts:signup'), data_short_password)
        self.assertEquals(response_short_password.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_short_password, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')

    def test_failure_post_with_password_similar_to_username(self):
        # ユーザーネームに類似したパスワードでリクエストを送信

        data_password_similar_to_username = {
             'username':'test0000',
             'email':'test@example.com',
             'password1':'test0000',
             'password2':'test0000',
             'age' : '22',

         }
        response_password_similar_to_username = self.client.post(reverse('accounts:signup'), data_password_similar_to_username)
        self.assertEquals(response_password_similar_to_username.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_password_similar_to_username, 'form', 'password2', 'The password is too similar to the username.')


    def test_failure_post_with_only_numbers_password(self):
        # 全て数字のpasswordでリクエストを送信

        data_password_only_numbers = {
             'username':'test',
             'email':'test@example.com',
             'password1':'12345678',
             'password2':'12345678',
             'age' : '22',
         }
        response_password_only_numbers = self.client.post(reverse('accounts:signup'), data_password_only_numbers)
        self.assertEquals(response_password_only_numbers.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_password_only_numbers, 'form', 'password2', 'This password is entirely numeric.')
        
    def test_failure_post_with_mismatch_password(self):
        # password1とpassword2が異なるデータでリクエストを送信

        data_mismatch_password = {
             'username':'test',
             'email':'test@example.com',
             'password1':'pass0000',
             'password2':'pas1111',
             'age' : '22',
         }
        response_mismatch_password = self.client.post(reverse('accounts:signup'), data_mismatch_password)
        self.assertEquals(response_mismatch_password.status_code, 200)
        self.assertFalse(CustomUser.objects.exists())
        self.assertFormError(response_mismatch_password, 'form', 'password2', 'The two password fields didn’t match.')
        

class TestHomeView(TestCase):
    def test_success_get(self):
        # リクエストを送信
        
        response_get = self.client.get(reverse('welcome:home'))
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'home.html')


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


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
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
