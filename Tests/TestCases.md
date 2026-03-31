# ADMS ERP - Test Cases Document
# This file documents all manual and automated test cases

## Test Suite Overview

### 1. Login Tests

| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-001 | Valid login | admin@adms.com / Admin@123 | Redirect to Items page | Happy Path |
| TC-002 | Invalid email format | notanemail / Admin@123 | Validation error: "Invalid email address" | Edge Case |
| TC-003 | Empty email | (blank) / Admin@123 | Validation error: "Email is required" | Edge Case |
| TC-004 | Empty password | admin@adms.com / (blank) | Validation error: "Password is required" | Edge Case |
| TC-005 | Wrong password | admin@adms.com / wrongpass | Error: "Invalid email or password" | Edge Case |
| TC-006 | Non-existent user | nobody@test.com / Test@123 | Error: "Invalid email or password" | Edge Case |
| TC-007 | SQL injection attempt | ' OR 1=1-- / x | Validation error or login failure | Security |
| TC-008 | Remember me checkbox | Check + valid login | Session persists after browser close | Feature |

### 2. Item Screen Tests (Add, Update, Delete, List, Search)

#### Add Item
| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-010 | Valid item creation | Name=Steel, Weight=50.5 | Item created; success message shown | Happy Path |
| TC-011 | Empty name | Name=(blank), Weight=10 | Validation error: "Item name is required" | Edge Case |
| TC-012 | Zero weight | Name=Iron, Weight=0 | Validation error: "Weight must be greater than 0" | Edge Case |
| TC-013 | Negative weight | Name=Iron, Weight=-5 | Validation error: "Weight must be greater than 0" | Edge Case |
| TC-014 | Very long name (201 chars) | Name=201char string | Validation error: "must be between 1 and 200 characters" | Edge Case |
| TC-015 | Weight with 4 decimal places | Name=Gold, Weight=1.2345 | Item created successfully | Happy Path |
| TC-016 | Optional description omitted | Name=Silver, Weight=5.0, Desc=(blank) | Item created with empty description | Happy Path |
| TC-017 | Extremely large weight | Name=Rock, Weight=99999999 | Item created successfully | Edge Case |
| TC-018 | Special characters in name | Name=Steel-100 (Grade A), Weight=10 | Item created successfully | Edge Case |

#### Update Item
| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-020 | Valid update | Change name and weight | "updated successfully" message | Happy Path |
| TC-021 | Update with empty name | Name=(blank) | Validation error: "Item name is required" | Edge Case |
| TC-022 | Update weight to 0 | Weight=0 | Validation error: "Weight must be greater than 0" | Edge Case |
| TC-023 | Update non-existent item | ID=99999 | 404 Not Found | Edge Case |

#### Delete Item
| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-030 | Delete item without children | Valid item ID | Item deleted; success message | Happy Path |
| TC-031 | Delete item with children | Item with child items | Error: "Cannot delete an item that has child items" | Edge Case |
| TC-032 | Delete non-existent item | ID=99999 | 404 Not Found | Edge Case |

#### List Items
| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-040 | List all items | None | All items displayed in table | Happy Path |
| TC-041 | Empty list | (no items exist) | "No items found" message shown | Edge Case |

#### Search Items
| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-050 | Search by name | "Steel" | Returns items with "Steel" in name | Happy Path |
| TC-051 | Search by description | "raw" | Returns items with "raw" in description | Happy Path |
| TC-052 | No results search | "xyz123abc" | "No items found" | Edge Case |
| TC-053 | Empty search | (blank) | All items returned | Edge Case |
| TC-054 | Case-insensitive search | "steel" / "STEEL" | Same results | Feature |

### 3. Process Item Tests

| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-060 | Process item with one child | Parent + 1 child | Parent marked processed, child created | Happy Path |
| TC-061 | Process item with multiple children | Parent + 3 children | Parent processed, 3 children created | Happy Path |
| TC-062 | No parent selected | No parent + 1 child | Validation error: "Please select a parent item" | Edge Case |
| TC-063 | No children added | Parent + 0 children | Validation error: "At least one child item is required" | Edge Case |
| TC-064 | Child with empty name | Name=(blank), Weight=5 | Child row ignored (filtered out) | Edge Case |
| TC-065 | Child with zero weight | Name=Part, Weight=0 | Validation error for weight | Edge Case |
| TC-066 | Child with negative weight | Name=Part, Weight=-1 | Validation error for weight | Edge Case |
| TC-067 | Process already-processed item | Select processed item | Item not available in dropdown | Edge Case |
| TC-068 | Child becomes further processable | After processing, select child as parent | Child appears in process dropdown | Feature |

### 4. Tree View Tests

| TC# | Test Case | Input | Expected Result | Type |
|-----|-----------|-------|-----------------|------|
| TC-070 | View full tree | None | All root items shown with hierarchy | Happy Path |
| TC-071 | View item-specific tree | Item ID | Shows subtree from that item | Happy Path |
| TC-072 | Tree toggle expand/collapse | Click toggle button | Subtree expands or collapses | Feature |
| TC-073 | Empty tree | (no items) | "No items found. The tree is empty." message | Edge Case |

### 5. Authentication / Authorization Tests

| TC# | Test Case | Expected Result | Type |
|-----|-----------|-----------------|------|
| TC-080 | Access items without login | Redirect to login | Security |
| TC-081 | Access process without login | Redirect to login | Security |
| TC-082 | Logout then access items | Redirect to login | Security |
