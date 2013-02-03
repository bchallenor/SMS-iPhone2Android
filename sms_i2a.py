#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from xml.sax.saxutils import quoteattr

def readSMSdb(dbfile):
    import sqlite3
    sms = []
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute('SELECT h.id as addr, m.date + 978307200 as date, m.text, is_from_me FROM message m INNER JOIN handle  h ON h.rowid = m.handle_id WHERE m.text IS NOT NULL')
    for sms_addr, sms_date, sms_body, sms_is_from_me in c.fetchall():
        if sms_addr: sms_addr = sms_addr.encode('utf8')
        if sms_body:
            sms_body = sms_body.encode('utf8')
        else:
            sms_body = ""
        sms.append((sms_addr, sms_date, sms_body, sms_is_from_me))
    return sms

def output2File(data, output_file):
    f = open(output_file,'w')
    f.write("""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
    <?xml-stylesheet type="text/xsl" href="sms.xsl"?>
    <smses count="%s">""" % len(data))
    for addr, date, body, is_from_me in data:
        # type 1 for received, 2 for sent
        typ = 2 if is_from_me == 1 else 1
        f.write("""<sms protocol="0" address=%s date="%d000" type="%s" subject="null" body=%s toa="null" sc_toa="null" service_center="null" read="1" status="-1" locked="0" readable_date="" contact_name="(Unknown)" />\n""" % (quoteattr(addr), date, typ, quoteattr(body)))
    f.write("</smses>\n")
    f.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert SMS from iPhone backup to Android SMS Backup")
    parser.add_argument('--smsdb',dest = "smsdb", help = "Path of SMS sqlite file.", required=True)
    parser.add_argument('--output',dest = "output", help = "filename of output", required=True)
    args =  parser.parse_args()
    d = readSMSdb(args.smsdb)
    output2File(d,args.output)

