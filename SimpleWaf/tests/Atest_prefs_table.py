import sys
sys.path.append('../code')
import DB_Wrapper
from Preferences_Items import Preferences_Items
from Preferences import Preferences
def main():
    ##update the table prefrnces ###
    DB_Wrapper.drop_table("Preferences")
    # create again
    DB_Wrapper.create_tables()

    example_of_settings_updations = [("facebook.com", 3, True, True, 3, True, 1)]
    pref_items = Preferences_Items(example_of_settings_updations)
    DB_Wrapper.special_insert_or_update_preferences_table_pref_items(pref_items)
    ## call to update the dict (in prodaction this will be called once in 24H)
    Preferences.update_dict()

    print(Preferences.get_preferences_of_website("facebook.com").to_string())
if __name__ == '__main__':
    main()