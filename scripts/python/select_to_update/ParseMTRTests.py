import getopt
import os
import re
import sys


def convert_select_to_update(ifile_path, ofile_path):
    list_of_queries = []
    f_out = open(ofile_path, "a")
    f_out.write("--disable_abort_on_error\n")

    with open(ifile_path, encoding='utf8') as f:
        read_next = False
        query = ""
        for line in f:
            if re.match("--error", line.strip(), re.IGNORECASE):
                continue
            if re.match("-- error", line.strip(), re.IGNORECASE):
                continue
            if re.match("select", line.strip(), re.IGNORECASE) or read_next:
                query = query + " " + line
                if line.strip().endswith(";"):
                    if re.search("from", query, re.IGNORECASE):
                        cut_query = re.split("from", query, maxsplit=1, flags=re.IGNORECASE)[-1].strip()
                        delimiters = "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", ";"
                        regex_pattern = '|'.join(map(re.escape, delimiters))
                        tables = re.split(regex_pattern, cut_query, flags=re.IGNORECASE)[0].strip()
                        conditions = cut_query.replace(tables, "").strip()
                        result_query = "update ut_tmp, " + tables + " set ut_tmp.a = 10 " + conditions + "\n"
                        f_out.write("create or replace table ut_tmp (a int);\n")
                        f_out.write(result_query)
                        f_out.write("drop table ut_tmp;\n")
                    read_next = False
                    query = ""
                else:
                    read_next = True
            else:
                f_out.write(line)

    f_out.write("--enable_abort_on_error\n")
    f.close()
    f_out.close()


def file_exists(fname):
    return os.path.isfile(fname)


def delete_file(fname):
    if file_exists(fname):
        os.remove(fname)


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('ParseMTRTests.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if len(sys.argv) < 2:
        print('ParseMTRTests.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ParseMTRTests.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == "" or outputfile == "":
        print('<inputfile> and <outputfile> must not be empty!')
        print('ParseMTRTests.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if not file_exists(inputfile):
        print('Input file ' + inputfile + ' not exist!')
        exit()
    if file_exists(outputfile):
        delete_file(outputfile)
    else:
        os.makedirs(os.path.dirname(outputfile), exist_ok=True)
    convert_select_to_update(inputfile, outputfile)
    print('Done!')


if __name__ == "__main__":
    main(sys.argv[1:])
