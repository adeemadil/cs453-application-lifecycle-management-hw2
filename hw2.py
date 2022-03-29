from perceval.backends.core.github import GitHub
from dateutil.tz import tzutc
import datetime
import dateutil.parser
import json

API_TOKEN = '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'

repo = GitHub( owner='osamatanveer', repository='test',  api_token=[API_TOKEN], sleep_for_rate=True, sleep_time=300)

user = { }
usersList = []
issues_count = 0
open_issues = 0
unopened_issues = 0
closed_issues_unresolved = 0
date_creation = None
recent_days_issue_count = 0
closed_issues_unresolved_time = None
closed_issues_atleast_one = 0
closed_issues_atleast_one_time = None
creation_date_first_issue = None
creation_date_last_issue = None
flag_first_issue = False

#Today's date
date_today = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
date_today = dateutil.parser.isoparse( str(date_today))

print( "Today's date is " + str(date_today))
print('--------Part 2--------')

#templist = [i for i in range(1000)]
#x = 0
#usersList.append(user)
for issue in repo.fetch():
    #print(issue)
    if( issue["category"] == "issue" and "pull_request" not in issue["data"]):

        if( flag_first_issue is False):
           creation_date_first_issue = creation_date_last_issue = dateutil.parser.parse( issue["data"]["created_at"])
           flag_first_issue = True

        issues_count = issues_count + 1

        if( issue["data"]["user"]["login"] not in user):
            user.update( {issue["data"]["user"]["login"] : 1})
        if( issue["data"]["user"]["login"] in user):
            user[ issue["data"]["user"]["login"]] = user[ issue["data"]["user"]["login"]] + 1

        date_creation = dateutil.parser.parse( str(issue["data"]["created_at"]))
        
        creation_date_first_issue = min(date_creation, creation_date_first_issue)
        creation_date_last_issue = max(date_creation, creation_date_last_issue)
        
        if( issue["data"]["state"] != "open"):
            unopened_issues = unopened_issues + 1

            if( issue["data"]):
                pass

        if( issue["data"]["state"] == "open"):
            open_issues = open_issues + 1
            if( (date_creation-date_today).days < 30):
                recent_days_issue_count = recent_days_issue_count + 1
        
    
    # # Serializing json
    # json_obj = json.dumps(issue, indent = 3)
    # # Writing to sample.json
    # with open("example" + str(templist[x]) + ".json", "w") as outfile:
    #     outfile.write((json_obj))
    # # break
    # x = x + 1

print('Date of first opened issue is ' + str(creation_date_first_issue.date()) + "  " + str(creation_date_first_issue.time()))
print('Date of last opened issue is ' + str(creation_date_last_issue.date()) + "  " + str(creation_date_last_issue.time()))

repo_age = (date_today - creation_date_first_issue).days
print("The repository's age is " + str(repo_age) + ' days')
if( recent_days_issue_count > 5):
    print('It is still active, it has ' + str(recent_days_issue_count) + ' issues opened in the last 30 days')
else:
    print('It not active, it has only ' + str(recent_days_issue_count) + ' issues opened in the last 30 days')
    
print('It has ' + str(issues_count) + ' issues')
print('It has ' + str(len(user)) + ' users')
# print(user)

print('--------Part 3--------')
print('It has ' + str(open_issues) + ' open issues')
print('It has ' + str(unopened_issues) + ' closed issues')

print('--------Part 4--------')
print("Top 5 users: ")
# for user in topUsersList:
#     print( user["name"] + "     " + user[])


print('--------Part 5--------')
print("No of closed issues that did not have any assignee is " + str(closed_issues_unresolved))
print("Average day of resolution for issues without an assignee is " + str(closed_issues_unresolved_time))

print('--------Part 6--------')
print("No of closed issues that had at least one assignee is " + str(closed_issues_atleast_one))
print("Average day of resolution for issues without atlaest one assignee is " + str(closed_issues_atleast_one_time))
