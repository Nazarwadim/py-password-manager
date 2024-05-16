from serializer import Serializer
from data_base import DataBase
from user import UserData


global_mock_base = DataBase(Serializer())

def find_user_by_title(users, title):
    for user in users:
        if user.title == title:
            return user
    return None

def test_start_new_open_close():
    global global_mock_base
    try:
        global_mock_base.new("1234", "test_base")
        assert(global_mock_base.is_open() == True)
        global_mock_base.close()
        assert(global_mock_base.is_open() == False)    
        global_mock_base.open("1234", "test_base") # Will be used in the next tests, so no close.
        assert(global_mock_base.is_open() == True)
    except Exception:
        print("Test start, new, open, close failed! Exit.")
        exit(-1)

def test_end():
    global global_mock_base
    global_mock_base.close()
    print("Test finished. No errors)")

def test_add_user():
    global global_mock_base
    try:
        global_mock_base.add_user_data(UserData("tit", "log", "pas", "email", "description"))
        assert(global_mock_base.get_user_data_count() == 1)
        
        global_mock_base.close()
        new_db = DataBase(Serializer())
        new_db.open("1234", "test_base")
        assert(new_db.get_user_data_count() == 1)
        data = new_db.get_data()
        assert(find_user_by_title(data, "tit") != None)
        new_db.close()
        global_mock_base.open("1234", "test_base")
        
    except Exception:
        print("Test add user failed! Exit.")
        exit(-1)

def test_remove_user():
    global global_mock_base
    try:
        global_mock_base.remove_user_data(0)
        assert(global_mock_base.get_user_data_count() == 0)
        global_mock_base.close()
        new_db = DataBase(Serializer())
        new_db.open("1234", "test_base")
        assert(new_db.get_user_data_count() == 0)
        data = new_db.get_data()
        assert(find_user_by_title(data, "tit") == None)
        new_db.close()
        global_mock_base.open("1234", "test_base")
        
    except Exception:
        print("Test remove user failed! Exit.")
        exit(-1)

def test():
    test_start_new_open_close()
    test_add_user()
    test_remove_user()
    test_end()