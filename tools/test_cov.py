import os

os.system('pytest --cov=photo_organizer --cov-report html .\\tests\\')
os.system('.\\htmlcov\\index.html')
