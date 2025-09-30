// META-INF/archetype-post-generate.groovy

// Root of the generated project
def projectDir = new File(request.outputDirectory, request.artifactId)

// Run git commands in the project dir
def run(List<String> args) {
    println ">> " + args.join(' ')
    def p = new ProcessBuilder(args as String[])
            .directory(projectDir)
            .redirectErrorStream(true)
            .start()
    p.inputStream.withReader { it.eachLine { println it } }
    if (p.waitFor() != 0) throw new RuntimeException("Command failed: " + args.join(' '))
}

// Make sure git is available
try {
    run(["git", "--version"])
} catch (e) {
    println "WARN: git is not available, skipping submodule setup."
    return
}

// Init repo if needed
if (!new File(projectDir, ".git").exists()) {
    run(["git", "init"])
}

// --- Hard-coded submodules ---
def submodules = [
    // [url, branch, path]
    ["git@github.com:your-org/ci-scripts.git", "main", "ci-scripts"],
    ["git@github.com:your-org/pcf-scripts.git", "main", "pcf-config/scripts"]
]

// Add each submodule
submodules.each { url, branch, path ->
    new File(projectDir, path).parentFile?.mkdirs()
    try {
        run(["git", "submodule", "add", "--branch", branch, url, path])
        run(["git", "submodule", "update", "--init", "--recursive"])
        println "✔ Added submodule ${url} -> ${path}"
    } catch (e) {
        println "WARN: Failed to add submodule '${path}': ${e.message}"
        println "Manual fix:"
        println "  cd \"${projectDir.absolutePath}\""
        println "  git submodule add --branch ${branch} ${url} ${path}"
    }
}

println "Submodules setup completed."
