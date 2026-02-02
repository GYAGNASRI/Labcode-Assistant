from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ---------- Simple mock "AI" logic for demo ----------

def mock_explain_code(code_text, language, concept, job_role):
    # Very simple heuristic explanation for MVP demo
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
    for c in main_concepts:
        practice_topics.append({
            "topic": c,
            "platform": "LeetCode / HackerRank",
            "sets": [
                f"{c.title()} basics (easy)",
                f"{c.title()} patterns (medium)",
                f"{c.title()} interview mix (medium/hard)"
            ]
        })

    if not practice_topics:
        practice_topics.append({
            "topic": "basics",
            "platform": "HackerRank",
            "sets": ["Intro problems (easy)"]
        })

    job_focus = ""
    if job_role == "SDE":
        job_focus = (
            "For SDE roles, focus on arrays, strings, recursion, "
            "and dynamic programming. "
            "This lab builds your problem‑solving foundation."
        )
    elif job_role == "Data Engineer":
        job_focus = (
            "For Data Engineer roles, focus on clean input/output handling, "
            "file processing, and basic algorithms that scale to large data."
        )
    elif job_role == "ML Engineer":
        job_focus = (
            "For ML Engineer roles, pay attention to how you structure data "
            "and write reusable functions. These habits carry into model code."
        )
    elif job_role == "Backend":
        job_focus = (
            "For Backend roles, focus on robustness, error handling, and "
            "modular code. These are the same skills used in APIs and services."
        )
    else:
        job_focus = (
            "Pick a role to see focused guidance on how this lab connects to careers."
        )

    explanation = {
        "summary": (
            f"This {language} program has about {num_lines} line(s) and "
            f"uses the core idea(s): {', '.join(main_concepts) or 'basic syntax'}."
        ),
        "flow": [
            "Take the required inputs from the user or predefined values.",
            "Perform the main computations step by step "
            "(loops, conditions, or function calls).",
            "Produce the final output that answers the lab question."
        ],
        "variables": [
            "Track how each variable changes inside loops and conditions.",
            "Note which variables are inputs, which are counters/indexes, "
            "and which store final results."
        ],
        "future_courses": future_courses,
        "practice_topics": practice_topics,
        "job_focus": job_focus,
    }
    return explanation


# ---------- Flask routes ----------

