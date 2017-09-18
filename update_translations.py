# import subprocess
# branches = []
#
# process = subprocess.Popen("git for-each-ref --format='%(refname:short)' refs/heads",
#                            stdout=subprocess.PIPE,
#                            stderr=subprocess.PIPE,
#                            shell=True)
# for line in process.stdout.readline():
#     # if line == '':
#     #     break
#     # branch = line.replace("'", '')
#     branches.append(line)
#
# print(branches)


import subprocess
import os

static_dir = '/static'
os.chdir('/Users/olaputin/work/translations_store')
out, _ = subprocess.Popen("git for-each-ref --format='%(refname:short)' refs/heads",
                          stdout=subprocess.PIPE, shell=True).communicate()
branches = [br for br in out.decode('utf-8').split('\n') if br]
print(branches)

for br in branches:
    out, _ = subprocess.Popen("git ls-tree {}:locale -r --name-status".format(br),
                              stdout=subprocess.PIPE, shell=True).communicate()
    print("branch = {}".format(br))
    print(out.decode('utf-8'))

# if __name__ == "__main__":
#     print("helloworld")