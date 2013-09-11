#!/usr/bin/env python

from __future__ import print_function, division, absolute_import, unicode_literals

import getpass
import github3
import os

TOKEN_NAME = "LICECOMB_GITHUB_TOKEN"

def build_github_connection():
    github_token = os.getenv(TOKEN_NAME)
    
    if not github_token:
        print("%s not found in environment" % TOKEN_NAME)
        username = raw_input("Enter your GitHub username, or blank to try to proceed without authentication: ")
        if username:
            password = getpass.getpass()
            github_token = github3.GitHub().authorize(username, password)
            
            if github_token:
                print("Generated authentication token for licecomb: %s" % github_token)
                print()
                print("TODO Instructions for saving")
            else:
                print("Authentication failed. TODO")

    return github3.GitHub(token=github_token)

gh = build_github_connection()

def licecomb(owner, repository_names, **options):
    repositories = get_repositories(owner, repository_names)

    status = {}
    for repository in repositories:
        if options['ignore_forks'] and repository.fork:
            continue
        status[repository.name] = repository_has_license(repository)

    # Now some nasty hackery to flip the dict into itself for ease of reporting...
    for (repository_name, has_license) in list(status.iteritems()):
        status[has_license] = (status.get(has_license, []) + [repository_name])

    return status


def get_repositories(owner, repository_names):
    if repository_names:
        repositories = []
        not_found = []
        for repository_name in repository_names:
            repository = gh.repository(owner, repository_name)
            if repository:
                repositories.append(repository)
            else:
                not_found.append(repository_name)
        if not_found:
            raise ValueError("Could not find repositories %s" % ", ".join(["%s/%s" % (owner, repository_name) for repository_name in not_found]))
    else:
        repositories = list(gh.iter_user_repos(login=owner))

    return repositories


def repository_has_license(repository):
    return bool(repository.contents("LICENSE") or repository.contents("LICENSE.md"))


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Check GitHub repositories for license files")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--ignore-forks", action="store_true")
    parser.add_argument("owner", nargs=1)
    parser.add_argument("repository_names", nargs="*", metavar="repository")
   
    args = parser.parse_args()

    args.owner = args.owner[0] # http://docs.python.org/2.7/library/argparse.html#nargs - "Note that nargs=1 produces a list of one item."

    status = licecomb(**vars(args))

    if args.verbose and True in status:
        for repository_name in status[True]:
            print("SUCCESS: Found a license file in %s/%s" % (args.owner, repository_name))
    if False in status:
        for repository_name in status[False]:
            print("ERROR: Could not find a license file in %s/%s" % (args.owner, repository_name), file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
