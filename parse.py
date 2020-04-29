from collections import defaultdict

class StatefulParser:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
    def match(self, string, nestlimit=None, include_delimiter=False):
        state = 0
        overflow = 0
        matches = defaultdict(list)
        matches[0] = ['']
        begin_hawk = ''
        end_hawk = ''
        cache = ''
        for c in string:
            begin_hawk += c
            end_hawk += c
            cache += c
            if len(begin_hawk) > len(self.begin):
                begin_hawk = begin_hawk[1:]
            if len(end_hawk) > len(self.end):
                end_hawk = end_hawk[1:]

            if begin_hawk == self.begin:
                if state == nestlimit:
                    overflow += 1
                else:
                    state += 1
                matches[state].append('')
                if not include_delimiter:
                    cache = ''
                    continue
            elif end_hawk == self.end:
                if include_delimiter:
                    matches[state][-1] += cache
                if overflow:
                    overflow -= 1
                else:
                    state -= 1
                matches[state].append('')
                cache = ''
                continue

            if cache not in self.begin and cache not in self.end:
                matches[state][-1] += cache
                cache = ''

        return matches


if __name__ == "__main__":
    s = StatefulParser('{{', '}}')
    print(s.match('hello {{world}} {{world2}} cool', nestlimit=1, include_delimiter=True))