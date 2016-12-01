# easyprog-v0.05

Utils for small programs' writting.

It currently works with a makefile, I DON'T like this,</br>
but it is really the most simple approch to achieve my</br>
goal for quick writing and testing small programs. </br>
I may replace makefile with something else someday.

It will support c,c++,python and java. But only c++ and python
are avaliable so far.

## progconf.py
Configure a programming environment.

To init a c++ programming environment:

```shell
python progconf.py name.cpp -t # generate a tempalte source file with '-t' option
make create                    # create source file with a template
make edit                      # edit source file
make                           # compile
make excute                    # run
```

## progfeed.py
Configure a testing environment.

To init a testing environment for binary a.out:

```shell
python progfeed.py -s ex=./a.out -s if=input # specify you excute command
python progfeed.py                           # run test
python progfeed.py -s pat=[1]+1              # tell `progfeed` how to parse the input file
python progfeed.py -s ic=1-$                 # use all test cases in the input file
python progfeed.py --set ic=1,2,4-10         # use 1, 2 and 4-10 test cases only
```

## update.sh
update the excutables in my system.

## parser.py
parsers

## common.py
common datas

## tcfparser.py
parser a test case file into seprated cases

## TODO.md
things to do

## DONE.md
things have been done
