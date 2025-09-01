
────────────────📁Classic Pipeline Job📁────────────────────

## ✅ Pipeline Project (Classic Pipeline Job)

This is not a Freestyle project or Multibranch pipeline — it's a standalone pipeline job created using:

> New Item > Pipeline

```
This kind of pipeline allows you to write Groovy-based scripts directly in the UI or reference them from SCM (e.g., Git). 
It is ideal for defining custom CI/CD workflows.
```

## 🔍 Sections Explained:

Section Purpose

####  General Set the name, description, enable/discard old builds, etc.
### Jira site : Jira Site URL  
   Enable project-based security : Inherit permissions from Parent ACL : If we use this feature we get can give access respective people 
###  GitLab Connection : Connection of Gitlab in build permnissions it shows $Gitlab-Prod$
   Use alternative credential : 
   Credential : $UP_GITLAB_TOKEN$ { we can use token which generally gotlab can access with this }
###  Discard old builds : Strategy 
 Log Rotation -
 Days to keep builds : $20$ {Past from how many days need to keep} 
 Max # of builds to keep : $20$ {Jenkins number of builds to keep}
 
###  Do not allow Concurrent builds : { If we click on it ,one instance of this job can run at any given time. }
 
###  This project is parameterized :
   String parameter : 
   Name : depCheck 
   Default Value :  true   
   Active Choice Parameter : 
   Name : branch
   Script : 
   Groovy Script : $ return["main"] $
   
  
 
## ❷Triggers Define when the pipeline should run (e.g., Poll SCM, GitHub hook trigger).
###  Build when a change is pushed to GitLab. GitLab webhook URL:
  https://jenkins-vcg1.vpc.verizon.com/vcg1/project/VZW.UNIFIED.CICD/VZW.UPE.EY2V_JITRUSAGEBROKER.CI_PIPELINE/VZW.UPE.EY2V_JITRUSAGEBROKER.CI_main/VZW.UPE.EY2V_JITRUSAGEBROKER.JITR-VT-USAGE-INQUIRY-EUREKA
###  Enabled GitLab triggers :
  Push Events :Click on it 
  

## Pipeline Core section where you configure: <br>• Definition: Choose "Pipeline script" (inline) or "Pipeline script from SCM"<br>• Script or Jenkinsfile: Define your CI/CD process in Groovy syntax.
Definition : 
Pipeline Script :
 Script :
 ```
 {
 @Library('unifiedPipeline') _
def repo
def URL
def triggerSource
def scm="Git"
def projectKey
def buildCause=currentBuild.buildCauses
if("${buildCause}".contains("com.dabsquared.gitlabjenkins.cause.GitLabWebHookCause"))
{
    echo "Setting Source information by gitlab"
    repo=env.gitlabSourceRepoName 
    URL=env.gitlabSourceRepoHttpUrl 
    triggerSource="MR"
} 
else
    { 
        echo "Setting Source information by API" 
        repo = "jitr-vt-usage-inquiry-eureka" 
        URL= "https://gitlab.verizon.com/EY2V_JITRUSAGEBROKER/jitr-vt-usage-inquiry-eureka" 
        triggerSource = "API" 
        serviceName = "jitr-vt-usage-inquiry-eureka"
        vsad="EY2V" 
    } 
mediator 
        { 
            repoName = repo 
            trunk= true 
            repoURL= URL 
            scmTriggerSource = triggerSource 
            scmType=scm 
            projectId="10401" 
           vsad="EY2V" 
           serviceName = "jitr-vt-usage-inquiry-eureka"
           gitGroupName = "EY2V_JITRUSAGEBROKER"
        }
          }
```
### Advanced Hidden by default. Used to configure custom quiet periods, retry counts, custom workspace, etc. Usually optional.




## ✅ Example Configurations

Option 1: Pipeline Script (inline)

You write the whole pipeline directly in the UI.


pipeline {
 agent any
 stages {
 stage('Build') {
 steps {
 echo 'Building...'
 }
 }
 stage('Test') {
 steps {
 echo 'Testing...'
 }
 }
 stage('Deploy') {
 steps {
 echo 'Deploying...'
 }
 }
 }
}

Option 2: Pipeline Script from SCM

You point to a Git repo with a Jenkinsfile.
Field Description
SCM Git, GitHub, Bitbucket, etc.
Repository URL Link to repo
Credentials Optional
Branch e.g., */main
Script Path Jenkinsfile or a custom name


### 💡 Summary
```
Feature Details

Type Pipeline Project (Declarative or Scripted)
UI Configuration Sections General, Triggers, Pipeline, Advanced
Common Use Case Customized CI/CD workflows for individual projects
Script Language Groovy (Declarative preferred)
Flexibility High (stages, agents, conditions, parallel builds, etc.)
```
────────────────────────────────────────────────────────────────────
