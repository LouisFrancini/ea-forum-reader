#!/usr/bin/env python3

PATH_STYLE = "localhost"
# PATH_STYLE = "official"


def posts(postid, postslug="", display_format="html"):
    if PATH_STYLE == "localhost":
        if display_format == "html":
            return "./posts.php?id=" + postid
        else:
            return "./posts.php?id=" + postid + "&amp;format=" + display_format
    else:
        if display_format == "html":
            return "/posts/" + postid + "/" + postslug
        else:
            return "/posts/" + postid + "/" + postslug + "?format=" + display_format

def users(userslug, display_format="html"):
    if PATH_STYLE == "localhost":
        return "./users.php?id=" + userslug + ("&amp;format=" + display_format if display_format != "html" else "")
    else:
        return "/users/" + userslug + ("?format=" + display_format if display_format != "html" else "")

def userlist():
    if PATH_STYLE == "localhost":
        return "./userlist.php"
    else:
        return "/userlist"