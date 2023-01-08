import unittest
from src.utils import parse_post_link


class TestParser(unittest.TestCase):
    def test_post_link_parse_case1(self):
        init_owner_id = "394467984"
        init_post_id = "394467984"
        url = f"https://vk.com/whopankrat?w=wall{init_owner_id}_{init_post_id}%2Fall"
        owner_id, post_id = parse_post_link(url)
        self.assertEqual(init_owner_id, owner_id)
        self.assertEqual(init_post_id, init_post_id)

    def test_post_link_parse_case2(self):
        init_owner_id = "394467984"
        init_post_id = "394467984"
        url = f"https://vk.com/whopankrat?w=wall{init_owner_id}_{init_post_id}"
        owner_id, post_id = parse_post_link(url)
        self.assertEqual(init_owner_id, owner_id)
        self.assertEqual(init_post_id, post_id)

    def test_post_link_parse_case3(self):
        invalid_url = "https://google.com"
        with self.assertRaises(Exception):
            _, _ = parse_post_link(invalid_url)


if __name__ == "__main__":
    unittest.main()
