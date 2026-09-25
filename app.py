import streamlit as st
import os

from recovery.file_integrity import check_file_integrity
from recovery.scanner import scan_directory
from recovery.candidate_recovery import test_fragment_orders
from recovery.prioritizer import prioritize_recovery
from recovery.relationship import analyze_relationships, suggest_order
from recovery.visual_similarity import compare_images
from recovery_report import generate_recovery_report


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Data Recovery",
    page_icon="🔎",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🔎 AI-Assisted Data Recovery")

st.write(
    "Analyze damaged storage fragments, reconstruct possible files, "
    "evaluate recovery integrity, and prioritize the strongest candidates."
)
# ==================================================
# RECOVERY PIPELINE
# ==================================================

st.subheader(
    "🔄 Recovery Intelligence Pipeline"
)

pipeline = [
    "📂 Scan",
    "🔎 Classify",
    "🧩 Reconstruct",
    "🔗 Analyze Relationships",
    "🛡️ Verify Integrity",
    "🧠 Prioritize",
    "✅ Recover"
]

st.write(
    "  →  ".join(pipeline)
)


# ==================================================
# PATHS
# ==================================================

damaged_directory = "data/damaged"
fragment_directory = "data/damaged/fragments"
candidate_directory = "data/recovered/candidates"
test_directory = "data/damaged/test_files"


# ==================================================
# SCAN BUTTON
# ==================================================

