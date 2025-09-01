## Freestyle Project: A Comprehensive Guide

A **Freestyle project** is the most fundamental and flexible job type in Jenkins. It allows you to configure nearly any build task using a graphical user interface. It's ideal for simple, standalone jobs where you need a quick setup without complex scripting.

---

### **Features Explained:**

### ❶ General

This section is for basic project settings.

* **Jira site:** Configures the Jira Site URL.
    * **Enable project-based security:** Inheriting permissions from a Parent ACL allows you to grant access to specific individuals.
* **GitLab Connection:** Connects to GitLab for build permissions, using the `$Gitlab-Prod$` connection.
* **Discard old builds:** This is a log rotation strategy.
    * **Days to keep builds:** `$20$`
    * **Max # of builds to keep:** `$20$`
* **This project is parameterized:** This option enables the "Build with Parameters" feature.
    * **Choice Parameter:**
        * **Name:** A user-defined name for the parameter.
        * **Choices:** A list of options the user can select from during a build.
* **Restrict where this project can be run:** This allows you to specify the node (e.g., a specific build agent) where the job should execute.
* **JDK:** You can specify a particular JDK version to use for the build.

---

### ❷ Source Code Management

This section is for connecting to a version control system. In this example, **"None"** is selected, indicating that no repository is connected directly to the job.

---

### ❸ Build Triggers

This section defines what events will initiate a build.

* **Build periodically with parameters:**
    * **Schedule:** `$0 */2 * * * %ENV=ST1CON$`
    This cron expression means the build will be triggered every two hours (`*/2`) on the specified environment (`ENV=ST1CON`), based on the choices provided in the "Build with Parameters" section.

---

### ❹ Build Environment

This section is for setting up the environment before the build steps execute.

* **Delete workspace before build starts:** This option ensures a clean workspace by deleting all previous files before a new build begins.
* **Set Build Name:** `$#${ENV}_${BUILD_NUMBER}$`
    * This sets the build display name. For example, if the `ENV` parameter is `ST1CON` and it's the 10th build, the name will be `#ST1CON_10`.
* **Set jenkins user build variables:** This allows you to define custom variables.
* **Terminate a build if it's stuck:**
    * **Time-out strategy:** `Absolute` with a value of `$15$`. This will automatically abort the build if it runs for more than 15 minutes.

---

### ❺ Build Steps

This is the core section where you define the build commands.

* **Execute shell:** A text box to add shell scripts.
* **Inject environment variables:**
    * **Properties File Path:** `propfile`
        * This references a file containing key-value pairs of environment variables.
    * **Properties Content:** The content is empty here but can be used to inject custom variables like `myIP` or `region` directly into the build.
* **VZ Cloud All-In-One: 1.2:** This is a custom plugin step.
    * **API Auth Credentials:** `$SVC-jenkinsbuildNew/********$`
        * **Purpose:** This authenticates Jenkins to access secure environments or APIs.
        * **Why?** Without credentials, Jenkins cannot securely access servers or cloud APIs.
    * **API:** `$AnsiblePlaybook$`
        * **Purpose:** Specifies the type of action to execute using the plugin.
        * **Why?** This indicates that an Ansible playbook will be run.
    * **VSAD/AppID:** `$RBMV$`
        * **Purpose:** An internal application or service identifier used for tracking.
        * **Why?** Scopes the job to a specific application or module.
    * **Git Repo URL:** `$git@gitlab.verizon.com...$`
        * **Purpose:** The repository where the Ansible playbook resides.
        * **Why?** Jenkins needs this URL to fetch the playbook.
    * **GitBranch/Commit ID:** `$main$`
        * **Purpose:** The branch or commit to pull from the repository.
        * **Why?** Ensures the correct version of the playbook is used.
    * **Playbook Path:** `/ansible/restartapiapps.yml`
        * **Purpose:** The relative path to the Ansible playbook file inside the repository.
        * **Why?** This file contains the automation logic.
    * **Ansible Version:** `$2.18$`
        * **Purpose:** Specifies which Ansible version to use.
        * **Why?** Compatibility is crucial for certain playbooks.
    * **Parameters:** `Empty` (optional)
        * **Purpose:** Additional command-line variables to pass to the playbook.
        * **Why?** Allows for customization via variables.
    * **Operating System:** `$Linux$`
        * **Purpose:** The target OS type.
        * **Why?** Ensures the correct syntax and commands are used.
    * **Server Authentication:** `$svc-pc_cicd_np (On-Premises NonProd)$`
        * **Purpose:** Credentials used by Jenkins to connect to the target servers.
        * **Why?** Ensures a secure connection for deployment.
    * **Inventory:** `Host List`
        * **Purpose:** Specifies the Ansible inventory type.
        * **Why?** Tells Ansible which group of servers to target.
    * **Server IPs:** `${myIP}`
        * **Purpose:** The exact IP addresses of the servers. `${myIP}` is an environment variable injected earlier.
        * **Why?** Allows for targeting specific dynamic IPs.

---

### ❻ Post-build Actions

This section defines actions that run after the build is complete, such as sending email notifications or archiving artifacts.

---

### 🟨 Limitations

Freestyle projects are **less flexible** than Pipelines, lack complex workflow capabilities, and are **not ideal** for modern CI/CD needs that require version-controlled scripts.
