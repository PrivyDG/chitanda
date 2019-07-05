from snowball.util import register


@register('!help')
def call(bot, author, message):
    return 'https://github.com/dzlr/snowball/blob/master/README.md'
