

Grab the code

bash
git clone https://github.com/mastercj26/zero-migration.git
cd zero-migration
Set up the party

bash
pip install -r requirements.txt
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/migration.proto
Start the circus (in separate terminals):

bash
# The ringmaster (migration service)
python server/migration.py

# Our performing servers
python server/app.py
python server/app.py --port 5001

# The audience seats (dashboard)
python frontend/app.py
Watch the show at http://localhost:8080
