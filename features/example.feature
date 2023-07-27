Feature: showing off behave

  Background: some requirement of this test
  Given some setup condition
    And some other setup action


  Scenario: run a simple test
     Given we have behave installed
      When we implement a test
      Then behave will test it for us!

  Scenario Outline: Blenders
   Given I put <thing> in a blender,
    When I switch the blender on
    Then it should transform into <other thing>


 Examples: Amphibians
   | thing         | other thing |
   | Red Tree Frog | mush        |

 Examples: Consumer Electronics
   | thing         | other thing |
   | iPhone        | toxic waste |
   | Galaxy Nexus  | toxic waste |

  Scenario: look up a book
    Given I search for a valid book
    Then the result page will include "success"

  Scenario: look up an invalid book
    Given I search for a invalid book
    Then the result page will include "failure"
