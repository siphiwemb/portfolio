from django.test import TestCase
from .models import (Profile, User)


class UserTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", first_name="usertest1", last_name="last1",
        password="kuytdas1s")

        user3 = User.objects.create(username="user3", first_name="usertest3", last_name="last3",
        password="kuytdas3s")

        Profile.objects.create(user=user1, cellphone="0846579871", house_no="325",
        street="stret1", surburb="surb1", city="city1", state="state1", latitude=-25.354987,
        longitude=24.356874)

        Profile.objects.create(user=user3, cellphone="0846579873", house_no="375",
        street="stret3", surburb="surb3", city="city3", state="state3", latitude=-24.354987,
        longitude=25.356874)

    def test_user_responses(self):
        """Users data comes back expected correctly identified"""
        user1 = User.objects.filter(username="user1").values("username", "first_name", "last_name", "password")
        user3 = User.objects.filter(username="user3").values("username", "first_name", "last_name", "password")
        self.assertEqual(list(user1), [{"username":"user1", "first_name":"usertest1", "last_name":"last1", "password":"kuytdas1s"}])
        self.assertEqual(list(user3), [{"username":"user3", "first_name":"usertest3", "last_name":"last3", "password":"kuytdas3s"}])
        
        user1_obj = User.objects.filter(username="user1").first()
        user3_obj = User.objects.filter(username="user3").first()

        profile1 = Profile.objects.filter(user=user1_obj.id).values("cellphone", "house_no", "street", "surburb", "city", 
        "state", "latitude", "longitude")

        profile1_res = {"cellphone":"0846579871", "house_no":"325", "street":"stret1", "surburb":"surb1", 
        "city":"city1", "state":"state1", "latitude":'-25.354987', "longitude":'24.356874'}
        self.assertEqual(profile1[0], profile1_res)

        profile3 = Profile.objects.filter(user=user3_obj.id).values("cellphone", "house_no", "street", "surburb", "city", 
        "state", "latitude", "longitude")
        profile3_res = {"cellphone":"0846579873", "house_no":"375", "street":"stret3", "surburb":"surb3", 
        "city":"city3", "state":"state3", "latitude":'-24.354987', "longitude":'25.356874'}
        self.assertEqual(profile3[0], profile3_res)
        