@app.route("/")
def home():
    # Single-file template for quick MVP demo
    page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Lab Code Assistant – MVP Preview</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <!-- Minimal CSS framework for quick, clean UI -->
        <link rel="stylesheet" href="https://unpkg.com/mvp.css" />
        <style>
            body {
                background: #050816;
                color: #e5e7eb;
            }
            header {
                background: radial-gradient(circle at top, #1d4ed8, #020617);
                color: #f9fafb;
                padding: 2.5rem 1.5rem;
                text-align: center;
            }
            header h1 {
                margin-bottom: 0.25rem;
            }
            .badge {
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.85);
                color: #a5b4fc;
                font-size: 0.75rem;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }
            main {
                max-width: 1080px;
                margin: -1.5rem auto 2rem;
                padding: 0 1rem 3rem;
            }
            .card {
                background: #020617;
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border: 1px solid rgba(148, 163, 184, 0.25);
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.7);
            }
            .grid {
                display: grid;
                grid-template-columns: 1.3fr 1fr;
                grid-gap: 1.5rem;
            }
            @media (max-width: 900px) {
                .grid {
                    grid-template-columns: 1fr;
                }
            }
            textarea {
                min-height: 200px;
                font-family: "JetBrains Mono", "Fira Code", monospace;
                font-size: 0.9rem;
                background: #020617;
                color: #e5e7eb;
                border-radius: 0.75rem;
            }
            select, input[type="text"] {
                background: #020617;
                color: #e5e7eb;
                border-radius: 0.75rem;
            }
            button, .primary-btn {
                background: linear-gradient(135deg, #6366f1, #22c55e);
                border: none;
                color: #f9fafb;
                border-radius: 999px;
                padding: 0.7rem 1.4rem;
                font-weight: 600;
                cursor: pointer;
            }
            button:hover, .primary-btn:hover {
                filter: brightness(1.08);
            }
            .pill {
                display: inline-flex;
                align-items: center;
                padding: 0.35rem 0.75rem;
                border-radius: 999px;
                font-size: 0.75rem;
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.5);
                margin: 0.15rem;
            }
            .pill span {
                margin-left: 0.4rem;
                color: #a5b4fc;
            }
            .stat-row {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                margin-top: 1rem;
            }
            .stat {
                flex: 1;
                min-width: 140px;
                padding: 0.8rem 1rem;
                border-radius: 0.75rem;
                background: radial-gradient(circle at top left, #1d4ed8, #020617);
                border: 1px solid rgba(148, 163, 184, 0.35);
            }
            .stat strong {
                display: block;
                font-size: 1.2rem;
                color: #e5e7eb;
            }
            .stat small {
                font-size: 0.8rem;
                color: #9ca3af;
            }
            .output-card {
                background: radial-gradient(circle at top, #0f172a, #020617);
                border-radius: 1rem;
                padding: 1rem;
                border: 1px solid rgba(148, 163, 184, 0.45);
                max-height: 480px;
                overflow-y: auto;
            }
            h2, h3, h4 {
                color: #e5e7eb;
            }
            .tag {
                display: inline-block;
                padding: 0.25rem 0.65rem;
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.85);
                font-size: 0.75rem;
                color: #a5b4fc;
                margin-right: 0.35rem;
                margin-top: 0.25rem;
            }
            footer {
                text-align: center;
                font-size: 0.8rem;
                color: #6b7280;
                margin-top: 2rem;
            }
        </style>
    </head>
    <body>
        <header>
            <p class="badge">MVP PREVIEW · STUDENT PROJECT</p>
            <h1>Lab Code Assistant</h1>
            <p>
                Turn your college programming labs from <strong>copy‑paste</strong> to
                concept‑driven, career‑ready practice.
            </p>
        </header>

        <main>
            <!-- Product value snapshot -->
            <section class="card">
                <h2>Why this exists</h2>
                <p>
                    Most students copy code from seniors or the internet, run it once,
                    write the output in the record, and forget the concept.
                    Lab Code Assistant converts each lab program into a clear explanation,
                    connects it to future subjects, and immediately suggests practice
                    problems that match interview patterns.
                </p>
                <div class="stat-row">
                    <div class="stat">
                        <strong>1 lab → roadmap</strong>
                        <small>From loops today to DSA, OS, DBMS tomorrow.</small>
                    </div>
                    <div class="stat">
                        <strong>Concept‑first</strong>
                        <small>Every program tagged to its core ideas and future use.</small>
                    </div>
                    <div class="stat">
                        <strong>Placement‑aware</strong>
                        <small>Highlights topics that repeat in SDE & data rounds.</small>
                    </div>
                </div>
            </section>

            <!-- Interactive MVP area -->
            <section class="card">
                <div class="grid">
                    <!-- Left: input -->
                    <div>
                        <h2>Try the Lab Assistant</h2>
                        <p>
                            Paste any simple C / C++ / Java / Python lab program.
                            Pick your lab concept and target job role, then generate
                            an explanation you can show in your MVP demo.
                        </p>

                        <form id="labForm" onsubmit="return false;">
                            <label for="language">Language</label>
                            <select id="language" name="language">
                                <option value="C">C</option>
                                <option value="C++">C++</option>
                                <option value="Java">Java</option>
                                <option value="Python" selected>Python</option>
                            </select>

                            <label for="concept">Lab concept (optional)</label>
                            <input
                                type="text"
                                id="concept"
                                name="concept"
                                placeholder="loops, arrays, functions, recursion..."
                            />

                            <label for="jobRole">Target job role</label>
                            <select id="jobRole" name="jobRole">
                                <option value="">Just pass the lab 😅</option>
                                <option value="SDE">SDE</option>
                                <option value="Data Engineer">Data Engineer</option>
                                <option value="ML Engineer">ML Engineer</option>
                                <option value="Backend">Backend Developer</option>
                            </select>

                            <label for="code">Paste your lab code</label>
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

                            <br />
                            <button onclick="generateExplanation()">
                                Generate explanation
                            </button>
                        </form>

                        <p style="margin-top:0.75rem; font-size:0.8rem; color:#9ca3af;">
                            Tip for your recording: show how the same code can be
                            viewed differently for an SDE vs ML Engineer role just by
                            changing the dropdown.
                        </p>
                    </div>

                    <!-- Right: output -->
                    <div>
                        <h3>Explanation output</h3>
                        <div id="outputCard" class="output-card">
                            <p style="color:#9ca3af;">
                                Run once to see the full structured breakdown
                                of your lab program here.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- How it fits the bigger product -->
            <section class="card">
                <h2>What a full product version includes</h2>
                <div>
                    <span class="tag">Digitized lab manuals</span>
                    <span class="tag">Topic‑wise semester map</span>
                    <span class="tag">AI code explanations</span>
                    <span class="tag">Future course linkage</span>
                    <span class="tag">Role‑based interview prep</span>
                    <span class="tag">Mastery dashboard</span>
                </div>
                <p style="margin-top:0.75rem;">
                    This MVP only demonstrates the core interaction:
                    “Paste lab code → get structured explanation +
                    practice guidance”. In a full build, the same engine
                    powers a dashboard that tracks which experiments you
                    understood, practiced online, and connected to future topics.
                </p>
            </section>

            <footer>
                Built as a student MVP for an AI‑powered lab learning platform.
            </footer>
        </main>

        <script>
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

                outputCard.innerHTML = "<p>Thinking like a lab TA... ⏳</p>";

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
                } catch (err) {
                    console.error(err);
                    outputCard.innerHTML =
                        "<p>Something went wrong. Please try again.</p>";
                }
            }

            function renderExplanation(data) {
                const outputCard = document.getElementById("outputCard");

                let html = "";
                html += `<h4>Plain‑language summary</h4>`;
                html += `<p>${data.summary}</p>`;

                html += `<h4>Step‑by‑step flow</h4><ol>`;
                (data.flow || []).forEach(step => {
                    html += `<li>${step}</li>`;
                });
                html += `</ol>`;

                html += `<h4>Variable‑by‑variable view</h4><ul>`;
                (data.variables || []).forEach(v => {
                    html += `<li>${v}</li>`;
                });
                html += `</ul>`;

                if (data.future_courses && data.future_courses.length) {
                    html += `<h4>Where this appears again in your degree</h4><ul>`;
                    data.future_courses.forEach(c => {
                        html += `<li>${c}</li>`;
                    });
                    html += `</ul>`;
                }

                if (data.practice_topics && data.practice_topics.length) {
                    html += `<h4>Practice problems (after lab)</h4>`;
                    data.practice_topics.forEach(block => {
                        html += `<p><strong>${block.topic}</strong> · ${block.platform}</p><ul>`;
                        block.sets.forEach(s => {
                            html += `<li>${s}</li>`;
                        });
                        html += `</ul>`;
                    });
                }

                html += `<h4>Career alignment</h4>`;
                html += `<p>${data.job_focus}</p>`;

                outputCard.innerHTML = html;
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
    # For Replit / local preview
    app.run(host="0.0.0.0", port=5000, debug=True)
