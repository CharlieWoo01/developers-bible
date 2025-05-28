import sys
import xml.etree.ElementTree as ET

def check_dependency_versions(pom_path, expected_deps):
    """
    Args:
        pom_path (str): Path to pom.xml
        expected_deps (dict): Mapping of (groupId, artifactId) -> expected_version
    """
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # Handle namespaces
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
            if actual_version != expected_version:
                mismatches.append((key, expected_version, actual_version))

        if mismatches:
            for (group_id, artifact_id), expected, actual in mismatches:
                print(f"❌ Mismatch for {group_id}:{artifact_id} - Expected: {expected}, Found: {actual}")
            sys.exit(1)

        print("✅ All dependency versions match.")
        sys.exit(0)

    except Exception as e:
        print(f"Error parsing pom.xml: {e}")
        sys.exit(2)

# === Example Usage ===
if __name__ == "__main__":
    expected_dependencies = {
        ("org.springframework.boot", "spring-boot-starter-web"): "3.2.1",
        ("com.example", "my-library"): "1.0.0"
    }
    check_dependency_versions("pom.xml", expected_dependencies)
