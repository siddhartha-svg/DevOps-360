18:53:04  Started by user Bhavana, Margam

18:53:04  Rebuilds build #273

18:53:04  Loading library unifiedPipeline@deploy_master_prod
18:53:04  Attempting to resolve deploy_master_prod from remote references...
18:53:04   > git --version # timeout=10
18:53:04   > git --version # 'git version 2.43.5'
18:53:04  using GIT_ASKPASS to set credentials UP_GITLAB_USER
18:53:04   > git ls-remote -h -- https://gitlab.verizon.com/marvel_cicd/pipelinesrc.git # timeout=10
18:53:05  Found match: refs/heads/deploy_master_prod revision b988ebdc25bf8f0b4598e29b7926b50ed6b7bfc1
18:53:05  The recommended git tool is: git
18:53:05  using credential UP_GITLAB_USER
18:53:05   > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP@libs/3ef34ce465c0ac5777e828623efc85a5618ed4c441587eb36321b208098cdb2d/.git # timeout=10
18:53:05  Fetching changes from the remote Git repository
18:53:05   > git config remote.origin.url https://gitlab.verizon.com/marvel_cicd/pipelinesrc.git # timeout=10
18:53:05  Fetching without tags
18:53:05  Fetching upstream changes from https://gitlab.verizon.com/marvel_cicd/pipelinesrc.git
18:53:05   > git --version # timeout=10
18:53:05   > git --version # 'git version 2.43.5'
18:53:05  using GIT_ASKPASS to set credentials UP_GITLAB_USER
18:53:05   > git fetch --no-tags --force --progress -- https://gitlab.verizon.com/marvel_cicd/pipelinesrc.git +refs/heads/*:refs/remotes/origin/* # timeout=10
18:53:06  Checking out Revision b988ebdc25bf8f0b4598e29b7926b50ed6b7bfc1 (deploy_master_prod)
18:53:06   > git config core.sparsecheckout # timeout=10
18:53:06   > git checkout -f b988ebdc25bf8f0b4598e29b7926b50ed6b7bfc1 # timeout=10
18:53:06  Commit message: "Merge branch 'V473188-deploy_master_prod-patch-02590' into 'deploy_master_prod'"
18:53:06   > git rev-list --no-walk b988ebdc25bf8f0b4598e29b7926b50ed6b7bfc1 # timeout=10
18:53:06  [Pipeline] Start of Pipeline
18:53:07  [Pipeline] node
18:53:07  Running on Unified-agent-10.34.124.169
 in /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP
