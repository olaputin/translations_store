import csv
import json
import os
import re
import shutil
import subprocess
from os import path


def init_workspace(base_dir):
    dirs = [
        base_dir,
        path.join(base_dir, 'lang_packages'),
        path.join(base_dir, 'json')
    ]
    for d in dirs:
        os.makedirs(d)


def cmd(command):
    out, _ = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()
    return out.decode('utf-8')


def update_translations():
    project_dir, _ = path.split(__file__)
    static_dir = path.join(project_dir, 'static')
    os.chdir(project_dir)
    version_pattern = re.compile(r"^origin/(?P<release>(master|release/[a-zA-Z0-9.-]+$))")

    cmd("git fetch")
    out = cmd("git for-each-ref --format='%(refname:short)' refs/remotes/origin")
    branches = [br for br in out.split('\n') if br]

    if not path.exists(static_dir):
        os.makedirs(static_dir)

    for br in branches:
        groups = version_pattern.match(br)
        if not groups:
            continue
        version = groups.group('release')
        branch_dir = path.join(static_dir, version)
        if path.exists(branch_dir):
            shutil.rmtree(branch_dir)

        init_workspace(branch_dir)

        out = cmd("git ls-tree {}:locale -r --name-status".format(br))

        for f in out.split('\n'):
            if not f or path.splitext(f)[1] != '.csv':
                continue
            new_filename = path.join(static_dir, version, f)
            cmd("git show {}:{} > {}".format(br, path.join('locale', f), new_filename))
            locale_id = None

            with open(new_filename, 'r') as lang_csv:
                lang_reader = csv.reader(lang_csv)
                objects = []
                for row in lang_reader:
                    if row[0] == 'LocaleIdentifier':
                        locale_id = row[1]
                    objects.append({'primary': row[0], 'secondary': row[1]})
                meta = {'total_count': len(objects)}
                json_filename = "{}.json".format(path.join(static_dir, version, 'json', locale_id))

                with open(json_filename, 'w') as json_file:
                    json.dump({'meta': meta, 'objects': objects}, json_file)


if __name__ == "__main__":
    update_translations()
