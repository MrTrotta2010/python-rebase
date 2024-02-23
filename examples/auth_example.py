"""Module that provides usage examples of the Session class"""
import sys
from src.python_rebase.rebase_client import ReBaseClient

sys.path.append('..')

print("> First, let's create a ReBaseClient", '\n')
rebase_client = ReBaseClient('mrtrotta2010@gmail.com', '6c2db8d6369ed5d1a9449d32d6253d4c')

print("> Now, let's try to authenticate the user")
response = rebase_client.authenticate()

print("> If your email address and your token are registered, you should receive a success message", '\n')
print(response)

print("> You can try authenticating as soon as you create your ReBaseClient instance, by passing the try_authenticate parameter as True")
rebase_client = ReBaseClient('mrtrotta2010@gmail.com', '6c2db8d6369ed5d1a9449d32d6253d4c', try_authenticate=True)

print("> However, if the authentication fails, an UnauthorizedUserError will be raised", '\n')
rebase_client = ReBaseClient('your@email.com', 'your_token', try_authenticate=True)
