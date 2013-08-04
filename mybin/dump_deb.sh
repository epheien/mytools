#!/bin/bash
# 把已安装的软件包的文件备份起来

if [ $# -lt 1 ]; then
    echo "usage: $0 {pkgname} {savename}"
    exit 1
fi

pkgname="$1"
outfile=${2:-"out.tgz"}

dpkg -l "$pkgname" >/dev/null || exit $?

tmpfile="`mktemp`"
tmpdir="`mktemp -d`"

outfile=`readlink -f "$outfile"`

true > "$tmpfile"
dpkg -L "$pkgname" | while read line; do
    if [ -e "$line" -a ! -d "$line" ]; then
        echo "$line" >> "$tmpfile"
    fi
done

#
saved_dir="`pwd`"
cd "$tmpdir" || exit $?
mkdir "DEBIAN"

# /var/lib/dpkg/info/*.* 有需要运行的脚本，而基本信息在 /var/lib/dpkg/status 里面
#awk "BEGIN {sw=0} {if(\$0==\"Package: $pkgname\" || sw){sw=1;print \$0;} if (sw && \$0==\"\") {sw=0;exit}}" "/var/lib/dpkg/status" \
dpkg -s "$pkgname" \
    | grep -v '^Status:\|^$' > DEBIAN/control
cp /var/lib/dpkg/info/$pkgname.* DEBIAN/
rm -f DEBIAN/$pkgname.list
cd DEBIAN && { rename "s/^$pkgname\\.//" $pkgname.*; cd - >/dev/null; }
echo DEBIAN >> "$tmpfile"

tar -Ppczf "$outfile" -T "$tmpfile" && echo "$outfile is ready"

cd "$saved_dir"
#echo "$tmpfile"
rm -f "$tmpfile"
rm -rf "$tmpdir"
