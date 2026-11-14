from functions.get_files_info import get_files_info

current_dir = get_files_info("calculator", ".")
result = ["Result for current directory:"]
for line in current_dir.split('\n'):
    result.append(line)
print("\n\t".join(result))
pkg_dir = get_files_info("calculator", "pkg")
result = ["Result for 'pkg' directory:"]
for line in pkg_dir.split('\n'):
    result.append(line)
print("\n\t".join(result))
bin_dir = get_files_info("calculator", "/bin")
result = ["Result for '/bin' directory:"]
for line in bin_dir.split('\n'):
    result.append(line)
print("\n\t".join(result))
parent_dir = get_files_info("calculator", "../")
result = ["Result for '../' directory:"]
for line in parent_dir.split('\n'):
    result.append(line)
print("\n\t".join(result))
