# -*- coding: utf-8 -*-

import argparse


def serverpool_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--worker', required=True, help="Define the number of worker for the pool.")

    args = parser.parse_args()
    return args


def client_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-KS', '--killserver', action='store_true', help='Kill the running server pool.')
    parser.add_argument('-CQ', '--cleanqueue', action='store_true', help='Clean the redis queue.')

    parser.add_argument('-ls', '--list', action='store_true', help='See the list task running.')

    run_parser = parser.add_subparsers(dest='mode').add_parser('run', help='task to run.')
    run_parser.add_argument('command', help='Command to run', nargs=argparse.REMAINDER)
    run_parser.add_argument('-f', '--file', help="Get list of command from file.")
    return parser.parse_args()
