# -*- coding: utf-8 -*-

from morph import morph

#--------------------------------------------------decorators ----------------------------------------------------------
def correct_length(function):
    result = []
    def wrapped(*args):
        for arg in args:
            if len(arg) > 0:
                result.append(function(arg))
            else:
                print "word is not correct", arg
        return result
    return wrapped

def correct_parse_symbol(function):
    def wrapped(*args):
        if len(args) > 2:
            raise "need one parse symbol"
        else:
            if isinstance(args[1], (unicode, str)):
                try:
                    function(args[0], args[1])
                except:
                    raise Exception.message
    return wrapped

@correct_length
def normal_form(line):
    return morph.parse(line)

@correct_parse_symbol
def normal_forms_parse(lines, parse_symbol):
    return [normal_form(line) for line in lines.split(parse_symbol)]

def normal_forms(lines):
    return [normal_form(line) for line in lines]