18:53:07  [Pipeline] {
18:53:07  [Pipeline] stage
18:53:07  [Pipeline] { (Init)
18:53:07  [Pipeline] script
18:53:07  [Pipeline] {
18:53:07  [Pipeline] withBuildUser
18:53:07  [Pipeline] {
18:53:07  [Pipeline] sh
18:53:08  + echo 'Bhavana, Margam'
18:53:08  [Pipeline] cleanWs
18:53:09  [WS-CLEANUP] Deleting project workspace...
18:53:09  [WS-CLEANUP] Deferred wipeout is used...
18:53:09  [WS-CLEANUP] done
18:53:09  [Pipeline] }
18:53:09  [Pipeline] // withBuildUser
18:53:09  [Pipeline] echo
18:53:09  reading adhoc parameters
18:53:09  [Pipeline] echo
18:53:09  deployZone --> b2b
18:53:09  [Pipeline] echo
18:53:09   DEPLOY_APP_FLAG --> OCP
18:53:09  [Pipeline] echo
18:53:09  pipelineParams => [GIT_GROUP:iipv_billing_profile_service, STAGES:ALL, RELEASE_BRANCH:25.89.100, DEPLOY_CONFIG_ONLY:false, DEPLOY_GC_ONLY:false, SOURCE_ENV:SITG, ENVIRONMENT_NAME:T1, SKIP_ARTIFACT_STAGING:false, DEPLOY_TYPE:EKS, VSAD:IIPV, DEPLOY_ENV:PROD, SKIP_GLOBAL_CONFIG_STAGE:false, SKIP_GLOBAL_SECRET_STAGE:false, DEPLOY_ZONE:b2b, PROJECT_CATEGORY:NA, DEPLOY_APP_FLAG:OCP, NOAPIGEE_FLAG:FALSE]
18:53:09  [Pipeline] echo
18:53:09  not a iot deployment
18:53:09  [Pipeline] echo
18:53:09  env.vsad_iot => NA
18:53:09  [Pipeline] echo
18:53:09  [INFO] [2025-09-05T09:23:09.772042413] Inside PipelineInit
18:53:09  [Pipeline] echo
18:53:09  paramJson => [GIT_GROUP:iipv_billing_profile_service, STAGES:ALL, RELEASE_BRANCH:25.89.100, DEPLOY_CONFIG_ONLY:false, DEPLOY_GC_ONLY:false, SOURCE_ENV:SITG, ENVIRONMENT_NAME:T1, SKIP_ARTIFACT_STAGING:false, DEPLOY_TYPE:EKS, VSAD:IIPV, DEPLOY_ENV:PROD, SKIP_GLOBAL_CONFIG_STAGE:false, SKIP_GLOBAL_SECRET_STAGE:false, DEPLOY_ZONE:b2b, PROJECT_CATEGORY:NA, DEPLOY_APP_FLAG:OCP, NOAPIGEE_FLAG:FALSE, IOT_DEPLOY:False, vsad_iot:NA]
18:53:09  [Pipeline] echo
18:53:09  dEnv => prod1
18:53:09  [Pipeline] echo
18:53:09   Deployment has parameter zone: b2b
18:53:09  [Pipeline] echo
18:53:09  Release Branch: release/25.89.100
18:53:09  [Pipeline] echo
18:53:09  latest app config only deployment is not enabled
18:53:09  [Pipeline] echo
18:53:09  PROD EASTWEST value: 
18:53:09  [Pipeline] echo
18:53:09  1. Base Pipeline Parameters => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:ALL, deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA]
18:53:09  [Pipeline] echo
18:53:09  env.DEPLOY_APP_FLAG => OCP
18:53:09  [Pipeline] echo
18:53:09  inside DEPLOY_APP_FLAG
18:53:09  [Pipeline] retry
18:53:09  [Pipeline] {
18:53:10  [Pipeline] dir
18:53:10  Running in /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service
18:53:10  [Pipeline] {
18:53:10  [Pipeline] checkout
18:53:10  The recommended git tool is: NONE
18:53:10  using credential UP_GITLAB_USER
18:53:10  Cloning the remote Git repository
18:53:10  Cloning repository https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git
18:53:10   > git init /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service # timeout=10
18:53:10  Fetching upstream changes from https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git
18:53:10   > git --version # timeout=10
18:53:10   > git --version # 'git version 2.43.5'
18:53:10  using GIT_ASKPASS to set credentials UP_GITLAB_USER
18:53:10   > git fetch --tags --force --progress -- https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git +refs/heads/*:refs/remotes/origin/* # timeout=10
18:53:47  Avoid second fetch
18:53:47  Checking out Revision 1d2ebd45e29fc67ea7b32a1b4e1e08e63aa453a7 (origin/ansible_prod)
18:53:48  Commit message: "Update b6ov_mbt_tdc.json"
18:53:47   > git config remote.origin.url https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git # timeout=10
18:53:47   > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
18:53:47   > git rev-parse origin/ansible_prod^{commit} # timeout=10
18:53:47   > git config core.sparsecheckout # timeout=10
18:53:47   > git checkout -f 1d2ebd45e29fc67ea7b32a1b4e1e08e63aa453a7 # timeout=10
18:53:48   > git rev-list --no-walk 1d2ebd45e29fc67ea7b32a1b4e1e08e63aa453a7 # timeout=10
18:53:48  [Pipeline] }
18:53:48  [Pipeline] // dir
18:53:48  [Pipeline] }
18:53:48  [Pipeline] // retry
18:53:48  [Pipeline] sh
18:53:49  + cp -rf iipv_billing_profile_service/EKS/IIPV_BILLING_PROFILE_SERVICE/iipv_billing_profile_service_ocp_prod.json /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service_ocp_prod.json
18:53:49  [Pipeline] readJSON
18:53:49  [Pipeline] echo
18:53:49  iipv_billing_profile_service deployConfigProperty => [pipeline_version:refs/heads/V1.3_OCP_Configmap, zone:[tdc, tpa, sac, b2b], prod_tdc_cluster:[name:tdcpdocpj14v.verizon.com, namespace:iipv-prod-bps, deploy-jenkins-label:unifiedpipeline-CD-ProdDeployAgent], prod_tpa_cluster:[name:tpapdocpj14v.verizon.com, namespace:iipv-prod-bps, deploy-jenkins-label:unifiedpipeline-CD-ProdDeployAgent], prod_sac_cluster:[name:sacpdocpj14v.verizon.com, namespace:iipv-prod-bps, deploy-jenkins-label:unifiedpipeline-CD-ProdDeployAgent], prod_b2b_cluster:[name:tpapdocpj14v.verizon.com, namespace:iipv-prod-bps-b2b, deploy-jenkins-label:unifiedpipeline-CD-ProdDeployAgent], artifactory_tdc_info:[prod-host:oneartifactoryci.verizon.com, prod-repo:iipv-docker-prod], artifactory_tpa_info:[prod-host:oneartifactoryci.verizon.com, prod-repo:iipv-docker-prod], artifactory_sac_info:[prod-host:oneartifactoryci.verizon.com, prod-repo:iipv-docker-prod], artifactory_b2b_info:[prod-host:oneartifactoryci.verizon.com, prod-repo:iipv-docker-prod], kubeConfig:[repo:gitlab.verizon.com/nsa_techops/nsa_svc.git, fileName:ocp_{{zone}}_bps_iipv_prod.config, service_account:{{zone}}pd-iipv-prod-bps-{{zone}}-ocp-sa, branch:master], aws_info:[aws_region:us-east-1, aws_account:ocp-pr], config:[global_cm:false, global_secret:true, global_config_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_config_branch:prod, global_configmap_name:global-properties, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, sealed_secret_name:prod-datasources], value_b2b_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], value_tdc_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], value_tpa_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], value_sac_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], email_recipient:dinesh.sundaram@verizon.com]
18:53:49  [Pipeline] sh
18:53:50  + rm -rf iipv_billing_profile_service@tmp
18:53:50  [Pipeline] echo
18:53:50  ############ Inside Schedule Parameters #############
18:53:50  [Pipeline] echo
18:53:50  ****** Creating Selective Pipeline Stages for Current Deployment ******
18:53:50  [Pipeline] echo
18:53:50  params.global_config_skip => true
18:53:50  [Pipeline] echo
18:53:50  params.global_secret_skip => false
18:53:50  [Pipeline] echo
18:53:50  Inside stage list exclude Ingress
18:53:50  [Pipeline] echo
18:53:50  Selected Pipeline Stages for current Deployment => [Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus]
18:53:50  [Pipeline] echo
18:53:50  Looking for b2b zone specific config
18:53:50  [Pipeline] echo
18:53:50  inside zone config for docker cred
18:53:50  [Pipeline] echo
18:53:50  inside PROD zone config
18:53:50  [Pipeline] echo
18:53:50  Inside OCP Zone
18:53:50  [Pipeline] echo
18:53:50  params => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv]
18:53:50  [Pipeline] echo
18:53:50  [INFO] [2025-09-05T09:23:50.836501919] Unable to read app_config detail. Cannot get property 'location' on null object
18:53:50  [Pipeline] echo
18:53:50  Final Pipeline Params => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv, email_recipient:dinesh.sundaram@verizon.com, region:us-east-1, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_{{zone}}_bps_iipv_prod.config, kubeConfigSA:{{zone}}pd-iipv-prod-bps-{{zone}}-ocp-sa, kubeConfigBranch:master, awsAccount:ocp-pr, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, global_secret_name:prod-datasources]
18:53:50  [Pipeline] echo
18:53:50  No Direct service list to deploy.. will use Fetchlist mechanism...
18:53:50  [Pipeline] echo
18:53:50  Final Pipeline Stages => [Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus]
18:53:50  [Pipeline] }
18:53:50  [Pipeline] // script
18:53:50  [Pipeline] }
18:53:51  [Pipeline] // stage
18:53:51  [Pipeline] stage
18:53:51  [Pipeline] { (Stage Artifact to Prod)
18:53:51  Stage "Stage Artifact to Prod" skipped due to when conditional
18:53:51  [Pipeline] getContext
18:53:51  [Pipeline] }
18:53:51  [Pipeline] // stage
18:53:51  [Pipeline] stage
18:53:51  [Pipeline] { (Get Services Image)
18:53:51  [Pipeline] script
18:53:51  [Pipeline] {
18:53:51  [Pipeline] echo
18:53:51  pCategory => NA
18:53:51  [Pipeline] dir
18:53:51  Running in /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service
18:53:51  [Pipeline] {
18:53:51  [Pipeline] checkout
18:53:51  The recommended git tool is: NONE
18:53:52  using credential UP_GITLAB_USER
18:53:52  Fetching changes from the remote Git repository
18:53:52   > git rev-parse --resolve-git-dir /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service/.git # timeout=10
18:53:52   > git config remote.origin.url https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git # timeout=10
18:53:52  Fetching upstream changes from https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git
18:53:52   > git --version # timeout=10
18:53:52   > git --version # 'git version 2.43.5'
18:53:52  using GIT_ASKPASS to set credentials UP_GITLAB_USER
18:53:52   > git fetch --tags --force --progress -- https://gitlab.verizon.com/marvel_cicd/pipeline-resources.git +refs/heads/*:refs/remotes/origin/* # timeout=10
18:53:53  Checking out Revision 966f9915c079871f0b496b2e48b8e24d08faf6b4 (origin/ansible_stage)
18:53:54  Commit message: "Update db_rtd_fs5v_oracle_T1.json"
18:53:53   > git rev-parse origin/ansible_stage^{commit} # timeout=10
18:53:53   > git config core.sparsecheckout # timeout=10
18:53:53   > git checkout -f 966f9915c079871f0b496b2e48b8e24d08faf6b4 # timeout=10
18:53:54   > git rev-list --no-walk 966f9915c079871f0b496b2e48b8e24d08faf6b4 # timeout=10
18:53:54  [Pipeline] }
18:53:54  [Pipeline] // dir
18:53:54  [Pipeline] echo
18:53:54  stage artifact params: [gitGroup:iipv_billing_profile_service, releaseId:release/25.89.100, branch:25.89.100, artifactStageFileName:prod.json, pArtifactoryRepo:iipv-docker-prod, sourceEnv:SITG, serviceListGitRepo:https://gitlab.verizon.com/nsa_cicd/prod_cicd/-/tree/Prod_test, deployType:EKS, env:T1, vsad:IIPV, config_repo_location:null, config_repo:null, config_repo_branch:null, deployConfigOnly:false]
18:53:54  [Pipeline] echo
18:53:54  using b2b config for SITG
18:53:54  [Pipeline] echo
18:53:54  using the IOT_DEPLOY-->False for SITG
18:53:54  [Pipeline] sh
18:53:55  + cp -rf iipv_billing_profile_service/EKS/IIPV_BILLING_PROFILE_SERVICE/iipv_billing_profile_service_ocp_T1.json /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/iipv_billing_profile_service_T1.json
18:53:55  [Pipeline] readJSON
18:53:55  [Pipeline] echo
18:53:55  iipv_billing_profile_service deployConfigProperty => [pipeline_version:refs/heads/V1.3_OCP_Configmap, zone:[tdc, tpa, sac, b2b], sitb_tdc_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitg_tdc_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitg_sac_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitb_sac_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitb_tpa_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitg_tpa_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitb_b2b_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], sitg_b2b_cluster:[name:tpanpocpj14v.ebiz.verizon.com, namespace:iipv-sit-bps], artifactory_tdc_info:[Non-prod-host:oneartifactoryci.verizon.com, Non-prod-repo:iipv-docker-np], artifactory_tpa_info:[Non-prod-host:oneartifactoryci.verizon.com, Non-prod-repo:iipv-docker-np], artifactory_sac_info:[Non-prod-host:oneartifactoryci.verizon.com, Non-prod-repo:iipv-docker-np], artifactory_b2b_info:[Non-prod-host:oneartifactoryci.verizon.com, Non-prod-repo:iipv-docker-np], kubeConfig:[repo:gitlab.verizon.com/nsa_techops/nsa_svc.git, fileName:ocp_tpa_iipv_bps_sit.config, service_account:tpanp-iipv-sit-bps-ocp-sa, branch:master], aws_info:[aws_region:us-east-1, aws_account:ocp-np], config:[global_cm:false, global_secret:true, global_config_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_config_branch:stage, global_configmap_name:global-properties, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:stage, sealed_secret_name:sit-datasources], valueg_tdc_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueb_tdc_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueg_tpa_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueg_sac_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueb_sac_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueg_b2b_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueb_b2b_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], valueb_tpa_yaml:[repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, branch:ansible_stage, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv], email_recipient:dinesh.sundaram@verizon.com]
18:53:55  [Pipeline] echo
18:53:55  stage artifact final params: [gitGroup:iipv_billing_profile_service, releaseId:release/25.89.100, branch:25.89.100, artifactStageFileName:prod.json, pArtifactoryRepo:iipv-docker-prod, sourceEnv:SITG, serviceListGitRepo:https://gitlab.verizon.com/nsa_cicd/prod_cicd/-/tree/Prod_test, deployType:EKS, env:T1, vsad:IIPV, config_repo_location:null, config_repo:null, config_repo_branch:null, deployConfigOnly:false, envIndex:SIT1G, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_tpa_iipv_bps_sit.config, kubeConfigBranch:master, kubeConfigSA:tpanp-iipv-sit-bps-ocp-sa, awsAccount:ocp-np, prodArtifactoryRepo:iipv-docker-prod, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-np, sitb_cluster_name:tpanpocpj14v.ebiz.verizon.com, sitb_cluster_namespace:iipv-sit-bps, sitg_cluster_name:tpanpocpj14v.ebiz.verizon.com, sitg_cluster_namespace:iipv-sit-bps, sitg_deployJenkinsLabel:null, sitb_deployJenkinsLabel:null]
18:53:55  [Pipeline] sh
18:53:56  + rm -rf iipv_billing_profile_service@tmp
18:53:56  [Pipeline] sh
18:53:57  ++ date -u +%m%d%Y%H%M%S
18:53:57  + echo 09052025132357
18:53:57  [Pipeline] dir
18:53:57  Running in /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/servicelist
18:53:57  [Pipeline] {
18:53:57  [Pipeline] retry
18:53:57  [Pipeline] {
18:53:58  [Pipeline] checkout
18:53:58  The recommended git tool is: NONE
18:53:58  using credential UP_GITLAB_USER
18:53:58  Cloning the remote Git repository
18:53:58  Cloning repository https://gitlab.verizon.com/nsa_cicd/prod_cicd.git
18:53:58   > git init /var/jenkins_vcg5/workspace/VZW.UNIF.CICD.PIPELINES/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/servicelist # timeout=10
18:53:58  Fetching upstream changes from https://gitlab.verizon.com/nsa_cicd/prod_cicd.git
18:53:58   > git --version # timeout=10
18:53:58   > git --version # 'git version 2.43.5'
18:53:58  using GIT_ASKPASS to set credentials UP_GITLAB_USER
18:53:58   > git fetch --tags --force --progress -- https://gitlab.verizon.com/nsa_cicd/prod_cicd.git +refs/heads/*:refs/remotes/origin/* # timeout=10
18:54:02  Avoid second fetch
18:54:02  Checking out Revision c518377f7e66b0c8b3087d0549d8184acf86941c (origin/Prod_test)
18:54:02  Commit message: "Update up_services_to_deploy.txt"
18:54:02   > git config remote.origin.url https://gitlab.verizon.com/nsa_cicd/prod_cicd.git # timeout=10
18:54:02   > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
18:54:02   > git rev-parse origin/Prod_test^{commit} # timeout=10
18:54:02   > git config core.sparsecheckout # timeout=10
18:54:02   > git checkout -f c518377f7e66b0c8b3087d0549d8184acf86941c # timeout=10
18:54:02   > git rev-list --no-walk c518377f7e66b0c8b3087d0549d8184acf86941c # timeout=10
18:54:03  [Pipeline] }
18:54:03  [Pipeline] // retry
18:54:03  [Pipeline] }
18:54:03  [Pipeline] // dir
18:54:03  [Pipeline] echo
18:54:03  temp vsad cofigured as: IIPV
18:54:03  [Pipeline] readFile
18:54:03  [Pipeline] echo
18:54:03  List of services to deploy in IIPV --> [bps-processor-service]
18:54:03  [Pipeline] echo
18:54:03  params => [gitGroup:iipv_billing_profile_service, releaseId:release/25.89.100, branch:25.89.100, artifactStageFileName:prod.json, pArtifactoryRepo:iipv-docker-prod, sourceEnv:SITG, serviceListGitRepo:https://gitlab.verizon.com/nsa_cicd/prod_cicd/-/tree/Prod_test, deployType:EKS, env:T1, vsad:IIPV, config_repo_location:null, config_repo:null, config_repo_branch:null, deployConfigOnly:false, envIndex:SIT1G, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_tpa_iipv_bps_sit.config, kubeConfigBranch:master, kubeConfigSA:tpanp-iipv-sit-bps-ocp-sa, awsAccount:ocp-np, prodArtifactoryRepo:iipv-docker-prod, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-np, sitb_cluster_name:tpanpocpj14v.ebiz.verizon.com, sitb_cluster_namespace:iipv-sit-bps, sitg_cluster_name:tpanpocpj14v.ebiz.verizon.com, sitg_cluster_namespace:iipv-sit-bps, sitg_deployJenkinsLabel:null, sitb_deployJenkinsLabel:null]
18:54:03  [Pipeline] echo
18:54:03  not an MTAS Condition
18:54:03  [Pipeline] retry
18:54:03  [Pipeline] {
18:54:03  [Pipeline] echo
18:54:03  [INFO] [2025-09-05T09:24:03.364397836] Inside Artifact Staging from SITG 
18:54:03  [Pipeline] echo
18:54:03  Jenkins Label param as:  null
18:54:03  [Pipeline] echo
18:54:03  Jenkins Label set as unifiedpipeline-CD-DeployAgent
18:54:03  [Pipeline] echo
18:54:03  [INFO] [2025-09-05T09:24:03.412940108] kubeConfigFileName is => ocp_tpa_iipv_bps_sit.config
18:54:03  [Pipeline] echo
18:54:03  [INFO] [2025-09-05T09:24:03.434004004] clusteLogin => gitlab.verizon.com/nsa_techops/nsa_svc.git|master|ocp_tpa_iipv_bps_sit.config|tpanp-iipv-sit-bps-ocp-sa|ocp-np
18:54:03  [Pipeline] build (Building VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.NPRD.JOBS » VZW.EKS.DEPLOYMENT.STATUS)
18:54:03  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.NPRD.JOBS » VZW.EKS.DEPLOYMENT.STATUS

18:54:18  Starting building: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.NPRD.JOBS » VZW.EKS.DEPLOYMENT.STATUS #22027

18:54:51  Build VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.NPRD.JOBS » VZW.EKS.DEPLOYMENT.STATUS #22027
 completed: SUCCESS
18:54:51  [Pipeline] echo
18:54:51  pipeline_status => [svc_list:[bps-gateway-service:25.89.1008fd1549268446509052025060930, bps-globalrouter-service:main195733f267453909042025104343, bps-processor-service:25.89.1005fa96fa268756109052025124557], cm_list:[]]
18:54:51  [Pipeline] }
18:54:51  [Pipeline] // retry
18:54:51  [Pipeline] echo
18:54:51  *****************Artfact Staging for Service: bps-processor-service Start *****************
18:54:51  [Pipeline] echo
18:54:51  [INFO] [2025-09-05T09:24:51.134522792] No config tag enrty found for bps-processor-service in the Deployed service list: Cannot invoke method split() on null object
18:54:51  [Pipeline] echo
18:54:51  serviceImageRetag --> 25.89.1005fa96fa268756109052025124557
18:54:51  [Pipeline] echo
18:54:51  sourceServiceName: bps-processor-service
18:54:51  [Pipeline] echo
18:54:51  api => https://oneartifactoryci.verizon.com/artifactory/api/copy/iipv-docker-np/vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557?to=iipv-docker-prod/vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557
18:54:51  [Pipeline] withCredentials
18:54:51  Masking supported pattern matches of $USERNAME or $PASSWORD
18:54:51  [Pipeline] {
18:54:51  [Pipeline] echo
18:54:51  Credentail Id: UP_NPARTIFACT_USER
18:54:51  [Pipeline] retry
18:54:51  [Pipeline] {
18:54:51  [Pipeline] sh
18:54:52  + curl -X POST -u ****:**** 'https://oneartifactoryci.verizon.com/artifactory/api/copy/iipv-docker-np/vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557?to=iipv-docker-prod/vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557' -u ****:****
18:54:52    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
18:54:52                                   Dload  Upload   Total   Spent    Left  Speed
18:54:52  
18:54:52    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
18:54:52  100   347    0   347    0     0   1094      0 --:--:-- --:--:-- --:--:--  1094
18:54:52  [Pipeline] echo
18:54:52  status => {
18:54:52    "messages" : [ {
18:54:52      "level" : "INFO",
18:54:52      "message" : "copying iipv-docker-np:vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557 to iipv-docker-prod:vzw/iipv/release/25.89.100/bps-processor-service/25.89.1005fa96fa268756109052025124557 completed successfully, 7 artifacts and 1 folders were copied"
18:54:52    } ]
18:54:52  }
18:54:52  [Pipeline] }
18:54:52  [Pipeline] // retry
18:54:52  [Pipeline] }
18:54:52  [Pipeline] // withCredentials
18:54:52  [Pipeline] echo
18:54:52  [INFO] [2025-09-05T09:24:52.611117181] Unable to tag git repo for service bps-processor-service. using existing config tag 
18:54:52  [Pipeline] echo
18:54:52  *****************Artfact Staging for Service: bps-processor-service End *****************
18:54:52  [Pipeline] echo
18:54:52  staged Service List --> bps-processor-service|25.89.1005fa96fa268756109052025124557|,
18:54:52  [Pipeline] writeFile
18:54:52  [Pipeline] withCredentials
18:54:52  Masking supported pattern matches of $USERNAME or $PASSWORD
18:54:52  [Pipeline] {
18:54:52  [Pipeline] echo
18:54:52  Credentail Id: UP_NPARTIFACT_USER
18:54:52  [Pipeline] retry
18:54:52  [Pipeline] {
18:54:52  [Pipeline] sh
18:54:53  + curl -s -u ****:**** -T prod.json https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/deploy/iipv/
18:54:53  {
18:54:53    "repo" : "I2IV_SRE",
18:54:53    "path" : "/release/25.89.100/deploy/iipv/prod.json",
18:54:53    "created" : "2025-09-04T13:58:49.415-04:00",
18:54:53    "createdBy" : "svc-npartifact-up",
18:54:53    "downloadUri" : "https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/deploy/iipv/prod.json",
18:54:53    "mimeType" : "application/json",
18:54:53    "size" : "85",
18:54:53    "checksums" : {
18:54:53      "sha1" : "d5fb9e19d6963d8d6276d9f333b1692970e39cc3",
18:54:53      "md5" : "1e7b8affa0d4783ade93b67de77ed1c7",
18:54:53      "sha256" : "6428a919777e1f18d8e6f09eeae0babc7014e29cc7863d45cb18b683cb4f0d55"
18:54:53    },
18:54:53    "originalChecksums" : {
18:54:53      "sha256" : "6428a919777e1f18d8e6f09eeae0babc7014e29cc7863d45cb18b683cb4f0d55"
18:54:53    },
18:54:53    "uri" : "https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/deploy/iipv/prod.json"
18:54:53  }
18:54:53  [Pipeline] }
18:54:53  [Pipeline] // retry
18:54:53  [Pipeline] }
18:54:54  [Pipeline] // withCredentials
18:54:54  [Pipeline] sh
18:54:54  + rm prod.json
18:54:55  [Pipeline] echo
18:54:55  [INFO] [2025-09-05T09:24:55.032524539] generateDeployServicesList() full_deployment => null
18:54:55  [Pipeline] withCredentials
18:54:55  Masking supported pattern matches of $USERNAME or $PASSWORD
18:54:55  [Pipeline] {
18:54:55  [Pipeline] echo
18:54:55  Credentail Id: UP_NPARTIFACT_USER
18:54:55  [Pipeline] retry
18:54:55  [Pipeline] {
18:54:55  [Pipeline] sh
18:54:55  + curl -u ****:**** -X GET https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/deploy/iipv/prod.json
18:54:55    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
18:54:55                                   Dload  Upload   Total   Spent    Left  Speed
18:54:55  
18:54:55    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
18:54:55  100    85  100    85    0     0    342      0 --:--:-- --:--:-- --:--:--   342
18:54:56  [Pipeline] }
18:54:56  [Pipeline] // retry
18:54:56  [Pipeline] readJSON
18:54:56  [Pipeline] }
18:54:56  [Pipeline] // withCredentials
18:54:56  [Pipeline] echo
18:54:56  service deploy: bps-processor-service|25.89.1005fa96fa268756109052025124557|
18:54:56  [Pipeline] }
18:54:56  [Pipeline] // script
18:54:56  [Pipeline] }
18:54:56  [Pipeline] // stage
18:54:56  [Pipeline] stage
18:54:56  [Pipeline] { (Parallel Config)
18:54:56  [Pipeline] parallel
18:54:56  [Pipeline] { (Branch: Deploy-Global Config)
18:54:56  [Pipeline] { (Branch: Deploy-Global Secret)
18:54:56  [Pipeline] stage
18:54:56  [Pipeline] { (Deploy-Global Config)
18:54:56  [Pipeline] stage
18:54:56  [Pipeline] { (Deploy-Global Secret)
18:54:56  [Pipeline] script
18:54:56  [Pipeline] {
18:54:56  [Pipeline] script
18:54:56  [Pipeline] {
18:54:56  [Pipeline] }
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.027748684] Inside DeployTasks
18:54:59  [Pipeline] // script
18:54:59  [Pipeline] }
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.093559057] deployType => GLOBAL_SECRET
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.127980104] Deploy Producer called
18:54:59  [Pipeline] // stage
18:54:59  [Pipeline] }
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.258380118] Deploy Factory Generated..
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.313140598] log: starting PROD Deployment for PROD environment 
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.343607237] param => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv, email_recipient:dinesh.sundaram@verizon.com, region:us-east-1, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_{{zone}}_bps_iipv_prod.config, kubeConfigSA:{{zone}}pd-iipv-prod-bps-{{zone}}-ocp-sa, kubeConfigBranch:master, awsAccount:ocp-pr, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, global_secret_name:prod-datasources, serviceList:bps-processor-service|25.89.1005fa96fa268756109052025124557|]
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.374100796] Zone check3 OCP: b2b
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.404352951] kubeConfigFileName is => ocp_b2b_bps_iipv_prod.config and kubeConfigSVCA is => b2bpd-iipv-prod-bps-b2b-ocp-sa
18:54:59  [Pipeline] echo
18:54:59  Jenkins Label param as:  unifiedpipeline-CD-ProdDeployAgent
18:54:59  [Pipeline] echo
18:54:59  Jenkins Label set as unifiedpipeline-CD-ProdDeployAgent
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.466003551] clusteLogin => gitlab.verizon.com/nsa_techops/nsa_svc.git|master|ocp_b2b_bps_iipv_prod.config|b2bpd-iipv-prod-bps-b2b-ocp-sa|ocp-pr
18:54:59  [Pipeline] retry
18:54:59  [Pipeline] {
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.537453791] Inside Global_Secret Deployment
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.561241634] ============== Printing Deployment Cluster Details - Start ==============
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.588719451] Canary dEnv => PROD
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.616484283] ClusterName => tpapdocpj14v.verizon.com
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.643150596] Namespace => iipv-prod-bps-b2b
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.668880792] ENV => prod :: EnvIndex => PROD :: GITLAB_HOST =>gitlab.verizon.com/nsa_techops/iipv_secret.git|prod
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.694005869] ============== Printing Deployment Cluster Details - End ==============
18:54:59  [Pipeline] echo
18:54:59  [INFO] [2025-09-05T09:24:59.718939401] deployJenkinsLabel => unifiedpipeline-CD-ProdDeployAgent
18:54:59  [Pipeline] build (Building VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.SEALED_SECRET_JOB)
18:54:59  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.SEALED_SECRET_JOB

18:55:16  Starting building: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.SEALED_SECRET_JOB #10538

18:56:34  Build VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.SEALED_SECRET_JOB #10538
 completed: SUCCESS
18:56:34  [Pipeline] echo
18:56:34  pipeline_status => ServiceNamesSuccess:iipv-prod-datasources ServiceNamesFail: HelmRevision:bps-gateway-service:12|bps-globalrouter-service:2|bps-processor-service:17|iipv-prod-datasources:31
18:56:34  [Pipeline] }
18:56:34  [Pipeline] // retry
18:56:34  [Pipeline] echo
18:56:34  [INFO] [2025-09-05T09:26:34.900283545] Deploy Completed..
18:56:34  [Pipeline] echo
18:56:34  deploy Secret success
18:56:34  [Pipeline] }
18:56:34  [Pipeline] // script
18:56:34  [Pipeline] }
18:56:35  [Pipeline] // stage
18:56:35  [Pipeline] }
18:56:35  [Pipeline] // parallel
18:56:35  [Pipeline] }
18:56:35  [Pipeline] // stage
18:56:35  [Pipeline] stage
18:56:35  [Pipeline] { (Deploy Services)
18:56:35  [Pipeline] script
18:56:35  [Pipeline] {
18:56:35  [Pipeline] echo
18:56:35  pipelineParams.deployType => EKS
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.292207738] Inside DeployTasks
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.312960688] deployType => EKS
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.333759149] Deploy Producer called
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.356361481] Deploy Factory Generated..
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.379872209] log: starting Deployment for PROD environment 
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.402206107] Zone check7 OCP: b2b
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.423727420] kubeConfigFileName is => ocp_b2b_bps_iipv_prod.config and kubeConfigSVCA is => b2bpd-iipv-prod-bps-b2b-ocp-sa
18:56:35  [Pipeline] echo
18:56:35  Docker Creds param as:  null
18:56:35  [Pipeline] echo
18:56:35  Docker Creds set as cicd-docker-prod-regcred
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.472200252] Inside PROD Deployment
18:56:35  [Pipeline] echo
18:56:35  Jenkins Label param as:  unifiedpipeline-CD-ProdDeployAgent
18:56:35  [Pipeline] echo
18:56:35  Jenkins Label set as  unifiedpipeline-CD-ProdDeployAgent
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.518278951] printing the parameters: [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv, email_recipient:dinesh.sundaram@verizon.com, region:us-east-1, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_{{zone}}_bps_iipv_prod.config, kubeConfigSA:b2bpd-iipv-prod-bps-b2b-ocp-sa, kubeConfigBranch:master, awsAccount:ocp-pr, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, global_secret_name:prod-datasources, serviceList:bps-processor-service|25.89.1005fa96fa268756109052025124557|, rollBack:no]
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.539189845] ============== Printing Deployment Cluster Details - Start ==============
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.559711711] clusteLogin => gitlab.verizon.com/nsa_techops/nsa_svc.git|master|ocp_b2b_bps_iipv_prod.config|b2bpd-iipv-prod-bps-b2b-ocp-sa|ocp-pr
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.579051466] ClusterName => tpapdocpj14v.verizon.com
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.599210146] Namespace => iipv-prod-bps-b2b
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.618987550] env apigee flag => false
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.639940353] NoApigee Flag => false
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.662126598] ENV => prod :: EnvIndex => PROD :: GIT_URL_VALUES_YAML =>gitlab.verizon.com/nsa_techops/hivv_1.18.git|ansible_prod
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.686022453] config_yaml_file_name => iipv_bps
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.707675739] ============== Printing Deployment Cluster Details - End ==============
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.731199377] param => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv, email_recipient:dinesh.sundaram@verizon.com, region:us-east-1, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_{{zone}}_bps_iipv_prod.config, kubeConfigSA:b2bpd-iipv-prod-bps-b2b-ocp-sa, kubeConfigBranch:master, awsAccount:ocp-pr, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, global_secret_name:prod-datasources, serviceList:bps-processor-service|25.89.1005fa96fa268756109052025124557|, rollBack:no]
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.753999843] dockerCred --> cicd-docker-prod-regcred
18:56:35  [Pipeline] echo
18:56:35  [INFO] [2025-09-05T09:26:35.777447700] deployJenkinsLabel --> unifiedpipeline-CD-ProdDeployAgent
18:56:35  [Pipeline] retry
18:56:35  [Pipeline] {
18:56:35  [Pipeline] build (Building VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.DEPLOY_JOB)
18:56:35  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.DEPLOY_JOB

18:56:54  Starting building: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.DEPLOY_JOB #23757

19:03:42  Build VZW.UNIF.CICD.PIPELINES » VZW.UNIF.DEPLOYMENT.PROD.JOBS » VZW.UNIF.EKS.DEPLOY_JOB #23757
 completed: SUCCESS
19:03:42  [Pipeline] }
19:03:42  [Pipeline] // retry
19:03:42  [Pipeline] echo
19:03:42  pipeline_status => ServiceNamesSuccess:bps-processor-service ServiceNamesFail: ConfigMapNamesSuccess: ConfigMapNamesFail:
19:03:42  [Pipeline] echo
19:03:42  [INFO] [2025-09-05T09:33:42.256126418] Deploy Completed..
19:03:42  [Pipeline] echo
19:03:42  deployTasks success
19:03:42  [Pipeline] }
19:03:42  [Pipeline] // script
19:03:42  [Pipeline] }
19:03:42  [Pipeline] // stage
19:03:42  [Pipeline] stage
19:03:42  [Pipeline] { (Get Deployment Status)
19:03:42  [Pipeline] script
19:03:42  [Pipeline] {
19:03:42  [Pipeline] sh
19:03:43  ++ date -u +%m%d%Y%H%M%S
19:03:43  + echo 09052025133342
19:03:43  [Pipeline] echo
19:03:43  No service failed to deploy
19:03:43  [Pipeline] echo
19:03:43  Empty: no config deployed successfully
19:03:43  [Pipeline] echo
19:03:43  Empty: no config deployment failed
19:03:43  [Pipeline] echo
19:03:43  combineSuccessList => [bps-processor-service]
19:03:43  [Pipeline] echo
19:03:43  combineFailedList => []
19:03:43  [Pipeline] echo
19:03:43  matchSer => bps-processor-service|25.89.1005fa96fa268756109052025124557|
19:03:43  [Pipeline] echo
19:03:43  serTag => 25.89.1005fa96fa268756109052025124557
19:03:43  [Pipeline] echo
19:03:43  svcImageSFtag => PF-PROD-09052025133342
19:03:43  [Pipeline] echo
19:03:43  Empty: no failed deployed service list found
19:03:43  [Pipeline] echo
19:03:43  [INFO] [2025-09-05T09:33:43.666045410] deploy Status JSON body: {
19:03:43      "deploySuccess": [
19:03:43          {
19:03:43              "serviceName": "bps-processor-service",
19:03:43              "serviceImageTag": "25.89.1005fa96fa268756109052025124557",
19:03:43              "artifactImageTag": "25.89.1005fa96fa268756109052025124557",
19:03:43              "status": "Deployed",
19:03:43              "rollbacklog": "",
19:03:43              "buildCommitId": "5fa96fa",
19:03:43              "buildId": 9999
19:03:43          }
19:03:43      ],
19:03:43      "deployFailure": [
19:03:43          
19:03:43      ]
19:03:43  }
19:03:43  [Pipeline] echo
19:03:43  [INFO] [2025-09-05T09:33:43.687268708] tagRepoSvcCm: [bps-processor-service:25.89.1005fa96fa268756109052025124557:PF-PROD-09052025133342]
19:03:43  [Pipeline] }
19:03:43  [Pipeline] // script
19:03:43  [Pipeline] }
19:03:43  [Pipeline] // stage
19:03:43  [Pipeline] stage
19:03:43  [Pipeline] { (Tag Repo)
19:03:43  [Pipeline] script
19:03:43  [Pipeline] {
19:03:43  [Pipeline] build (Scheduling VZW.UNIF.CICD.PIPELINES » VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD » VZW.UNIF.DEPLOYMENT.PIPELINE-TAG-REPO)
19:03:43  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD » VZW.UNIF.DEPLOYMENT.PIPELINE-TAG-REPO

19:03:43  [Pipeline] }
19:03:43  [Pipeline] // script
19:03:43  [Pipeline] }
19:03:44  [Pipeline] // stage
19:03:44  [Pipeline] stage
19:03:44  [Pipeline] { (Pod-HC)
19:03:44  [Pipeline] script
19:03:44  [Pipeline] {
19:03:44  [Pipeline] echo
19:03:44  env.CONFIG_ONLY => false
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.755457289] Inside ValidationTasks
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.777262477] EKS
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.809132680] Validation Producer called
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.842153713] Validation Factory Generated
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.866754250] log: starting Deployment for PROD environment 
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.892047589] Zone check11 OCP: b2b
19:03:44  [Pipeline] echo
19:03:44  [INFO] [2025-09-05T09:33:44.918410427] kubeConfigFileName is => ocp_b2b_bps_iipv_prod.config and kubeConfigSVCA is => b2bpd-iipv-prod-bps-b2b-ocp-sa
19:03:44  [Pipeline] retry
19:03:44  [Pipeline] {
19:03:44  [Pipeline] echo
19:03:45  [INFO] [2025-09-05T09:33:44.985890088] Inside PROD Deployment
19:03:45  [Pipeline] echo
19:03:45  [INFO] [2025-09-05T09:33:45.010081248] clusteLogin => gitlab.verizon.com/nsa_techops/nsa_svc.git|master|ocp_b2b_bps_iipv_prod.config|b2bpd-iipv-prod-bps-b2b-ocp-sa|ocp-pr
19:03:45  [Pipeline] echo
19:03:45  Jenkins Label param as:  unifiedpipeline-CD-ProdDeployAgent
19:03:45  [Pipeline] echo
19:03:45  Jenkins Label set as  unifiedpipeline-CD-ProdDeployAgent
19:03:45  [Pipeline] echo
19:03:45  param.CMD_PIPELINE => null
19:03:45  [Pipeline] build (Building VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.POD.HEALTH)
19:03:45  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.POD.HEALTH

19:04:00  Starting building: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.POD.HEALTH #18072

19:12:31  Build VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.POD.HEALTH #18072
 completed: FAILURE
19:12:31  [Pipeline] echo
19:12:31  podHC_Status => null
19:12:32  [Pipeline] }
19:12:32  [Pipeline] // retry
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.064722117] Validation Completed
19:12:32  [Pipeline] }
19:12:32  [Pipeline] // script
19:12:32  [Pipeline] }
19:12:32  [Pipeline] // stage
19:12:32  [Pipeline] stage
19:12:32  [Pipeline] { (Ingress HC)
19:12:32  [Pipeline] script
19:12:32  [Pipeline] {
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.273072551] Inside ValidationTasks
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.294020803] EKS
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.315865301] Validation Producer called
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.337445814] Validation Factory Generated
19:12:32  [Pipeline] retry
19:12:32  [Pipeline] {
19:12:32  [Pipeline] echo
19:12:32  [INFO] [2025-09-05T09:42:32.403459696] Inside Ingress Health Check Job
19:12:32  [Pipeline] echo
19:12:32  Jenkins Label param as:  unifiedpipeline-CD-ProdDeployAgent
19:12:32  [Pipeline] echo
19:12:32  Jenkins Label set as  unifiedpipeline-CD-ProdDeployAgent
19:12:32  [Pipeline] build (Building VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.INGRESS.HEALTH)
19:12:32  Scheduling project: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.INGRESS.HEALTH

19:12:48  Starting building: VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.INGRESS.HEALTH #17915

19:17:32  Build VZW.UNIF.CICD.PIPELINES » VZW.UNIF.VALIDATION.PROD.JOBS » VZW.EKS.INGRESS.HEALTH #17915
 completed: SUCCESS
19:17:32  [Pipeline] }
19:17:32  [Pipeline] // retry
19:17:32  [Pipeline] echo
19:17:32  [INFO] [2025-09-05T09:47:32.890466573] Validation Completed
19:17:32  [Pipeline] echo
19:17:32  Ingress success
19:17:32  [Pipeline] }
19:17:32  [Pipeline] // script
19:17:32  [Pipeline] }
19:17:33  [Pipeline] // stage
19:17:33  [Pipeline] stage
19:17:33  [Pipeline] { (Update Deploy Status)
19:17:33  [Pipeline] script
19:17:33  [Pipeline] {
19:17:33  [Pipeline] echo
19:17:33  updateArtifactTag => false
19:17:33  [Pipeline] echo
19:17:33  validatePostPodHC => true
19:17:33  [Pipeline] echo
19:17:33  pipelineParams => [releaseId:release/25.89.100, branch:25.89.100, trunk:false, stages:[Global_Config, Global_Secret, Fetch_DeployList, Service_Deploy, Pod_HC, Ingress_HC, Ingress_HC, Update_DeployStatus], deployConfigOnly:false, skipArtifactStaging:false, deployGcOnly:false, deployEnv:PROD, dEnv:prod1, env:T1, envIndex:1, WorkflowId:null, gitGroup:iipv_billing_profile_service, vsad:IIPV, deployType:EKS, skipGC:false, skipGS:false, noApigeeFlag:false, active_passive_sync:true, deployZone:b2b, latest_app_config_only:NA, projectCategory:NA, vsad_iot:NA, global_config_skip:true, global_secret_skip:false, pipeline_version:refs/heads/V1.3_OCP_Configmap, dockerRegCreds:null, sourceEnv:SITG, dcRegion:, artifactoryHost:oneartifactoryci.verizon.com, artifactoryRepo:iipv-docker-prod, PROD_cluster_name:tpapdocpj14v.verizon.com, PROD_cluster_namespace:iipv-prod-bps-b2b, PROD_noapigee_flag:false, PROD_deployJenkinsLabel:unifiedpipeline-CD-ProdDeployAgent, valueYaml_repo:gitlab.verizon.com/nsa_techops/hivv_1.18.git, valueYaml_branch:ansible_prod, config_yaml_file_name:iipv_bps, values_yaml_file_name:iipv, email_recipient:dinesh.sundaram@verizon.com, region:us-east-1, kubeConfigRepo:gitlab.verizon.com/nsa_techops/nsa_svc.git, kubeConfigFileName:ocp_{{zone}}_bps_iipv_prod.config, kubeConfigSA:b2bpd-iipv-prod-bps-b2b-ocp-sa, kubeConfigBranch:master, awsAccount:ocp-pr, global_secret_repo:gitlab.verizon.com/nsa_techops/iipv_secret.git, global_secret_branch:prod, global_secret_name:prod-datasources, serviceList:bps-processor-service|25.89.1005fa96fa268756109052025124557|, rollBack:no, deployStatus:ServiceNamesSuccess:bps-processor-service ServiceNamesFail: ConfigMapNamesSuccess: ConfigMapNamesFail:, parsedDeployStatus:[deploySuccess:[[serviceName:bps-processor-service, serviceImageTag:25.89.1005fa96fa268756109052025124557, artifactImageTag:25.89.1005fa96fa268756109052025124557, status:Deployed, rollbacklog:, buildCommitId:5fa96fa, buildId:9999]], deployFailure:[]], validator:Ingress, appType:EKS, podHCStatus:null]
19:17:33  [Pipeline] sh
19:17:33  ++ date -u +%m%d%Y%H%M%S
19:17:33  + echo 09052025134733
19:17:34  [Pipeline] echo
19:17:34  No service failed to deploy
19:17:34  [Pipeline] echo
19:17:34  Empty: no config deployed successfully
19:17:34  [Pipeline] echo
19:17:34  Empty: no config deployment failed
19:17:34  [Pipeline] echo
19:17:34  combineSuccessList => [bps-processor-service]
19:17:34  [Pipeline] echo
19:17:34  combineFailedList => []
19:17:34  [Pipeline] echo
19:17:34  matchSer => bps-processor-service|25.89.1005fa96fa268756109052025124557|
19:17:34  [Pipeline] echo
19:17:34  serTag => 25.89.1005fa96fa268756109052025124557
19:17:34  [Pipeline] echo
19:17:34  svcImageSFtag => PF-PROD-09052025134733
19:17:34  [Pipeline] echo
19:17:34  Empty: no failed deployed service list found
19:17:34  [Pipeline] echo
19:17:34  [INFO] [2025-09-05T09:47:34.358262022] deploy Status JSON body: {
19:17:34      "deploySuccess": [
19:17:34          {
19:17:34              "serviceName": "bps-processor-service",
19:17:34              "serviceImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:34              "artifactImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:34              "status": "Deployed",
19:17:34              "rollbacklog": "",
19:17:34              "buildCommitId": "5fa96fa",
19:17:34              "buildId": 9999
19:17:34          }
19:17:34      ],
19:17:34      "deployFailure": [
19:17:34          
19:17:34      ]
19:17:34  }
19:17:34  [Pipeline] echo
19:17:34  [INFO] [2025-09-05T09:47:34.379535850] tagRepoSvcCm: [bps-processor-service:25.89.1005fa96fa268756109052025124557:PF-PROD-09052025134733]
19:17:34  [Pipeline] sh
19:17:35  ++ date -u +%m%d%Y%H%M%S
19:17:35  + echo 09052025134734
19:17:35  [Pipeline] readJSON
19:17:35  [Pipeline] echo
19:17:35  No pod image tag found
19:17:35  [Pipeline] echo
19:17:35  No pod image tag found
19:17:35  [Pipeline] echo
19:17:35  No helm revision info found
19:17:35  [Pipeline] echo
19:17:35  No rollback log found
19:17:35  [Pipeline] echo
19:17:35  No rolloutList log found
19:17:35  [Pipeline] echo
19:17:35  Empty: no pod Image tag info found for service bps-processor-service
19:17:35  [Pipeline] echo
19:17:35  [INFO] [2025-09-05T09:47:35.588126005] combined deploy Status JSON body after pod HC: {
19:17:35      "serviceData": [
19:17:35          {
19:17:35              "serviceName": "bps-processor-service",
19:17:35              "serviceImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:35              "artifactImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:35              "status": "Deployed",
19:17:35              "rollbacklog": "",
19:17:35              "buildCommitId": "5fa96fa",
19:17:35              "buildId": 9999
19:17:35          }
19:17:35      ]
19:17:35  }
19:17:35  [Pipeline] libraryResource
19:17:35  [Pipeline] writeFile
19:17:35  [Pipeline] readJSON
19:17:35  [Pipeline] sh
19:17:36  ++ date -u +%Y-%m-%dT%H:%M:%SZ
19:17:36  + echo 2025-09-05T13:47:36Z
19:17:36  [Pipeline] echo
19:17:36  Formatted mail Deployment Report Object: [Success:[[serviceName:bps-processor-service, serviceImageTag:25.89.1005fa96fa268756109052025124557, artifactImageTag:25.89.1005fa96fa268756109052025124557, status:Deployed, rollbacklog:, buildCommitId:5fa96fa, buildId:9999]], Failed:[], deploymentTime:2025-09-05T13:47:36Z, jobUrl:https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/, deployedEnv:PROD, deploymentLog:https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/iipv_billing_profile_service/eks/PROD_313.json, globalConfigDeployment:false, globalSecretsDeployment:true]
19:17:36  [Pipeline] echo
19:17:36  mail payload: {
19:17:36      "serviceData": [
19:17:36          {
19:17:36              "serviceName": "bps-processor-service",
19:17:36              "serviceImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:36              "artifactImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:36              "status": "Deployed",
19:17:36              "rollbacklog": "",
19:17:36              "buildCommitId": "5fa96fa",
19:17:36              "buildId": 9999
19:17:36          }
19:17:36      ],
19:17:36      "deploymentTime": "2025-09-05T13:47:36Z",
19:17:36      "jobUrl": "https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/",
19:17:36      "deployedEnv": "PROD",
19:17:36      "deploymentLog": "https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/iipv_billing_profile_service/eks/PROD_313.json",
19:17:36      "vsad": "IIPV",
19:17:36      "gitGroupName": "iipv_billing_profile_service",
19:17:36      "passiveEnv": null,
19:17:36      "globalConfigDeployment": "false",
19:17:36      "globalSecretsDeployment": "true",
19:17:36      "releaseBranch": "25.89.100"
19:17:36  }
19:17:37  [Pipeline] sh
19:17:37  + curl -X POST --data '{
19:17:37      "serviceData": [
19:17:37          {
19:17:37              "serviceName": "bps-processor-service",
19:17:37              "serviceImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:37              "artifactImageTag": "25.89.1005fa96fa268756109052025124557",
19:17:37              "status": "Deployed",
19:17:37              "rollbacklog": "",
19:17:37              "buildCommitId": "5fa96fa",
19:17:37              "buildId": 9999
19:17:37          }
19:17:37      ],
19:17:37      "deploymentTime": "2025-09-05T13:47:36Z",
19:17:37      "jobUrl": "https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/",
19:17:37      "deployedEnv": "PROD",
19:17:37      "deploymentLog": "https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/iipv_billing_profile_service/eks/PROD_313.json",
19:17:37      "vsad": "IIPV",
19:17:37      "gitGroupName": "iipv_billing_profile_service",
19:17:37      "passiveEnv": null,
19:17:37      "globalConfigDeployment": "false",
19:17:37      "globalSecretsDeployment": "true",
19:17:37      "releaseBranch": "25.89.100"
19:17:37  }' -H 'Content-Type: application/json' https://sre-marvel-cicd.ebiz.verizon.com/unifiedapi/api/cd-email-notification
19:17:37    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
19:17:37                                   Dload  Upload   Total   Spent    Left  Speed
19:17:37  
19:17:37    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
19:17:40    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
19:17:40  100  1005    0    20  100   985      8    426  0:00:02  0:00:02 --:--:--   434
19:17:40  100  1005    0    20  100   985      8    426  0:00:02  0:00:02 --:--:--   434
19:17:40  [Pipeline] echo
19:17:40  mailResponse: {"status":"SUCCESS"}
19:17:40  [Pipeline] libraryResource
19:17:40  [Pipeline] writeFile
19:17:40  [Pipeline] readJSON
19:17:40  [Pipeline] sh
19:17:41  ++ date -u +%Y-%m-%dT%H:%M:%SZ
19:17:41  + echo 2025-09-05T13:47:40Z
19:17:41  [Pipeline] echo
19:17:41  [INFO] [2025-09-05T09:47:41.707726017] Service Status Object:[serviceData:[[serviceName:bps-processor-service, serviceImageTag:25.89.1005fa96fa268756109052025124557, artifactImageTag:25.89.1005fa96fa268756109052025124557, status:Deployed, rollbacklog:, buildCommitId:5fa96fa, buildId:9999]], deploymentTime:2025-09-05T13:47:36Z, jobUrl:https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/, deployedEnv:PROD, deploymentLog:https://oneartifactoryci.verizon.com/artifactory/I2IV_SRE/release/25.89.100/iipv_billing_profile_service/eks/PROD_313.json, vsad:IIPV, gitGroupName:iipv_billing_profile_service, passiveEnv:null, globalConfigDeployment:false, globalSecretsDeployment:true, releaseBranch:25.89.100]
19:17:41  [Pipeline] echo
19:17:41  [INFO] [2025-09-05T09:47:41.729971642] service => [serviceName:bps-processor-service, serviceImageTag:25.89.1005fa96fa268756109052025124557, artifactImageTag:25.89.1005fa96fa268756109052025124557, status:Deployed, rollbacklog:, buildCommitId:5fa96fa, buildId:9999]
19:17:41  [Pipeline] echo
19:17:41  [INFO] [2025-09-05T09:47:41.751869760] service Image tag: 25.89.1005fa96fa268756109052025124557
19:17:41  [Pipeline] retry
19:17:41  [Pipeline] {
19:17:41  [Pipeline] echo
19:17:41  jsonPayLoad => [vsad:IIPV, releaseBranch:25.89.100, deployType:EKS, deployEnviroment:PROD, bgFlag:NA, trafficFlag:null, isActiveOrPassive:false, deployedBy:Bhavana, Margam, workflowId:0, jiraId:NA, deploymentComments:NA, services:[[gitlabGroupName:iipv_billing_profile_service, serviceName:bps-processor-service, commitId:5fa96fa, serviceTag:25.89.1005fa96fa268756109052025124557, configTag:, dbChangesTag:NA, deploymentStatus:Success, jenkinsConsoleLogURL:https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/, deploymentTimeStamp:2025-09-05T13:47:40Z, pipelineBuildId:9999]]]
19:17:41  [Pipeline] sh
19:17:42  + curl -X POST --data '{"vsad":"IIPV","releaseBranch":"25.89.100","deployType":"EKS","deployEnviroment":"PROD","bgFlag":"NA","trafficFlag":"null","isActiveOrPassive":"false","deployedBy":"Bhavana, Margam","workflowId":0,"jiraId":"NA","deploymentComments":"NA","services":[{"gitlabGroupName":"iipv_billing_profile_service","serviceName":"bps-processor-service","commitId":"5fa96fa","serviceTag":"25.89.1005fa96fa268756109052025124557","configTag":"","dbChangesTag":"NA","deploymentStatus":"Success","jenkinsConsoleLogURL":"https://jenkins-vcg5.vpc.verizon.com/vcg5/job/VZW.UNIF.CICD.PIPELINES/job/VZW.UNIF.CICD.DEPLOYMENT.PIPELINES-PROD/job/VZW.UNIF.EKS_DEPLOYMENT.PIPELINE-OCP/313/","deploymentTimeStamp":"2025-09-05T13:47:40Z","pipelineBuildId":9999}]}' -H 'Content-Type: application/json' https://sre-marvel-cicd.ebiz.verizon.com/insightsapi/api/cd-report/deployment/log
19:17:42    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
19:17:42                                   Dload  Upload   Total   Spent    Left  Speed
19:17:42  
19:17:43    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
19:17:43  100   817    0    87  100   730     82    693  0:00:01  0:00:01 --:--:--   775
19:17:43  100   817    0    87  100   730     82    692  0:00:01  0:00:01 --:--:--   775
19:17:43  [Pipeline] echo
19:17:43  response => {"status":"SUCCESS","data":[{"serviceName":"bps-processor-service","cdLogId":4218675}]}
19:17:43  [Pipeline] readJSON
19:17:43  [Pipeline] echo
19:17:43  [status:SUCCESS, data:[[serviceName:bps-processor-service, cdLogId:4218675]]]
19:17:43  [Pipeline] }
19:17:43  [Pipeline] // retry
19:17:43  [Pipeline] echo
19:17:43  deployTime => 2025-09-05T13:47:36Z
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.221215553] Inside ARTasks
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.243565670] JFROG
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.303543287] inside post action
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.328004660] start of AR Upload
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.351333404] inside File upload method
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.371305319] Inside FILE type artifact
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.393646126] Upload initiate
19:17:44  [Pipeline] writeFile
19:17:44  [Pipeline] echo
19:17:44  [INFO] [2025-09-05T09:47:44.480327695] artifactCred => UP_NPARTIFACT_USER
19:17:44  [Pipeline] withCredentials
19:17:44  Masking supported pattern matches of $USERNAME or $PASSWORD
19:17:44  [Pipeline] {
19:17:44  [Pipeline] retry
19:17:44  [Pipeline] {
19:17:44  [Pipeline] sh
19:17:45  + curl -s -u ****:**** -T PROD_2025-09-05T13:47:36Z.json https://oneartifactoryci.verizon.com/artifactory/iipv-docker-prod/vzw/iipv/release/25.89.100/deploymentStatus/PROD_2025-09-05T13:47:36Z.json
19:17:45  {
19:17:45    "repo" : "iipv-docker-prod",
19:17:45    "path" : "/vzw/iipv/release/25.89.100/deploymentStatus/PROD_2025-09-05T13:47:36Z.json",
19:17:45    "created" : "2025-09-05T09:47:45.192-04:00",
19:17:45    "createdBy" : "svc-npartifact-up",
19:17:45    "downloadUri" : "https://oneartifactoryci.verizon.com/artifactory/iipv-docker-prod/vzw/iipv/release/25.89.100/deploymentStatus/PROD_2025-09-05T13:47:36Z.json",
19:17:45    "mimeType" : "application/json",
19:17:45    "size" : "985",
19:17:45    "checksums" : {
19:17:45      "sha1" : "001316c9191f170f4576bd3d7810f9d90a79a6e7",
19:17:45      "md5" : "5f4875757271328b9d8d5067164ad510",
19:17:45      "sha256" : "ec86eb3c96967869d150c1ba47d11ae90d19768743ba371da02c55d8150e9287"
19:17:45    },
19:17:45    "originalChecksums" : {
19:17:45      "sha256" : "ec86eb3c96967869d150c1ba47d11ae90d19768743ba371da02c55d8150e9287"
19:17:45    },
19:17:45    "uri" : "https://oneartifactoryci.verizon.com/artifactory/iipv-docker-prod/vzw/iipv/release/25.89.100/deploymentStatus/PROD_2025-09-05T13:47:36Z.json"
19:17:45  }
19:17:45  [Pipeline] }
19:17:45  [Pipeline] // retry
19:17:45  [Pipeline] echo
19:17:45  [INFO] [2025-09-05T09:47:45.704524030] uploaded to artifactory 
19:17:45  [Pipeline] }
19:17:45  [Pipeline] // withCredentials
19:17:45  [Pipeline] sh
19:17:46  + rm PROD_2025-09-05T13:47:36Z.json
19:17:46  [Pipeline] echo
19:17:46  [INFO] [2025-09-05T09:47:46.826838693] repo upload path -> iipv-docker-prod/vzw/iipv/release/25.89.100
19:17:46  [Pipeline] echo
19:17:46  [INFO] [2025-09-05T09:47:46.850768597] update tag is set to false
19:17:46  [Pipeline] echo
19:17:46  Update tag success
19:17:46  [Pipeline] echo
19:17:46  https://oneartifactoryci.verizon.com/artifactory/iipv-docker-prod/vzw/iipv/release/25.89.100/deploymentStatus/PROD_2025-09-05T13:47:36Z.json
19:17:46  [Pipeline] }
19:17:46  [Pipeline] // script
19:17:46  [Pipeline] }
19:17:47  [Pipeline] // stage
19:17:47  [Pipeline] stage
19:17:47  [Pipeline] { (Declarative: Post Actions)
19:17:47  [Pipeline] script
19:17:47  [Pipeline] {
19:17:47  [Pipeline] addBadge
19:17:47  [Pipeline] cleanWs
19:17:47  [WS-CLEANUP] Deleting project workspace...
19:17:47  [WS-CLEANUP] Deferred wipeout is used...
19:17:47  [WS-CLEANUP] done
19:17:47  [Pipeline] }
19:17:47  [Pipeline] // script
19:17:47  [Pipeline] }
19:17:47  [Pipeline] // stage
19:17:47  [Pipeline] }
19:17:47  [Pipeline] // node
19:17:47  [Pipeline] End of Pipeline
19:17:47  Finished: SUCCESS
