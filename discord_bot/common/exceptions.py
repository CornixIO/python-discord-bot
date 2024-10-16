class TooManyRequests(Exception):
    def __init__(self, response_json, url):
        super().__init__(response_json)
        self.response_json = response_json
        self.url = url


class DiscordMissingAccess(Exception):
    pass


class DiscordUnknownChannel(Exception):
    pass


class DiscordUnauthorized(Exception):
    pass


CODE_TO_EXCEPTION = {
    50001: DiscordMissingAccess,
    50007: DiscordUnauthorized,
    10003: DiscordUnknownChannel
}
