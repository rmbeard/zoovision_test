# coding=utf-8



print "I'm import_test.py and my name is: " + __name__

print "Importing module_test"
import Chapter2.experiments.module_test

print "Calling function1 from within import_test"
Chapter2.experiments.module_test.function1()
