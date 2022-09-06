import sys, os

def handler(file_name):
        working_file =  file_name[0] + '_Output.wrk'
        output_file = open(working_file, 'w')
        with open(file_name[0]+'.txt', 'r') as source:
            source_text = source.read()
        return source_text, output_file