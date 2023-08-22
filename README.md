# Unit Test Cases

## Description
In this sample application we are just exploring how to write unit test cases, this includes simple flask based CRUD api's.
* There is one file named **_unit_test_case.py_** this basically guide how to write unit test cases for the CRUD api's by using unittest module which is included in the Python Standard Library.
* A file named **_test_app.py_**, this is used to write test cases for the same app using pytest module.
* One selenium script **_selenium_test_app.py_** is also there to understand how to write automation test cases using Selenium.

## Installation

To install and run the UnitTest Cases, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/hk-systango/UnitTestCases.git
   ```

2. Navigate to the application directory:

   ```shell
   cd UnitTestCases
   ```

3. Create a virtual environment:

   ```shell
   python -m venv venv
   ```

4. Activate the virtual environment:

     ```shell
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

6. Configuration:
    
   - Create a `.env` file in the root directory:
     ```shell
     touch .env
     ```
   - Go through the `sample.env` file and add the necessary configurations to the `.env` file.
   - Source .env file
     ```shell
     source .env
     ```
     
7. To run the application:

   ```shell
   python app.py
   ```

8. To run Unittest cases

   * To run test cases which is written using _**unittest**_ module
   ```shell
   python unit_test_case.py
   ```
   * To run test cases which is written using **_pytest_** module. This command executes all the test cases which is written inside the file which starts using a word '_test__'
   ```shell
   pytest
   ```
   * To run selenium automation test cases. Make sure to use .env file before running automation script.
   ```shell
   python selenium_test_app.py
   ```
