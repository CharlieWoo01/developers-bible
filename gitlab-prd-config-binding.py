import gitlab
import os
import yaml
import csv
from base64 import b64decode

# --- Load environment variables ---
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")  # Required GitLab personal access token
GITLAB_URL = os.environ.get("CI_API_V4_URL", "https://gitlab.com/api/v4").replace("/api/v4", "")  # GitLab base URL
GROUP_ID = os.environ.get("GROUP_ID")  # ID of the GitLab group containing microservices
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() != "false"  # Dry run enabled unless explicitly set to false

# --- Safety check ---
if not GITLAB_TOKEN or not GROUP_ID:
    raise Exception("Missing GITLAB_TOKEN or GROUP_ID")

# --- Connect to GitLab instance ---
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
group = gl.groups.get(GROUP_ID)

# --- Fetch all projects (including nested subgroups) ---
projects = group.projects.list(include_subgroups=True, all=True)

# --- This will store the CSV report data ---
report = []

# --- Loop over each project in the group ---
for project_info in projects:
    project = gl.projects.get(project_info.id)
    name = project.name

    lib_found = False  # Whether lib-ops-otel is found in pom.xml
    otel_binding_present = False  # Whether 'otel' is already in prd.yml bindings
    action = "skipped"  # What action was taken

    try:
        # --- Try to load and inspect the pom.xml for the OTEL library ---
        try:
            pom = project.files.get(file_path="pom.xml", ref="main")
            if "lib-ops-otel" in b64decode(pom.content).decode():
                lib_found = True
        except gitlab.exceptions.GitlabGetError:
            pass  # pom.xml not found — skip dependency check

        # --- If OTEL lib is used, check and modify the PCF config if needed ---
        if lib_found:
            path = "config/pcf/prd.yml"  # Assumed path to PCF production config
            try:
                file = project.files.get(file_path=path, ref="main")
                content = b64decode(file.content).decode()

                # Load YAML config
                config = yaml.safe_load(content) or {}
                bindings = config.get("bindings", [])

                # Check for 'otel' in bindings
                if "otel" in bindings:
                    otel_binding_present = True
                    action = "otel already present"
                else:
                    if DRY_RUN:
                        action = "would add otel"
                    else:
                        # Add otel to bindings and push update
                        bindings.append("otel")
                        config["bindings"] = bindings
                        new_content = yaml.dump(config, sort_keys=False)

                        # Commit updated config file back to the repo
                        project.files.update({
                            "file_path": path,
                            "branch": "main",
                            "content": new_content,
                            "commit_message": "Add OTEL binding to PCF config for prd"
                        })
                        action = "otel added"
            except gitlab.exceptions.GitlabGetError:
                action = "pcf config missing"  # Config file does not exist
    except Exception as e:
        action = f"error: {str(e)}"  # Catch-all in case anything breaks

    # --- Add row to the report ---
    report.append({
        "project_name": name,
        "lib_found": lib_found,
        "otel_binding_present": otel_binding_present,
        "action_taken": action
    })

# --- Write the report to a CSV file for visibility/debugging ---
with open("report.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["project_name", "lib_found", "otel_binding_present", "action_taken"])
    writer.writeheader()
    writer.writerows(report)

print("✅ Done — report.csv generated")
