import time
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pathlib import Path


class ApplicationFiller:
    """Automates filling out job application forms."""

    def __init__(self, driver: webdriver.Chrome, user_profile: Dict):
        self.driver = driver
        self.profile = user_profile
        self.personal_info = user_profile.get('personal_info', {})
        self.wait = WebDriverWait(driver, 10)

    def fill_text_field(self, element, value: str):
        """Fill a text input field."""
        try:
            element.clear()
            element.send_keys(value)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"  Error filling text field: {e}")
            return False

    def detect_and_fill_field(self, field_identifier: str, value: str) -> bool:
        """Detect and fill a field by various identifiers."""
        # Try multiple selector strategies
        selectors = [
            (By.ID, field_identifier),
            (By.NAME, field_identifier),
            (By.CSS_SELECTOR, f"input[placeholder*='{field_identifier}' i]"),
            (By.CSS_SELECTOR, f"input[aria-label*='{field_identifier}' i]"),
            (By.XPATH, f"//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{field_identifier.lower()}')]/following::input[1]")
        ]

        for by, selector in selectors:
            try:
                element = self.driver.find_element(by, selector)
                return self.fill_text_field(element, value)
            except NoSuchElementException:
                continue

        return False

    def fill_basic_info(self) -> Dict[str, bool]:
        """Fill basic personal information fields."""
        results = {}

        # Common field mappings
        field_mappings = {
            'name': self.personal_info.get('name', ''),
            'first name': self.personal_info.get('name', '').split()[0] if self.personal_info.get('name') else '',
            'last name': self.personal_info.get('name', '').split()[-1] if self.personal_info.get('name') else '',
            'email': self.personal_info.get('email', ''),
            'phone': self.personal_info.get('phone', ''),
            'location': self.personal_info.get('location', ''),
            'city': self.personal_info.get('location', '').split(',')[0] if self.personal_info.get('location') else '',
            'linkedin': self.personal_info.get('linkedin', ''),
            'portfolio': self.personal_info.get('portfolio', ''),
            'website': self.personal_info.get('portfolio', ''),
            'github': self.personal_info.get('github', ''),
        }

        print("  Filling basic information...")
        for field_name, value in field_mappings.items():
            if value:
                results[field_name] = self.detect_and_fill_field(field_name, value)

        return results

    def upload_resume(self, resume_path: str) -> bool:
        """Upload resume file."""
        if not Path(resume_path).exists():
            print(f"  Resume file not found: {resume_path}")
            return False

        # Try to find file upload input
        upload_selectors = [
            "input[type='file']",
            "input[name*='resume' i]",
            "input[name*='cv' i]",
            "input[id*='resume' i]",
            "input[id*='cv' i]",
        ]

        for selector in upload_selectors:
            try:
                upload_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                upload_input.send_keys(str(Path(resume_path).absolute()))
                print(f"  ✓ Resume uploaded: {resume_path}")
                time.sleep(2)
                return True
            except NoSuchElementException:
                continue

        print("  ✗ Could not find resume upload field")
        return False

    def answer_common_questions(self) -> Dict[str, bool]:
        """Answer common application questions."""
        results = {}

        # Common yes/no questions
        yes_no_patterns = {
            'authorized to work': True,
            'require sponsorship': False,
            'require visa': False,
            'over 18': True,
            'drug test': True,
            'background check': True,
        }

        print("  Answering common questions...")

        # Try to find and answer yes/no questions
        for pattern, answer in yes_no_patterns.items():
            try:
                # Look for radio buttons or checkboxes
                question_elements = self.driver.find_elements(
                    By.XPATH,
                    f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{pattern}')]"
                )

                if question_elements:
                    # Find associated yes/no inputs
                    value_to_select = 'yes' if answer else 'no'
                    radio_buttons = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        f"input[type='radio'][value*='{value_to_select}' i]"
                    )

                    if radio_buttons:
                        radio_buttons[0].click()
                        results[pattern] = True
                        time.sleep(0.5)

            except Exception as e:
                continue

        return results

    def detect_easy_apply_button(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """Detect 'Easy Apply' or similar quick application buttons."""
        easy_apply_selectors = [
            "button.jobs-apply-button",
            "button[aria-label*='Easy Apply' i]",
            "button:contains('Easy Apply')",
            "//button[contains(text(), 'Easy Apply')]",
            "//button[contains(text(), 'Apply Now')]",
            ".jobs-apply-button",
        ]

        for selector in easy_apply_selectors:
            try:
                if selector.startswith("//"):
                    button = self.driver.find_element(By.XPATH, selector)
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                return button
            except NoSuchElementException:
                continue

        return None

    def click_next_or_submit(self) -> bool:
        """Click Next or Submit button in multi-step forms."""
        button_selectors = [
            "button[aria-label*='Submit' i]",
            "button[aria-label*='Next' i]",
            "button[type='submit']",
            "//button[contains(text(), 'Next')]",
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Continue')]",
        ]

        for selector in button_selectors:
            try:
                if selector.startswith("//"):
                    button = self.driver.find_element(By.XPATH, selector)
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)

                if button.is_enabled():
                    button.click()
                    time.sleep(2)
                    return True
            except NoSuchElementException:
                continue

        return False

    def handle_multi_step_form(self, max_steps: int = 10) -> bool:
        """Handle multi-step application forms."""
        print("  Navigating multi-step form...")

        for step in range(max_steps):
            print(f"    Step {step + 1}...")

            # Fill any visible fields
            self.fill_basic_info()
            self.answer_common_questions()

            # Try to proceed to next step
            if not self.click_next_or_submit():
                print("    No more steps found")
                break

            time.sleep(2)

            # Check if we've reached confirmation page
            if self._is_confirmation_page():
                print("  ✓ Application submitted successfully!")
                return True

        return False

    def _is_confirmation_page(self) -> bool:
        """Check if current page is a confirmation/success page."""
        confirmation_indicators = [
            "application submitted",
            "thank you for applying",
            "we've received your application",
            "application received",
            "successfully applied"
        ]

        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

        return any(indicator in page_text for indicator in confirmation_indicators)
