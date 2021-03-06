import requests
import api


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = "2079825120798251207982517d2016c85822079207982517e535d7eba20d50852291298"
    v = '5.103'
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    return response.json()['response']['items']




def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    fields = 'bdate'
    years = []
    middle_age = 0
    date = get_friends(user_id, fields)
    for lists in date:
        if not 'bdate' in lists:
            continue
        else:
            year = lists['bdate'].split(".")
            if len(year) == 3:
                years.append(2019 - int(year[2]))
    for el in years:
        middle_age += el
    middle_age = "%.0f" % (middle_age / len(years))
    return middle_age

print(age_predict(196806984))
