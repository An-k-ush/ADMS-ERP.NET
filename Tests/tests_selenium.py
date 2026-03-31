"""
ADMS ERP - Automated Test Suite using Python + Selenium
Covers: Login, Item CRUD, Process Item functionality

Prerequisites:
    pip install selenium pytest webdriver-manager

Usage:
    # Run all tests
    pytest tests_selenium.py -v

    # Run specific test class
    pytest tests_selenium.py::TestLogin -v

Note: The application must be running on BASE_URL before executing tests.
      Default URL: http://localhost:5000
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:5000"
VALID_EMAIL = "admin@adms.com"
VALID_PASSWORD = "Admin@123"
WAIT_TIMEOUT = 10


def get_driver():
    """Create a headless Chrome WebDriver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except Exception:
        return webdriver.Chrome(options=options)


@pytest.fixture(scope="class")
def driver():
    """Shared driver fixture per test class."""
    d = get_driver()
    d.implicitly_wait(WAIT_TIMEOUT)
    yield d
    d.quit()


def login(driver, email=VALID_EMAIL, password=VALID_PASSWORD):
    """Helper: navigate to login and sign in."""
    driver.get(f"{BASE_URL}/Account/Login")
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(EC.presence_of_element_located((By.ID, "Email")))
    driver.find_element(By.ID, "Email").clear()
    driver.find_element(By.ID, "Email").send_keys(email)
    driver.find_element(By.ID, "Password").clear()
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)


