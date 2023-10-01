Feature: Git Basic Operations
  Scenario: Initialize a new repository
    Given new local repository path
    When executing 'git init'
    Then new empty repository will be created

  Scenario: Clone repository
    Given remote repository
    When executing 'git clone'
    Then new repository will be cloned

  Scenario: Add a new file
    Given new git repository
    And new file has been created
    When executing 'git add' on file
    Then new file will be added to the git tracking

  Scenario: Remove a file
    Given new git repository
    And new file has been created
    And new file has been added to tracking
    And commit changes
    When executing 'git rm' on file
    Then the file will be removed from the git tracking

  Scenario: Move (rename) a file
    Given new git repository
    And new file has been created
    And new file has been added to tracking
    And commit changes
    When executing 'git mv' on file
    Then the file will be renamed