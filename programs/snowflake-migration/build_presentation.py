"""Generate Redshift Shutdown presentation as PPTX -- plan & impact focused."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

DARK_BG = RGBColor(0x1B, 0x1B, 0x2F)
ACCENT = RGBColor(0x29, 0xB6, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xB0, 0xB0, 0xB0)
GREEN = RGBColor(0x66, 0xBB, 0x6A)
RED = RGBColor(0xEF, 0x53, 0x50)
ORANGE = RGBColor(0xFF, 0xA7, 0x26)
MUTED_BLUE = RGBColor(0x42, 0xA5, 0xF5)

W = Inches(13.333)
H = Inches(7.5)


def set_slide_bg(slide, color=DARK_BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, left, top, width, height, text, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return tf


def add_bullet_list(slide, left, top, width, height, items, size=16, color=WHITE):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
    return tf


def add_metric_box(slide, left, top, width, height, label, value, sub=None, value_color=ACCENT):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x25, 0x25, 0x40)
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    p = tf.paragraphs[0]
    p.text = value
    p.font.size = Pt(32)
    p.font.color.rgb = value_color
    p.font.bold = True

    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.size = Pt(13)
    p2.font.color.rgb = LIGHT_GRAY
    p2.alignment = PP_ALIGN.CENTER

    if sub:
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(11)
        p3.font.color.rgb = LIGHT_GRAY
        p3.alignment = PP_ALIGN.CENTER


def add_table(slide, left, top, width, rows_data):
    rows = len(rows_data)
    cols = len(rows_data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, Inches(0.42 * rows))
    table = table_shape.table
    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                if i == 0:
                    p.font.bold = True
                    p.font.color.rgb = WHITE
                else:
                    p.font.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
                p.alignment = PP_ALIGN.LEFT
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0x2A, 0x2A, 0x45) if i == 0 else RGBColor(0x20, 0x20, 0x38)


def build_presentation():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # ===== SLIDE 1: Title =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.5),
             "Redshift Shutdown", size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(1), Inches(3.5), Inches(11), Inches(0.8),
             "Phased Consumer Cutover", size=24, color=ACCENT, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(1), Inches(4.8), Inches(11), Inches(0.6),
             "Data Platform Team  |  September 2026", size=16, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

    # ===== SLIDE 2: Current State - Cluster =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Current State: Cluster", size=34, color=WHITE, bold=True)

    add_metric_box(slide, Inches(0.8), Inches(1.3), Inches(2.8), Inches(1.5),
                   "Nodes", "5 x ra3.16xl", "ito-ds-redshift-dsredshift-kfbgevo589gl")
    add_metric_box(slide, Inches(4.0), Inches(1.3), Inches(2.8), Inches(1.5),
                   "Peak CPU (hourly avg)", "43.5%", "Room to resize to 3 nodes (~73%)")
    add_metric_box(slide, Inches(7.2), Inches(1.3), Inches(2.8), Inches(1.5),
                   "Disk Used", "10.5%", "RA3 managed storage -- not a constraint")
    add_metric_box(slide, Inches(10.4), Inches(1.3), Inches(2.8), Inches(1.5),
                   "Peak Connections", "123", "Trending down from Aug baseline")

    add_text(slide, Inches(0.8), Inches(3.3), Inches(11.5), Inches(0.5),
             "All data has been migrated to Snowflake. Redshift is no longer the source of truth.", size=18, color=GREEN, bold=True)
    add_bullet_list(slide, Inches(0.8), Inches(4.0), Inches(11.5), Inches(2.5), [
        "Active users down from 36 (Aug) to 22 -- but query volume flat at ~100K/day",
        "Automated processes dominate: Overlord, dbt, Fivetran, MV refreshes account for 99%+ of queries",
        "Concurrency scaling already at $0 (was $8-13K/mo in Q1)",
        "Cluster cannot be turned off until all consumers are re-pointed or disabled",
    ], size=16)

    # ===== SLIDE 3: Current State - Daily Cost =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Current State: Daily Cost", size=34, color=WHITE, bold=True)

    add_metric_box(slide, Inches(4.0), Inches(1.2), Inches(5.0), Inches(1.8),
                   "Total Daily Spend", "$1,556/day", "$47,225/month  |  $567K annualized", value_color=RED)

    add_table(slide, Inches(0.8), Inches(3.4), Inches(11.5), [
        ["Component", "Daily", "Monthly", "Annualized", "Type"],
        ["Compute (5 x ra3.16xlarge)", "$1,267", "$38,500", "$462,500", "Fixed until resized or terminated"],
        ["Spectrum (S3 data scanned)", "$149", "$4,500", "$54,400", "Variable -- drops with MV shutoff"],
        ["Managed Storage (RMS)", "$41", "$1,250", "$15,000", "Fixed until terminated"],
        ["Snapshots", "$9", "$275", "$3,300", "Fixed until deleted"],
        ["Fivetran MAR (RS destination)", "$90", "$2,700", "$32,400", "Variable -- drops to $0 when paused"],
    ])

    # ===== SLIDE 4: Current State - Active Consumers =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Current State: Active Consumers", size=34, color=WHITE, bold=True)

    add_text(slide, Inches(0.8), Inches(1.1), Inches(11.5), Inches(0.5),
             "The cluster stays on because these automated processes still read from it:", size=16, color=LIGHT_GRAY)

    add_table(slide, Inches(0.8), Inches(1.7), Inches(11.5), [
        ["Consumer", "Queries (7d)", "Avg Daily", "% of Total", "Status"],
        ["Overlord + MV Refreshes (datasciadmin)", "412,624", "~47,000", "57.7%", "52 orphaned MVs; active ones need cutover"],
        ["Fivetran (service_fivetran)", "124,431", "~39,000", "17.4%", "8 of 18 connectors orphaned; 10 have active RS consumers"],
        ["dbt Cloud (service_dbt)", "138,800", "~19,000", "19.4%", "RS dbt models to be replaced by Snowflake models"],
        ["QuickSight (service_qs_*)", "11,818", "~9,600", "1.7%", "ECM dashboards in progress (DNA-6080)"],
        ["Amplitude (service_amplitude)", "10,596", "~1,050", "1.5%", "Evaluate consumer dependency"],
        ["InfoSec (service_security)", "7,406", "~1,000", "1.0%", "Runs until cluster off -- no action needed"],
        ["Human users", "~5,500", "~113", "<1%", "22 active, ~130 inactive (can disable)"],
    ])

    # ===== SLIDE 3: The Plan =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "The Plan: Phased Shutdown", size=34, color=WHITE, bold=True)

    add_table(slide, Inches(0.8), Inches(1.3), Inches(11.5), [
        ["Phase", "What", "Weekly Savings", "Monthly Savings", "Status"],
        ["1. Quick Wins", "Pause 8 orphaned Fivetran connectors, stop 52 orphan MVs, disable inactive users & jobs", "$735/wk", "$3.2K/mo", "Ready now"],
        ["2. Resize 5 to 3 nodes", "Elastic resize -- CloudWatch confirms safe (43.5% peak CPU)", "$3,549/wk", "$15.4K/mo", "Ready after Phase 1"],
        ["3. Consumer Cutover", "Re-point remaining dbt, Overlord, and QuickSight consumers", "--", "Enables 4 & 5", "In progress"],
        ["4. Resize 3 to 2 nodes", "After workload reduction drops peak CPU below 35%", "$1,771/wk", "$7.7K/mo", "Blocked on Phase 3"],
        ["5. Full Shutdown", "Terminate cluster after 7 days at 0 queries", "$4,207/wk", "$18.3K/mo", "Blocked on OpenAir"],
    ])

    add_text(slide, Inches(0.8), Inches(4.8), Inches(11.5), Inches(0.5),
             "Phases 1 + 2 deliver $18.6K/month savings and can be executed immediately.", size=18, color=GREEN, bold=True)
    add_text(slide, Inches(0.8), Inches(5.4), Inches(11.5), Inches(0.5),
             "Critical path to full shutdown: OpenAir reverse ETL (SOX-compliant, 23 jobs, Finance sign-off).", size=16, color=RED)

    # ===== SLIDE 4: Savings Trajectory =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Savings Trajectory", size=34, color=WHITE, bold=True)

    add_table(slide, Inches(0.8), Inches(1.3), Inches(11.5), [
        ["Milestone", "% Complete", "Daily", "Weekly", "Monthly"],
        ["Today (assessment done)", "16%", "$0", "$0", "$0"],
        ["Phase 1 executed", "37%", "$105", "$735", "$3,167"],
        ["Resized to 3 nodes", "70%", "$612", "$4,284", "$18,567"],
        ["Consumers cut over", "85%", "$612", "$4,284", "$18,567"],
        ["Resized to 2 nodes", "91%", "$865", "$6,055", "$26,250"],
        ["Full shutdown", "100%", "$1,556", "$10,892", "$47,225"],
    ])

    add_text(slide, Inches(0.8), Inches(4.6), Inches(11.5), Inches(0.8),
             "Every day we delay Phase 1 costs $105.  Every day we delay the resize costs another $507.",
             size=20, color=ORANGE, bold=True, align=PP_ALIGN.CENTER)

    # ===== SLIDE 5: What We Found =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Assessment Findings", size=34, color=WHITE, bold=True)

    add_text(slide, Inches(0.8), Inches(1.2), Inches(11.5), Inches(0.5),
             "We inventoried every object in Redshift and classified it by activity and load mechanism:", size=16, color=LIGHT_GRAY)

    add_metric_box(slide, Inches(0.8), Inches(1.9), Inches(2.8), Inches(1.4),
                   "Landing Tables", "1,136", "Where data first enters Redshift", value_color=MUTED_BLUE)
    add_metric_box(slide, Inches(4.0), Inches(1.9), Inches(2.8), Inches(1.4),
                   "Active Landing Tables", "970", "Have query activity in last 10 days", value_color=GREEN)
    add_metric_box(slide, Inches(7.2), Inches(1.9), Inches(2.8), Inches(1.4),
                   "Orphaned Landing Tables", "166", "Zero consumer reads -- safe to stop", value_color=RED)
    add_metric_box(slide, Inches(10.4), Inches(1.9), Inches(2.8), Inches(1.4),
                   "Orphaned MVs", "52", "Refreshing daily, nobody reading", value_color=RED)

    add_text(slide, Inches(0.8), Inches(3.7), Inches(5.5), Inches(0.5),
             "Approach: physical read tracking", size=18, color=ACCENT, bold=True)
    add_bullet_list(slide, Inches(0.8), Inches(4.2), Inches(5.5), Inches(2.5), [
        "Tracked every physical table read over a 10-day window",
        "Objects with zero consumer reads are confirmed orphans",
        "Initial text-based analysis found ~150 orphans; physical tracking",
        "  corrected this to 52 (queries read through intermediate views)",
    ], size=14)

    add_text(slide, Inches(6.8), Inches(3.7), Inches(5.5), Inches(0.5),
             "Approach: lineage for active consumers", size=18, color=ACCENT, bold=True)
    add_bullet_list(slide, Inches(6.8), Inches(4.2), Inches(5.5), Inches(2.5), [
        "For active objects: Atlan lineage maps the full dependency chain",
        "Example: mv_spectrum.workiva_workspace feeds 234 downstream objects",
        "  -- 12 direct dependents, 100 dbt models, 82 views, 9 QS datasets",
        "This tells us what to re-point before we can turn off each pipeline",
    ], size=14)

    # ===== SLIDE 6: Blockers & Risks =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Blockers & Risks", size=34, color=WHITE, bold=True)

    add_text(slide, Inches(0.8), Inches(1.3), Inches(3.8), Inches(0.5),
             "OpenAir Reverse ETL", size=20, color=RED, bold=True)
    add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(3.8), Inches(2.0), [
        "23 bidirectional Salesforce-OpenAir sync jobs",
        "SOX-compliant, revenue-impacting",
        "Requires Finance/Accounting sign-off",
        "Cross-team: CPX, BizTech, Finance",
        "Non-prod environment provisioning delayed",
    ], size=13)

    add_text(slide, Inches(4.9), Inches(1.3), Inches(3.8), Inches(0.5),
             "FedRAMP Boundary Change", size=20, color=RED, bold=True)
    add_bullet_list(slide, Inches(4.9), Inches(1.8), Inches(3.8), Inches(2.0), [
        "Tennessee Valley Authority is FedRAMP sponsor",
        "Must accept removal of Redshift from FedRAMP boundary",
        "Acceptance has not been received",
        "Blocks full cluster termination",
    ], size=13)

    add_text(slide, Inches(9.0), Inches(1.3), Inches(3.8), Inches(0.5),
             "ECM QuickSight Dashboards", size=20, color=ORANGE, bold=True)
    add_bullet_list(slide, Inches(9.0), Inches(1.8), Inches(3.8), Inches(1.3), [
        "QuickSight datasets still reading from Redshift",
        "DNA-6080 in progress (Alexandre Cerqueira)",
    ], size=13)

    add_text(slide, Inches(9.0), Inches(3.3), Inches(3.8), Inches(0.5),
             "Jira Pipeline Missing in Snowflake", size=20, color=ORANGE, bold=True)
    add_bullet_list(slide, Inches(9.0), Inches(3.8), Inches(3.8), Inches(1.3), [
        "No equivalent pipeline exists in Snowflake",
        "Downstream dbt models and views depend on it",
        "3-4 weeks to build",
    ], size=13)

    add_text(slide, Inches(0.8), Inches(5.2), Inches(11.5), Inches(0.5),
             "OpenAir, FedRAMP, and Jira block full shutdown but do NOT block the resize to 3 nodes.", size=16, color=GREEN)

    # ===== SLIDE 7: Timeline =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Timeline", size=34, color=WHITE, bold=True)

    add_table(slide, Inches(0.8), Inches(1.2), Inches(11.5), [
        ["Week", "Milestone", "Savings Impact", "Owner"],
        ["Sept 15-19", "Phase 1: Pause 8 Fivetran connectors, stop 52 orphan MVs, disable inactive users & Overlord jobs", "$735/wk", "Data Platform"],
        ["Sept 22-26", "Phase 2: Resize cluster from 5 to 3 nodes", "+$3,549/wk", "Data Platform"],
        ["Sept 22-30", "ECM QuickSight migration complete (DNA-6080)", "--", "Alison Weingarten"],
        ["Sept 22 - Oct 10", "Consumer cutover: map lineage, assign tickets by team, re-point consumers", "--", "Data Platform + stakeholders"],
        ["Oct 6-17", "Jira pipeline stood up in Snowflake", "--", "Data Platform"],
        ["Oct 13-31", "OpenAir reverse ETL cutover (SOX, Finance sign-off)", "--", "CPX / BizTech / Finance"],
        ["TBD", "FedRAMP boundary change accepted by Tennessee Valley Authority", "--", "Security / Compliance"],
        ["Late Oct", "Phase 4: Resize 3 to 2 nodes (after CPU drops below 35%)", "+$1,771/wk", "Data Platform"],
        ["Nov 1 target", "Phase 5: Terminate cluster (after 7 days at 0 queries)", "+$4,207/wk", "Data Platform"],
    ])

    add_text(slide, Inches(0.8), Inches(5.4), Inches(5.5), Inches(0.5),
             "Target: $0 Redshift by November 1", size=20, color=GREEN, bold=True)

    add_text(slide, Inches(6.8), Inches(5.4), Inches(5.5), Inches(0.5),
             "Risks: OpenAir SOX sign-off and FedRAMP acceptance could push past October", size=15, color=RED)

    # ===== SLIDE 8: Next Steps & Ask =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
             "Next Steps", size=34, color=WHITE, bold=True)

    add_text(slide, Inches(0.8), Inches(1.3), Inches(5.8), Inches(0.5),
             "This week", size=22, color=GREEN, bold=True)
    add_bullet_list(slide, Inches(0.8), Inches(1.9), Inches(5.8), Inches(2.0), [
        "Execute Phase 1: pause 8 orphaned Fivetran connectors, stop 52 orphan MVs,",
        "  disable 8 dormant Overlord jobs, disable ~130 inactive users",
        "Submit cluster resize from 5 to 3 nodes",
        "Combined impact: $612/day savings ($223K annualized)",
    ], size=16)

    add_text(slide, Inches(0.8), Inches(4.0), Inches(5.8), Inches(0.5),
             "Coming weeks", size=22, color=ORANGE, bold=True)
    add_bullet_list(slide, Inches(0.8), Inches(4.6), Inches(5.8), Inches(2.0), [
        "Run lineage extraction for all 843 active landing tables",
        "Group remaining consumers by owning team",
        "Create cutover tickets -- track progress via daily scan pipeline",
    ], size=16)

    add_text(slide, Inches(7.2), Inches(1.3), Inches(5.5), Inches(0.5),
             "Discussion", size=22, color=MUTED_BLUE, bold=True)
    add_bullet_list(slide, Inches(7.2), Inches(1.9), Inches(5.5), Inches(4.0), [
        "Are we aligned on the phased approach?",
        "",
        "Who owns the resize change window?",
        "",
        "How do we assign consumer cutover work by team?",
        "",
        "Escalation path for OpenAir SOX dependency?",
    ], size=17)

    # Save
    output = "/Users/deanmccall/Documents/dna_ai_program_manager/programs/snowflake-migration/redshift-shutdown-presentation.pptx"
    prs.save(output)
    print(f"Saved to {output}")
    return output


if __name__ == "__main__":
    build_presentation()
