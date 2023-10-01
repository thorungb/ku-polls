# Ku-polls Application v1.0.0 Release Notes

## Features Included

1. **Admin Interface**
   - Authorized administrators can create, edit, and manage poll questions and choices through an admin interface.

2. **User Participation**
   - Users can view and participate by voting on the available poll questions.
   - Everyone, authenticated or not, can see the total number of votes for each choice in the poll.

3. **Database Storage**
   - The poll questions and their respective choices, along with user responses, are stored in a database.

4. **Publication Date and Availability**
   - Each poll has a specified publication date, becoming visible to users on or after this date.
   - Users can only vote on polls available within the specified end date.

5. **Redirection and Security**
   - The web application redirects to the polls index page if someone goes to the base URL of the website or an unavailable poll.
   - Sensitive configuration data is externalized.

6. **User Experience**
   - Users can see poll results without voting.
   - Users can log in and log out.
   - Users must log in to vote; otherwise, they are redirected to the login page.
   - Users can view their previous votes for each poll question and change their previous votes.

7. **Navigation**
   - The navigation bar is consistently displayed across web pages and contains a login or logout link.

8. **Confirmation Messages**
   - A visual confirmation message is displayed when a user successfully submits a vote.

## How to Report Issues

If you encounter any bugs or issues, please [create a new issue](https://github.com/thorungb/ku-polls/issues/new) on my GitHub repository.
Please provide detailed steps to reproduce the issue, expected behavior, and actual behavior in your issue report.
