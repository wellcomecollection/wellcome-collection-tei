file_count()
{
    if [ ! -e "$1" ]
    then
        exit 1
    fi

    local -i files=$(find "$(readlink -f -- "$1")" -type f -print0 | grep -cz -- -)
    echo $files
}
