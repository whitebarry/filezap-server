import src.user_mgmt.model as model

class UserDataStore(object):
    """
    Interface class for dynamodb users table
    """
    def __init__(self, config, dynamodb=None):
        """
        :param dynamodb: Only used for test mocking, do not pass in production code
        """
        if not dynamodb:
            import boto3
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self._table = dynamodb.Table(config.get('USER_DB_TABLE'))


    def add_user(self, user):
        self._table.put_item(Item=user.to_dict())


    def get_user(self, username):
        user_dict = self._table.get_item(Key={'username': username}).get('Item')
        if user_dict:
            return model.User.from_dict(user_dict)


    def delete_user(self, username):
        self._table.delete_item(Key={'username': username})
