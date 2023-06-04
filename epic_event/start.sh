sleep 5
python -m manage migrate
python -m manage init_groups
if [ $TEST_ARG == 1 ]; then
    python -m manage test
    if [ $? -ne 0 ]; then
        echo "Test failed !"
        exit 1
    else
        echo "Test successed !"
        exit 0
    fi
else
    python -m manage runserver 0.0.0.0:8000
fi