#!/usr/bin/python3
import math
import flask
import argparse
import datetime
import itertools
import json
import os
import sys
import datetime

app = flask.Flask("IP-Listener")
app.config["IP_MAP"] = dict()

TIMEDELTA = datetime.timedelta(days=1)
MAP_FILE_PATH = "/app/data/blockmap.conf"

def remove_stale_ips():
    '''Remove IPs older than 1 day'''

    keys = list(app.config["IP_MAP"].keys())
    for key in keys:
        value = app.config["IP_MAP"].get(key)
        if not value:
            continue # is already gone
        elif datetime.datetime.now() - value > TIMEDELTA:
            del app.config["IP_MAP"][key]

def dump_map():
    '''Dump a nginx map with the current IP whitelist'''

    start_str = "map $http_x_real_ip $valid_real_ip {\n"
    default_str = "    default 0;\n"
    template_ip_str = '    "{}" 1;\n';
    end_str = "}"

    # write map file #
    with open(MAP_FILE_PATH, "w") as f:

        f.write(start_str)
        f.write(default_str)
        for ip in app.config["IP_MAP"].keys():
            f.write(template_ip_str.format(ip))
        f.write(end_str)

@app.route('/am-i-unlocked')
def get_status():
    '''Return information if an IP is unlocked and until when'''

    ip = flask.request.headers.get("X-Real-IP") or flask.request.headers.get("X-Real-IP")

    if not ip:
        print("WARNING: Using request.remote_addr because no header is present", file=sys.stderr)
        ip = flask.request.remote_addr

    date = app.config["IP_MAP"].get(ip)
    if date:
        delta = datetime.datetime.now() - date + TIMEDELTA
        timedelta_str = str(datetime.timedelta(seconds=math.ceil(delta.total_seconds())))
        return (f"Network Unlocked ({timedelta_str} remaining)")
    else:
        return (f"Network Locked")

    return (json.dumps(app.config["IP_MAP"], indent=2, default=str, sort_keys=True), 200)


@app.route('/list')
def list_ips():
    '''Return current IP map'''

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["APP_SECRET"]:
        return ("Nope", 403)

    return (json.dumps(app.config["IP_MAP"], indent=2, default=str, sort_keys=True), 200)

@app.route('/activate')
def activate():

    secret = flask.request.args.get("secret")
    if not secret or secret != app.config["APP_SECRET"]:
        return ("Nope", 403)

    # get X-Real-IP or X-Forwarded-For #
    ip = flask.request.headers.get("X-Real-IP") or flask.request.headers.get("X-Real-IP")

    if not ip:
        print("WARNING: Using request.remote_addr because no header is present", file=sys.stderr)
        ip = flask.request.remote_addr

    # unlock #
    print("Unlocking IP:", ip)
    app.config["IP_MAP"].update({ ip : datetime.datetime.now() })
    remove_stale_ips()
    dump_map()

    return ("", 204)

def create_app():
    '''Call to init all'''
    
    app.config["APP_SECRET"] = os.environ["APP_SECRET"]
    dump_map()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Start IP Listener',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--interface', default="localhost",
            help='Interface on which flask (this server) will take requests on')
    parser.add_argument('--port', default="5000",
            help='Port on which flask (this server) will take requests on')

    args = parser.parse_args()

    with app.app_context():
        create_app()
   
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host=args.interface, port=args.port)
