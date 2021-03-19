import boto3
import re

ASTERISK_RE_REPLACE = '[A-Z-a-z0-9]*'

iam = boto3.resource('iam')

def user_policy_statements(user_name):
    """
    Get the policies attached to a user
    :param user_name: The name of the user
    :return: List
    """
    policies = []
    user = iam.User(user_name)
    
    # add user inline policies
    user_policies = [p.policy_document['Statement'] for p in user.policies.all()]
    for p in user_policies:
        policies.extend(p)

    # add user attached policies
    user_attached_policies = [p.default_version.document['Statement'] for p in user.attached_policies.all()]
    for p in user_attached_policies:
        policies.extend(p)

    # add policies from the groups the user belongs to
    for g in user.groups.all():
        
        group_policies = [p.policy_document['Statement'] for p in g.policies.all()]
        for p in group_policies:
            policies.extend(p)

        group_attached_policies = [p.default_version.document['Statement'] for p in g.attached_policies.all()]
        for p in group_attached_policies:
            policies.extend(p)

    return policies

def role_policy_statements(role_name):
    """
    Gets all the statements attached to a role
    :param role_name: The name of the role to retrieve the statements
    :return: List of iam.Statement dictionary
    """
    policies = []
    role = iam.Role(role_name)
    
    role_policies = [p.policy_document['Statement'] for p in role.policies.all()]
    for p in role_policies:
        policies.extend(p)
    
    attached_policies = [p.default_version.document['Statement'] for p in role.attached_policies.all()]
    for p in attached_policies:
        policies.extend(p)

    return policies
    

def expand_statements(statements, all_actions):
    """
    Expands policy statements, returning all services and actions permitted to be
    called.
    :param policy: Dictionary containing policy statement
    :return: List of <service:action> allowed by the policy
    """
    policy_actions = []
    allowed_actions = []

    # collect the actions
    for p in statements:
        if isinstance(p['Action'], list):
            policy_actions.extend(p['Action'])
        else:
            policy_actions.append(p['Action'])
        
    # expand the actions
    for pa in policy_actions:
        for a in all_actions:
            if match_action(pa, a):
                allowed_actions.append(a)

    return allowed_actions

def match_action(pattern, action):
    """
    Accepts a pattern and potential action, returning whether 
    the pattern matches the action
    :param pattern: IAM action pattern
    :param action: AWS Service Action (service:action)
    :return: True if matches, false otherwise
    """
    if pattern == '*' or pattern == '*:*' or pattern == action:
        return True

    # build a pattern for the action
    re_pattern = '^{}$'.format(pattern.replace('*', ASTERISK_RE_REPLACE))
    return re.match(re_pattern, action)
