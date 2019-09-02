#!/usr/bin/env python3
# coding: utf-8

import argparse, logging, json, pyexcel
import databaseSchema as dbs

parser = argparse.ArgumentParser(argument_default=False, description='Export database to various spreadsheet formats.')
parser.add_argument('database', help='The location of the database.')
parser.add_argument('project', help='The name of the crawling project.')
parser.add_argument('spider', help='The name of the spider.')
parser.add_argument('job', help='The id of the job.')
parser.add_argument('destination', help='The file name to use for the exported data.')
parser.add_argument('--verbose', '-v', action='count', default=0, help='Turn on verbose mode.') # TODO
parser.add_argument('--log', help='Logfile path. If omitted, stdout is used.')
parser.add_argument('--debug', '-d', action='store_true', help='Log all messages including debug.') # TODO
parser.add_argument('--quiet', '-q', action='store_true', help='Don\'t output any messages.') # TODO
parser.add_argument('--all', '-a', action='store_true', help='Export to all supported formats.')
parser.add_argument('--json', action='store_true', help='Export to JSON.')
parser.add_argument('--csv', action='store_true', help='Export to CSV.') # TODO
parser.add_argument('--tsv', action='store_true', help='Export to TSV.') # TODO
parser.add_argument('--xml', action='store_true', help='Export to XML.') # TODO
parser.add_argument('--xlsx', action='store_true', help='Export to Microsoft Office Excel (min. 2007) XML.')
parser.add_argument('--xls', action='store_true', help='Export to Microsoft Office Excel.')
parser.add_argument('--ods', action='store_true', help='Export to Libre Office / Open Office / Star Office Open Document Spreadsheet.')
parser.add_argument('--separator', help='The separator to use.') # TODO
parser.add_argument('--beautify', help='Beautify output.')
args = parser.parse_args()

logging.addLevelName(99, "SILENT")
logging.addLevelName(15, "DETAIL")

if args.debug:
    loglevel = logging.DEBUG
elif args.verbose:
    loglevel = logging.DETAIL
elif args.quiet:
    loglevel = logging.SILENT
else:
    loglevel = logging.INFO

if args.log:
    logging.basicConfig(filename=args.log, filemode='a', level=loglevel)
else:
    logging.basicConfig(level=loglevel)

class OutputFormat(object):
    '''represents an output format'''
    def __init__(self, format):
        self.format = format
        self.filename = '{dest}.{format}'.format(dest=args.destination, format=self.format)

writers = []
results = []

if args.all or args.json:
    writers.append(OutputFormat('json'))
if args.all or args.csv:
    logging.debug('Adding CSV writer')
    writers.append(OutputFormat('csv'))
if args.all or args.tsv:
    logging.debug('Adding TSV writer')
    writers.append(OutputFormat('tsv'))
if args.all or args.xml:
    logging.debug('Adding XML writer')
    of = OutputFormat('xml')
    # TODO
    writers.append(of)
if args.all or args.xlsx:
    logging.debug('Adding XLSX writer')
    writers.append(OutputFormat('xlsx'))
if args.all or args.xls:
    logging.debug('Adding XLS writer')
    writers.append(OutputFormat('xls'))
if args.all or args.ods:
    logging.debug('Adding ODS writer')
    writers.append(OutputFormat('ods'))

session = dbs.init_session(args.database)
items = session.query(dbs.Item).filter(dbs.Item.job_id==args.job)
first_line = True
for item in items:
    if first_line:
        logging.debug('Defining fieldnames')
        fieldnames = set()
        for field in item.fields:
            fieldnames.add(field.name)
        fieldnames = sorted(list(fieldnames))
        # for writer in writers:
        #     if writer.format == 'xml':
        #         logging.debug('Writing XML header')
        #         ...
        #         # does this need a header?
        first_line = False
    # build dict
    logging.debug('Building row')
    row = {}
    for field in item.fields:
        if field.name not in fieldnames:
            logging.error('Fieldnames not always the same!')
            close_Writers()
            session.close()
            exit()
        row[field.name] = field.value
    results.append(row)
    # for writer in writers:
    #     if writer.format == 'xml':
    #         logging.debug('Writing row to XML')
    #         writer.writer.export_item(row)
for writer in writers:
    if writer.format == 'json':
        logging.debug('Saving JSON')
        with open(writer.filename, 'w', encoding='utf-8') as jsonfile:
            if args.beautify:
                json.dump({'items':results}, jsonfile, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
            else:
                json.dump({'items':results}, jsonfile, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
    elif writer.format == 'csv':
        logging.debug('Saving CSV')
        pyexcel.save_as(records=results, dest_file_name=writer.filename)
    elif writer.format == 'tsv':
        logging.debug('Saving TSV')
        pyexcel.save_as(records=results, dest_file_name=writer.filename)
    # elif writer.format == 'xml':
    #     logging.debug('Saving XML')
    #     writer.writer.finish_exporting()
    elif writer.format == 'xlsx':
        logging.debug('Saving XLSX')
        pyexcel.save_as(records=results, dest_file_name=writer.filename)
    elif writer.format == 'xls':
        logging.debug('Saving XLS')
        pyexcel.save_as(records=results, dest_file_name=writer.filename)
    elif writer.format == 'ods':
        logging.debug('Saving ODS')
        pyexcel.save_as(records=results, dest_file_name=writer.filename)
logging.debug('Closing writers')
session.close()
logging.info('DONE!')
