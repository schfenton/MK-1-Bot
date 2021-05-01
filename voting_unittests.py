import STAR_voting
import unittest

class TestList(unittest.TestCase):

    def test_vote_err_01(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(STAR_voting.PollError):
            poll.add_vote([1, 2, 3])

    def test_vote_err_02(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        with self.assertRaises(STAR_voting.PollError):
            poll.add_vote([1, 2, 3])

    def test_vote_err_03(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(TypeError):
            poll.add_vote("1")

    def test_vote_err_04(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(STAR_voting.PollError):
            poll.add_vote([])

    def test_vote_err_05(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(TypeError):
            poll.add_vote([-1, 1, 5, 2])

    def test_vote_err_05b(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(TypeError):
            poll.add_vote([6, 1, 5, 2])

    def test_vote_err_06(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(TypeError):
            poll.add_vote(["1", 3, 4, 0])

    def test_vote_err_06b(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(TypeError):
            poll.add_vote([None, 3, 4, 0])

    def test_candidate_err_01(self):
        poll = STAR_voting.Poll(["A"])
        with self.assertRaises(STAR_voting.PollError):
            poll.open()

    def test_candidate_err_02(self):
        poll = STAR_voting.Poll([])
        with self.assertRaises(STAR_voting.PollError):
            poll.open()

    def test_01(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        poll.add_vote([1, 2, 3, 4])
        poll.add_vote([5, 4, 2, 0])
        self.assertTrue(poll.get_votes(), [[1, 2, 3, 4], [5, 4, 2, 0]])

    def test_poll_err(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        with self.assertRaises(STAR_voting.PollError):
            poll.close()

    def test_max(self):
        self.assertTrue(STAR_voting.find_max_index([1, 1, -10, -20]), ([0, 1], [2]))
        self.assertTrue(STAR_voting.find_max_index([-1240, 123540, 4104233104, 0, 512, 4302, 123540, -143250403, 20]),
                        ([2], [1, 6]))
        self.assertTrue(STAR_voting.find_max_index([5, 13, 9]), [[1], [2]])
        self.assertTrue(STAR_voting.find_max_index([11, 7, 8, 8, 9, 8]), [[0], [4]])

    def test_rank_01(self):
        poll = STAR_voting.Poll(["A", "B", "C"])
        poll.open()
        poll.add_vote([0, 3, 5])
        poll.add_vote([5, 3, 0])
        poll.add_vote([4, 3, 3])
        self.assertTrue(poll.compare_rank([0, 1, 2]), [0])

    def test_rank_02(self):
        poll = STAR_voting.Poll(["A", "B", "C"])
        poll.open()
        poll.add_vote([0, 3, 5])
        poll.add_vote([5, 3, 0])
        poll.add_vote([3, 3, 3])
        self.assertTrue(poll.compare_rank([0, 1, 2]), [1, 3])

    def test_rank_03(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D", "E"])
        poll.open()
        poll.add_vote([0, 3, 5, 4, 5])
        poll.add_vote([5, 3, 0, 1, 4])
        poll.add_vote([3, 3, 3, 1, 4])
        self.assertTrue(poll.compare_rank([1, 2, 3]), [1, 2])

    def test_rank_04(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D", "E"])
        poll.open()
        poll.add_vote([0, 3, 5, 4, 5])
        poll.add_vote([5, 3, 0, 1, 4])
        poll.add_vote([3, 3, 3, 1, 4])
        self.assertTrue(poll.compare_rank([4, 1, 3]), [4])

    def test_poll_01(self):
        poll = STAR_voting.Poll(["A", "B", "C"])
        poll.open()
        poll.add_vote([0, 5, 3])
        poll.add_vote([0, 3, 5])
        poll.add_vote([5, 3, 0])
        poll.add_vote([0, 2, 1])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "B")

    def test_poll_02(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D", "E", "F"])
        poll.open()
        poll.add_vote([5, 4, 0, 2, 1, 3])
        poll.add_vote([3, 0, 5, 4, 3, 2])
        poll.add_vote([3, 3, 3, 2, 5, 3])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")

    def test_poll_03(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D", "E", "F"])
        poll.open()
        poll.add_vote([5, 4, 0, 2, 1, 3])
        poll.add_vote([3, 0, 5, 4, 3, 2])
        poll.add_vote([3, 3, 3, 2, 5, 3])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")

    def test_poll_04(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        poll.add_vote([5, 3, 2, 1])
        poll.add_vote([0, 1, 0, 1])
        poll.add_vote([3, 0, 0, 2])
        poll.add_vote([4, 2, 4, 2])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")

    def test_poll_05(self):
        poll = STAR_voting.Poll(["A", "B", "C"])
        poll.open()
        poll.add_vote([5, 3, 3])
        poll.add_vote([3, 4, 3])
        poll.add_vote([0, 1, 2])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")
        # self.assertTrue(poll.get_results()['tied'], ["B", "C"])

    def test_poll_06(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        poll.add_vote([4, 2, 5, 2])
        poll.add_vote([5, 2, 3, 0])
        poll.add_vote([2, 0, 4, 2])
        poll.add_vote([3, 1, 2, 1])
        poll.add_vote([1, 3, 1, 2])
        poll.add_vote([4, 0, 3, 3])
        poll.add_vote([3, 4, 5, 4])
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "C")

    def test_poll_07(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        poll.open()
        for i in range(50):
            poll.add_vote([5]*len(poll.get_candidates()))
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")
        # self.assertTrue(poll.get_results()['tied'], ["B", "C", "D", "E", "F", "G", "H", "I"])

    def test_poll_08(self):
        poll = STAR_voting.Poll(["A", "B", "C", "D"])
        poll.open()
        for i in range(100):
            poll.add_vote([0]*len(poll.get_candidates()))
        poll.close()
        self.assertTrue(poll.get_results()['winner'], "A")
        # self.assertTrue(poll.get_results()['tied'], ["B", "C", "D"])


if __name__ == '__main__':
    unittest.main()