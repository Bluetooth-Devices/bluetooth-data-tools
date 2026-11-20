#!/usr/bin/env sh
# Assert a published release carries the full artifact set ci.yml builds.
#
# Reads one filename per line on stdin (PyPI's `urls[].filename`) and checks
# that every platform family in ci.yml's `build_wheels` matrix is represented.
#
# Existence of the version on PyPI is not enough: the `release` job publishes
# the sdist plus the single wheel it built on its own runner *before*
# `build_wheels` runs, so a version whose entire wheel matrix was lost still
# resolves on PyPI. v1.29.21 shipped exactly that way -- one armv7l cell failed,
# `upload_pypi` was skipped, and the release looks present but is binary-empty
# for every target except the release runner's own.
#
# Reading filenames from stdin keeps the matching logic testable without a
# network round-trip.

set -eu

files=$(cat)

if [ -z "$files" ]; then
    echo "no filenames on stdin" >&2
    exit 2
fi

# One entry per os/musl/qemu combination the build_wheels matrix produces.
# Globs, not exact tags: manylinux/musllinux filenames carry a moving
# `_<major>_<minor>_` ABI stamp and may list several platform tags joined by
# `.`, so only the trailing architecture is stable.
missing=0
total=0
while IFS='	' read -r pattern label; do
    [ -n "$pattern" ] || continue
    total=$((total + 1))
    found=0
    for name in $files; do
        # shellcheck disable=SC2254 # $pattern is a glob on purpose.
        case "$name" in
        $pattern)
            found=1
            break
            ;;
        esac
    done
    if [ "$found" -eq 0 ]; then
        echo "missing: $label ($pattern)" >&2
        missing=$((missing + 1))
    fi
done <<'EOF'
*-win_amd64.whl	Windows x86-64
*-macosx_*_x86_64.whl	macOS x86-64
*-macosx_*_arm64.whl	macOS arm64
*-manylinux*_x86_64.whl	manylinux x86-64
*-manylinux*_aarch64.whl	manylinux aarch64
*-manylinux*_armv7l.whl	manylinux armv7l
*-musllinux*_x86_64.whl	musllinux x86-64
*-musllinux*_aarch64.whl	musllinux aarch64
*-musllinux*_armv7l.whl	musllinux armv7l
*.tar.gz	source distribution
EOF

if [ "$missing" -gt 0 ]; then
    echo "$missing of $total artifact families missing" >&2
    exit 1
fi

echo "all $total artifact families present"
