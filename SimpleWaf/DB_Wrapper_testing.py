import unittest
import DB_Wrapper
import sys
import argparse
from datetime import datetime, timedelta

def calc_n_days_from_now(n: int) -> str:
    current_date = datetime.now()
    future_date = current_date + timedelta(days=n)
    return future_date.strftime('%Y-%m-%d')

def calc_attacker_free_date(attacker_ip: str) -> str:
    NUM_OF_DAYS = 30
    DB_Wrapper.special_insert_or_update_attackers_score(attacker_ip)
    current_score = DB_Wrapper.get_score_of_attacker(attacker_ip)
    DAYS_UNTIL_FREE: int = int(NUM_OF_DAYS * current_score)
    return calc_n_days_from_now(DAYS_UNTIL_FREE)

def when_find_attacker(attacker_ip: str):
    free_date = calc_attacker_free_date(attacker_ip)
    DB_Wrapper.special_insert_or_update_attackers_table(attacker_ip, free_date)


class TestDB(unittest.TestCase):

    def test_create_tables(self):
        ### for creating everything needed before testing ###
        DB_Wrapper.create_tables()

    def test_attackers_table(self):
        example_ip = "111.111.111.112"
        example_date = "2025-01-01"
        DB_Wrapper.insert_into_attackers(example_ip, example_date)
        self.assertTrue(DB_Wrapper.is_ip_blocked(example_ip), "Attacker not inserted as planned.")
        DB_Wrapper.delete_attacker(example_ip)
        self.assertFalse(DB_Wrapper.is_ip_blocked(example_ip), "Attacker not deleted as planned.")

    def test_websites_table(self):
        example_ip = "22.22.2.2"
        example_host_name = "my_site.com"
        DB_Wrapper.special_insert_or_update_website_ip(example_host_name, example_ip)
        test_ip = DB_Wrapper.get_ip_address_by_host_name(example_host_name)
        self.assertEqual(test_ip, example_ip, "IP didn't match.")
        new_ip = "33.33.3.3"
        DB_Wrapper.special_insert_or_update_website_ip(example_host_name, new_ip)
        new_test_ip = DB_Wrapper.get_ip_address_by_host_name(example_host_name)
        self.assertEqual(new_test_ip, new_ip, "Updated IP didn't match.")

    def test_attackers_score_table(self):
        example_ip = "222.222.222.112"
        DB_Wrapper.special_insert_or_update_attackers_score(example_ip)
        DB_Wrapper.reset_score_of_attacker(example_ip)
        current_score = DB_Wrapper.get_score_of_attacker(example_ip)
        self.assertEqual(current_score, 1, "Failed to reset score.")
        DB_Wrapper.special_insert_or_update_attackers_score(example_ip)
        self.assertEqual(DB_Wrapper.get_score_of_attacker(example_ip), 1.2, "Failed to update score.")

    def test_attackers_find(self):
        example_ip = "123.123.123.123"
        DB_Wrapper.reset_score_of_attacker(example_ip)
        when_find_attacker(example_ip)
        self.assertEqual(DB_Wrapper.get_score_of_attacker(example_ip), 1.2, "Failed to update score.")
        free_date = DB_Wrapper.get_date_to_free_of_attacker(example_ip)
        test_free_date = datetime.strptime(calc_n_days_from_now(int(30 * 1.2)), '%Y-%m-%d').date()
        self.assertEqual(free_date, test_free_date, "Free date is wrong.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Save and parse the database configuration
        parser = argparse.ArgumentParser(description="DB Wrapper Testing")
        parser.add_argument("host", type=str, help="Database host")
        parser.add_argument("user", type=str, help="Database username")
        parser.add_argument("password", type=str, help="Database password")
        parser.add_argument("database", type=str, help="Database name")
        args, remaining_args = parser.parse_known_args()
        DB_Wrapper.db_config = {
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "database": args.database,
        }
        # Remove arguments for unittest
        sys.argv = [sys.argv[0]] + remaining_args
    print(DB_Wrapper.db_config)
    unittest.main()
