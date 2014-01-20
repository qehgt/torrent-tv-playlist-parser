#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def get_all_lines(file_name):
    with open(file_name, "r") as f:
        all_lines = [line.replace('\n', '') for line in f.readlines()[1:]] # skip the first line + remove all '\n'

    return all_lines


class Channel:
    def __init__(self, description, url):
        self.desc = description
        self.url = url

    def __str__(self):
        return '[\'' + self.desc + '\', \'' + self.url + '\']'

    def get_group(self, s):
        start = s.find('(')
        end   = s.find(')')

        if start == -1 or end == -1:
            return None, ""

        return s[start+1:end], s[end+1:]

    def get_groups(self):
        groups = []

        s = self.desc

        curr_group, s = self.get_group(s)
        groups.append(curr_group)
        while True:
            curr_group, s = self.get_group(s)
            if curr_group != None:
                groups.append(curr_group)
            else:
                break

        return groups



def normalize_group_name(name):
    synonyms = {'Украина' : set(['укр', 'Украина', 'Ukraine', 'украина'])}
    for key, value in synonyms.items():
        if name in value:
            return key

    return name


def create_groups(channels):
    by_groups = {}

    for ch in channels:
        groups = [normalize_group_name(x) for x in ch.get_groups()]
        for gr in groups:
            g = by_groups.setdefault(gr, [])
            g.append(ch)

    return by_groups


def save_one_group(group, channels):
    header = '#EXTM3U\n'
    with open(str(group) + '.m3u', 'wb') as f:
        f.write(header)
        for ch in channels:
            f.write(ch.desc + '\n')
            f.write(ch.url  + '\n')
        

def save_by_groups(channels):
    by_groups = create_groups(channels)

    for gr in by_groups.keys():
        save_one_group(gr, by_groups[gr])



def usage():
    print 'Usage:'
    print 'create_groups_for_torrent_tv.py <torrent-tv.m3u>'


def main():
    # input arguments
    if len(sys.argv) <= 1:
        usage()
        sys.exit(1)

    lines = get_all_lines(sys.argv[1])

    # generate pairs from the list
    channels = []
    for d, u in zip(lines[0::2], lines[1::2]):
        channels.append(Channel(d, u))

    save_by_groups(channels)


if __name__ == "__main__":
    main()
