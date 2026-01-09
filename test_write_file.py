from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

 # because an absolute second arg
 # replaces the first in os.path.join
 # the only shared path is root, NOT /.../calculator so it would fail
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
