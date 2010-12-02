import cgi

from simpytmpl import filters


class HTML(filters.Literal):
    pass


class HTMLFilter(filters.SimpleFilter):
    filter_type = HTML
    escape = cgi.escape
