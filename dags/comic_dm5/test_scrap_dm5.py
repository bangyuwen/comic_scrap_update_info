"""depercate
"""
import unittest
from datetime import datetime, time, timedelta
import scrap_dm5

datetime_now = datetime.now(pytz.timezone('Asia/Shanghai'))

class test(unittest.TestCase):
    def test_parse_comic(self):
        self.assertEqual(scrap_dm5.parse_comic({
            'website': 'dm5', 'title': '军阀霸宠：纯情妖女火辣辣',
            'chapter': '最新第52話', 'update_time': '今天 02:06更新'
        }, datetime_now), {
            'website': 'dm5',
            'title': '军阀霸宠：纯情妖女火辣辣',
            'chapter_num': '52',
            'chapter_title': '',
            'update_time': '今天 02:06更新'
        })

    def test_parse_datetime(self):
        self.assertEqual(scrap_dm5.parse_datetime("昨天 16:14更新", datetime_now), "1532247240")


if __name__ == '__main__':
    unittest.main()
