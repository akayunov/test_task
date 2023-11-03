apt install docker

docker build . -f build/Dockerfile  -t task

git clone git@github.com:akayunov/test_task.git

cd task

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

to run test: pytest tests