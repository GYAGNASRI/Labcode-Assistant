from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ---------- Simple mock "AI" logic for demo ----------

def mock_explain_code(code_text, language, concept, job_role):
    lines = code_text.strip().split("\n")
    num_lines = len(lines)
    has_loop = any(
        kw in code_text
        for kw in ["for ", "while ", "for(", "while("]
    )
    has_if = any(
        kw in code_text
        for kw in ["if ", "if("]
    )

    main_concepts = []
    if has_loop:
        main_concepts.append("loops")
    if "[" in code_text or "Array" in code_text or "array" in code_text:
        main_concepts.append("arrays")
    if "func" in code_text or "def " in code_text or "void " in code_text:
        main_concepts.append("functions")
    if has_if:
        main_concepts.append("conditions")

    if not main_concepts and concept:
        main_concepts.append(concept)

    future_courses = []
    if "arrays" in main_concepts or "loops" in main_concepts:
        future_courses.extend(["Data Structures", "Algorithms"])
    if "functions" in main_concepts:
        future_courses.append("Operating Systems")
    if "conditions" in main_concepts:
        future_courses.append("DBMS (query conditions)")

    practice_topics = []
    for c in main_concepts or ["basics"]:
        practice_topics.append({
            "topic": c,
            "platform": "LeetCode / HackerRank",
            "sets": [
                f"{c.title()} basics (easy)",
                f"{c.title()} patterns (medium)",
                f"{c.title()} interview mix (medium/hard)"
            ]
        })

    job_focus = ""
    if job_role == "SDE":
        job_focus = (
            "For SDE roles, focus on arrays, strings, recursion, "
            "and dynamic programming. This lab builds your "
            "problem‑solving foundation."
        )
    elif job_role == "Data Engineer":
        job_focus = (
            "For Data Engineer roles, pay attention to clean input/output, "
            "loops over large data, and how you structure records."
        )
    elif job_role == "ML Engineer":
        job_focus = (
            "For ML Engineer roles, practice turning raw input into "
            "clean numeric features, and write reusable helper functions."
        )
    elif job_role == "Backend":
        job_focus = (
            "For Backend roles, think about edge cases, robustness, and "
            "how this logic would sit behind an API endpoint."
        )
    else:
        job_focus = (
            "Pick a role to see focused guidance on how this lab connects "
            "to careers and interview patterns."
        )

    explanation = {
        "summary": (
            f"This {language} program has about {num_lines} line(s) and uses "
            f"the core idea(s): {', '.join(main_concepts) or 'basic syntax'}."
        ),
        "flow": [
            "Read inputs or initial values that define the problem.",
            "Use loops, conditions, and function calls to transform the data.",
            "Produce the final result and display it to the user.",
        ],
        "variables": [
            "Track counters and indexes inside loops carefully.",
            "Separate input variables, working variables, and result variables.",
        ],
        "future_courses": future_courses or [
            "You will revisit these basics in later subjects like DSA and OS."
        ],
        "practice_topics": practice_topics,
        "job_focus": job_focus,
    }
    return explanation


# ---------- Flask routes ----------

