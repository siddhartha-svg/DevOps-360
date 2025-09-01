### `README.md` File

This document provides a comprehensive overview of a **Classic Pipeline Job** in Jenkins, detailing its configuration sections and an example of the Groovy-based script used to define custom CI/CD workflows.

-----

## ✅ Pipeline Project (Classic Pipeline Job)

This is not a Freestyle project or Multibranch pipeline—it's a standalone pipeline job created using:

> New Item \> Pipeline

This kind of pipeline allows you to write Groovy-based scripts directly in the UI or reference them from SCM (e.g., Git). It's ideal for defining custom CI/CD workflows.

-----

## 🔍 Sections Explained

### ❶ General

  * **Jira site:** The Jira Site URL is configured.
      * **Enable project-based security:** Inheriting permissions from a Parent ACL allows you to give access to specific individuals.
  * **GitLab Connection:** Connects to GitLab for build permissions, using the `$Gitlab-Prod$` connection.
      * **Use alternative credential:** A credential token (`$UP_GITLAB_TOKEN$`) is used for accessing GitLab.
  * **Discard old builds:** This strategy manages log rotation.
      * **Days to keep builds:** `$20$`
      * **Max \# of builds to keep:** `$20$`
  * **Do not allow Concurrent builds:** If this is enabled, only one instance of the job can run at any given time.
  * **This project is parameterized:** This allows the user to input parameters when triggering a build.
      * **String parameter:**
          * **Name:** `depCheck`
          * **Default Value:** `true`
      * **Active Choice Parameter:**
          * **Name:** `branch`
          * **Script:** `Groovy Script: return["main"]`

-----

### ❷ Triggers

This section defines when the pipeline should run.

  * **Build when a change is pushed to GitLab:** A GitLab webhook URL is configured to trigger the pipeline on code pushes. The URL is: `https://jenkins-vcg1.vpc.verizon.com/vcg1/project/VZW.UNIFIED.CICD/VZW.UPE.EY2V_JITRUSAGEBROKER.CI_PIPELINE/VZW.UPE.EY2V_JITRUSAGEBROKER.CI_main/VZW.UPE.EY2V_JITRUSAGEBROKER.JITR-VT-USAGE-INQUIRY-EUREKA`
  * **Enabled GitLab triggers:**
      * **Push Events:** This trigger is enabled.

-----

### ❸ Pipeline

This is the core section for configuring the pipeline definition and script.

  * **Definition:** `Pipeline Script` (inline) is selected.
  * **Script:** The Groovy script defines the pipeline logic.
    ```groovy
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
    ```

-----

### ❹ Advanced

This section is hidden by default and is used for configurations such as custom quiet periods, retry counts, or custom workspaces. It is usually optional.

-----

## ✅ Example Configurations

### Option 1: Pipeline Script (inline)

You write the entire pipeline directly in the UI.

```groovy
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
```

### Option 2: Pipeline Script from SCM

You point to a Git repo with a `Jenkinsfile`.

| Field | Description |
| :--- | :--- |
| **SCM** | Git, GitHub, Bitbucket, etc. |
| **Repository URL** | Link to repo |
| **Credentials** | Optional |
| **Branch** | e.g., `*/main` |
| **Script Path** | `Jenkinsfile` or a custom name |

-----

## 💡 Summary

| Feature | Details |
| :--- | :--- |
| **Type** | Pipeline Project (Declarative or Scripted) |
| **UI Configuration Sections** | General, Triggers, Pipeline, Advanced |
| **Common Use Case** | Customized CI/CD workflows for individual projects |
| **Script Language** | Groovy (Declarative is preferred) |
| **Flexibility** | High (stages, agents, conditions, parallel builds, etc.) |
