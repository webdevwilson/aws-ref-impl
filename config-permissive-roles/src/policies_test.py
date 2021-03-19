import unittest
import policies
import json
from os import path

class PoliciesTests(unittest.TestCase):

    def setUp(self):
        fixture_file = path.dirname(__file__) + '/policies_fixture.json'
        with open(fixture_file) as fp:
            self.fixture = json.load(fp)

        iam_reference_file = 'iam_reference.json'
        with open(iam_reference_file) as fp:
            self.service_actions = json.load(fp)

    def test_unit_expand_admin(self):
        expanded = policies.expand_statements([{
            'Action': ['*:*']
        }], self.service_actions)
        self.assertEqual(len(self.service_actions), len(expanded))

    def test_unit_expand_exact(self):
        expanded = policies.expand_statements([{
            'Action': ['ec2:DescribeInstances']
        }], self.service_actions)
        self.assertEqual(len(expanded), 1)
        self.assertIn('ec2:DescribeInstances', expanded)

    def test_unit_expand_service(self):
        expanded = policies.expand_statements([{
            'Action': ['codecommit:*']
        }], self.service_actions)
        self.assertEqual(25, len(expanded))

    def test_unit_expand_wildcard(self):
        expanded = policies.expand_statements([{
            'Action': ['elasticbeanstalk:Describe*']
        }], self.service_actions)
        self.assertEqual(9, len(expanded))

    def test_unit_expand(self):
        expanded = policies.expand_statements(self.fixture, self.service_actions)
        self.assertIn('secretsmanager:CreateSecret', expanded)

    def test_unit_match_all(self):
        self.assertTrue(policies.match_action('*', 'ec2:StartInstance'))
        self.assertTrue(policies.match_action('*', 'codecommit:GetRepositoryTriggers'))

    def test_unit_match_exact(self):
        self.assertTrue(policies.match_action('ec2:StartInstance', 'ec2:StartInstance'))
        self.assertFalse(policies.match_action('ec2:StartInstance', 'ec2:StopInstance'))

    def test_unit_wildcard_end(self):
        pattern = 'ec2:Describe*'

        # passes
        self.assertTrue(policies.match_action(pattern, 'ec2:DescribeInstances'))
        self.assertTrue(policies.match_action(pattern, 'ec2:DescribeFleets'))

        # fails
        self.assertFalse(policies.match_action(pattern, 'ec2:StartInstance'))
        self.assertFalse(policies.match_action(pattern, 'ec2:StopInstance'))
        self.assertFalse(policies.match_action(pattern, 'ec2:TerminateInstance'))

    def test_unit_wildcard_front(self):
        pattern = 'secretsmanager:*Secret'

        # passes
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:DeleteSecret'))
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:DescribeSecret'))

        # fails
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:GetSecretValue'))
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:PutResourcePolicy'))
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:PutSecretValue'))
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:TagResource'))

    def test_unit_wildcard_both(self):
        pattern = 'secretsmanager:*Secret*'

        # passes
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:DeleteSecret'))
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:DescribeSecret'))
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:GetSecretValue'))
        self.assertTrue(policies.match_action(pattern, 'secretsmanager:PutSecretValue'))

        # fails
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:PutResourcePolicy'))
        self.assertFalse(policies.match_action(pattern, 'secretsmanager:TagResource'))

    def test_int_get_role(self):
        p = policies.role_policy_statements('test-config-permissive')
        self.assertEqual(len(p), 5)
        
        actions = policies.expand_statements(p, self.service_actions)
        
        self.assertEqual(len(actions), 18)
        self.assertIn('ec2:DescribeInstances', actions)
        self.assertIn('s3:PutObject', actions)
        self.assertIn('secretsmanager:RotateSecret', actions)
        self.assertIn('appstream:GetApplication', actions)
        self.assertNotIn('s3:ListBuckets', actions)
        self.assertNotIn('s3:GetObject', actions)

    def test_int_get_users(self):
        p = policies.user_policy_statements('test-config-permissive')
        
        self.assertEqual(len(p), 5)
        
        actions = policies.expand_statements(p, self.service_actions)
        
        self.assertEqual(len(actions), 18)
        self.assertIn('ec2:DescribeInstances', actions)
        self.assertIn('s3:PutObject', actions)
        self.assertIn('secretsmanager:RotateSecret', actions)
        self.assertIn('appstream:GetApplication', actions)
        self.assertNotIn('s3:ListBuckets', actions)
        self.assertNotIn('s3:GetObject', actions)

if __name__ == '__main__':
    unittest.main()