@app.route("/")
def home():
    page = """
    <!DOCTYPE html>
    <html lang="en" data-theme="dark">
    <head>
        <meta charset="UTF-8" />
        <title>Lab Code Assistant – Student Lab Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="https://unpkg.com/mvp.css" />
        <style>
            :root {
                --bg: #020617;
                --bg-elevated: #020617;
                --bg-panel: #020617;
                --border-subtle: rgba(148, 163, 184, 0.4);
                --accent-1: #6366f1;
                --accent-2: #22c55e;
                --accent-soft: rgba(79, 70, 229, 0.2);
            }
            body {
                background: radial-gradient(circle at top, #0f172a, #020617);
                color: #e5e7eb;
                padding: 0;
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont,
                             "Segoe UI", sans-serif;
            }
            .shell {
                display: grid;
                grid-template-columns: 240px 1fr;
                min-height: 100vh;
            }
            @media (max-width: 900px) {
                .shell {
                    grid-template-columns: 1fr;
                }
            }
            /* Sidebar */
            .sidebar {
                border-right: 1px solid var(--border-subtle);
                background: linear-gradient(180deg, #020617, #020617);
                padding: 1rem 1.25rem;
            }
            .logo {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
            }
            .logo-badge {
                width: 32px;
                height: 32px;
                border-radius: 12px;
                background: radial-gradient(circle at 10% 0%, #22c55e, #1d4ed8);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 1.1rem;
                color: #f9fafb;
            }
            .sidebar nav {
                margin-top: 1rem;
            }
            .nav-section-title {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #64748b;
                margin: 0.75rem 0 0.35rem;
            }
            .nav-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0.5rem 0.65rem;
                border-radius: 0.75rem;
                cursor: pointer;
                font-size: 0.9rem;
                color: #e5e7eb;
            }
            .nav-item:hover {
                background: rgba(15, 23, 42, 0.8);
            }
            .nav-item.active {
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid var(--accent-soft);
                box-shadow: 0 10px 25px rgba(15, 23, 42, 1);
            }
            .nav-chip {
                font-size: 0.7rem;
                padding: 0.12rem 0.55rem;
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.6);
                color: #a5b4fc;
            }
            .sidebar-footer {
                margin-top: 2rem;
                font-size: 0.75rem;
                color: #64748b;
            }
            .sidebar-footer span {
                display: block;
            }

            /* Main area */
            .main {
                padding: 1.25rem 1.5rem 2rem;
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            .topbar {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 0.5rem;
            }
            .topbar-left h1 {
                font-size: 1.25rem;
                margin-bottom: 0.1rem;
            }
            .tagline {
                font-size: 0.8rem;
                color: #9ca3af;
            }
            .topbar-right {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .pill-btn {
                border-radius: 999px;
                border: 1px solid var(--border-subtle);
                padding: 0.4rem 0.8rem;
                background: rgba(15, 23, 42, 0.9);
                font-size: 0.8rem;
                cursor: pointer;
                color: #e5e7eb;
            }
            .pill-btn-primary {
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                border: none;
            }

            /* Tabs / content */
            .tabs {
                display: flex;
                gap: 0.4rem;
                border-bottom: 1px solid rgba(51, 65, 85, 0.8);
                margin-top: 0.5rem;
            }
            .tab {
                padding: 0.45rem 0.85rem;
                border-radius: 999px 999px 0 0;
                font-size: 0.8rem;
                cursor: pointer;
                color: #9ca3af;
            }
            .tab.active {
                color: #e5e7eb;
                background: radial-gradient(circle at top, #1d4ed8, #020617);
                border: 1px solid rgba(148, 163, 184, 0.8);
                border-bottom: none;
            }

            .layout {
                display: grid;
                grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
                gap: 1rem;
                align-items: stretch;
            }
            @media (max-width: 900px) {
                .layout {
                    grid-template-columns: 1fr;
                }
            }
            .panel {
                background: rgba(2, 6, 23, 0.9);
                border-radius: 1rem;
                padding: 1rem;
                border: 1px solid rgba(148, 163, 184, 0.4);
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.9);
            }
            .panel-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.5rem;
            }
            .panel-header h2 {
                font-size: 1rem;
            }
            .panel-tag {
                font-size: 0.7rem;
                border-radius: 999px;
                border: 1px solid rgba(148, 163, 184, 0.5);
                padding: 0.15rem 0.55rem;
                color: #a5b4fc;
            }

            label {
                font-size: 0.8rem;
                color: #9ca3af;
            }
            select, input[type="text"] {
                background: #020617;
                color: #e5e7eb;
                border-radius: 0.6rem;
                border: 1px solid rgba(148, 163, 184, 0.7);
                padding: 0.4rem 0.6rem;
                font-size: 0.85rem;
            }
            textarea {
                background: #020617;
                color: #e5e7eb;
                border-radius: 0.75rem;
                border: 1px solid rgba(148, 163, 184, 0.7);
                font-family: "JetBrains Mono", "Fira Code", monospace;
                font-size: 0.85rem;
                min-height: 230px;
            }
            .small-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.5rem;
            }
            @media (max-width: 600px) {
                .small-grid {
                    grid-template-columns: 1fr;
                }
            }

            .primary-btn {
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                border: none;
                color: #f9fafb;
                border-radius: 999px;
                padding: 0.55rem 1.2rem;
                font-size: 0.85rem;
                font-weight: 600;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
            }
            .primary-btn span {
                font-size: 1rem;
            }
            .subtext {
                font-size: 0.75rem;
                color: #9ca3af;
                margin-top: 0.25rem;
            }

            .output-scroll {
                max-height: 450px;
                overflow-y: auto;
                padding-right: 0.25rem;
            }
            .pill {
                display: inline-flex;
                align-items: center;
                padding: 0.3rem 0.65rem;
                border-radius: 999px;
                font-size: 0.75rem;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.6);
                margin: 0.15rem;
            }
            .pill-dot {
                width: 7px;
                height: 7px;
                border-radius: 999px;
                background: #22c55e;
                margin-right: 0.35rem;
            }
            .topic-chip {
                font-size: 0.75rem;
                background: rgba(37, 99, 235, 0.12);
                border-radius: 999px;
                padding: 0.18rem 0.55rem;
                margin: 0.15rem;
                border: 1px solid rgba(59, 130, 246, 0.4);
                color: #bfdbfe;
            }

            .progress-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 0.5rem;
            }
            .progress-card {
                flex: 1;
                min-width: 160px;
                border-radius: 0.75rem;
                background: radial-gradient(circle at top left, #1d4ed8, #020617);
                border: 1px solid rgba(148, 163, 184, 0.5);
                padding: 0.6rem 0.75rem;
            }
            .progress-card strong {
                font-size: 0.95rem;
                display: block;
            }
            .progress-card small {
                font-size: 0.75rem;
                color: #9ca3af;
            }

            footer {
                font-size: 0.75rem;
                color: #6b7280;
                margin-top: auto;
                text-align: right;
                padding-top: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="shell">
            <!-- Sidebar navigation -->
            <aside class="sidebar">
                <div class="logo">
                    <div class="logo-badge">L</div>
                    <div>
                        <strong>Lab Code Assistant</strong>
                        <div style="font-size:0.75rem; color:#9ca3af;">
                            AI‑powered lab learning
                        </div>
                    </div>
                </div>

                <nav>
                    <div class="nav-section-title">Workspace</div>
                    <div class="nav-item active">
                        <span>Today&apos;s Lab</span>
                        <span class="nav-chip">Live</span>
                    </div>
                    <div class="nav-item">
                        <span>Practice Roadmap</span>
                        <span style="font-size:0.7rem; color:#64748b;">Coming soon</span>
                    </div>
                    <div class="nav-item">
                        <span>Interview Prep</span>
                        <span style="font-size:0.7rem; color:#64748b;">Coming soon</span>
                    </div>

                    <div class="nav-section-title">Shortcuts</div>
                    <div class="nav-item">
                        <span>Upload lab manual</span>
                        <span style="font-size:0.7rem; color:#64748b;">Beta</span>
                    </div>
                    <div class="nav-item">
                        <span>Faculty view</span>
                        <span style="font-size:0.7rem; color:#64748b;">Beta</span>
                    </div>
                </nav>

                <div class="sidebar-footer">
                    <span>Tip: Use this page in your MVP demo.</span>
                    <span>Show code → explanation → roadmap in one screen.</span>
                </div>
            </aside>

            <!-- Main content -->
            <main class="main">
                <div class="topbar">
                    <div class="topbar-left">
                        <h1>Today&apos;s Lab Session</h1>
                        <div class="tagline">
                            Paste your program, pick a concept and job role, and
                            watch the assistant turn it into a story you can remember.
                        </div>
                    </div>
                    <div class="topbar-right">
                        <button class="pill-btn">
                            🎯 Focus mode
                        </button>
                        <button class="pill-btn pill-btn-primary" onclick="demoFill()">
                            ⚡ Quick demo code
                        </button>
                    </div>
                </div>

                <div class="tabs">
                    <div class="tab active">Explain my lab</div>
                    <div class="tab">Connect to future subjects</div>
                    <div class="tab">Interview view</div>
                </div>

                <section class="layout">
                    <!-- Left panel: input -->
                    <section class="panel">
                        <div class="panel-header">
                            <h2>Lab input</h2>
                            <span class="panel-tag">Student view</span>
                        </div>
                        <p style="font-size:0.85rem; color:#9ca3af;">
                            Imagine you are in your college lab right now. Fill this
                            exactly like you would describe today&apos;s program to a friend.
                        </p>

                        <div class="small-grid">
                            <div>
                                <label for="language">Language</label><br />
                                <select id="language" name="language">
                                    <option value="C">C</option>
                                    <option value="C++">C++</option>
                                    <option value="Java">Java</option>
                                    <option value="Python" selected>Python</option>
                                </select>
                            </div>
                            <div>
                                <label for="concept">Main concept</label><br />
                                <input
                                    type="text"
                                    id="concept"
                                    name="concept"
                                    placeholder="loops, arrays, functions, recursion..."
                                />
                            </div>
                        </div>

                        <div class="small-grid" style="margin-top:0.5rem;">
                            <div>
                                <label for="labTitle">Lab exercise title</label><br />
                                <input
                                    type="text"
                                    id="labTitle"
                                    name="labTitle"
                                    placeholder="e.g., Sum of N integers using loop"
                                />
                            </div>
                            <div>
                                <label for="jobRole">Target job role</label><br />
                                <select id="jobRole" name="jobRole">
                                    <option value="">Just pass the lab 😅</option>
                                    <option value="SDE">SDE</option>
                                    <option value="Data Engineer">Data Engineer</option>
                                    <option value="ML Engineer">ML Engineer</option>
                                    <option value="Backend">Backend Developer</option>
                                </select>
                            </div>
                        </div>

                        <div style="margin-top:0.75rem;">
                            <label for="code">Paste your lab code</label><br />
                            <textarea
                                id="code"
                                name="code"
                                placeholder="Paste your lab program here..."
                            ># Example: sum of n numbers
n = int(input("Enter n: "))
s = 0
for i in range(n):
    s += i
print("Sum:", s)</textarea>
                            <div class="subtext">
                                Hint: Use small, clean examples in your MVP demo so
                                the explanation fits on one screen.
                            </div>
                        </div>

                        <div style="margin-top:0.85rem; display:flex; align-items:center; justify-content:space-between;">
                            <button class="primary-btn" onclick="generateExplanation()">
                                <span>✨</span>
                                <span>Explain this lab</span>
                            </button>
                            <div style="font-size:0.75rem; color:#9ca3af;">
                                1 click → explanation + roadmap + interview view
                            </div>
                        </div>
                    </section>

                    <!-- Right panel: output -->
                    <section class="panel">
                        <div class="panel-header">
                            <h2>Assistant output</h2>
                            <span class="panel-tag">What you can record</span>
                        </div>
                        <div id="outputCard" class="output-scroll">
                            <p style="font-size:0.85rem; color:#9ca3af;">
                                After you click <strong>Explain this lab</strong>,
                                the assistant will fill this space with:
                            </p>
                            <ul style="font-size:0.85rem; color:#9ca3af;">
                                <li>A plain‑language explanation of your program</li>
                                <li>Step‑by‑step flow for your record notebook</li>
                                <li>Concept tags and future course links</li>
                                <li>Practice topics and interview hints</li>
                            </ul>
                            <p style="font-size:0.8rem; color:#64748b;">
                                This scrolling panel is perfect to show in your
                                hackathon or project MVP video.
                            </p>
                        </div>
                    </section>
                </section>

                <!-- Progress / concept chips -->
                <section class="panel">
                    <div class="panel-header">
                        <h2>Concept snapshot for this program</h2>
                        <span class="panel-tag">Mini dashboard</span>
                    </div>
                    <p style="font-size:0.8rem; color:#9ca3af;">
                        These pills simulate how, in a full product, the system
                        would track your concept mastery and practice status for
                        each lab exercise.
                    </p>
                    <div id="conceptChips">
                        <span class="pill">
                            <span class="pill-dot"></span>
                            Concept: not detected yet
                        </span>
                    </div>
                    <div class="progress-row">
                        <div class="progress-card">
                            <strong>Lab understanding</strong>
                            <small>We&apos;ll mark this green once you run an explanation.</small>
                        </div>
                        <div class="progress-card">
                            <strong>Practice linked</strong>
                            <small>Practice topics update based on your lab code.</small>
                        </div>
                        <div class="progress-card">
                            <strong>Interview relevance</strong>
                            <small>Role‑aware hints change with your job choice.</small>
                        </div>
                    </div>
                </section>

                <footer>
                    Built as an interactive MVP for an AI‑powered Lab Code Assistant.
                </footer>
            </main>
        </div>

        <script>
            function demoFill() {
                document.getElementById("language").value = "Python";
                document.getElementById("concept").value = "loops";
                document.getElementById("labTitle").value = "Sum of N numbers using loop";
                document.getElementById("jobRole").value = "SDE";
                document.getElementById("code").value =
`# Program: sum of first n natural numbers
n = int(input("Enter n: "))
s = 0
for i in range(1, n + 1):
    s += i
print("Sum:", s)`;
            }

            async function generateExplanation() {
                const code = document.getElementById("code").value;
                const language = document.getElementById("language").value;
                const concept = document.getElementById("concept").value;
                const jobRole = document.getElementById("jobRole").value;
                const outputCard = document.getElementById("outputCard");

                if (!code.trim()) {
                    outputCard.innerHTML = "<p>Please paste some code first.</p>";
                    return;
                }

                outputCard.innerHTML = "<p>Thinking like your favourite lab senior... ⏳</p>";

                try {
                    const res = await fetch("/api/explain", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            code: code,
                            language: language,
                            concept: concept,
                            job_role: jobRole,
                        }),
                    });

                    if (!res.ok) {
                        throw new Error("Server error");
                    }

                    const data = await res.json();
                    renderExplanation(data);
                    updateConceptChips(data);
                } catch (err) {
                    console.error(err);
                    outputCard.innerHTML =
                        "<p>Something went wrong. Please try again.</p>";
                }
            }

            function renderExplanation(data) {
                const outputCard = document.getElementById("outputCard");

                let html = "";
                html += `<h3>Plain‑language summary</h3>`;
                html += `<p>${data.summary}</p>`;

                html += `<h3>Step‑by‑step flow (record‑friendly)</h3><ol>`;
                (data.flow || []).forEach(step => {
                    html += `<li>${step}</li>`;
                });
                html += `</ol>`;

                html += `<h3>Variable‑by‑variable thinking</h3><ul>`;
                (data.variables || []).forEach(v => {
                    html += `<li>${v}</li>`;
                });
                html += `</ul>`;

                if (data.future_courses && data.future_courses.length) {
                    html += `<h3>Where you see this again</h3>`;
                    html += `<p style="font-size:0.85rem;">These are future subjects where the same idea will appear in a heavier form.</p><ul>`;
                    data.future_courses.forEach(c => {
                        html += `<li>${c}</li>`;
                    });
                    html += `</ul>`;
                }

                if (data.practice_topics && data.practice_topics.length) {
                    html += `<h3>Practice after today&apos;s lab</h3>`;
                    data.practice_topics.forEach(block => {
                        html += `<p><strong>${block.topic}</strong> · ${block.platform}</p><ul>`;
                        block.sets.forEach(s => {
                            html += `<li>${s}</li>`;
                        });
                        html += `</ul>`;
                    });
                }

                html += `<h3>Career alignment</h3>`;
                html += `<p>${data.job_focus}</p>`;

                outputCard.innerHTML = html;
            }

            function updateConceptChips(data) {
                const chips = document.getElementById("conceptChips");
                const topics = (data.practice_topics || []).map(p => p.topic);
                const uniqueTopics = Array.from(new Set(topics));

                if (!uniqueTopics.length) {
                    chips.innerHTML =
                        '<span class="pill"><span class="pill-dot"></span>No concept detected</span>';
                    return;
                }

                let html = "";
                uniqueTopics.forEach(topic => {
                    html += `<span class="topic-chip">${topic}</span>`;
                });
                chips.innerHTML = html;
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(page)


@app.route("/api/explain", methods=["POST"])
def api_explain():
    payload = request.get_json(force=True)
    code_text = payload.get("code", "")
    language = payload.get("language", "C")
    concept = payload.get("concept", "")
    job_role = payload.get("job_role", "")

    explanation = mock_explain_code(code_text, language, concept, job_role)
    return jsonify(explanation)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
