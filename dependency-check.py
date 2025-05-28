import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Set enforcement date
ENFORCEMENT_DATE = datetime(2025, 6, 6)

def check_dependency_versions(pom_path, expected_deps):
    """
    Parses pom.xml and checks dependency versions with:
    - Exact match (if version is specified)
    - Presence check (if version is None)
    Includes date-based enforcement for mismatches.
    """
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}

        found_versions = {}

        for dependency in root.findall(".//mvn:dependency", ns):
            group_id = dependency.find("mvn:groupId", ns)
            artifact_id = dependency.find("mvn:artifactId", ns)
            version = dependency.find("mvn:version", ns)

            if group_id is not None and artifact_id is not None:
                key = (group_id.text, artifact_id.text)
                if key in expected_deps:
                    found_versions[key] = version.text if version is not None else None

        mismatches = []

        for key, expected_version in expected_deps.items():
            actual_version = found_versions.get(key)

            # Case 1: Expected exact version
            if expected_version is not None:
                if actual_version != expected_version:
                    mismatches.append((key, expected_version, actual_version))

            # Case 2: Expected to exist but version doesn't matter
            else:
                if actual_version is None:
                    mismatches.append((key, "any", "missing"))

        if mismatches:
            today = datetime.today()
            if today >= ENFORCEMENT_DATE:
                for (group_id, artifact_id), expected, actual in mismatches:
                    print(f"❌ Mismatch for {group_id}:{artifact_id} - Expected: {expected}, Found: {actual}")
                sys.exit(1)
            else:
                for (group_id, artifact_id), expected, actual in mismatches:
                    print(f"⚠️  Warning: {group_id}:{artifact_id} - Expected: {expected}, Found: {actual}")
                print(f"⚠️  These mismatches will cause failure after {ENFORCEMENT_DATE.date()}")
                sys.exit(0)

        print("✅ All dependency versions match or are present.")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error parsing pom.xml: {e}")
        sys.exit(2)


# === Define expected dependencies ===
# - Specify version string for exact match
# - Use None if version does not matter (presence only)
expected_dependencies = {
    ("org.springframework.boot", "spring-boot-starter-web"): "3.2.1",
    ("com.example", "optional-lib"): None
}

# Run the check
check_dependency_versions("pom.xml", expected_dependencies)
