──────────────────────────────🛑Freestyle Project🛑───────────────────────────────
① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳

A Freestyle project is the most fundamental and flexible job type in Jenkins. It allows you to configure nearly any build task using a graphical user interface. It's ideal for simple, standalone jobs where you need a quick setup without complex scripting.

**Features Explained:**

### ❶General : Set project name, description, and discard old builds.
① Jira site : Jira Site URL  
   Enable project-based security : Inherit permissions from Parent ACL : If we use this feature we get can give access respective people 
② GitLab Connection : Connection of Gitlab in build permnissions it shows $Gitlab-Prod$
③ Discard old builds : Strategy 
 Log Rotation -
 Days to keep builds : $20$ {Past from how many days need to keep} 
 Max # of builds to keep : $20$ {Jenkins number of builds to keep}
④ This project is parameterized : 
   Choice Parameter : 
   Name - {You can give the name what you want to keep on build with parameters while triggering}
   Choices - {You will have differnent choices in jenkins while building } 
⑤ Restrict where this project can be run : {Name of Node}
⑥ JDK : If you want to use any jdk you can mention here 
⑦ 
⑧
❷Source Code Management : Connect to Git/SVN and configure repo details.
① None : You are not connecting any gitlap repo here 
②
③ 
④ 
⑤ 
⑥ 
⑦ 
⑧
### ❸Build Triggers  : Specify triggers (e.g., Poll SCM, cron jobs, GitHub webhook).
① Build periodically with parameters : 
  Schedule :
  $0 */2 * * * %ENV=ST1CON$ {It means that Based on Build with parameters if ENV name and ST1CON choice is would be trigger based on give timeline}  
②
③ 
④ 
⑤ 
⑥ 
⑦ 
⑧
### ❹Build Environment : Set up environment variables, credentials, wrappers, etc.
① Delete workspace before build starts : 
  If you're triggering any build it will delete everything in workspace of jenkins and it will trigger fresh Build 
② Set Build Name : 
  $#${ENV}_${BUILD_NUMBER}$ {if you use like this it will show Name which you added in build with parameters that will show here and number of build}
③ Set jenkins user build variables : 
④ Terminate a build if it's stuck : 
  Time-out strategy :
  Absolute : $15$ {if build taking more than 15 minutes build will automatically abrted}

⑤ 
⑥ 
⑦ 
⑧

### ❺Build Steps : Add build commands (e.g., Execute Shell, Invoke Ant).
① Execute shell :
  You can Add shell script in the box 
② Inject environment variables :
  Properties File Path : $propfile$ { }
  Inject Environment Variables (from 1st image)
Properties File Path: propfile
Refers to a file containing key-value pairs of environment variables.
Properties Content: Empty (can also be filled directly).
Why? Injects custom values into the Jenkins build (e.g., myIP, region, etc.).
  
③ VZ Cloud All-In-One:1.2
API Auth Credentials : 
- Specific Credentials : $SVC-jenkinsbuildNew/********$
{ Purpose Authenticates Jenkins to access secured environments (e.g., internal servers or APIs)
It’s using a service account (SVC) which has necessary permissions.
Why? Without credentials, Jenkins can't access servers, git, or cloud APIs securely}

API :  $AnsiblePlaybook$ { we can use either cloudformationtemplate or ec2instancestate or any other  
Purpose: Tells Jenkins which type of action/API to execute using the plugin.
Why? There may be multiple API types (e.g., Shell Script, Puppet, Ansible). This specifies you are running an Ansible playbook}

VSAD/AppID:   $RBMV$
{Purpose: Likely an internal application or service identifier within Verizon systems.
Why? Used for tracking or scoping the job to a specific app/module}

Git Repo URL : $git@gitlab.verizon.com...$
{ Purpose: This is the repository where your Ansible playbook resides.
Why? Jenkins fetches the playbook from this Git repo before executing it.}

GitBranch/Commit ID : $main$
{ Purpose: The branch (or specific commit) from the repo that Jenkins will use.
Why? Ensures Jenkins pulls the correct version of the playbook. }

Playbook Path

Value: /ansible/restartapiapps.yml
{ Purpose: The relative file path inside the Git repo pointing to the Ansible playbook file.
Why? This is the playbook that contains the automation logic to be executed.}


Ansible Version : $2.18$
{ Purpose: Specifies which Ansible version to use while executing the playbook.
Why? Compatibility matters — some playbooks may use features only available in specific versions.}


Parameters : { Empty (optional)
Purpose: Additional command-line variables or parameters passed to the playbook (e.g., -e var=value).
Why? Useful if your playbook supports customization via variables.}


Operating System: $Linux$
{Purpose: Target OS type where the playbook will be executed.
Why? Ensures the right syntax/commands are used in the playbook (Linux vs Windows differ).}

Server Authentication : $svc-pc_cicd_np (On-Premises NonProd)$
{Purpose: Specifies the credentials Jenkins should use to connect to the target servers.
Why? Ensures secure connection and access to deploy or restart services.}

Inventory : $Host List$
{Purpose: Specifies the Ansible inventory type.
Why? Tells Ansible which group of servers to target. Can be dynamic or static.}

Server IPs: $ ${myIP}  $
{Purpose: Specifies the exact IP(s) of the server(s) where the playbook should run.
${myIP} is a Jenkins environment variable (injected earlier).
Why? You’re targeting specific dynamic IPs during runtime.}


④ 
⑤ 
⑥ 
⑦ 
⑧

### ❻Post-build Actions : Define actions like email notifications, archiving artifacts, etc.
① 
②
③ 
④ 
⑤ 
⑥ 
⑦ 
⑧

🟨 Limitations: Less flexible, no complex workflows, not ideal for modern CI/CD needs.
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────