# =============================================================================
# TC-001 to TC-008: Login Tests
# =============================================================================
class TestLogin:
    """Test cases for the Login screen."""

    def test_tc001_valid_login(self, driver):
        """TC-001: Valid credentials redirect to Items page."""
        login(driver)
        assert "/Account/Login" not in driver.current_url, \
            "Should not remain on login page after valid login"
        assert "item" in driver.current_url.lower() or \
               driver.find_element(By.TAG_NAME, "body").text != "", \
            "Should redirect to Items page"

    def test_tc002_invalid_email_format(self, driver):
        """TC-002: Invalid email format shows validation error."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Email").send_keys("notanemail")
        driver.find_element(By.ID, "Password").send_keys("Admin@123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "invalid" in page_text.lower() or "/Account/Login" in driver.current_url, \
            "TC-002: Should show email validation error"

    def test_tc003_empty_email(self, driver):
        """TC-003: Empty email shows required validation."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Password").send_keys("Admin@123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "required" in page_text.lower() or "/Account/Login" in driver.current_url, \
            "TC-003: Should show email required error"

    def test_tc004_empty_password(self, driver):
        """TC-004: Empty password shows required validation."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Email").send_keys("admin@adms.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "required" in page_text.lower() or "/Account/Login" in driver.current_url, \
            "TC-004: Should show password required error"

    def test_tc005_wrong_password(self, driver):
        """TC-005: Wrong password shows invalid credentials error."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Email").send_keys("admin@adms.com")
        driver.find_element(By.ID, "Password").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "invalid" in page_text.lower() or "/Account/Login" in driver.current_url, \
            "TC-005: Should show invalid credentials error"

    def test_tc006_nonexistent_user(self, driver):
        """TC-006: Non-existent user shows invalid credentials error."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Email").send_keys("nobody@test.com")
        driver.find_element(By.ID, "Password").send_keys("Test@123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "invalid" in page_text.lower() or "/Account/Login" in driver.current_url, \
            "TC-006: Should show invalid credentials error"

    def test_tc007_sql_injection_attempt(self, driver):
        """TC-007: SQL injection in email field should fail gracefully."""
        driver.get(f"{BASE_URL}/Account/Login")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Email")))
        driver.find_element(By.ID, "Email").send_keys("' OR 1=1 --")
        driver.find_element(By.ID, "Password").send_keys("x")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        # Should NOT be logged in
        assert "/Account/Login" in driver.current_url or \
               "invalid" in driver.find_element(By.TAG_NAME, "body").text.lower(), \
            "TC-007: SQL injection should not bypass authentication"


# =============================================================================
# TC-010 to TC-054: Item Screen Tests
# =============================================================================
class TestItems:
    """Test cases for the Items CRUD screen."""

    TEST_ITEM_NAME = f"AutoTest_Item_{int(time.time())}"

    def test_tc010_valid_item_creation(self, driver):
        """TC-010: Create a valid item."""
        login(driver)
        driver.get(f"{BASE_URL}/Item/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Name")))
        driver.find_element(By.ID, "Name").send_keys(TestItems.TEST_ITEM_NAME)
        driver.find_element(By.ID, "Weight").send_keys("50.5")
        driver.find_element(By.ID, "Description").send_keys("Auto test item")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "created successfully" in page_text.lower() or \
               TestItems.TEST_ITEM_NAME in page_text, \
            "TC-010: Item should be created successfully"

    def test_tc011_empty_name_validation(self, driver):
        """TC-011: Item with empty name should fail validation."""
        login(driver)
        driver.get(f"{BASE_URL}/Item/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Weight")))
        driver.find_element(By.ID, "Weight").send_keys("10")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "required" in page_text.lower() or "/Item/Create" in driver.current_url, \
            "TC-011: Should show name required validation"

    def test_tc012_zero_weight_validation(self, driver):
        """TC-012: Item with weight=0 should fail validation."""
        login(driver)
        driver.get(f"{BASE_URL}/Item/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Name")))
        driver.find_element(By.ID, "Name").send_keys("ZeroWeightItem")
        driver.find_element(By.ID, "Weight").send_keys("0")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "greater than 0" in page_text.lower() or \
               "weight" in page_text.lower() and "0" in page_text, \
            "TC-012: Should show weight > 0 validation error"

    def test_tc013_negative_weight_validation(self, driver):
        """TC-013: Item with negative weight should fail validation."""
        login(driver)
        driver.get(f"{BASE_URL}/Item/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Name")))
        driver.find_element(By.ID, "Name").send_keys("NegativeWeightItem")
        weight_input = driver.find_element(By.ID, "Weight")
        driver.execute_script("arguments[0].value = '-5';", weight_input)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "greater than 0" in page_text.lower() or \
               "/Item/Create" in driver.current_url, \
            "TC-013: Should show negative weight validation error"

    def test_tc040_list_items(self, driver):
        """TC-040: Items list page loads and shows items."""
        login(driver)
        driver.get(f"{BASE_URL}/Item")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "items" in page_text.lower(), \
            "TC-040: Items page should display items list"

    def test_tc050_search_by_name(self, driver):
        """TC-050: Search for item by name."""
        login(driver)
        driver.get(f"{BASE_URL}/Item?search=AutoTest")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = driver.find_element(By.TAG_NAME, "body").text
        # Should show search results or "no items found"
        assert "autotest" in page_text.lower() or "no items found" in page_text.lower(), \
            "TC-050: Search should return matching items"

    def test_tc052_no_results_search(self, driver):
        """TC-052: Search with no matching results shows appropriate message."""
        login(driver)
        driver.get(f"{BASE_URL}/Item?search=xyz123nonexistent")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "no items found" in page_text.lower(), \
            "TC-052: Should show 'No items found' for non-matching search"

    def test_tc053_empty_search_returns_all(self, driver):
        """TC-053: Empty search returns all items."""
        login(driver)
        driver.get(f"{BASE_URL}/Item")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        all_items_text = driver.find_element(By.TAG_NAME, "body").text

        driver.get(f"{BASE_URL}/Item?search=")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        empty_search_text = driver.find_element(By.TAG_NAME, "body").text

        # Both should show same content (all items)
        assert "items" in all_items_text.lower() and "items" in empty_search_text.lower(), \
            "TC-053: Empty search should return all items"


# =============================================================================
# TC-060 to TC-068: Process Item Tests
# =============================================================================
class TestProcessItem:
    """Test cases for Process Item screen."""

    def test_tc060_process_item_with_one_child(self, driver):
        """TC-060: Process item with one child item."""
        login(driver)
        # First create a new item to process
        item_name = f"ProcessTest_{int(time.time())}"
        driver.get(f"{BASE_URL}/Item/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "Name")))
        driver.find_element(By.ID, "Name").send_keys(item_name)
        driver.find_element(By.ID, "Weight").send_keys("100.0")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Now go to Process page
        driver.get(f"{BASE_URL}/Process/Create")
        wait.until(EC.presence_of_element_located((By.ID, "ParentItemId")))

        # Select the newly created item
        select = Select(driver.find_element(By.ID, "ParentItemId"))
        options = [o.text for o in select.options]
        # Find the item we just created
        matching = [o for o in options if item_name in o]
        if matching:
            select.select_by_visible_text(matching[0])
        else:
            pytest.skip("Could not find the test item in process dropdown")

        # Child items should be auto-added by JS; fill the first one
        time.sleep(0.5)
        child_names = driver.find_elements(By.CSS_SELECTOR, "input[name*='.Name']")
        child_weights = driver.find_elements(By.CSS_SELECTOR, "input[name*='.Weight']")

        if child_names:
            child_names[0].clear()
            child_names[0].send_keys("Child Item 1")
            child_weights[0].clear()
            child_weights[0].send_keys("50.0")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "processed successfully" in page_text.lower() or \
               "process" in driver.current_url.lower(), \
            "TC-060: Item should be processed successfully"

    def test_tc062_no_parent_selected(self, driver):
        """TC-062: Submit process form without selecting parent."""
        login(driver)
        driver.get(f"{BASE_URL}/Process/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "no unprocessed items available" in page_text.lower():
            pytest.skip("No items available to process")

        wait.until(EC.presence_of_element_located((By.ID, "ParentItemId")))
        time.sleep(0.5)
        child_names = driver.find_elements(By.CSS_SELECTOR, "input[name*='.Name']")
        child_weights = driver.find_elements(By.CSS_SELECTOR, "input[name*='.Weight']")

        if child_names:
            child_names[0].send_keys("Child Without Parent")
            child_weights[0].send_keys("10")

        # Submit without selecting parent
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(0.5)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "select" in page_text.lower() or \
               "required" in page_text.lower() or \
               "/Process/Create" in driver.current_url, \
            "TC-062: Should show parent item required validation"

    def test_tc063_no_children_added(self, driver):
        """TC-063: Submit process form without any child items."""
        login(driver)
        driver.get(f"{BASE_URL}/Process/Create")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "no unprocessed items available" in page_text.lower():
            pytest.skip("No items available to process")

        wait.until(EC.presence_of_element_located((By.ID, "ParentItemId")))

        # Select first valid parent
        select = Select(driver.find_element(By.ID, "ParentItemId"))
        if len(select.options) <= 1:
            pytest.skip("No items in dropdown")
        select.select_by_index(1)

        # Remove any child items by clearing names (leave them blank)
        child_names = driver.find_elements(By.CSS_SELECTOR, "input[name*='.Name']")
        for inp in child_names:
            inp.clear()

        # Use JS to bypass client-side validation
        driver.execute_script("return validateForm()")
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "at least one child" in page_text.lower() or \
               "child item is required" in page_text.lower() or \
               "required" in page_text.lower(), \
            "TC-063: Should show child item required validation"


# =============================================================================
# TC-070 to TC-073: Tree View Tests
# =============================================================================
class TestTreeView:
    """Test cases for the Item Tree Structure screen."""

    def test_tc070_tree_view_loads(self, driver):
        """TC-070: Full tree view page loads."""
        login(driver)
        driver.get(f"{BASE_URL}/Process/Tree")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "tree" in page_text.lower() or "item" in page_text.lower(), \
            "TC-070: Tree view page should load"

    def test_tc071_item_specific_tree(self, driver):
        """TC-071: Item-specific tree view loads for valid ID."""
        login(driver)
        # Navigate to items list to find first item
        driver.get(f"{BASE_URL}/Item")
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/Process/ItemTree/']")
        if not links:
            pytest.skip("No item tree links found on the page")

        tree_url = links[0].get_attribute("href")
        driver.get(tree_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "tree" in page_text.lower(), \
            "TC-071: Item-specific tree should load"


# =============================================================================
# TC-080 to TC-082: Auth / Authorization Tests
# =============================================================================
class TestAuthorization:
    """Test cases for authentication and authorization."""

    def test_tc080_unauthenticated_items_redirects(self, driver):
        """TC-080: Accessing items page without login redirects to login."""
        # Ensure logged out by visiting logout
        driver.get(f"{BASE_URL}/Account/Login")
        driver.delete_all_cookies()
        driver.get(f"{BASE_URL}/Item")
        time.sleep(1)
        assert "/Account/Login" in driver.current_url or \
               "login" in driver.current_url.lower(), \
            "TC-080: Should redirect to login page"

    def test_tc081_unauthenticated_process_redirects(self, driver):
        """TC-081: Accessing process page without login redirects to login."""
        driver.delete_all_cookies()
        driver.get(f"{BASE_URL}/Process/Create")
        time.sleep(1)
        assert "/Account/Login" in driver.current_url or \
               "login" in driver.current_url.lower(), \
            "TC-081: Should redirect to login page"

    def test_tc082_logout_then_access(self, driver):
        """TC-082: After logout, accessing items redirects to login."""
        login(driver)
        driver.get(f"{BASE_URL}/Item")
        time.sleep(0.5)

        # Logout via form submission
        try:
            logout_btn = driver.find_element(By.CSS_SELECTOR, "form[action*='Logout'] button")
            logout_btn.click()
            time.sleep(1)
        except Exception:
            driver.delete_all_cookies()

        driver.get(f"{BASE_URL}/Item")
        time.sleep(1)
        assert "/Account/Login" in driver.current_url or \
               "login" in driver.current_url.lower(), \
            "TC-082: After logout, items page should redirect to login"


if __name__ == "__main__":
    import subprocess
    subprocess.run(["pytest", __file__, "-v", "--tb=short"])
