# config-permissive-roles

Scans an account and utilizes CloudTrail to determine if a user or role has been given too many permissions. It does this by searching CloudTrail for API calls that have been made by that user. If a user has permissions they have not used, the user or role is flagged to be granted too many permissions.

This would be most effective after CloudTrail has ran for a while and some data has been collected for the user.