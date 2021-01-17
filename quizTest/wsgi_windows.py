activate_this = 'C:\\Users\\escaper\\Desktop\\projects\\quiz\\winVenv\\Scripts\\activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:\\Users\\escaper\\Desktop\\projects\\quiz\\winVenv\\Lib\\site-packages')



os.environ['DJANGO_SETTINGS_MODULE'] = 'quizTest.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quizTest.settings")

# Add the app's directory to the PYTHONPATH
sys.path.append('C:\\Users\\escaper\\Desktop\\projects\\quiz\\quizTest')
sys.path.append('C:\\Users\\escaper\\Desktop\\projects\\quiz\\quizTest\\quizTest')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()