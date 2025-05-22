# create requirement
pip freeze > requirement.txt

# VM Startup Script

python -m venv myenv
myenv\Scripts\activate

pip install -r .\requirement.txt

# work on python

python main.py

# test cases

pytest tests
