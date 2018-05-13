from unittest import TestCase, main
from run import compile
from exceptions import CompileException


class TestParser(TestCase):

    def test_1(self):
        result = compile("key:value")
        self.assertEqual(str(result), "(AND: ('key', 'value'))")

    def test_2(self):
        result = compile("key:value and key1:value1 or key2:value2")
        self.assertEqual(str(result), "(OR: (AND: ('key', 'value'), ('key1', 'value1')), ('key2', 'value2'))")

    def test_3(self):
        result = compile("key:value and key1:value1 and not key2:value2 ")
        self.assertEqual(str(result), "(AND: ('key', 'value'), ('key1', 'value1'), (NOT (AND: ('key2', 'value2'))))")

    def test_4(self):
        result = compile("(key:value and key1:value1) or not key2:value2 ")
        self.assertEqual(str(result), "(OR: (AND: ('key', 'value'), ('key1', 'value1')), (NOT (AND: ('key2', 'value2'))))")

    def test_5(self):
        result = compile("classification_text:~^value.*fin$ and key1:value1")
        self.assertEqual(str(result), "(AND: ('classification_text__iregex', '^value.*fin$'), ('key1', 'value1'))")

    def test_6(self):
        result = compile("classification_text:*motif* and key1:value1")
        self.assertEqual(str(result), "(AND: ('classification_text__icontains', 'motif'), ('key1', 'value1'))")

    def test_7(self):
        result = compile("classification_text:debut* and key1:value1")
        self.assertEqual(str(result), "(AND: ('classification_text__istartswith', 'debut'), ('key1', 'value1'))")

    def test_8(self):
        result = compile("classification_text:*fin and key1:value1")
        self.assertEqual(str(result), "(AND: ('classification_text__iendswith', 'fin'), ('key1', 'value1'))")

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


if __name__ == '__main__':
    main()
