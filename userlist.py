#!/usr/bin/env python3

import sys
from urllib.parse import quote

import config
import util
import linkpath

def users_list_query(sort_by="karma", run_query=True):
    sort_line = ""
    if sort_by == "postCount":
        sort_line = 'sort: {postCount: -1}'
    elif sort_by == "commentCount":
        sort_line = 'sort: {commentCount: -1}'
    else:
        sort_line = 'sort: {karma: -1}'
    query = ("""
        {
          users(input: {
            terms: {
              view: "LWUsersAdmin"
              limit: 500
              %s
            }
          }) {
            results {
              _id
              slug
              karma
              postCount
              commentCount
            }
          }
        }
    """ % sort_line)

    if not run_query:
        return query + ('''\n<a href="%s">Run this query</a>\n\n''' % (config.GRAPHQL_URL.replace("graphql", "graphiql") + "?query=" + quote(query)))
    request = util.send_query(query)
    return request.json()['data']['users']['results']


def show_users_list(sort_by, display_format):
    users = users_list_query(sort_by=sort_by, run_query=(False if display_format == "queries" else True))

    if display_format == "queries":
        result = "<pre>"
        result += users + "\n"
        result += "</pre>\n"
        return result

    result = """<!DOCTYPE html>
    <html>
    """
    result += util.show_head("Users list")
    result += "<body>\n"
    result += util.show_navbar(navlinks=[
            '''<a href="%s" title="Show all the GraphQL queries used to generate this page">Queries</a>''' % linkpath.userlist(display_format="queries")
        ])
    result += '''<div id="wrapper">'''
    result += '''<div id="content">'''

    result += ('''
        <table>
            <tr>
                <th>Username</th>
                <th>User ID</th>
                <th><a href="%s">Karma</a></th>
                <th><a href="%s">Post count</a></th>
                <th><a href="%s">Comment count</a></th>
            </tr>
    ''' % (
            linkpath.userlist(sort="karma"),
            linkpath.userlist(sort="postCount"),
            linkpath.userlist(sort="commentCount")
        )
    )

    for user in users:
        if user['slug'] is None:
            linked_user = "[deleted]"
        else:
            linked_user = '''<a href="%s">%s</a>''' % (linkpath.users(userslug=user['slug']), user['slug'])
        result += ('''
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td style="text-align: right;">%s</td>
                <td style="text-align: right;">%s</td>
                <td style="text-align: right;">%s</td>
            </tr>
        ''' % (
                linked_user,
                user['_id'],
                user['karma'],
                user['postCount'],
                user['commentCount']
            )
        )

    result += "</div>"  # content
    result += "</div>"  # wrapper
    result += "</body>"
    result += "</html>"

    return result


if __name__ == "__main__":
    arg_count = 2
    if len(sys.argv) != arg_count + 1:
        print("Unexpected number of arguments")
    else:
        print(show_users_list(sort_by=sys.argv[1], display_format=sys.argv[2]))
