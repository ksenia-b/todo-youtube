##  Build the docker image:
docker image build -t todo-youtube .

## Review list of images:
docker image ls

## Run the docker container
docker run -p 5001:5000 -d todo-youtube



# sqlite commands:
sqlite> from app import db
sqlite> db.create_all()

sqlite> .tables
sqlite> insert into test_table values(2, 'bar');
sqlite> select * from test_table;
1|foo
2|bar
sqlite> .exit

# Postmen collection:
https://documenter.getpostman.com/view/7422784/TW6zFmuR