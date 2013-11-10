#!/usr/bin/env python
"""
Takes the existing database (as indicated by the alchemy configuration file) and creates
a dump CSV file with the appropriate columns as needed for the disambiguation:

  patent doc number, main class, sub class, inventor first name, inventor middle name, inventor last name,
  city, state, zipcode, country, assignee
"""
import codecs
from lib import alchemy
from lib.assignee_disambiguation import get_assignee_id
from lib.handlers.xml_util import normalize_utf8
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy import extract
from datetime import datetime
import sys

gyear = sys.argv[1]
print gyear

def dump(doctype='grant'):
    # get patents as iterator to save memory
    # use subqueryload to get better performance by using less queries on the backend:
    # --> http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading
    if doctype == 'application':
        patents = (p for p in alchemy.appsession.query(alchemy.schema.App_Application).filter(extract('year', alchemy.schema.App_Application.date) == gyear).options(subqueryload('rawinventors'), subqueryload('rawassignees'), subqueryload('classes')).yield_per(1))
    else:
        patents = (p for p in alchemy.grantsession.query(alchemy.schema.Patent).filter(extract('year', alchemy.schema.Patent.date) == gyear).options(subqueryload('rawinventors'), subqueryload('rawassignees'), subqueryload('classes')).yield_per(1))

    # create CSV file row using a dictionary. Use `ROW(dictionary)`

    ROW = lambda x: u'{name_first}\t{name_middle}\t{name_last}\t{number}\t{mainclass}\t{subclass}\t{city}\t{state}\t{country}\t{assignee}\t{rawassignee}\n'.format(**x)

    insert_rows = []

    i = 0
    for patent in patents:
        i += 1
        if i % 100000 == 0:
          print i, datetime.now()
        try:
          # create common dict for this patent
          loc = patent.rawinventors[0].rawlocation
          mainclass = patent.classes[0].mainclass_id if patent.classes else ''
          subclass = patent.classes[0].subclass_id if patent.classes else ''
          row = {'number': patent.number,
                 'mainclass': mainclass,
                 'subclass': subclass,
                 'state': loc.state if loc else '',
                 'country': loc.country if loc else '',
                 'city': loc.city if loc else '',
                 }
          row['assignee'] = get_assignee_id(patent.assignees[0]) if patent.assignees else ''
          row['rawassignee'] = get_assignee_id(patent.rawassignees[0]) if patent.rawassignees else ''
          # generate a row for each of the inventors on a patent
          for ri in patent.rawinventors:
              namedict = {'name_first': ri.name_first}
              raw_name = ri.name_last.split(' ')
              # name_last is the last space-delimited word. Middle name is everything before that
              name_middle, name_last = ' '.join(raw_name[:-1]), raw_name[-1]
              namedict['name_middle'] = name_middle
              namedict['name_last'] = name_last
              tmprow = row.copy()
              tmprow.update(namedict)
              newrow = normalize_utf8(ROW(tmprow))
              with codecs.open('disambiguator.csv', 'a', encoding='utf-8') as csv:
                  csv.write(newrow)
        except Exception as e:
          print e
          continue
