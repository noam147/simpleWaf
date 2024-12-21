import unittest
import DB_Wrapper


class TestDB(unittest.TestCase):

    def test_create_tables(self):
        ### for creating everything needed before testing ###
        DB_Wrapper.create_tables()
    def test_attackers_table(self):
        example_ip = "111.111.111.112"

        example_date = "2025-01-01"
        #test insertion:
        DB_Wrapper.insert_into_attackers(example_ip,example_date)
        if DB_Wrapper.is_ip_blocked(example_ip) == False:
            self.fail("attacker didn't inserted as planned")
        #test deletion:
        DB_Wrapper.delete_attacker(example_ip)
        if DB_Wrapper.is_ip_blocked(example_ip) == True:
            self.fail("attacker didn't delete as planned")
    def test_websites_table(self):
        example_ip = "22.22.2.2"
        example_host_name = "my_site.com"

        # insertion:
        DB_Wrapper.special_insert_or_update_website_ip(example_host_name,example_ip)#gives error when trying to mult - this is good but maybe needs to check if update will work
        #test ip
        test_ip = DB_Wrapper.get_ip_address_by_host_name(example_host_name)
        if test_ip != example_ip:
            self.fail("ip didn't mach")

        #test updating ip:
        new_ip = "33.33.3.3"
        DB_Wrapper.special_insert_or_update_website_ip(example_host_name,new_ip)
        new_test_ip = DB_Wrapper.get_ip_address_by_host_name(example_host_name)
        if new_test_ip != new_ip:
            self.fail("ip didn't mach at updating")
    def test_attackers_score_table(self):
        example_ip = "222.222.222.112"
        ### add attacker to db or increase its score ###
        DB_Wrapper.special_insert_or_update_attackers_score(example_ip)
        ### we want for the test to reset its score ###
        DB_Wrapper.reset_score_of_attacker(example_ip)
        current_score = DB_Wrapper.get_score_of_attacker(example_ip)
        if current_score != 1:
            self.fail("failed reset score")
        ### test adding with defult amount ###
        DB_Wrapper.special_insert_or_update_attackers_score(example_ip)
        current_score = DB_Wrapper.get_score_of_attacker(example_ip)
        if current_score != 1.2:
            self.fail("failed updating score")
        ### test with custom add amount ###
        DB_Wrapper.special_insert_or_update_attackers_score(example_ip,amount_to_add=0.3)
        current_score = DB_Wrapper.get_score_of_attacker(example_ip)
        if current_score != 1.5:
            self.fail("failed updating score")
    def test_attackers_find(self):
        example_ip = "123.123.123.123"
        ### at start insert the attacker to get score of 1 or more ###
        DB_Wrapper.when_find_attacker(example_ip)
        ### we want for the test to reset its score ###
        DB_Wrapper.reset_score_of_attacker(example_ip)

        DB_Wrapper.when_find_attacker(example_ip)
        current_score = DB_Wrapper.get_score_of_attacker(example_ip)
        ### inital score = 1 + amount to add = 0.2
        if current_score != 1.2:
            self.fail("failed score, check default amount to add")
        free_date = DB_Wrapper.get_date_to_free_of_attacker(example_ip)
        test_free_date_str = DB_Wrapper.calc_n_days_from_now(int(30*1.2))
        test_free_date = DB_Wrapper.datetime.strptime(test_free_date_str, '%Y-%m-%d').date()
        if free_date != test_free_date:
            self.fail("free date is wrong")

if __name__ == '__main__':

    unittest.main()
