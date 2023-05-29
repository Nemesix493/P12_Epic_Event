sleep 5
python -m manage migrate
python -m manage init_groups
python -m manage runserver 0.0.0.0:8000