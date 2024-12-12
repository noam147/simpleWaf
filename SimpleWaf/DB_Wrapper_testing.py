import unittest
import DB_Wrapper

class TestDB(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
