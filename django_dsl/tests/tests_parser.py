from unittest import TestCase, main
from run import compile
from exceptions import CompileException


class TestParser(TestCase):

    def test_1(self):
        result = compile("key:value")
        self.assertEqual(str(result), "(AND: ('key__iexact', 'value'))")

    def test_2(self):
        result = compile("key:value and key1:value1 or key2:value2")
        self.assertEqual(str(result), "(OR: (AND: ('key__iexact', 'value'), "
                                      "('key1__iexact', 'value1')), ('key2__iexact', 'value2'))")

    def test_3(self):
        result = compile("key:value and key1:value1 and not key2:value2 ")
        self.assertEqual(str(result), "(AND: ('key__iexact', 'value'), "
                                      "('key1__iexact', 'value1'), (NOT (AND: ('key2__iexact', 'value2'))))")

    def test_4(self):
        result = compile("(key:value and key1:value1) or not key2:value2 ")
        self.assertEqual(str(result), "(OR: (AND: ('key__iexact', 'value'), ('key1__iexact', 'value1')), "
                                      "(NOT (AND: ('key2__iexact', 'value2'))))")

    def test_5(self):
        result = compile("column_name:~^value.*fin$ and key1:value1")
        self.assertEqual(str(result), "(AND: ('column_name__iregex', '^value.*fin$'), "
                                      "('key1__iexact', 'value1'))")

    def test_6(self):
        result = compile("column_name:*motif* and key1:value1")
        self.assertEqual(str(result), "(AND: ('column_name__icontains', 'motif'), ('key1__iexact', 'value1'))")

    def test_7(self):
        result = compile("column_name:debut* and key1:value1")
        self.assertEqual(str(result), "(AND: ('column_name__istartswith', 'debut'), "
                                      "('key1__iexact', 'value1'))")

    def test_8(self):
        result = compile("column_name:*fin and key1:value1")
        self.assertEqual(str(result), "(AND: ('column_name__iendswith', 'fin'), ('key1__iexact', 'value1'))")

    def test_9(self):
        result = compile("key>1")
        self.assertEqual(str(result), "(AND: ('key__gt', 1))")

    def test_10(self):
        result = compile("key<1 and key1:value1")
        self.assertEqual(str(result), "(AND: ('key__lt', 1), ('key1__iexact', 'value1'))")

    def test_11(self):
        result = compile("key<=1 and key1:value1")
        self.assertEqual(str(result), "(AND: ('key__lte', 1), ('key1__iexact', 'value1'))")

    def test_12(self):
        result = compile("key>=1 and key1:value1")
        self.assertEqual(str(result), "(AND: ('key__gte', 1), ('key1__iexact', 'value1'))")

    def test_fail_1(self):
        with self.assertRaises(CompileException):
            compile("(key:value and key1:value1)) or not key2:value2 ")

    def test_fail_2(self):
        with self.assertRaises(CompileException):
            compile("key:value and key1:")

    def test_fail_3(self):
        with self.assertRaises(CompileException):
            compile("key:value and :value1")

    def test_fail_4(self):
        with self.assertRaises(CompileException):
            compile("key1:value1 or")

    def test_fail_5(self):
        with self.assertRaises(ValueError):
            compile("key<test and key1:value1")


if __name__ == '__main__':
    main()
