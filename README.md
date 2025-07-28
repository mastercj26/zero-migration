

Grab the code


git clone https://github.com/mastercj26/zero-migration.git
cd zero-migration


pip install -r requirements.txt
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/migration.proto
Start the circus (in separate terminals):


# The ringmaster (migration service)
python server/migration.py

# Our performing servers
python server/app.py
python server/app.py --port 5001

# The audience seats (dashboard)
python frontend/app.py
Watch the show at http://localhost:8080
<img width="926" height="570" alt="image" src="https://github.com/user-attachments/assets/5ce84714-877b-4c86-941d-a20a8998e86b" />
