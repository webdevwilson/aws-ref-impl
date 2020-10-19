# new-user-create-login-send-email

Creates a login for an IAM user after creation, then sends an email to that user.

## Parameters
 * **FromEmailAddress** - The from address of the email
 * **BccEmailAddresses** - Email addresses to BCC on the email
 * **EmailSubject** - The subject of the email
 * **EmailBody** - The body of the email
 * **PasswordLength** - The length of the generated password
 * **UsernameRegex** - Regex the username must match to be configured