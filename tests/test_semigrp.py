import unittest
import sys
import os
from semigroups import (Semigroup, Transformation, Bipartition,
                        FullTransformationMonoid, CayleyGraph,
                        FpSemigroup, FpMonoid, TransDirectProduct,
                        SymmetricGroup, TransDihedralGroup, PartialPerm)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.insert(1, path)
del path


class TestSemigroup(unittest.TestCase):
    def test_init(self):
        Semigroup(-1)
        Semigroup(Transformation([1, 0, 1]), Transformation([0, 0, 0]))

        with self.assertRaises(ValueError):
            Semigroup()

        with self.assertRaises(TypeError):
            Semigroup(Bipartition([1, -1], [2], [-2]), Transformation([0, 1]))

        with self.assertRaises(TypeError):
            Semigroup({2, 3})

    def test_right_cayley_graph(self):
        Semigroup(-1).right_cayley_graph()
        self.assertTrue(isinstance(Semigroup(-1).right_cayley_graph(),
                                   CayleyGraph))

    def test_left_cayley_graph(self):
        Semigroup(Transformation([0, 1])).right_cayley_graph()
        self.assertTrue(isinstance(Semigroup(-1).left_cayley_graph(),
                                   CayleyGraph))

    def test_IsomorphicTransSemigroup(self):
        S = FpMonoid("ab",[["aa","a"],["bb","b"],["ab","ba"]])
        self.assertEqual(sorted(list(Semigroup(Transformation([0, 1, 2, 3]),
                                               Transformation([0, 3, 0, 3]),
                                               Transformation([3, 1, 1, 3])))),
                         sorted(list(S.IsomorphicTransSemigroup())))

    def test_size(self):
        self.assertEqual(SymmetricGroup(4).size(), 24)
        self.assertEqual(SymmetricGroup(9).size(), 362880)
        self.assertEqual(SymmetricGroup(10).size(), 3628800)
        C4 = Semigroup(Transformation([1, 2, 3, 0]))
        self.assertEqual(C4.size(), 4)
        self.assertEqual(TransDirectProduct(C4,C4).size(), 16)
        M = FpMonoid("ab", [["aaaa", "a"], ["bb", "b"], ["ab", "ba"]])
        self.assertEqual(M.size(), 8)
        T = FpMonoid("ab", [["a^6", "1"], ["bb", "aaa"], ["aba", "b"]])
        self.assertEqual(T.size(), 12)

    def test_contain_1(self):
        self.assertTrue(1 in Semigroup(-1))

        S1 = Semigroup(Transformation([2, 3, 2, 5, 6, 5, 8, 9, 8, 10, 10]),
                       Transformation([3, 4, 5, 6, 7, 8, 9, 7, 10, 9, 10]))

        self.assertTrue(Transformation([5, 6, 5, 8, 9, 8, 10, 9, 10, 10, 10])
                        in S1)
        self.assertTrue(Transformation([10, 10, 10, 10, 10,
                                        10, 10, 10, 10, 10, 10]) in S1)

        self.assertFalse(Transformation([0, 1, 2, 3, 4,
                                         5, 6, 7, 8, 9, 10]) in S1)

        S2 = FpMonoid("ab", [["aa", "a"], ["bb", "b"], ["ab", "ba"]])
        S2 = S2.IsomorphicTransSemigroup()

        self.assertTrue(all(t in S2.copy() for t in S2))
        self.assertFalse(Transformation([0]) in S2)

        S3 = Semigroup(Transformation([0, 1, 1, 1]),
                       Transformation([0, 1, 2, 1]))
        elements = list(S3)
        for t in FullTransformationMonoid(4):
            if t in elements:
                self.assertTrue(t in S3.copy())
            else:
                self.assertFalse(t in S3.copy())

        S4 = Semigroup(Transformation([1, 2, 3, 0]))
        elements = list(S4)
        for t in FullTransformationMonoid(4):
            if t in elements:
                self.assertTrue(t in S4.copy())
            else:
                self.assertFalse(t in S4.copy())

        S5 = Semigroup(Transformation([0, 3, 4, 3, 4, 6, 6]),
                       Transformation([3, 5, 1, 6, 3, 1, 3]),
                       Transformation([4, 1, 5, 3, 6, 5, 6]))

        self.assertTrue(Transformation([0, 3, 4, 3, 4, 6, 6]) in S5.copy())
        self.assertTrue(Transformation([3, 5, 1, 6, 3, 1, 3]) in S5.copy())
        self.assertTrue(Transformation([4, 1, 5, 3, 6, 5, 6]) in S5.copy())
        self.assertTrue(Transformation([6, 3, 6, 3, 6, 6, 6]) in S5.copy())
        self.assertTrue(Transformation([3, 6, 3, 6, 3, 3, 3]) in S5.copy())
        self.assertTrue(Transformation([4, 3, 6, 3, 6, 6, 6]) in S5.copy())
        self.assertTrue(Transformation([6, 1, 5, 3, 6, 5, 6]) in S5.copy())

        self.assertFalse(Transformation([4, 3, 3, 3, 6, 6, 6]) in S5.copy())
        self.assertFalse(Transformation([3, 5, 6, 6, 3, 1, 3]) in S5.copy())
        self.assertFalse(Transformation([6, 1, 3, 3, 6, 5, 6]) in S5.copy())
        self.assertFalse(Transformation([3, 6, 6, 6, 3, 3, 3]) in S5.copy())
        self.assertFalse(Transformation([6, 3, 3, 3, 6, 6, 6]) in S5.copy())
        self.assertFalse(Transformation([4, 1, 3, 3, 6, 5, 6]) in S5.copy())

        S6 = TransDirectProduct(S3, S5)
        self.assertTrue(all(t in S6.copy() for t in S6))

    def test_contain_2(self):
        S7 = Semigroup(Transformation([0, 1, 1]))
        self.assertTrue(all(t in S7.copy() for t in S7))

        S8 = FpMonoid("ab", [["aaaa", "a"], ["bb", "b"], ["ab", "ba"]])
        S8 = S8.IsomorphicTransSemigroup()
        for t in S8:
            self.assertTrue(t in S8.copy())

        S9 = SymmetricGroup(9)
        self.assertTrue(S9[10000] in S9.copy())

        S10 = TransDihedralGroup(4)
        for perm in S10:
            self.assertTrue(perm in S10.copy())

        S11 = Semigroup([Transformation([3, 5, 1, 3, 1, 4]),
                         Transformation([3, 1, 2, 3, 4, 5]),
                         Transformation([0, 3, 3, 3, 3, 3])])

        self.assertTrue(Transformation([3, 5, 1, 3, 1, 4]) in S11.copy())
        self.assertTrue(Transformation([3, 1, 4, 3, 4, 5]) in S11.copy())

        self.assertFalse(Transformation([0, 5, 1, 3, 1, 4]) in S11.copy())
        self.assertFalse(Transformation([0, 1, 2, 3, 4, 5]) in S11.copy())
        self.assertFalse(Transformation([0, 1, 4, 3, 4, 5]) in S11.copy())
        self.assertFalse(Transformation([0, 4, 5, 3, 5, 1]) in S11.copy())

        S12 = Semigroup([Transformation([0, 0, 5, 3, 6, 2, 1]),
                         Transformation([0, 0, 2, 3, 6, 5, 1]),
                         Transformation([0, 1, 2, 0, 4, 5, 6])])

        for g in S12:
            self.assertTrue(g in S12.copy())

        self.assertFalse(Transformation([0, 1, 2, 3, 4, 5, 6]) in S12.copy())
        self.assertFalse(Transformation([0, 1, 0, 3, 4, 0, 6]) in S12.copy())
        self.assertFalse(Transformation([0, 1, 0, 0, 4, 0, 6]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 3, 0, 0, 0]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 0, 0, 0, 0]) in S12.copy())
        self.assertFalse(Transformation([0, 1, 5, 3, 4, 2, 6]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 0, 1, 0, 0]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 0, 6, 0, 1]) in S12.copy())
        self.assertFalse(Transformation([0, 1, 5, 0, 4, 2, 6]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 3, 6, 0, 1]) in S12.copy())
        self.assertFalse(Transformation([0, 0, 0, 3, 1, 0, 0]) in S12.copy())

        S13 = S12._big_trans_semilattice(15)
        T = Transformation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(T in S13.copy())
        T = Transformation([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(T in S13.copy())
        T = Transformation([0, 1, 0, 3, 4, 5, 6, 7, 0, 9, 0, 11, 0, 13, 0])
        self.assertTrue(T in S13.copy())

        T = Transformation([2, 1, 2, 3, 4, 5, 6, 7, 2, 9, 2, 11, 2, 13, 2])
        self.assertFalse(T in S13.copy())

        S14 = S12._big_trans_semilattice(20)
        T = Transformation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(T in S14.copy())
        T = Transformation([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                            0, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.assertTrue(T in S14.copy())
        T = Transformation([0, 0, 0, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.assertTrue(T in S14.copy())

        T = Transformation([2, 1, 2, 3, 4, 5, 6, 7, 2, 9,
                            2, 11, 2, 13, 2, 2, 2, 2, 2, 2])
        self.assertFalse(T in S14.copy())

        S15 = Semigroup(PartialPerm([0, 2, 3], [2, 1, 4], 5))
        S15.enumerate()
        self.assertTrue(PartialPerm([0, 2, 3], [2, 1, 4], 5) in S15)
        self.assertTrue(PartialPerm([0], [1], 5) in S15)

        S16 = Semigroup(Transformation([1, 1, 1, 2]))
        S16.enumerate()
        self.assertTrue(Transformation([1, 1, 1, 2]) in S16)
        self.assertTrue(Transformation([1, 1, 1, 1]) in S16)

class TestOtherFunctions(unittest.TestCase):
    def test_FullTransformationMonoid(self):
        self.assertEqual(FullTransformationMonoid(3)[7],
                         Semigroup(Transformation([1, 0, 2]),
                                   Transformation([0, 0, 2]),
                                   Transformation([2, 0, 1]))[7])
        self.assertEqual(FullTransformationMonoid(2)[5],
                         Semigroup(Transformation([0, 0]),
                                   Transformation([0, 1]))[5])
        self.assertEqual(FullTransformationMonoid(1)[0],
                         Semigroup(Transformation([0]))[0])

        with self.assertRaises(TypeError):
            FullTransformationMonoid(2.5)

        with self.assertRaises(ValueError):
            FullTransformationMonoid(-7)

if __name__ == "__main__":
    unittest.main()
