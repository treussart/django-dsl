from unittest import TestCase, main
from run import compile_expr
from exceptions import CompileException


class TestParser(TestCase):
    def test_1(self):
        result = compile_expr("key:value")
        self.assertEqual(str(result), "(AND: ('key__iexact', 'value'))")

    def test_2(self):
        result = compile_expr("key:value and key1:value1 or key2:value2")
        self.assertEqual(
            str(result),
            "(OR: (AND: ('key__iexact', 'value'), "
            "('key1__iexact', 'value1')), ('key2__iexact', 'value2'))",
        )

    def test_3(self):
        result = compile_expr("key:value and key1:value1 and not key2:value2 ")
        self.assertEqual(
            str(result),
            "(AND: ('key__iexact', 'value'), "
            "('key1__iexact', 'value1'), (NOT (AND: ('key2__iexact', 'value2'))))",
        )

    def test_4(self):
        result = compile_expr("(key:value and key1:value1) or not key2:value2 ")
        self.assertEqual(
            str(result),
            "(OR: (AND: ('key__iexact', 'value'), ('key1__iexact', 'value1')), "
            "(NOT (AND: ('key2__iexact', 'value2'))))",
        )

    def test_5(self):
        result = compile_expr("column_name:~^value.*fin$ and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('column_name__iregex', '^value.*fin$'), "
            "('key1__iexact', 'value1'))",
        )

    def test_6(self):
        result = compile_expr("column_name:*motif* and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('column_name__icontains', 'motif'), ('key1__iexact', 'value1'))",
        )

    def test_7(self):
        result = compile_expr("column_name:debut* and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('column_name__istartswith', 'debut'), "
            "('key1__iexact', 'value1'))",
        )

    def test_8(self):
        result = compile_expr("column_name:*fin and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('column_name__iendswith', 'fin'), ('key1__iexact', 'value1'))",
        )

    def test_9(self):
        result = compile_expr("key>1")
        self.assertEqual(str(result), "(AND: ('key__gt', 1))")

    def test_10(self):
        result = compile_expr("key<1 and key1:value1")
        self.assertEqual(
            str(result), "(AND: ('key__lt', 1), ('key1__iexact', 'value1'))"
        )

    def test_11(self):
        result = compile_expr("key<=1 and key1:value1")
        self.assertEqual(
            str(result), "(AND: ('key__lte', 1), ('key1__iexact', 'value1'))"
        )

    def test_12(self):
        result = compile_expr("key>=1 and key1:value1")
        self.assertEqual(
            str(result), "(AND: ('key__gte', 1), ('key1__iexact', 'value1'))"
        )

    def test_9_1(self):
        result = compile_expr("key>2018-05-04")
        self.assertEqual(
            str(result), "(AND: ('key__date__gt', datetime.date(2018, 5, 4)))"
        )

    def test_10_1(self):
        result = compile_expr("key<2018-05-04 and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('key__date__lt', datetime.date(2018, 5, 4)), "
            "('key1__iexact', 'value1'))",
        )

    def test_11_1(self):
        result = compile_expr("key<=2018-05-04 and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('key__date__lte', datetime.date(2018, 5, 4)), "
            "('key1__iexact', 'value1'))",
        )

    def test_12_1(self):
        result = compile_expr("key>=2018-05-04 and key1:value1")
        self.assertEqual(
            str(result),
            "(AND: ('key__date__gte', datetime.date(2018, 5, 4)), "
            "('key1__iexact', 'value1'))",
        )

    def test_13(self):
        result = compile_expr("key:True")
        self.assertEqual(str(result), "(AND: ('key__isnull', True))")

    def test_14(self):
        result = compile_expr("key:False")
        self.assertEqual(str(result), "(AND: ('key__isnull', False))")

    def test_15(self):
        result = compile_expr("key:2018-05-04_2018-05-05")
        self.assertEqual(
            str(result),
            "(AND: ('key__range', (datetime.date(2018, 5, 4), datetime.date(2018, 5, 5))))",
        )

    def test_16(self):
        result = compile_expr("key:2~*.^$?{}[]|!+-éèàû")
        self.assertEqual(str(result), "(AND: ('key__iexact', '2~*.^$?{}[]|!+-éèàû'))")

    def test_17(self):
        result = compile_expr("key::1:2:3")
        self.assertEqual(str(result), "(AND: ('key__iexact', ':1:2:3'))")

    def test_18(self):
        result = compile_expr("key:True2")
        self.assertEqual(str(result), "(AND: ('key__iexact', 'True2'))")

    def test_19(self):
        result = compile_expr(r"key:\*test")
        self.assertEqual(str(result), "(AND: ('key__iexact', '*test'))")

    def test_20(self):
        result = compile_expr(r"key:test\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', 'test*'))")

    def test_21(self):
        result = compile_expr(r"key:\*test\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', '*test*'))")

    def test_21_1(self):
        result = compile_expr(r"key:\*test*")
        self.assertEqual(str(result), "(AND: ('key__istartswith', '*test'))")

    def test_21_2(self):
        result = compile_expr(r"key:*test\*")
        self.assertEqual(str(result), "(AND: ('key__iendswith', 'test*'))")

    def test_22(self):
        result = compile_expr(r"key:\~test")
        self.assertEqual(str(result), "(AND: ('key__iexact', '~test'))")

    def test_23(self):
        result = compile_expr(r"key:\~*test\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', '~*test*'))")

    def test_24(self):
        result = compile_expr(r"key:\*test\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', '*test*'))")

    def test_25(self):
        result = compile_expr(r"key:*te\*st\*")
        self.assertEqual(str(result), r"(AND: ('key__iendswith', 'te\\*st*'))")

    def test_26(self):
        result = compile_expr(r"key:\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', '*'))")

    def test_27(self):
        result = compile_expr(r"key:\*\*")
        self.assertEqual(str(result), "(AND: ('key__iexact', '**'))")

    def test_28(self):
        result = compile_expr(r"key:*")
        self.assertEqual(str(result), "(AND: ('key__icontains', ''))")

    def test_29(self):
        result = compile_expr(r"key:\~test*")
        self.assertEqual(str(result), "(AND: ('key__istartswith', '~test'))")

    def test_fail_1(self):
        with self.assertRaises(CompileException):
            compile_expr("(key:value and key1:value1)) or not key2:value2 ")

    def test_fail_2(self):
        with self.assertRaises(CompileException):
            compile_expr("key:value and key1:")

    def test_fail_3(self):
        with self.assertRaises(CompileException):
            compile_expr("key:value and :value1")

    def test_fail_4(self):
        with self.assertRaises(CompileException):
            compile_expr("key1:value1 or")

    def test_fail_5(self):
        with self.assertRaises(CompileException):
            compile_expr("key<test and key1:value1")

    def test_fail_6(self):
        with self.assertRaises(CompileException):
            compile_expr("key1:valu(e1")

    def test_fail_7(self):
        with self.assertRaises(CompileException):
            compile_expr("key1:True:True")

    def test_fail_8(self):
        with self.assertRaises(CompileException):
            result = compile_expr("key1<valu:e1")
            print(result)

    def test_fail_9(self):
        with self.assertRaises(CompileException):
            result = compile_expr("key1<valu<=e1")
            print(result)


if __name__ == "__main__":
    main()
