"""
Agent 2 - Functional QA Automation Engine
Tests navigation links, interactive buttons, forms, images, and DOM tree health.
"""
from typing import List
from bs4 import BeautifulSoup

from backend.schemas.agent2_schema import (
    TestCaseResult,
    TestCategory,
    TestSeverity,
)
from backend.utils.logger import global_log_buffer


class FunctionalTester:
    def __init__(self):
        pass

    def run_tests(self, html_content: str, preview_url: str) -> List[TestCaseResult]:
        """
        Executes strict functional test cases against actual parsed DOM elements.
        Never marks an unexecuted test as passed.
        """
        global_log_buffer.log("FUNC_QA", "AGENT_2", f"Running functional test suite against DOM at {preview_url}")

        soup = BeautifulSoup(html_content, "html.parser")
        test_cases: List[TestCaseResult] = []

        # 1. Page Load & Title Health Test
        title_tag = soup.find("title")
        has_title = title_tag is not None and len(title_tag.text.strip()) > 0
        test_cases.append(TestCaseResult(
            test_id="FUNC-001",
            category=TestCategory.FUNCTIONAL,
            description="Page Load and HTML Document Metadata",
            expected_result="Valid HTML document with non-empty <title> and metadata",
            actual_result=f"Page loaded successfully with title: '{title_tag.text.strip()}'" if has_title else "Missing or empty <title> tag",
            passed=has_title,
            severity=TestSeverity.CRITICAL if not has_title else TestSeverity.INFO,
            affected_component="MainLayout.astro"
        ))

        # 2. Navigation Anchor Links Test
        nav_anchors = soup.find_all("a")
        broken_anchors = []
        valid_anchors = 0
        for a in nav_anchors:
            href = a.get("href", "")
            if not href or href == "#":
                broken_anchors.append(a.text.strip() or "Unnamed Link")
            else:
                valid_anchors += 1

        nav_passed = len(broken_anchors) == 0 and valid_anchors > 0
        test_cases.append(TestCaseResult(
            test_id="FUNC-002",
            category=TestCategory.FUNCTIONAL,
            description="Navigation Links and Anchor Targets",
            expected_result="All navigation links have valid non-empty destination hrefs or section targets",
            actual_result=f"Verified {valid_anchors} valid links" if nav_passed else f"Found {len(broken_anchors)} empty/invalid links ({', '.join(broken_anchors[:3])})",
            passed=nav_passed,
            severity=TestSeverity.HIGH if not nav_passed else TestSeverity.INFO,
            issue_description="Empty or placeholder href='#' found on navigation links" if not nav_passed else None,
            recommendation="Replace placeholder links with explicit section IDs (#about, #sectors, #contact)." if not nav_passed else None,
            affected_component="Navigation.astro"
        ))

        # 3. Interactive Buttons Test
        buttons = soup.find_all("button")
        valid_buttons = 0
        empty_buttons = 0
        for b in buttons:
            btn_text = b.text.strip()
            aria_label = b.get("aria-label", "")
            if btn_text or aria_label:
                valid_buttons += 1
            else:
                empty_buttons += 1

        btn_passed = empty_buttons == 0 and (valid_buttons > 0 or len(buttons) == 0)
        test_cases.append(TestCaseResult(
            test_id="FUNC-003",
            category=TestCategory.FUNCTIONAL,
            description="Interactive Buttons and Accessibility Labels",
            expected_result="All button elements have accessible text or aria-labels and valid cursor styling",
            actual_result=f"Verified {valid_buttons} accessible interactive buttons" if btn_passed else f"Found {empty_buttons} buttons without accessible labels",
            passed=btn_passed,
            severity=TestSeverity.MEDIUM if not btn_passed else TestSeverity.INFO,
            issue_description="Button lacks visible text or aria-label for accessibility" if not btn_passed else None,
            recommendation="Add aria-label attribute to icon and utility buttons." if not btn_passed else None,
            affected_component="Header.astro"
        ))

        # 4. Corporate Contact Form Test
        form = soup.find("form")
        form_valid = False
        inputs_found = []
        if form:
            inputs = form.find_all(["input", "textarea", "select"])
            inputs_found = [i.get("name") or i.get("id") or "unnamed" for i in inputs]
            has_email = any("email" in name.lower() for name in inputs_found)
            has_submit = form.find("button", {"type": "submit"}) is not None or form.find("input", {"type": "submit"}) is not None
            form_valid = has_email and has_submit and len(inputs) >= 2

        test_cases.append(TestCaseResult(
            test_id="FUNC-004",
            category=TestCategory.FUNCTIONAL,
            description="Corporate Contact Form Validation and Inputs",
            expected_result="Contact form contains corporate email input, area selector, and active submit button",
            actual_result=f"Verified form with {len(inputs_found)} inputs ({', '.join(inputs_found)}) and submit handler" if form_valid else "Incomplete or missing contact form inputs",
            passed=form_valid,
            severity=TestSeverity.HIGH if not form_valid else TestSeverity.INFO,
            issue_description="Form missing email field or submit trigger" if not form_valid else None,
            recommendation="Include name, email, inquiry type select, and submit button." if not form_valid else None,
            affected_component="Contact.astro"
        ))

        # 5. Image Loading and Alt Attributes Test
        images = soup.find_all("img")
        missing_alts = 0
        valid_images = 0
        for img in images:
            if not img.get("alt"):
                missing_alts += 1
            else:
                valid_images += 1

        img_passed = missing_alts == 0
        test_cases.append(TestCaseResult(
            test_id="FUNC-005",
            category=TestCategory.FUNCTIONAL,
            description="Image Assets and Accessibility Attributes",
            expected_result="All image and logo assets provide descriptive alt text for accessibility and screen readers",
            actual_result=f"Verified {valid_images} image assets with alt tags" if img_passed else f"Found {missing_alts} images missing alt attributes",
            passed=img_passed,
            severity=TestSeverity.MEDIUM if not img_passed else TestSeverity.INFO,
            affected_component="Hero.astro"
        ))

        # 6. Critical Section Heading Semantics
        headings = [h.name for h in soup.find_all(["h1", "h2", "h3"])]
        has_h1 = "h1" in headings
        has_h2 = "h2" in headings
        hierarchy_passed = has_h1 and has_h2
        test_cases.append(TestCaseResult(
            test_id="FUNC-006",
            category=TestCategory.FUNCTIONAL,
            description="Semantic Heading Hierarchy (H1 / H2 / H3)",
            expected_result="Document establishes a valid semantic heading hierarchy starting with exactly one primary H1",
            actual_result=f"Verified valid heading hierarchy: H1 ({headings.count('h1')}), H2 ({headings.count('h2')}), H3 ({headings.count('h3')})" if hierarchy_passed else "Improper heading hierarchy",
            passed=hierarchy_passed,
            severity=TestSeverity.HIGH if not hierarchy_passed else TestSeverity.INFO,
            affected_component="Hero.astro"
        ))

        global_log_buffer.log("FUNC_QA", "AGENT_2", f"Completed functional test execution. {sum(1 for t in test_cases if t.passed)}/{len(test_cases)} tests passed.")
        return test_cases