if st.button("🔍 Scan Storage"):

    if not os.path.exists(damaged_directory):

        st.error("Damaged data folder not found.")

    else:

        # ==================================================
        # SCAN MAIN DAMAGED DIRECTORY
        # ==================================================

        results = scan_directory(
            damaged_directory
        )

        # ==================================================
        # SCAN TEST FILE DIRECTORY
        # ==================================================

        if os.path.exists(test_directory):

            test_results = scan_directory(
                test_directory
            )

            results.extend(
                test_results
            )

        # ==================================================
        # RECOVERY OVERVIEW
        # ==================================================

        total = len(results)

        recognized = sum(
            1
            for item in results
            if item["type"] != "UNKNOWN"
        )

        unknown = total - recognized

        st.subheader(
            "📊 Recovery Overview"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Files Found",
            total
        )

        col2.metric(
            "Recognized",
            recognized
        )

        col3.metric(
            "Unknown",
            unknown
        )

        # ==================================================
        # DETECTED DATA
        # ==================================================

        st.subheader(
            "📁 Detected Data"
        )

        st.dataframe(
            results,
            width="stretch"
        )

        # ==================================================
        # FILE INTEGRITY ANALYSIS
        # ==================================================

        st.subheader(
            "🛡️ File Integrity Analysis"
        )

        integrity_results = []

        for item in results:

            file_type = item["type"]

            # --------------------------------------------------
            # Extension fallback
            # --------------------------------------------------

            if file_type == "UNKNOWN":

                extension = os.path.splitext(
                    item["filename"]
                )[1].lower()

                if extension in [
                    ".jpg",
                    ".jpeg"
                ]:

                    file_type = "JPEG"

                elif extension == ".png":

                    file_type = "PNG"

                elif extension == ".pdf":

                    file_type = "PDF"

                elif extension == ".txt":

                    file_type = "TXT"

            # --------------------------------------------------
            # Analyze supported files
            # --------------------------------------------------

            if file_type in [
                "JPEG",
                "PNG",
                "PDF",
                "TXT"
            ]:

                integrity = check_file_integrity(
                    item["path"],
                    file_type
                )

                integrity_results.append({

                    "File": item["filename"],

                    "Type": file_type,

                    "Integrity Score": integrity["score"],

                    "Status": (
                        "VALID"
                        if integrity["valid"]
                        else "DAMAGED / UNREADABLE"
                    ),

                    "Evidence": "; ".join(
                        integrity["evidence"]
                    )

                })

        if integrity_results:

            st.dataframe(
                integrity_results,
                width="stretch"
            )

        else:

            st.info(
                "No supported files available "
                "for integrity analysis."
            )

        # ==================================================
        # FRAGMENT RECONSTRUCTION
        # ==================================================

        if os.path.exists(
            fragment_directory
        ):

            st.subheader(
                "🧩 Fragment Reconstruction"
            )

            recovery_results = test_fragment_orders(
                fragment_directory,
                candidate_directory
            )

            # --------------------------------------------------
            # PRIORITIZATION
            # --------------------------------------------------

            prioritized_results = prioritize_recovery(
                recovery_results
            )

            # --------------------------------------------------
            # AVAILABLE FRAGMENTS
            # --------------------------------------------------

            available_fragments = len(
                [
                    filename
                    for filename in os.listdir(
                        fragment_directory
                    )
                    if filename.endswith(".part")
                ]
            )

            # --------------------------------------------------
            # RECOVERY REPORT
            # --------------------------------------------------

            report = generate_recovery_report(
                recovery_results,
                available_fragments=available_fragments
            )

            # Keep the recovery report available across Streamlit reruns
            st.session_state["recovery_report"] = report

            # ==================================================
            # FRAGMENT RELATIONSHIP ANALYSIS
            # ==================================================

            st.subheader(
                "🔗 Fragment Relationship Analysis"
            )

            relationship_results = analyze_relationships(
                fragment_directory
            )

            if relationship_results:

                best_relationship = max(
                    relationship_results,
                    key=lambda result: result["score"]
                )

                st.write(
                    "**Recommended Fragment Order:**"
                )

                st.code(
                    " → ".join(
                        best_relationship["order"]
                    )
                )

                st.metric(
                    "Structural Relationship Score",
                    f'{best_relationship["score"]}%'
                )

                st.write(
                    "**Relationship Evidence:**"
                )

                for evidence in best_relationship["evidence"]:

                    st.success(
                        f"✓ {evidence}"
                    )

                st.info(
                    "The relationship engine tests possible fragment "
                    "orders and evaluates them using file-format "
                    "structural evidence."
                )

            # ==================================================
            # RECOVERY INTELLIGENCE
            # ==================================================

            st.subheader(
                "🏆 Recovery Intelligence"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Candidates Generated",
                len(prioritized_results)
            )

            col2.metric(
                "Best Recovery Score",
                f'{report["best_score"]}%'
            )

            col3.metric(
                "Status",
                report["status"]
            )

            # --------------------------------------------------
            # EXPLAINABLE RECOVERY SCORING
            # --------------------------------------------------

            st.write("### 🧠 Why this recovery score?")

            st.write(
                "The recovery score is an evidence-based integrity score. "
                "Each detected recovery signal contributes to the final score."
            )

            score = report["best_score"]

            if score >= 90:

                st.success(
                    f"🟢 Strong recovery evidence detected — {score}/100"
                )

            elif score >= 50:

                st.warning(
                    f"🟡 Partial recovery evidence detected — {score}/100"
                )

            else:

                st.error(
                    f"🔴 Weak recovery evidence detected — {score}/100"
                )

            st.write(
                "**Evidence contributing to the recovery assessment:**"
            )

            for evidence in report.get("evidence", []):

                if "JPEG header" in evidence:

                    st.write(
                        "✓ JPEG header detected — file structure starts correctly"
                    )

                elif "JPEG end marker" in evidence:

                    st.write(
                        "✓ JPEG end marker detected — file appears to have a valid ending"
                    )

                elif "Image successfully verified" in evidence:

                    st.write(
                        "✓ Image successfully verified — reconstructed data can be opened as an image"
                    )

                elif "Sufficient data size" in evidence:

                    st.write(
                        "✓ Sufficient data size — candidate contains enough recovered data"
                    )

                else:

                    st.write(
                        f"✓ {evidence}"
                    )

            st.caption(
                "Note: This score represents recovery evidence and integrity signals, "
                "not a statistical probability of successful recovery."
            )

            # ==================================================
            # AI-ASSISTED RECOVERY DECISION
            # ==================================================

            st.subheader(
                "🧠 AI-Assisted Recovery Decision"
            )

            if prioritized_results:

                best_candidate = prioritized_results[0]

                decision_score = best_candidate["recovery_score"]

                st.write(
                    "**Selected Candidate:**"
                )

                st.code(
                    " → ".join(
                        best_candidate["order"]
                    )
                )

                decision_col1, decision_col2 = st.columns(2)

                decision_col1.metric(
                    "Evidence Score",
                    f"{decision_score}%"
                )

                if decision_score >= 90:
                    decision_col2.success(
                        "🟢 HIGH RECOVERY CONFIDENCE"
                    )

                elif decision_score >= 50:
                    decision_col2.warning(
                        "🟡 PARTIAL RECOVERY"
                    )

                else:
                    decision_col2.error(
                        "🔴 LOW RECOVERY CONFIDENCE"
                    )

                st.write(
                    "**Why this candidate was prioritized:**"
                )

                for evidence in best_candidate.get(
                    "evidence",
                    []
                ):
                    st.write(
                        f"✓ {evidence}"
                    )

                st.info(
                    "The system prioritizes the candidate with "
                    "the strongest available recovery evidence. "
                    "The score represents evidence strength, "
                    "not a statistical probability of recovery."
                )

            # ==================================================
            # PRIORITIZED RECOVERIES
            # ==================================================

            st.subheader(
                "🥇 Prioritized Recoveries"
            )

            for result in prioritized_results:

                priority = result["priority"]

                score = result["recovery_score"]

                if priority == 1:

                    label = "🥇 Highest Priority"

                elif priority == 2:

                    label = "🥈 Second Priority"

                else:

                    label = f"Priority {priority}"

                with st.expander(
                    f"{label} — Recovery Score: {score}%"
                ):

                    st.write(
                        "**Fragment Reconstruction Order:**"
                    )

                    st.code(
                        " → ".join(
                            result["order"]
                        )
                    )

                    st.progress(
                        score / 100
                    )

                    if score >= 90:

                        st.success(
                            "🟢 Strong recovery evidence detected."
                        )

                    elif score >= 50:

                        st.warning(
                            "🟡 Partial recovery may be possible."
                        )

                    else:

                        st.error(
                            "🔴 Low recovery confidence."
                        )

                    if "evidence" in result:

                        st.write(
                            "**🔍 Recovery Evidence:**"
                        )

                        for evidence in result["evidence"]:

                            st.write(
                                f"✓ {evidence}"
                            )

                        # ==================================================
            # RECOMMENDED RECOVERY
            # ==================================================

            if prioritized_results:

                st.subheader(
                    "⭐ Recommended Recovery Candidate"
                )

                best = prioritized_results[0]

                st.write(
                    f'**Recovery Score:** '
                    f'{best["recovery_score"]}%'
                )

                st.write(
                    "**Fragment Reconstruction Order:**"
                )

                st.code(
                    " → ".join(
                        best["order"]
                    )
                )

                if best["recovery_score"] >= 90:

                    st.success(
                        "🟢 HIGH CONFIDENCE — "
                        "Strong evidence of successful recovery."
                    )

                elif best["recovery_score"] >= 50:

                    st.warning(
                        "🟡 MEDIUM CONFIDENCE — "
                        "Partial recovery may be possible."
                    )

                else:

                    st.error(
                        "🔴 LOW CONFIDENCE — "
                        "Recovery evidence is weak."
                    )

                # ==================================================
                # RECOVERED FILE PREVIEW
                # ==================================================

                st.write(
                    "**🖼️ Recovered File Preview:**"
                )

                recovered_file = best["candidate"]

                if os.path.exists(recovered_file):

                    st.image(
                        recovered_file,
                        caption="Recovered candidate selected by the recovery engine",
                        width="stretch"
                    )

                    st.success(
                        "✅ Recovered file successfully reconstructed and verified."
                    )

                else:

                    st.warning(
                        "Recovered candidate file could not be found."
                    )

            # ==================================================
            # AI-ASSISTED RECOVERY DECISION
            # ==================================================

            st.subheader(
                "🧠 AI-Assisted Recovery Decision"
            )

            st.write(
                "The system combines file integrity, "
                "fragment reconstruction, and relationship "
                "evidence to identify the strongest recovery candidate."
            )

            decision_col1, decision_col2, decision_col3 = st.columns(3)

            decision_col1.metric(
                "Recovery Status",
                report["status"]
            )

            decision_col2.metric(
                "Evidence Score",
                f'{best["recovery_score"]}%'
            )

            decision_col3.metric(
                "Fragments Available",
                available_fragments
            )

            st.write(
                "**🎯 Selected Recovery Candidate:**"
            )

            st.code(
                os.path.basename(
                    best["candidate"]
                )
            )

            st.write(
                "**🔗 Recommended Fragment Order:**"
            )

            st.code(
                " → ".join(
                    best["order"]
                )
            )

            st.info(
                "The recovery score represents the strength "
                "of observed recovery evidence. It is not a "
                "statistical probability of successful recovery."
            )

            # ==================================================
            # RECOVERY EVIDENCE
            # ==================================================

            st.subheader(
                "🔍 Recovery Evidence"
            )

            # Retrieve the latest report from session state
            report = st.session_state.get(
                "recovery_report",
                report
            )

            evidence_list = best.get(
                "evidence",
                []
            )

            if evidence_list:

                for evidence in evidence_list:

                    st.success(
                        f"✓ {evidence}"
                    )

            else:

                st.info(
                    "No detailed evidence available."
                )

            st.info(
                "The candidate with the strongest "
                "integrity evidence is prioritized "
                "for further investigation."
            )
            # AI-ASSISTED RECOVERY DECISION
            # ==================================================

            st.subheader(
                "🧠 AI-Assisted Recovery Decision"
            )

            st.write(
                "The system combines file integrity, "
                "fragment reconstruction, and relationship "
                "evidence to identify the strongest recovery candidate."
            )

            decision_col1, decision_col2, decision_col3 = st.columns(3)

            decision_col1.metric(
                "Recovery Status",
                report["status"]
            )

            decision_col2.metric(
                "Evidence Score",
                f'{best["recovery_score"]}%'
            )

            decision_col3.metric(
                "Fragments Available",
                available_fragments
            )

            st.write(
                "**🎯 Selected Recovery Candidate:**"
            )

            st.code(
                os.path.basename(
                    best["candidate"]
                )
            )

            st.write(
                "**🔗 Recommended Fragment Order:**"
            )

            st.code(
                " → ".join(
                    best["order"]
                )
            )

            st.info(
                "The recovery score represents the strength "
                "of observed recovery evidence. It is not a "
                "statistical probability of successful recovery."
            )

            # ==================================================
            # RECOVERY EVIDENCE
            # ==================================================

            st.subheader(
                "🔍 Recovery Evidence"
            )

            # Retrieve the latest report from session state
            report = st.session_state.get(
                "recovery_report",
                report
            )

            evidence_list = best.get(
                "evidence",
                []
            )

            if evidence_list:

                for evidence in evidence_list:

                    st.success(
                        f"✓ {evidence}"
                    )

            else:

                st.info(
                    "No detailed evidence available."
                )

            st.info(
                "The candidate with the strongest "
                "integrity evidence is prioritized "
                "for further investigation."
            )

        else:

            st.warning(
                "No fragment directory found."
            )

        # ==================================================
        # VISUAL INTELLIGENCE
        # ==================================================

        st.subheader(
            "🧠 Visual Intelligence"
        )

        st.write(
            "Analyze recovered images and identify "
            "visual relationships between them."
        )

        recovered_images = []

        if os.path.exists(
            candidate_directory
        ):

            for filename in os.listdir(
                candidate_directory
            ):

                if filename.lower().endswith(
                    (
                        ".jpg",
                        ".jpeg",
                        ".png"
                    )
                ):

                    recovered_images.append(
                        os.path.join(
                            candidate_directory,
                            filename
                        )
                    )

        if len(recovered_images) >= 2:

            visual_results = compare_images(
                recovered_images
            )

            st.write(
                f"**Images analyzed:** "
                f"{len(recovered_images)}"
            )

            if visual_results:

                st.write(
                    "**🔗 Detected Visual Relationships:**"
                )

                for relationship in visual_results:

                    similarity = relationship[
                        "similarity"
                    ]

                    image_a = relationship[
                        "image_a"
                    ]

                    image_b = relationship[
                        "image_b"
                    ]

                    if similarity >= 70:

                        st.success(
                            f"🟢 {image_a} ↔ {image_b} "
                            f"— Similarity: {similarity}%"
                        )

                    elif similarity >= 40:

                        st.warning(
                            f"🟡 {image_a} ↔ {image_b} "
                            f"— Similarity: {similarity}%"
                        )

                    else:

                        st.write(
                            f"⚪ {image_a} ↔ {image_b} "
                            f"— Similarity: {similarity}%"
                        )

            else:

                st.info(
                    "No visual relationships detected."
                )

        else:

            st.info(
                "At least two recovered images are "
                "required for visual comparison."
            )