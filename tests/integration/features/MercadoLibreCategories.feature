Feature: Getting all relevant categories with their attributes when required.

  Scenario: A new requirement for a Token is issued
    When A new user requires a new Token with the following data
      | Field                 | Value                                 |
      | APP_SECRET            | 3LXCReMX8QEUBUspm3tGZbXISRUajg9z      |
      | APP_ID                | 3586824506967371                      |
      | REDIRECT_URL          | https://google.com                    |
      | TG_CODE               | TG-61e75bf0e92533001b7add46-52073370  |
    Then A new User should be stored on the Django database with the following values
      | Field                 | Value                                 |
      | MELI_ID               | 52073370                              |
      | APP_ID                | 3586824506967371                      |
      | APP_SECRET            | 3LXCReMX8QEUBUspm3tGZbXISRUajg9z      |
      | REDIRECT_URL          | https://google.com                    |
    Then A new Token should be generated and stored in Redis
      | Field                 | Value                                 |
      | ACCESS_TOKEN          | RandomValue                           |
      | TOKEN_TYPE            | bearer                                |
      | EXPIRES_IN            | 21600                                 |
      | USER_ID               | 52073370                              |
      | REFRESH_TOKEN         | RandomValue                           |

