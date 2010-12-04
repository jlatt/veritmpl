#!/usr/bin/env python
if __name__ == '__main__':
    import sys

    import templates


    t = templates.Main(
        title='This is my awesome page!',
        body=templates.Default(
            heading='Welcome to my template language.',
            )
        )
    t(sys.stdout)
